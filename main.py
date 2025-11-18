import json
import os
from pathlib import Path

from conversion import convert_datasets
from template import prompt_template

if __name__ == "__main__":
    print("Dataset to ShareGPT Converter")
    print("Following the research-backed prompting strategies")

    dataset = "scb-mt"
    prompt_style = "zero-shot"
    few_shot_k = None
    conversion = []
    current_file_name = None
    output_dir = f"./sharegpt/{dataset}_{prompt_style}"

    # Define the directory to iterative over
    data_dir = Path("data/scb_2020")

    for file_path in data_dir.iterdir():
        if file_path.is_file() and file_path.suffix == ".csv":
            current_file_name = file_path.name

            # 1) Structured Format
            conversion = convert_datasets(
                output_dir=output_dir,
                samples_per_dataset=None,
                which_dataset=dataset,
                prompt_style=prompt_style,
                # Pass the current filename in a list
                which_file=current_file_name,
            )

            if conversion:
                print("\n Example Output (First Conversation):")
                print(json.dumps(conversion[0], ensure_ascii=False, indent=2))
            else:
                print("No data processed or returned for this file")

    # Create metadata file
    metadata = {
        "prompt_style": prompt_style,
        "few_shot_k": few_shot_k if prompt_style == "few_shot" else 0,
        "datasets": {name: len(data) for name, data in conversion},
    }

    metadata_path = os.path.join(output_dir, f"{dataset}_{prompt_style}_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
