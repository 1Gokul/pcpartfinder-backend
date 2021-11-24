import subprocess
import pyodbc
import os

TABLE_NAME = "crawler_data"
RESULT_KEYS = ["name", "price", "url", "store"]
STORES = ["Vedant_Computers", "MD_Computers", "Prime_ABGB", "IT_Depot", "PC_Shop"]


def crawl_data():
    """
    Crawl the data and insert the info into a database.
    """
    subprocess.call("python3 " + "crawler.py", shell=True)


async def search(query):
    """
    Query the database and return the results, if any.
    """

    CONNECTION_STRING = (
        f"Driver={os.getenv('DRIVER')}; Server={os.getenv('HOST')}; UID={os.getenv('USERID')};"
        f"PWD={os.getenv('PASSWORD')}; Database={os.getenv('DATABASE_NAME')};"
    )

    # Establish a connection
    with pyodbc.connect(CONNECTION_STRING) as conn:

        cursor = conn.cursor()
        try:
            cursor.execute(
                f"SELECT Name, Price, URL, StoreName FROM {TABLE_NAME} "
                f"WHERE UPPER(Name) LIKE '%{query.upper()}%' ORDER BY StoreName",
            )

            # Fetch all the rows
            query_results = cursor.fetchall()

            """
            There is no JSON aggregation function (as far as I know) in SQL Server to aggregate and 
            group the results by store.
            "data" below is a dict of arrays for each store specified in the "STORES" list above.
            Each row item has a StoreName column which will be used to segregate them.
            The below code creates a dict for each row and adds the dict to "data" using the key specified by
            the StoreName column of that row.
            """
            data = {store: [] for store in STORES}

            for row in query_results:
                row_item = {}

                for index, value in enumerate(row):
                    # Add the row's column values to the dict
                    row_item[RESULT_KEYS[index]] = value

                # Add them to the dict specified by the "store" column
                data[row_item["store"]].append(row_item)

        except Exception as ex:
            template = "Exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    # Return the results as an list of dicts
    return [{"store_name": key, "store_results": value} for key, value in data.items() if len(value)]
