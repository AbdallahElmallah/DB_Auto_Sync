import json
import psycopg2
import requests
import logging
import sys
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

LOG_FILENAME = 'db.log'
SELECT_QUERY = "SELECT * FROM integration.failed_requests WHERE DATE(create_at) = %s;"
INSERT_QUERY = "INSERT INTO integration.failed_requests_history VALUES (%s, %s, %s, %s);"
DELETE_QUERY = "DELETE FROM integration.failed_requests WHERE id = %s;"

logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
}

current_date = datetime.now().date()

failed_complaints = []

def make_get_request(ComplaintID):
    url = f"{os.getenv('API_BASE_URL')}/{ComplaintID}"
    try:
        response = requests.get(url)
        return response.status_code == 200 and response.text.lower() == "true"
   
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
        exit()
    except requests.RequestException as e:
        logging.error(f"Error making GET request for ComplaintID {ComplaintID}: {e}")
        return False

def process_failed_requests(db_params):
    successful_requests = 0
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        cursor.execute(SELECT_QUERY,(current_date,))
        rows = cursor.fetchall()
        
        for row in rows:
            complaint_id_data = json.loads(row[2])
            ComplaintID = complaint_id_data.get('ComplaintID', '')
            if ComplaintID:
                if make_get_request(ComplaintID):
                    successful_requests += 1
                    cursor.execute(INSERT_QUERY, (row[0], row[1], row[2], row[3]))
                    cursor.execute(DELETE_QUERY, (row[0],))
                else:
                    failed_complaints.append(ComplaintID)
        connection.commit()

    except psycopg2.Error as e:
        logging.error(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return successful_requests

success_count = process_failed_requests(db_params)

logging.info(f"Number of successful requests: {success_count}")
logging.info(f"Failed ComplaintID values: {failed_complaints}")

sys.exit()