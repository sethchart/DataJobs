# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
from pathlib import Path


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Takes raw data (data/raw) and executes transformer step to produce
    processed data (data/processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making processed dataset from raw dataset.')
    df = pd.read_csv(Path(input_filepath).joinpath('dataset.csv'))

    df.to_csv(Path(output_filepath).joinpath('dataset.csv'))

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    # load_dotenv(find_dotenv())

    main()
