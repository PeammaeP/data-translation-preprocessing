import json
import os

from document_document.scb_mt import convert_scb_mt_to_sharegpt


def convert_datasets(
    output_dir="./sharegpt_datasets",
    samples_per_dataset=None,
    prompt_style="structured",
    few_shot_k=1,
    which_dataset=None,
    which_file=None,
):
    """
    Convert all datasets to ShareGPT formart following best practices

    Args:
        output_dir: Output Directories
        sample_per_dataset: Max samples per dataset (None for all)
        prompt_style: 'zero_shot', 'one_shot', 'few_shot', 'structured'
        few_shot_k: Number of examples for few-shot (1-5)
    """
    os.makedirs(output_dir, exist_ok=True)

    conversion = []

    if which_dataset == "scb-mt":
        print("\n=== Conversting SCB-MT-EN-TH-2020 ===")
        try:
            scb_data = convert_scb_mt_to_sharegpt(
                max_samples=samples_per_dataset,
                prompt_style=prompt_style,
                few_shot_k=few_shot_k,
                which_file=which_file,
            )
            conversion.append(("scb_mt_train", scb_data))
        except Exception as e:
            print(f"Error converting SCB-MT {e}")

    path = os.path.join(output_dir, f"{which_dataset}_{which_file}_sharegpt.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(conversion, f, ensure_ascii=False, indent=2)
    print(f"\n Saved {len(conversion)} to {path}")

    # Create metadata file
    metadata = {
        "total_conversations": len(conversion),
        "prompt_style": prompt_style,
        "few_shot_k": few_shot_k if prompt_style == "few_shot" else 0,
        "datasets": {name: len(data) for name, data in conversion},
    }

    metadata_path = os.path.join(
        output_dir, f"{which_dataset}_{which_file}_metadata.json"
    )
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return conversion
