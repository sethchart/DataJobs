#! ~/usr/bin/env python3
"""This script executes a query against the jobs database and stores the
resulting raw data.
"""

from job_database import JobsDb

def main():
    """main.
    Loads the query from make_dataset.sql, executes the query ans saves the
    result as a csv file.
    """
    with open('./make_dataset.sql', mode='r') as file:
        query = file.read()
    db = JobsDb()
    data = db.load_query_as_df(query)
    db.close()
    data.to_csv('data/raw/data.csv')

if __name__ == '__main__':
    main()
