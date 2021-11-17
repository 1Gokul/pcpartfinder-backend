# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import psycopg2
import os

TABLE_NAME = "crawler_data"


class PartScraperPipeline(object):
    def __init__(self):
        """
        Sets the connection string and creates a table if it doesn't exist.
        """

        self.connection_string = (
            f"host={os.getenv('HOST')} user={os.getenv('USERID')} password={os.getenv('PASSWORD')} "
            f"dbname={os.getenv('DATABASE_NAME')} sslmode={os.getenv('SSLMODE')}"
        )

        with psycopg2.connect(self.connection_string) as conn:

            cursor = conn.cursor()

            # Check if a table by the name {TABLE_NAME} exists.
            cursor.execute(
                "select exists(select * from information_schema.tables where table_name=%s)",
                (TABLE_NAME,),
            )

            # If a table exists, remove the old data inside.
            if cursor.fetchone()[0]:
                cursor.execute(f"TRUNCATE TABLE {TABLE_NAME}")

            # Else if no table exists, create one.
            else:
                cursor.execute(
                    (
                        f"CREATE TABLE {TABLE_NAME} ("
                        "id SERIAL NOT NULL PRIMARY KEY,"
                        "name VARCHAR(300) NOT NULL,"
                        "price INTEGER NOT NULL,"
                        "url VARCHAR(1000) NOT NULL,"
                        "store VARCHAR(50) NOT NULL"
                        ");"
                    )
                )

    def process_item(self, item, spider):
        """
        Save information about the scraped part into the database.
        """

        # Establish a connection
        with psycopg2.connect(self.connection_string) as conn:

            # While the connection is open, add the item's data.
            cursor = conn.cursor()
            try:
                cursor.execute(
                    f"INSERT INTO {TABLE_NAME} (name, price, url, store) VALUES (%s, %s, %s,%s)",
                    (
                        item["name"],
                        item["price"],
                        item["url"],
                        item["store"],
                    ),
                )
            except Exception as ex:
                template = "Exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)

        return item
