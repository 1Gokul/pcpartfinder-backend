import subprocess
import psycopg2
import os

TABLE_NAME = "crawler_data"


def crawl_data():
    """
    Crawl the data and insert the info into a database.
    """
    subprocess.call("python " + "crawler.py", shell=True)


async def search(query):
    """
    Query the database and return the results, if any.
    """

    CONNECTION_STRING = (
        f"host={os.getenv('SERVER')} user={os.getenv('USERID')} password={os.getenv('PASSWORD')} "
        f"dbname={os.getenv('DATABASE_NAME')} sslmode={os.getenv('SSLMODE')}"
    )

    results = None

    # Establish a connection
    with psycopg2.connect(CONNECTION_STRING) as conn:

        cursor = conn.cursor()
        try:
            cursor.execute(
                f"SELECT json_build_object(store, json_agg({TABLE_NAME})) FROM {TABLE_NAME} "
                f"WHERE name ILIKE '%{query}%' GROUP BY store",
            )

            results = cursor.fetchall()

        except Exception as ex:
            template = "Exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    # result[0] because all the results are enclosed in extra lists in the query result.
    return [result[0] for result in results]
