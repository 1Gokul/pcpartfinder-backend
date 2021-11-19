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
        f"host={os.getenv('HOST')} user={os.getenv('USERID')} password={os.getenv('PASSWORD')} "
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

    # Format the result into an easily accessible dict
    # (result[0] because the Postgres query result encloses each store's items in extra lists.)
    return [
        {"store_name": key, "store_results": value}
        for result in results
        for key, value in result[0].items()
    ]
