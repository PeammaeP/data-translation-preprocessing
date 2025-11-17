from typing import List


class TranslationPromptTemplate:
    """
    Implements prompting strategies from:
    - Adaptive MT with fuzzy matches (zero-shot, one-shot, few-shot)
    - Structured Format to preserve LLM capabilities
    """

    @staticmethod
    def zero_shot(source_text: str, source_lang: str, target_lang: str) -> str:
        """
        Zero-shot template
        """
        return f"Translate this from {source_lang} to {target_lang}:\n{source_lang} : {source_text}\n {target_lang}:"

    @staticmethod
    def one_shot(
        source_text: str,
        example_src: str,
        example_target: str,
        source_lang: str,
        target_lang: str,
    ) -> str:
        """
        One-shot template
        """
        return (
            f"Translate this from {source_lang} to {target_lang}:\n"
            f"{source_lang}: {example_src}\n"
            f"{target_lang}: {example_target}\n"
            f"{source_lang}: {source_text}\n"
            f"{target_lang}:"
        )

    @staticmethod
    def few_shot(
        source_text: str, source_lang: str, target_lang: str, examples: List[tuple]
    ) -> str:
        """
        Few-shot Template
        Examples : [(src_1, tgt_1), (src_2, tgt_2), .. , (src_n, tgt_n)]
        """
        prompt_parts = [f"Translate this from {source_lang} to {target_lang}:"]

        for src, target in examples:
            prompt_parts.append(f"{source_lang}: {src}")
            prompt_parts.append(f"{target_lang}: {target}")

        prompt_parts.append(f"{source_lang}: {source_text}")
        prompt_parts.append(f"{target_lang}:")

        return "\n".join(prompt_parts)

    @staticmethod
    def structured_format(source_text: str, source_lang: str, target_lang: str) -> str:
        """
        Structured the format to preserve LLM capabilities
        """
        lang_map = {"English": "English", "Thai": "Thai", "en": "English", "th": "Thai"}
        src_full = lang_map.get(source_lang, source_lang)
        target_full = lang_map.get(target_lang, target_lang)

        return f"Translate the following {src_full} text to {target_full}:\n\n {source_text}"
