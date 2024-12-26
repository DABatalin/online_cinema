# Загрузка данных из csv в базу

import psycopg2
import csv
import os

DB_CONFIG = {
    "host": "localhost",
    "database": "fast_api",
    "user": "admin",
    "password": "admin",
    "port": '5431'
}

def _prepare_row_data(row, columns, row_index, array_delimiter=','):
    """Prepares a single row for insertion, converting values to the correct type."""
    row_data = []
    for col in columns:
        value = row.get(col)  # Use .get() for missing columns
        if value == "":  # Treat empty strings as None for all columns
            value = None
        elif value is not None:
            if col == 'id' or col == 'film_id':
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    print(f"Warning: Invalid '{col}' value '{value}' in row {row_index}. Skipping this row.")
                    return None

            elif col == 'genre_ids':
                if value is not None:
                    value = [int(genre_id.strip()) for genre_id in value.split(array_delimiter) if genre_id.strip()]
        row_data.append(value)

    return row_data


def import_csv_data(csv_file_path, table_name, columns, row_limit=None, skip_rows_without_id=False, array_delimiter=','):
    """Imports data from a CSV file into a PostgreSQL table, limiting the number of rows.
       Handles empty cells, type conversions, and array columns."""
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
             # Check if specified columns are present in the csv header
            if not set(columns).issubset(reader.fieldnames):
                 raise ValueError(f"The specified columns '{columns}' are not present in the CSV header. Available columns are: {reader.fieldnames}")

            data = []
            for i, row in enumerate(reader):
                if row_limit and i >= row_limit:
                    break
                row_data = _prepare_row_data(row, columns, i + 1, array_delimiter)
                if row_data is None and skip_rows_without_id:
                    continue  # Skip row
                if row_data is not None:
                    data.append(row_data)


            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
            if data:  # Check if data list is not empty
                 cur.executemany(query, data)

        conn.commit()
        print(f"Data successfully imported into table {table_name} (up to {row_limit or 'all'} rows).")

    except psycopg2.Error as e:
        print(f"PostgreSQL error: {e}")
        if conn:
            conn.rollback()
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error in input file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def import_film_genres(csv_file_path, table_name, columns, films_ids):
    """Imports data into filmgenres table filtering by film_id in films"""
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # Check if specified columns are present in the csv header
            if not set(columns).issubset(reader.fieldnames):
                raise ValueError(f"The specified columns '{columns}' are not present in the CSV header. Available columns are: {reader.fieldnames}")

            data = []
            for i, row in enumerate(reader):
                film_id = int(row['film_id'])
                genre_id = int(row['genre_id'])
                if film_id in films_ids:
                    data.append((film_id, genre_id))

            query = f"INSERT INTO {table_name} (film_id, genre_id) VALUES (%s, %s)"
            if data:
                 cur.executemany(query, data)

        conn.commit()
        print(f"Data successfully imported into table {table_name} filtering by film_id.")

    except psycopg2.Error as e:
        print(f"PostgreSQL error: {e}")
        if conn:
            conn.rollback()
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error in input file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_films_ids() -> list:
    """Gets ids of all films from films table"""
    conn = None
    cur = None
    films_ids = []
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT id FROM films")
        films_ids = [row[0] for row in cur.fetchall()]

    except psycopg2.Error as e:
        print(f"PostgreSQL error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    return films_ids

if __name__ == '__main__':

    # Import films with a limit of 10000 rows
    import_csv_data('csv_files/films.csv', 'films', ["id","title","film_link","average_rating","description","vote_count"])

    # Import all rows into genres
    import_csv_data('csv_files/genre.csv', 'genre', ["id", "name"])
    #Import only valid rows for film_genres
    films_ids = get_films_ids()

    import_film_genres('csv_files/film_genre.csv', 'film_genres', ["film_id", "genre_ids"], films_ids)