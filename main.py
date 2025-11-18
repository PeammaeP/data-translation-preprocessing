import argparse
import json
import os
from pathlib import Path

from conversion import convert_datasets


def parse_arguments():
    parser = argparse.ArgumentParser(description="Dataset to ShareGPT Converter")

    parser.add_argument(
        "--dataset",
        type=str,
        default="scb-mt",
        help="Name of the dataset (default: scb-mt)",
    )

    parser.add_argument(
        "--data_dir",
        type=str,
        default="data/scb_2020",
        help="Path to the dictionary containing CSV files",
    )

    parser.add_argument(
        "--prompt_style",
        type=str,
        default="structured",
        choices=["zero-shot", "one-shot", "few-shot", "structured"],
        help="The prompting strategy to use",
    )

    parser.add_argument(
        "--few_shot_k",
        type=int,
        default=0,
        help="Number of example for few-shot (only used if style is few-shot)",
    )

    parser.add_argument(
        "--pool_size",
        type=int,
        default=1000,
        help="Size of the context pool for sampling examples",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    print("Dataset to ShareGPT Converter")
    print("Following the research-backed prompting strategies")

    print(f"Mode: {args.prompt_style}")
    if args.prompt_style == "few-shot":
        print(f"K-Shot: {args.few_shot_k}")

    output_dir = f"./sharegpt/{args.dataset}_{args.prompt_style}"
    # Define the directory to iterative over
    data_dir = Path("data/scb_2020")

    conversion_result = []
    current_file_name = None
    processed_files_stats = {}

    if not data_dir.exists():
        print(f"Error: Directory {data_dir} not found.")
        exit(1)

    for file_path in data_dir.iterdir():
        if file_path.is_file() and file_path.suffix == ".csv":
            current_file_name = file_path.name

            conversion = convert_datasets(
                output_dir=output_dir,
                samples_per_dataset=None,
                prompt_style=args.prompt_style,
                few_shot_k=args.few_shot_k,
                context_pool_size=args.pool_size,
                which_dataset=args.dataset,
                which_file=current_file_name,
            )

            if conversion:
                processed_files_stats[current_file_name] = len(conversion)

    # Create metadata file
    metadata = {
        "dataset_name": args.dataset,
        "prompt_style": args.prompt_style,
        "few_shot_k": args.few_shot_k if args.prompt_style == "few-shot" else 0,
        "context_pool_size": args.pool_size,
        "files_processed": processed_files_stats,
        "total_samples": sum(processed_files_stats.values()),
    }

    metadata_path = os.path.join(
        output_dir, f"{args.dataset}_{args.prompt_style}_metadata.json"
    )
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nConversion complete. Metadata saved to {metadata_path}")
