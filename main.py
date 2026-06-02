import os
import pandas as pd
from datasets import load_dataset, Dataset
from dotenv import load_dotenv

load_dotenv()

def download_and_push():
    HF_DATASET_ID = "adeshkin/kjh-asr-sents"
    NEW_SENTENCES_FILE = "/home/adeshkin/Downloads/common_voice_life_final.txt"
    dataset = load_dataset(HF_DATASET_ID, split="train")
    old_df = dataset.to_pandas()

    new_sentences = []
    with open(NEW_SENTENCES_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                new_sentences.append({"kjh": line})

    new_df = pd.DataFrame(new_sentences)
    combined_df = pd.concat([old_df, new_df], ignore_index=True)
    print(len(combined_df))
    combined_df = combined_df.drop_duplicates(subset="kjh", keep="first")
    print(len(combined_df))
    kjh_sents = combined_df['kjh'].values.tolist()
    text = ' '.join(kjh_sents)
    print(repr(''.join(sorted(set(text)))))
    combined_df = combined_df.reset_index(drop=True)
    print(combined_df.head())
    hf_dataset = Dataset.from_pandas(combined_df, preserve_index=False)

    hf_dataset.push_to_hub(
        "adeshkin/kjh-asr-sents",
        split='train',
        token=os.getenv("WRITE_HF_TOKEN")
    )


if __name__ == "__main__":
    download_and_push()
