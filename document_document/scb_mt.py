import random

import pandas as pd
from datasets import Dataset

from template.prompt_template import TranslationPromptTemplate


def convert_scb_mt_to_sharegpt(
    max_samples=None,
    prompt_style="structured",
    few_shot_k=0,
    context_pool_size=1000,
    which_file=None,
    translation="en2th",
):
    """
    Convert SCB-MT-EN-TH-2020 to "sharegpt" format with various prompting strategies

    Args:
        max_samples: Maximum number of samples to convert (None for all)
        prompt_style: 'zero_shot', 'one_shot', 'few_shot', 'structured'
        few_shot_k: Number of examples for few-shot (0-5 recommended)
        context_pool_size: Size of context pool for fuzzy matching
    """
    print("Loading SCB-MT-EN-TH-2020 ...")
    df = pd.read_csv(f"./data/scb_2020/{which_file}")
    dataset = Dataset.from_pandas(df)

    if max_samples:
        dataset = dataset.select(range(min(max_samples, len(dataset))))

    # Create context pool for few-shot examples
    context_pool_list = []
    context_indices_set = set()

    if prompt_style in ["one-shot", "few-shot"] and context_pool_size > 0:
        pool_size = min(context_pool_size, len(dataset))

        context_indices = random.sample(range(len(dataset)), pool_size)
        context_indices_set = set(context_indices)

        context_pool_list = dataset.select(context_indices).to_list()

    sharegpt_data = []
    template = TranslationPromptTemplate()

    for idx, item in enumerate(dataset):
        # Skip if item is in context pool to avoid data leakage
        if idx in context_indices_set:
            continue

        if translation == "en2th":
            src_lang = "English"
            tgt_lang = "Thai"
            ex_src_key = "en_text"
            ex_tgt_key = "th_text"
            src_text = item[ex_src_key]
            tgt_text = item[ex_tgt_key]
        else:
            src_lang = "Thai"
            tgt_lang = "English"
            ex_src_key = "th_text"
            ex_tgt_key = "en_text"
            src_text = item[ex_src_key]
            tgt_text = item[ex_tgt_key]

        prompt = ""

        # EN -> TH Translation
        if prompt_style == "zero-shot":
            prompt = template.zero_shot(src_text, src_lang, tgt_lang)
        elif prompt_style == "one-shot" and context_pool_list:
            example = random.choice(context_pool_list)
            prompt = template.one_shot(
                src_text,
                example[ex_src_key],
                example[ex_tgt_key],
                src_lang,
                tgt_lang,
            )
        elif prompt_style == "few-shot" and context_pool_list:
            k = min(few_shot_k, len(context_pool_list))

            examples = random.sample(context_pool_list, k)

            example_pairs = [(ex[ex_src_key], ex[ex_tgt_key]) for ex in examples]
            prompt = template.few_shot(src_text, src_lang, tgt_lang, example_pairs)
        else:  # structured (default)
            prompt = template.structured_format(src_text, src_lang, tgt_lang)

        sharegpt_data.append(
            {
                "conversations": [
                    {"from": "human", "value": prompt},
                    {"from": "gpt", "value": tgt_text},
                ],
                "system": f"You are a professional {src_lang}-{tgt_lang} translator.",
            }
        )

    return sharegpt_data
