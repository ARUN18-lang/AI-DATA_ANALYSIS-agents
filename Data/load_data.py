import sqlite3

def get_details_from_sqlite_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    result = {}

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    result['tables'] = str(tables)

    for table_name in tables:
        table_key = f"table_{table_name}"

        cursor.execute(f"PRAGMA table_info({table_name});")
        schema = cursor.fetchall()
        result[f"{table_key}_schema"] = str(schema)

        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]
        result[f"{table_key}_row_count"] = str(row_count)

        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
        sample_data = cursor.fetchall()
        result[f"{table_key}_sample_data"] = str(sample_data)

        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [col[1] for col in cursor.fetchall()]
        result[f"{table_key}_columns"] = str(columns)

        null_query = "SELECT " + ", ".join([
            f"SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END) AS {col}_nulls" for col in columns
        ]) + f" FROM {table_name};"
        cursor.execute(null_query)
        null_counts = cursor.fetchone()
        result[f"{table_key}_null_counts"] = str(dict(zip(columns, null_counts)))

    conn.close()
    return result

