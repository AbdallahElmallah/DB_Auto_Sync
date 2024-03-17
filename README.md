# Database Sync Script

This Python script automates the synchronization of database records by retrieving failed requests from a database, reattempting them using an API, and updating the database accordingly.

## Purpose
- Automates routine database synchronization tasks
- Increases efficiency by handling failed requests automatically

## How It Works
1. Queries the database for failed requests.
2. Attempts to reprocess each failed request using an API.
3. Updates the database with successful requests and logs failed requests.

## Usage
1. Ensure Python 3 is installed on your system.
2. Install required dependencies using pip:
- pip install -r requirements.txt

3. Set up environment variables in a `.env` file.
4. Run the script to initiate the synchronization process:
- python db_sync_script.py

## Requirements
- Python 3
- PostgreSQL database
- Requests library
- psycopg2 library
- python-dotenv library

