import os
import sqlite3
from pathlib import Path


def load_env_file(env_path=".env"):
    if not Path(env_path).exists():
        return

    with open(env_path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def get_db_path():
    load_env_file()
    return os.getenv("DB_PATH", "./data/database.db")


def connect():
    db_path = get_db_path()
    try:
        connection = sqlite3.connect(db_path)
        print("Connected to existing SQLite database.")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def format_rows(columns, rows, max_rows=20):
    display_rows = rows[:max_rows]
    widths = [len(str(column)) for column in columns]

    for row in display_rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value)))

    header = " | ".join(str(column).ljust(widths[i]) for i, column in enumerate(columns))
    separator = "-+-".join("-" * width for width in widths)
    body = [
        " | ".join(str(value).ljust(widths[i]) for i, value in enumerate(row))
        for row in display_rows
    ]

    lines = [header, separator, *body]
    if len(rows) > max_rows:
        lines.append(f"... showing {max_rows} of {len(rows)} rows")
    return "\n".join(lines)


def run_queries_from_file(connection, filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        queries = [q.strip() for q in content.split(";") if q.strip()]
        cursor = connection.cursor()

        for i, query in enumerate(queries, start=1):
            cleaned_lines = [
                line for line in query.splitlines() if not line.strip().startswith("--")
            ]
            cleaned_query = "\n".join(cleaned_lines).strip()

            if not cleaned_query or not any(c.isalnum() for c in cleaned_query):
                continue

            try:
                print(f"\nQuery {i}:\n{cleaned_query}")
                cursor.execute(cleaned_query)

                if cursor.description:
                    columns = [description[0] for description in cursor.description]
                    rows = cursor.fetchall()
                    print(format_rows(columns, rows))
                else:
                    connection.commit()
                    print("Query executed successfully.")
            except Exception as e:
                print(f"Error in Query {i}: {e}")
    except Exception as e:
        print(f"Error processing queries from {filepath}: {e}")


if __name__ == "__main__":
    connection = connect()
    if connection:
        run_queries_from_file(connection, "./src/sql/queries.sql")
        connection.close()
