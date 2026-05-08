# https://commonvoice.mozilla.org/kjh/write
import pandas as pd
import re
from razdel import tokenize, sentenize


def count_syllables(text):
    vowels = set("ёеыаоэяиюуіӧӱ")
    syllables_count = sum(1 for char in text.lower() if char in vowels)

    return syllables_count


def filter_sentences(sentences):
    filtered_sentences = []

    allowed_pattern = re.compile(r'^[А-Яа-яЁёІіҒғҢңҶҷӦӧӰӱ\s.,!?]+$')
    acronym_pattern = re.compile(r'\b[А-ЯЁІҒҢҶӦӰ]{2,}\b')

    for sentence in sentences:
        sentence = re.sub(r'\s+', ' ', sentence)
        sentence = re.sub(r'\s+([.,!?])', r'\1', sentence)

        original = sentence.strip()
        if not original:
            continue

        if original.count('...') > 0:
            continue

        if len(list(sentenize(original))) != 1:
            continue

        tokens = list(tokenize(original))
        words = [token.text for token in tokens if any(c.isalpha() for c in token.text)]

        if not (3 <= len(words) <= 12):
            continue

        if re.search(r'\d', original):
            continue

        if acronym_pattern.search(original):
            continue

        if not allowed_pattern.match(original):
            print(original)
            continue

        if original.count(',') > 2:
            continue

        filtered_sentences.append(original)

    return filtered_sentences


def clean_text(text):
    text = ' '.join(re.findall(r'[^\W\d_]+', text))
    text = re.sub(r'\\s+', ' ', text)

    return text.strip()


def main():
    with open('/home/adeshkin/Downloads/prince_kjh_ru_khakas_fixed.txt') as f:
        chosen_sentences1 = [x.strip() for x in f.readlines()]

    chosen_sentences = []
    for sent in chosen_sentences1:
        sentences = [s.text for s in sentenize(sent)]
        chosen_sentences.extend(sentences)

    print(len(chosen_sentences))
    filtered_sentences = filter_sentences(chosen_sentences)
    print('filtered_sentences', len(filtered_sentences))

    df = pd.DataFrame(filtered_sentences, columns=['kjh'])
    df['syl_count'] = df['kjh'].apply(lambda x: count_syllables(x))
    df = df[(df['syl_count'] >= 5) & (df['syl_count'] <= 30)]
    df['kjh'] = df['kjh'].apply(lambda x: x.removeprefix("– "))

    print(len(df))
    df['kjh_lower'] = df['kjh'].str.lower()
    df['kjh_word'] = df['kjh_lower'].apply(clean_text)
    df = df.drop_duplicates(subset='kjh_word', keep='first')
    print(len(df))

    # df, _ = train_test_split(
    #     df,
    #     train_size=1000,
    #     stratify=df['syl_count'],
    #     random_state=42
    # )

    with open('/home/adeshkin/Downloads/common_voice_little_prince.txt', 'w') as f:
        for sent in df['kjh'].values.tolist():
            f.write(sent.strip() + '\n')

    df.to_csv('/home/adeshkin/Downloads/common_voice_little_prince.csv', index=False)


if __name__ == '__main__':
    main()
