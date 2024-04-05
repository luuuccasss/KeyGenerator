import sqlite3
import mysql.connector
import secrets
import string
from config import mysql_config, key_pattern, key_content

def generate_key():
    characters = ''
    if key_content == 'numeric':
        characters = string.digits
    elif key_content == 'alphabetic':
        characters = string.ascii_uppercase
    elif key_content == 'alphanumeric':
        characters = string.ascii_uppercase + string.digits

    key = ''
    for char in key_pattern:
        if char == 'X':
            key += secrets.choice(characters)
        else:
            key += char
    return key

def connect_to_sqlite():
    return sqlite3.connect('keys.db')

def connect_to_mysql():
    return mysql.connector.connect(**mysql_config)

def create_table_sqlite(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS keys (
                      id INTEGER PRIMARY KEY,
                      key_text TEXT UNIQUE)''')


def create_table_mysql(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS `keys` (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      key_text VARCHAR(255) UNIQUE)''')


def insert_key_sqlite(cursor, key):
    cursor.execute('INSERT INTO keys (key_text) VALUES (?)', (key,))
    cursor.connection.commit()

def insert_key_mysql(cursor, key):
    cursor.execute('INSERT INTO `keys` (key_text) VALUES (%s)', (key,))
    cursor._connection.commit()

def delete_key_by_id_sqlite(cursor, key_id):
    cursor.execute('DELETE FROM `keys` WHERE id = ?', (key_id,))
    cursor.connection.commit()

def delete_key_by_id_mysql(cursor, key_id):
    cursor.execute('DELETE FROM `keys` WHERE id = %s', (key_id,))
    cursor.connection.commit()

def generate_and_insert_key(cursor, db_type):
    key = generate_key()
    if db_type == 'sqlite':
        insert_key_sqlite(cursor, key)
    elif db_type == 'mysql':
        insert_key_mysql(cursor, key)
    print("New key generated and inserted: ", key)

def display_all_keys(cursor):
    cursor.execute('SELECT id, key_text FROM `keys`')
    keys = cursor.fetchall()
    if keys:
        print("List of generated keys: ")
        for key in keys:
            print("ID:", key[0], "Key:", key[1])
    else:
        print("No keys found.")

def export_keys_to_txt(cursor, db_type):
    if db_type == 'sqlite':
        cursor.execute('SELECT key_text FROM `keys`')
    elif db_type == 'mysql':
        cursor.execute('SELECT key_text FROM `keys`')
    keys = cursor.fetchall()
    if keys:
        with open('keys_export.txt', 'w') as file:
            for key in keys:
                file.write(key[0] + '\n')
        print("All keys exported to keys_export.txt successfully.")
    else:
        print("No keys found to export.")

def choose_database_type():
    while True:
        print("\nChoose database type:")
        print("1. SQLite")
        print("2. MySQL")
        choice = input("Your choice: ")
        if choice == '1':
            return 'sqlite'
        elif choice == '2':
            return 'mysql'
        else:
            print("Invalid choice. Please enter 1 or 2.")

def main():
    db_type = choose_database_type()
    if db_type == 'sqlite':
        connection = connect_to_sqlite()
        cursor = connection.cursor()
        create_table_sqlite(cursor)
    elif db_type == 'mysql':
        connection = connect_to_mysql()
        cursor = connection.cursor()
        create_table_mysql(cursor)

    while True:
        print("\nWhat would you like to do?")
        print("1. Generate and insert a new key")
        print("2. Display all generated keys")
        print("3. Delete a key by its ID")
        print("4. Export keys to text file")
        print("5. Quit")

        choice = input("Your choice: ")

        if choice == '1':
            generate_and_insert_key(cursor, db_type)
        elif choice == '2':
            display_all_keys(cursor)
        elif choice == '3':
            key_id = input("Please enter the ID of the key to delete: ")
            if db_type == 'sqlite':
                delete_key_by_id_sqlite(cursor, key_id)
            elif db_type == 'mysql':
                delete_key_by_id_mysql(cursor, key_id)
            print("Key deleted successfully.")
        elif choice == '4':
            export_keys_to_txt(cursor, db_type)
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
