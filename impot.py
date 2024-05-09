import sqlite3

def import_sql_to_sqlite(sql_file, sqlite_db):
    # Connect to SQLite database
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()

    # Read SQL file
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_commands = f.read()

    # Execute SQL commands
    cursor.executescript(sql_commands)

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print(f"Data from {sql_file} imported into SQLite database successfully!")

if __name__ == "__main__":
    sql_file_path = 'data.sql'  # Path to your SQL backup file
    sqlite_db_path = 'db.sqlite3'  # Path to your SQLite database file
    import_sql_to_sqlite(sql_file_path, sqlite_db_path)
