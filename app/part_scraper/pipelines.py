# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pyodbc
import os

from config import DB_TABLE_NAME


class PartScraperPipeline(object):
    def __init__(self):
        """
        Sets the connection string and creates a table if it doesn't exist.
        """

        self.connection_string = (
            f"Driver={os.getenv('DRIVER')}; Server={os.getenv('HOST')}; UID={os.getenv('USERID')};"
            f"PWD={os.getenv('PASSWORD')}; Database={os.getenv('DATABASE_NAME')};"
        )

        with pyodbc.connect(self.connection_string) as conn:

            cursor = conn.cursor()

            # If no table of that particular name exists, create one.
            if cursor.tables(table=DB_TABLE_NAME, tableType="TABLE").fetchone():
                cursor.execute(f"TRUNCATE TABLE {DB_TABLE_NAME}")

            else:
                cursor.execute(
                    (
                        f"CREATE TABLE {DB_TABLE_NAME} ("
                        "ID INT PRIMARY KEY IDENTITY(1,1),"
                        "Name VARCHAR(300) NOT NULL, "
                        "Price INT, "
                        "URL VARCHAR(1000), "
                        "StoreName VARCHAR(50), "
                        ");"
                    )
                )

    def process_item(self, item, spider):
        """
        Save information about the scraped part into the database.
        """

        # Establish a connection
        with pyodbc.connect(self.connection_string) as conn:

            # While the connection is open, add the item's data.
            cursor = conn.cursor()
            try:
                cursor.execute(
                    f"INSERT INTO {DB_TABLE_NAME}(Name, Price, URL, StoreName) VALUES (?, ?, ?, ?)",
                    item["name"],
                    item["price"],
                    item["url"],
                    item["store"],
                )

                conn.commit()

            except Exception as ex:
                template = "Exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                conn.rollback()

        return item
