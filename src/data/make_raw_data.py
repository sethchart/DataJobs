# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from src.data.job_database import JobsDb
# from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Gets data from external source (data/external) and saves raw dataset
    for analysis (data/raw).
    """
    logger = logging.getLogger(__name__)
    logger.info('making raw dataset from external source.')
    query_file = Path(__file__).resolve().parents[0].joinpath('make_raw_data.sql')
    with open(query_file, mode='r') as file:
        query = file.read()
    db = JobsDb(Path(input_filepath).joinpath('jobs.sqlite'))
    df = db.load_query_as_df(query)
    db.close()
    df.to_csv(Path(output_filepath).joinpath('dataset.csv'))

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    # load_dotenv(find_dotenv())

    main()
