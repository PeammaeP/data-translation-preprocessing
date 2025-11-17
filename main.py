import json

from conversion import convert_datasets

if __name__ == "__main__":
    print("Dataset to ShareGPT Converter")
    print("Following the research-backed prompting strategies")

    dataset = "scb-mt"
    file = "assorted_government.csv"
    prompt_style = "zero-shot"

    # 1) Structured Format
    scb_data = convert_datasets(
        output_dir=f"./sharegpt/{dataset}_{prompt_style}",
        samples_per_dataset=None,
        which_dataset=dataset,
        prompt_style=prompt_style,
        which_file=file,
    )

    print("\n Example Output (First Conversation):")
    print(json.dumps(scb_data[0], ensure_ascii=False, indent=2))
