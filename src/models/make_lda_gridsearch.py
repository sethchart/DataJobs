# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
from collections import defaultdict
from scipy import io
from joblib import dump
from pathlib import Path
from sklearn.decomposition import LatentDirichletAllocation

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Takes processed data and runs a search over LDA hyper-parameters.
    """
    logger = logging.getLogger(__name__)
    logger.info('grid searching model hyper-parameters for LDA model.')
    description_matrix = io.mmread(
        Path(input_filepath).joinpath('descriptions.mtx')
    )
    scores = defaultdict(list)
    for n_components in range(6, 52, 2):
        lda = LatentDirichletAllocation(
            n_components = n_components,
            learning_method = 'online',
            learning_decay = 0.9,
            n_jobs = -1
        )
        lda.fit(description_matrix)
        dump(lda,
             Path(output_filepath).joinpath(f'lda-{n_components}_topics.joblib')
            )
        perplexity = lda.perplexity(description_matrix)
        scores['n_components'].append(n_components)
        scores['perplexity'].append(perplexity)

    pd.DataFrame(scores).to_csv(
        Path(output_filepath).joinpath('scores.csv')
    )

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    # load_dotenv(find_dotenv())

    main()
