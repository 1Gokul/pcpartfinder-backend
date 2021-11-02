# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pyodbc
import os

STORES=["VedantComputers"]

class PartScraperPipeline(object):
    def __init__(self):
        """
        Initializes Database and adds tables.
        """

        self.connection_string = (
            f"DRIVER={'ODBC Driver 17 for SQL Server'};SERVER={os.getenv('SERVER')};"
            f"UID={os.getenv('USERID')};PWD={os.getenv('PASSWORD')};"
            f"database={os.getenv('DATABASE_NAME')}"
        )

        cnxn = pyodbc.connect(self.connection_string)
        with cnxn:
            cursor = cnxn.cursor()

            # Create a table for each store to be crawled (if they don't exist already).
            for store in STORES:

                # If no table of that particular name exists, create one.
                if not cursor.tables(table=store, tableType="TABLE").fetchone():
                    cursor.execute(
                        (f"CREATE TABLE {store} ("
                        "ID INT PRIMARY KEY IDENTITY(1,1),"
                        "Name VARCHAR(100) NOT NULL, "
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
        cnxn = pyodbc.connect(self.connection_string)
        with cnxn:

            # While the connection is open, add the item's data.
            cursor = cnxn.cursor()
            try:
                cursor.execute(
                    f"INSERT INTO {item['store']}(Name, Price, URL, StoreName) VALUES (?, ?, ?, ?)",
                    item["name"],
                    item["price"],
                    item["url"],
                    item["store"],
                )
    
                cnxn.commit()

            except Exception as ex:
                print("EXCEPTION- ", ex)
                cnxn.rollback()

        return item
