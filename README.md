# ShareGPT Converter

This tool creates instruction-tuning datasets for Large Language Models (LLMs) by converting datasets from English to Thai translation dataset into the **ShareGPT** format.

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

Example:
- Zero-shot Prompting
```json
  {
    "conversations": [
      {
        "from": "human",
        "value": "Translate this from English to Thai:\nEnglish : FAR LEFT: Indonesian National Police Chief Tito Karnavian, from left, Philippine National Police Chief Ronald Dela Rosa and Royal Malaysian Police Inspector General Khalid Abu Bakar link arms before the Trilateral Security Meeting in Pasay city, southeast of Manila, Philippines, in June 2017. [THE ASSOCIATED PRESS]\n Thai:"
      },
      {
        "from": "gpt",
        "value": "(ซ้ายสุด) นายติโต คาร์นาเวียน ผู้บัญชาการตำรวจแห่งชาติอินโดนีเซีย (จากซ้าย) นายโรนัลด์ เดลา โรซา ผู้บัญชาการตำรวจแห่งชาติฟิลิปปินส์ และนายคาลิด อาบู บาการ์ ผู้บัญชาการตํารวจแห่งชาติมาเลเซีย ไขว้แขนกันก่อนเริ่มการประชุมความมั่นคงไตรภาคีในเมืองปาเซย์ ซึ่งอยู่ทางตะวันออกเฉียงใต้ของกรุงมะนิลา ประเทศฟิลิปปินส์ ในเดือนมิถุนายน พ.ศ. 2560 ดิแอสโซซิเอทเต็ด เพรส"
      }
    ],
    "system": "You are a professional English-Thai translator."
  }
```
- One-shot Prompting
```json
  {
    "conversations": [
      {
        "from": "human",
        "value": "Translate this from English to Thai:\nEnglish: South Korea has also launched Exercise Ulchi Taegeuk, a new civilian-military exercise scheduled for May 27-30, to supplant the previous joint Ulchi Freedom Guardian (UFG) exercise, which was suspended by the Pentagon in June 2018.\nThai: นอกจากนี้ เกาหลีใต้ยังเปิดตัวการฝึกภายใต้รหัส อุลชี แทกึก ซึ่งเป็นการฝึกระหว่างทหารและพลเรือนแบบใหม่ที่จะจัดขึ้นในวันที่ 27-30 พฤษภาคม เพื่อแทนที่การฝึกร่วมก่อนหน้านี้ภายใต้รหัส อุลชี ฟรีดอม การ์เดียน ซึ่งกระทรวงกลาโหมสหรัฐฯ สั่งระงับในเดือนมิถุนายน พ.ศ. 2561\nEnglish: (Pictured: A rocket believed to be a Hwasong missile such as the one used in a May 2017 North Korean test is displayed at a military parade in Pyongyang in April 2017.)To deter such conflict, Wee emphasized that the regular deployment of U.S. strategic assets was discussed at KIDD and that both sides “highlighted the importance of the deployment of the Terminal High Altitude Area Defense (THAAD) system.”\nThai:"
      },
      {
        "from": "gpt",
        "value": "(ภาพ: จรวดซึ่งเชื่อว่าเป็นขีปนาวุธฮวาซองเช่นเดียวกับที่เกาหลีเหนือใช้ในการทดสอบเมื่อเดือนพฤษภาคม พ.ศ. 2560 ได้ถูกจัดแสดงในการสวนสนามทางทหารที่กรุงเปียงยางเมื่อเดือนเมษายน พ.ศ. 2560)เพื่อยับยั้งความขัดแย้งดังกล่าว พล.ท. วีเน้นย้ำว่า การเจรจาด้านกลาโหมแบบบูรณาการระหว่างเกาหลี-สหรัฐฯ ได้แลกเปลี่ยนความคิดเห็นในเรื่องการเคลื่อนกำลังยุทโธปกรณ์ด้านยุทธศาสตร์ของสหรัฐฯ โดยปกติ และทั้งสองฝ่าย “มุ่งให้ความสำคัญกับการเคลื่อนกำลังระบบป้องกันขีปนาวุธในบริเวณพิกัดตำแหน่งสูง”"
      }
    ],
    "system": "You are a professional English-Thai translator."
  },
```
- Few-shot Prompting (K=5)
```json
  {
    "conversations": [
      {
        "from": "human",
        "value": "Translate this from English to Thai:\nEnglish: “This decision was driven by DCNS’s ability to best meet all of our unique capability requirements,” Australian Defence Minister Marise Payne wrote in an essay for the Australian Strategic Policy Institute. “These included superior sensor performance and stealth characteristics, as well as range and endurance similar to the Collins Class submarine” — the older models that the new submarines will replace.\nThai: “การตัดสินใจนี้ได้รับการผลักดันจากความสามารถของดีซีเอ็นเอสในการตอบสนองข้อกำหนดทั้งหมดของเราในด้านขีดความสามารถเฉพาะ” นางมาริส เพย์นรัฐมนตรีว่าการกระทรวงกลาโหมออสเตรเลียเขียนในบทความสำหรับสถาบันนโยบายยุทธศาสตร์ออสเตรเลีย “ซึ่งประกอบด้วยประสิทธิภาพของเซนเซอร์และคุณลักษณะการซ่อนตัวที่เหนือกว่า รวมทั้งพิสัยและความทนทานที่คล้ายคลึงกับเรือดำน้ำขั้นคอลลินส์” ซึ่งเป็นเรือดำน้ำรุ่นเก่ากว่าซึ่งเรือดำน้ำรุ่นใหม่นี้จะมาแทนที่\nEnglish: “China always adheres to the principle of the use of outer space for peaceful purposes, and opposes the weaponization of or an arms race in outer space,” it said.\nThai: “จีนปฏิบัติตามหลักการของการใช้อวกาศเพื่อวัตถุประสงค์แห่งสันติภาพอยู่เสมอ และต่อต้านการใช้อาวุธหรือการแข่งขันด้านอาวุธในอวกาศ” เอกสารระบุ\nEnglish: Under the terms of the deal, known as the Compact of Free Association, U.S. military components have exclusive access to airspace and territorial waters of the Federated States of Micronesia, the Marshall Islands and Palau. In exchange, the small islands receive financial assistance.\nThai: กองทัพสหรัฐฯ ได้รับสิทธิพิเศษในการเข้าถึงน่านฟ้าและน่านน้ำที่เป็นอาณาเขตของสหพันธรัฐไมโครนีเซีย หมู่เกาะมาร์แชล และปาเลา ภายใต้เงื่อนไขของข้อตกลงนี้ซึ่งเป็นที่รู้จักในชื่อ ความสัมพันธ์เสรี โดยประเทศที่ทำข้อตกลงจะได้รับความช่วยเหลือทางการเงินเป็นการแลกเปลี่ยน\nEnglish: “This is the new India and the flight of its dreams is endless,” Modi said at the groundbreaking ceremony for the rail, according to The Guardian newspaper. “Japan has shown that it’s a true friend of India,” Modi said.\nThai: “นี่คืออินเดียยุคใหม่ และการทะยานตามความฝันของอินเดียจะไม่สิ้นสุด” นายโมทีกล่าวในพิธีเปิดตัวโครงการรถไฟ หนังสือพิมพ์ เดอะการ์เดียน รายงาน “ญี่ปุ่นได้แสดงความเป็นมิตรแท้ต่ออินเดีย” นายโมทีกล่าว\nEnglish: Moreover, although UNCLOS talks about “rocks” and “islands” as different things, it doesn’t provide clear and measurable guidelines about how to distinguish between the two. As a result of these and other particularities, the specifics of many cases are not answered directly by the treaty. They are worked out gradually through state practice and jurisprudence. This isn’t a bad thing, but it does takes time and, in the meantime, leaves governments with little guidance about whether their claims are “reasonable” or likely to be supported by law.\nThai: นอกจากนี้ แม้อนุสัญญาสหประชาชาติว่าด้วยกฎหมายทางทะเลจะระบุว่า “โขดหิน” และ “หมู่เกาะ” เป็นสิ่งที่แตกต่างกัน แต่ก็ไม่ได้ระบุแนวทางที่ชัดเจนและสามารถวัดได้เกี่ยวกับวิธีการแยกแยะความแตกต่างระหว่างพื้นที่สองลักษณะนี้ ความไม่ชัดเจนเหล่านี้และลักษณะเฉพาะอื่น ๆ ทำให้ไม่มีคำตอบโดยตรงที่เป็นรายละเอียดเฉพาะจากอนุสัญญาในหลายกรณี ประเทศต่าง ๆ ค่อย ๆ แก้ปัญหาโดยใช้แนวปฏิบัติของรัฐและหลักกฎหมาย แม้จะไม่ใช่เรื่องที่ไม่ดีแต่มันก็ใช้เวลานาน ในขณะเดียวกันก็ทำให้รัฐบาลของประเทศเหล่านั้นมีแนวทางเพียงเล็กน้อยในการพิจารณาว่าการอ้างสิทธิของตนนั้น “มีเหตุผล” หรือมีแนวโน้มที่จะได้รับการสนับสนุนตามกฎหมายหรือไม่\nEnglish: FAR LEFT: Indonesian National Police Chief Tito Karnavian, from left, Philippine National Police Chief Ronald Dela Rosa and Royal Malaysian Police Inspector General Khalid Abu Bakar link arms before the Trilateral Security Meeting in Pasay city, southeast of Manila, Philippines, in June 2017. [THE ASSOCIATED PRESS]\nThai:"
      },
      {
        "from": "gpt",
        "value": "(ซ้ายสุด) นายติโต คาร์นาเวียน ผู้บัญชาการตำรวจแห่งชาติอินโดนีเซีย (จากซ้าย) นายโรนัลด์ เดลา โรซา ผู้บัญชาการตำรวจแห่งชาติฟิลิปปินส์ และนายคาลิด อาบู บาการ์ ผู้บัญชาการตํารวจแห่งชาติมาเลเซีย ไขว้แขนกันก่อนเริ่มการประชุมความมั่นคงไตรภาคีในเมืองปาเซย์ ซึ่งอยู่ทางตะวันออกเฉียงใต้ของกรุงมะนิลา ประเทศฟิลิปปินส์ ในเดือนมิถุนายน พ.ศ. 2560 ดิแอสโซซิเอทเต็ด เพรส"
      }
    ],
    "system": "You are a professional English-Thai translator."
  },
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
