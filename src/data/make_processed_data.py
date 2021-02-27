# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
from scipy import io
from pickle import dump
from pathlib import Path
from src.features.vectorizers import description_vectorizer, title_vectorizer


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
    descriptions = df['description'].tolist()
    description_matrix = description_vectorizer.fit_transform(descriptions)
    io.mmwrite(Path(output_filepath).joinpath('descriptions.mtx'),
               description_matrix)
    description_tokens = description_vectorizer.get_feature_names()
    dump(description_tokens,
         open(Path(output_filepath).joinpath('description_tokens.pkl'),'wb')
        )
    titles = df['title'].tolist()
    title_matrix = title_vectorizer.fit_transform(descriptions)
    io.mmwrite(Path(output_filepath).joinpath('titles.mtx'), title_matrix)
    title_tokens = title_vectorizer.get_feature_names()
    dump(title_tokens,
         open(Path(output_filepath).joinpath('title_tokens.pkl'), 'wb')
        )

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    # load_dotenv(find_dotenv())

    main()
