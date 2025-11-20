import pandas as pd


# Helper to parse ID "1.2" -> (1,2) for sorting
def parse_id(id_str):
    parts = id_str.split(".")
    return int(parts[0]), int(parts[1])


def group_data(data):
    groups = {}
    for doc_id, sentence in zip(data["ids"], data["sentences"]):
        unit_id, seq_id = parse_id(doc_id)

        if unit_id not in groups:
            groups[unit_id] = []

        # store sequence ID, we can sort later
        groups[unit_id].append((seq_id, sentence))
    return groups


def align_hplt_groups(src_data, tgt_data):
    # Group sentences by Unit ID (prefix)
    src_groups = group_data(src_data)
    tgt_groups = group_data(tgt_data)

    aligned_pairs = []

    # Iterate through Unit IDs found in source
    # Sorting Key to keep processing order deterministic
    for unit_id in sorted(src_groups.keys()):
        # Only process if this Unit ID exists in both languages
        if unit_id in tgt_groups:
            # Sort by Suffix (.1, .2, .3)
            # Ensuring that "1.1" comes before "1.2"
            src_list = sorted(src_groups[unit_id], key=lambda x: x[0])
            tgt_list = sorted(tgt_groups[unit_id], key=lambda x: x[0])

            # Join text
            en_combined = " ".join([text for _, text in src_list]).strip()
            th_combined = " ".join([text for _, text in tgt_list]).strip()

            if en_combined and th_combined:
                aligned_pairs.append(
                    {
                        "en_text": en_combined,
                        "th_text": th_combined,
                    }
                )
    return aligned_pairs


def convert_hplt_json_to_csv(src_json, tgt_json, output_filename="hplt_aligned.csv"):
    aligned_pairs = align_hplt_groups(src_json, tgt_json)

    df = pd.DataFrame(aligned_pairs)

    df.to_csv(output_filename, index=False, encoding="utf-8")

    print(f"Saved in to {output_filename}")
