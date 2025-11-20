import csv


def merge_txt_stream(english_file, thai_file, output_file):
    print("Merging files ...")

    with open(english_file, "r", encoding="utf-8") as f_en, open(
        thai_file, "r", encoding="utf-8"
    ) as f_th, open(output_file, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.writer(f_out)

        # writer header
        writer.writerow(["en_text", "th_text"])

        # zip() reads both files lijne by line simultaneously
        for en_line, th_line in zip(f_en, f_th):
            writer.writerow([en_line.strip(), th_line.strip()])

    print(f"Saved to {output_file}")
