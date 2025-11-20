import pandas as pd


def convert_txt_to_csv(input_file, output_file):
    print(f"Reading {input_file}...")

    # Method: Read line by line to handle potential separator issues safely
    data = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Try splitting by TAB first (Standard)
            parts = line.split("\t")

            # If TAB fails (maybe it's multiple spaces?), try splitting by 2+ spaces
            if len(parts) < 2:
                import re

                # Split by 2 or more spaces (regex)
                parts = re.split(r"\s{2,}", line)

            if len(parts) >= 2:
                # English is the first part
                en_text = parts[0].strip()
                # Thai is the rest (joined back just in case)
                th_text = " ".join(parts[1:]).strip()

                data.append({"en_text": en_text, "th_text": th_text})
            else:
                print(f"Skipping ambiguous line: {line}")

    # Convert to DataFrame and Save
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Saved {len(df)} pairs to {output_file}")


convert_txt_to_csv("dictionary-en-th.txt", "dictionary-en-th.csv")
