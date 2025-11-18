# ShareGPT Converter

This tool creates instruction-tuning datasets for Large Language Models (LLMs) by converting the [SCB-MT-2020](https://github.com/vistec-AI/dataset) English–Thai translation dataset into the **ShareGPT** format.

It supports various prompting strategies (zero-shot, one-shot, few-shot, and structured) to improve model performance during fine-tuning.

---

## 🌟 Features

- **Multiple Prompt Styles**  
  Convert data using `structured`, `zero-shot`, `one-shot`, or `few-shot` formats.

- **Dynamic Context Pooling**  
  Automatically samples random examples from the dataset to serve as "shots" for few-shot prompting, helping prevent data leakage.

- **Batch Processing**  
  Iterates through all CSV files in a directory automatically.

- **Git LFS Ready**  
  Configured to handle large JSON output files produced during conversion.

---

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/PeammaeP/data-translation-preprocessing.git
   cd data-translation-preprocessing
   ```

2. **Set up a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scriptsctivate
   ```

3. **Install dependencies**

   ```bash
   pip install pandas datasets
   ```

4. **Initialize Git LFS**

   Since the generated JSON files can be large (>100MB), you must install Git Large File Storage (LFS) before pushing to GitHub.

   ```bash
   git lfs install
   git lfs track "*.json"
   ```

---

## 📂 Data Structure

### Input Format

The tool expects a directory (default: `data/scb_2020/`) containing CSV files with at least the following columns:

- `en_text`: English sentence  
- `th_text`: Thai sentence  

### Output Format (ShareGPT)

The output will be saved in:

```text
sharegpt/{dataset}_{style}/
```

Example (`sharegpt/scb-mt_structured/data.json`):

```json
[
  {
    "conversations": [
      {
        "from": "human",
        "value": "Translate the following English sentence to Thai: Hello world"
      },
      {
        "from": "gpt",
        "value": "สวัสดีชาวโลก"
      }
    ],
    "system": "You are a professional English-Thai translator."
  }
]
```

---

## 🚀 Usage

Run `main.py` to convert your datasets.

### 1. Default Run (Structured Mode)

Converts all CSV files using the basic structured prompt.

```bash
python main.py
```

### 2. Zero-Shot Mode

Asks the model to translate without providing examples.

```bash
python main.py --prompt_style zero-shot
```

### 3. One-Shot Mode

Includes 1 random example from the dataset in the prompt context.

```bash
python main.py --prompt_style one-shot --pool_size 500
```

### 4. Few-Shot Mode

Includes `K` random examples in the prompt context.

```bash
# 3-shot learning
python main.py --prompt_style few-shot --few_shot_k 3
```

### 5. Custom Directories

If your raw CSV files are in a different location:

```bash
python main.py --data_dir "./raw_data" --dataset "custom-dataset"
```

---

## ⚙️ Arguments Reference

| Argument        | Type | Default         | Description                                                 |
|----------------|------|-----------------|-------------------------------------------------------------|
| `--prompt_style` | str  | `structured`    | Strategy: `zero-shot`, `one-shot`, `few-shot`, `structured` |
| `--dataset`      | str  | `scb-mt`        | Name of the dataset (used for folder naming).              |
| `--data_dir`     | str  | `data/scb_2020` | Directory containing the input CSV files.                  |
| `--few_shot_k`   | int  | `0`             | Number of examples to use (only for few-shot style).       |
| `--pool_size`    | int  | `1000`          | Number of samples to reserve for context generation.       |

---

## ⚠️ Troubleshooting

### “File is too large” error when pushing

If you see an error like:

> `File sharegpt/... is 104.45 MB; this exceeds GitHub's file size limit`

it means Git LFS was not tracking the files when they were committed.

**Fix:**

```bash
git lfs track "*.json"
git add .gitattributes
git reset --soft HEAD~1  # Undo the last commit but keep files
git add .                # Re-add files (LFS will now pick them up)
git commit -m "Add large dataset files with LFS"
git push origin main
```
