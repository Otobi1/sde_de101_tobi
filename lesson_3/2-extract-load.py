
# Extract: Process to pull data from Source system
# Load: Process to write data to a destination system

# Common upstream & downstream systems
# OLTP (Online Transaction Processing) Databases: Postgres, MySQL, sqlite3, etc
# OLAP (Online Analytical Processing) Databases: Snowflake, BigQuery, Clickhouse, DuckDB, etc
# Cloud data storage: AWS S3, GCP Cloud Store, Minio, etc
# Queue systems: Kafka, Redpanda, etc
# API
# Local disk: csv, excel, json, xml files
# SFTP\FTP server

# Q1

# Databases: When reading or writing to a database we use a database driver. Database drivers are libraries that we can use to read or write to a database.
# Question: How do you read data from a sqlite3 database and write to a DuckDB database?



'''   For some yet to be determined reason I can't get sqlite3 to work here - will come back to it
'''
import sqlite3 # import the sqlite3 database driver 

# Connect to the SQLite database
sqlite_conn = sqlite3.connect(
    "tpch.db"
)  # Typically this will involve a connection string, sqlite3 db is stored as a file

# Fetch data from the SQLite Customer table using conn.execute
customers = sqlite_conn.execute(
    "SELECT * FROM Customer"
).fetchall()  # Fetch data from the SQLite Customer table

import duckdb  # duckdb database driver

duckdb_conn = duckdb.connect("duckdb.db")  # Duckdb connection string
# Insert data into the DuckDB Customer table
insert_query = f"""
INSERT INTO Customer (customer_id, zipcode, city, state_code, datetime_created, datetime_updated)
VALUES (?, ?, ?, ?, ?, ?)
"""  # Insert into query

duckdb_conn.executemany(insert_query, customers)

# Commit and close the connections
# Commit tells the DB connection to send the data to the database and commit it, if you don't commit the data will not be inserted
duckdb_conn.commit()

# We should close the connection, as DB connections are expensive
sqlite_conn.close()
duckdb_conn.close()



# Q2 

# Cloud storage
# Question: How do you read data from the S3 location given below and write the data to a DuckDB database?
# Data source: https://docs.opendata.aws/noaa-ghcn-pds/readme.html station data at path "csv.gz/by_station/ASN00002022.csv.gz"
# Hint: Use boto3 client with UNSIGNED config to access the S3 bucket
# Hint: The data will be zipped you have to unzip it

import csv 
import gzip
from io import StringIO

import boto3 
import duckdb
from botocore import UNSIGNED
from botocore.client import Config 

bucket_name = "noaa-ghcn-pds"
file_key = "csv.gz/by_station/ASN00002022.csv.gz"
# Create a boto3 client with anonymous access
s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))

s3_client

# Download the CSV file from S3
response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
compressed_data = response["Body"].read()

# Decompress the gzip data
csv_data = gzip.decompress(compressed_data).decode("utf-8")

# Read the CSV file using csv.reader
csv_reader = csv.reader(StringIO(csv_data))
data = list(csv_reader)
# Connect to the DuckDB database (assume WeatherData table exists)
duckdb_conn = duckdb.connect("duckdb.db")


