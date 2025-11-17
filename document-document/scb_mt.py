import random

from datasets import load_dataset

from template.prompt_template import TranslationPromptTemplate


def convert_scb_mt_to_sharegpt(
    split="train",
    max_samples=None,
    prompt_style="structured",
    few_shot_k=0,
    context_pool_size=1000,
):
    """
    Convert SCB-MT-EN-TH-2020 to "sharegpt" format with various prompting strategies

    Args:
        split:s 'train', 'validation', or 'test'
        max_samples: Maximum number of samples to convert (None for all)
        prompt_style: 'zero_shot', 'one_shot', 'few_shot', 'structured'
        few_shot_k: Number of examples for few-shot (0-5 recommended)
        context_pool_size: Size of context pool for fuzzy matching
    """
    print(f"Loading SCB-MT-EN-TH-2020 ({split}) ...")
    dataset = load_dataset("data/scb_mt_enth_2020", split=split)

    if max_samples:
        dataset = dataset.select(range(min(max_samples, len(dataset))))

    # Create context pool for few-shot examples
    context_pool = []

    if prompt_style in ["one_shot", "few_shot"] and context_pool_size > 0:
        pool_size = min(context_pool_size, len(dataset))
        context_indices = random.sample(range(len(dataset)), pool_size)
        context_pool.append([dataset[i] for i in context_indices])

    sharegpt_data = []
    template = TranslationPromptTemplate()

    for idx, item in enumerate(dataset):
        # Skip if item is in context pool to avoid data leakage
        if idx in [dataset.index(c) for c in context_pool[:10]]:
            continue

        # EN -> TH Translation
        if prompt_style == "zero_shot":
            prompt = template.zero_shot(item["en"], "English", "Thai")
        elif prompt_style == "one_shot" and context_pool:
            example = random.choice(context_pool)
            prompt = template.one_shot(
                item["en"], example["en"], example["th"], "English", "Thai"
            )
        elif prompt_style == "few_shot" and context_pool:
            examples = random.sample(context_pool, min(few_shot_k, len(context_pool)))
            example_pairs = [(ex["en"], ex["th"]) for ex in examples]
            prompt = template.few_shot(item["en"], "English", "Thai", example_pairs)
        else:  # structured (default)
            prompt = template.structured_format(item["en"], "English", "Thai")

        sharegpt_data.append(
            {
                "conversations": [
                    {"from": "human", "value": prompt},
                    {"from": "gpt", "value": item["th"]},
                ],
                "system": "You are a professional English-Thai translator.",
            }
        )

    return sharegpt_data
