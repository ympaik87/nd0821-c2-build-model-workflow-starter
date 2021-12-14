#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    input_artifact_df = pd.read_csv(artifact_local_path)

    min_price = args.min_price
    max_price = args.max_price
    idx = input_artifact_df['price'].between(min_price, max_price)
    input_artifact_df = input_artifact_df[idx].copy()
    logger.info("Dataset `price` range is set as: %s - %s",
                min_price, max_price)

    input_artifact_df['last_review'] = pd.to_datetime(
        input_artifact_df['last_review'])
    logger.info('Dataset `last_review` type is set as datetime')

    output_artifact_path = args.output_artifact
    input_artifact_df.to_csv(output_artifact_path, index=False)
    logger.info("Artifact is saved to %s", output_artifact_path)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(output_artifact_path)
    run.log_artifact(artifact)
    logger.info("Cleaned dataset uploaded to Wandb")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help='Type an input artifect name (string)',
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help='Type an output artifect name (string)',
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help='Type an output type (string)',
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Type a description for output (string)",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help='Type minimum price to consider (float)',
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help='Type maximum price to consider (float)',
        required=True
    )

    args_in = parser.parse_args()

    go(args_in)