# Insert data into the DuckDB WeatherData table
insert_query = """
INSERT INTO WeatherData (id, date, element, value, m_flag, q_flag, s_flag, obs_time)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

duckdb_conn.executemany(insert_query, data[:100000])

# Commit and close the connection
duckdb_conn.commit()
duckdb_conn.close()


# Q3 

# API
# Question: How do you read data from the CoinCap API given below and write the data to a DuckDB database?
# URL: "https://api.coincap.io/v2/exchanges"
# Hint: use requests library

import duckdb
import requests

# Define the API endpoint
url = "https://api.coincap.io/v2/exchanges"

# Fetch data from the CoinCap API
response = requests.get(url)
data = response.json()["data"]
# data

# Connect to the DuckDB database
duckdb_conn = duckdb.connect("duckdb.db")
# duckdb_conn

# Check if the table exists
result = duckdb_conn.execute("SELECT * FROM information_schema.tables WHERE table_name = 'Exchanges'").fetchall()
result

if not result:
    # Create the table if it does not exist
    create_table_query = """
    CREATE TABLE Exchanges (
        id VARCHAR,
        name VARCHAR,
        rank INT,
        percentTotalVolume DOUBLE,
        volumeUsd DOUBLE,
        tradingPairs VARCHAR,
        socket VARCHAR,
        exchangeUrl VARCHAR,
        updated VARCHAR
    );
    """
    duckdb_conn.execute(create_table_query)

# Prepare data for insertion
insert_data = []
for exchange in data:
    try:
        trading_pairs = exchange["tradingPairs"]
        try:
            trading_pairs = int(trading_pairs)
        except ValueError:
            # Handle the case where tradingPairs is not an integer
            trading_pairs = None

        insert_data.append(
            (
                exchange["exchangeId"],
                exchange["name"],
                int(exchange["rank"]),
                float(exchange["percentTotalVolume"]) if exchange["percentTotalVolume"] else None,
                float(exchange["volumeUsd"]) if exchange["volumeUsd"] else None,
                trading_pairs,
                exchange["socket"],
                exchange["exchangeUrl"],
                exchange["updated"],
            )
        )
    except Exception as e:
        print(f"Error processing record {exchange}: {e}")

# Print a sample of the prepared data for debugging
print(insert_data[:5])

# Insert data into the DuckDB Exchanges table
for record in insert_data:
    try:
        duckdb_conn.execute("INSERT INTO Exchanges (id, name, rank, percentTotalVolume, volumeUsd, tradingPairs, socket, exchangeUrl, updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", record)
    except Exception as e:
        print(f"Error inserting record {record}: {e}")

# Verify the insertion
result = duckdb_conn.execute("SELECT * FROM Exchanges").fetchall()
print(result)

# Commit and close the connection
duckdb_conn.commit()
duckdb_conn.close()


# to check column data type in tables in duck db 

import duckdb

# Connect to the DuckDB database
duckdb_conn = duckdb.connect("duckdb.db")

# Function to retrieve table schema details
def get_table_schema(table_name):
    # Use PRAGMA statement to get table information
    schema_info = duckdb_conn.execute(f"PRAGMA table_info('{table_name}')").fetchall()
    return schema_info

# Check details of the 'Exchanges' table
table_name = 'Exchanges'
schema_info = get_table_schema(table_name)

# Print the table schema details
print(f"Schema details for table '{table_name}':")
for column in schema_info:
    print(f"Column Name: {column[1]}, Data Type: {column[2]}, Nullable: {'YES' if column[3] == 0 else 'NO'}")

# Close the connection
duckdb_conn.close()



# to drop tables in duckdb 

import duckdb

# Connect to the DuckDB database
duckdb_conn = duckdb.connect("duckdb.db")

# Function to drop a table
def drop_table(table_name):
    try:
        duckdb_conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"Table '{table_name}' dropped successfully.")
    except Exception as e:
        print(f"Error dropping table '{table_name}': {e}")

# Drop the 'Exchanges' table
drop_table('Exchanges')

# Close the connection
duckdb_conn.close()


# Q4 

# Local disk
# Question: How do you read a CSV file from local disk and write it to a database?
# Look up open function with csvreader for python

import csv

data_location = "./data/customers.csv"
with open(data_location, "r", newline="") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row
    for row in csvreader:
        print(row)


# Q5 

# Web scraping
# Questions: Use beatiful soup to scrape the below website and print all the links in that website
# URL of the website to scrape

import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = 'https://example.com'

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content of the webpage
soup = BeautifulSoup(response.text, 'html.parser')

# Example: Find and print all the links on the webpage
for link in soup.find_all('a'):
    print(link.get('href'))
