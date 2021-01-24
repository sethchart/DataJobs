"""
This module builds a SQLite database to receive job postings from careerjet.com
and provides methods for reading from and writing to the database.
"""

__author__ = "Seth Chart"
__version__ = "0.1.0"
__license__ = "MIT"

import sqlite3
import pandas as pd

class JobsDb(object):

    def __init__(self):
        self.conn = sqlite3.connect('../data/jobs.sqlite')
        self.cur = self.conn.cursor()
        jobs_create_query = """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            description TEXT NOT NULL
        )
        """
        self.cur.execute(jobs_create_query)

    def close(self):
        """Closes the cursor and connection created by instantiating a JobsDb object."""
        self.cur.close()
        self.conn.close()

    def list_tables(self):
        """Queries the database and returns a list of table names."""
        query = """
            SELECT name
            FROM sqlite_master
            WHERE type='table';
        """
        response = self.cur.execute(query).fetchall()
        table_names = [r[0] for r in response]
        return table_names

    def list_column_names(self, table_name):
        """Given the name of a table in the data base, this function returns a list of column names.

        Keyword Arguments:
        table_name -- name of the table whose columns will be listed.

        Use list_tables method to obtain a list of tables.
        """
        query = f"""
            PRAGMA table_info({table_name});
            """
        response = self.cur.execute(query).fetchall()
        column_names = [r[1] for r in response]
        return column_names

    def load_query_as_df(self, query):
        """Given a valid SQL query formated as a string,
        this function returns the output of the query as
        a pandas dataframe.

        Keyword Arguments:
        query -- SQL query formated as a string.
        """
        df = pd.read_sql(query, self.conn, index_col='id')
        return df

    def load_table_as_df(self, table_name):
        """Given the name of a table in the database,
        this function loads the table as as pandas dataframe.

        Keyword Arguments:
        table_name -- name of tables whoes contents will be returned as a dataframe

        Use the list_tables method to obtain a list of tables.
        """
        query = f"""
            SELECT *
            FROM {table_name};
            """
        df = self.load_query_as_df(query)
        return df 

    def write_row_to_table(self, table_name, row_dict):
        """Given a table name and a dictionary with keys matching table column names
        and values complying with column datatypes, this function writes a new row
        to the specified table.

        Keyword Arguments:
        table_name -- name of the table to write to.
        row_dict -- dictionary containing row data.

        Use the list_tables method to obtain a list of tables.
        """
        query = f"""
            INSERT INTO {table_name} ({', '.join(row_dict.keys())})
            VALUES {tuple(row_dict.values())}
        """
        self.cur.execute(query)
        self.conn.commit()
