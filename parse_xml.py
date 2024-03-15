import xml.etree.ElementTree as ET
import arabic_reshaper
from bidi.algorithm import get_display
import random
import cv2
import numpy as np

SOURCE = 'arwiki-20180120-pages-articles-multistream.xml'

ALLOWED_CHARS = ['ا', 'أ', 'إ', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ـ', 'ﻷ',
                 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ة', 'ه', 'و', 'ي', 'ى', 'ئ']

NUM_MAPPING = {"0": "٠",
               "1": "١",
               "2": "٢",
               "3": "٣",
               "4": "٤",
               "5": "٥",
               "6": "٦",
               "7": "٧",
               "8": "٨",
               "9": "٩"}

ALLOWED_NUMS = list(NUM_MAPPING.values())

ALLOWED_PUNC = ["!", ".", "_", "؟", "،",
                "-", "%", "*", "$", "(", ")", ":", ",", "/", "\\", "\n", "ً", "؛"]

ALLOWED_PUNC2 = ["!", "_", ")", "(", "*"]

TOTAL_LINES = 5000
NUM_LINES_SPLIT = 0.75

num_lines_ct = 0


def success_criteria(char):
    return char in ALLOWED_CHARS or\
        char in ALLOWED_PUNC or\
        char in ALLOWED_NUMS


def includes(text, allow_list):
    return any(
        [True for char in text if char in allow_list])


context = ET.iterparse(SOURCE, events=("start", "end"))

corpus = set()
for index, (event, elem) in enumerate(context):

    if isinstance(elem.text, str):
        splitted_text = elem.text.split(" ")
        cleaned_words = []

        for word in splitted_text:
            # replace english nums with arabic ones.
            for key, value in NUM_MAPPING.items():
                word = word.replace(key, value)

            word = word.replace("\t", "").replace("\r", "").strip()
            # must be in allowed chars, punc and nums
            is_allowed_word = all(list(map(success_criteria, word)))

            if is_allowed_word:
                cleaned_words.append(word)

        full_text = " ".join(cleaned_words)
        lines = full_text.split("\n")

        window_size = 75
        for line in lines:
            for punc in ALLOWED_PUNC2:
                line = line.replace(punc, "")

            for i in range(0, len(line)-window_size, window_size):
                window_line = line[i: window_size+i]

                window_line = " ".join(
                    [word for word in window_line.split(" ") if len(word) > 3])

                # slice_idx = random.randint(4, 6)
                # final_line = " ".join(window_line.split(" ")[:slice_idx])

                if len(window_line) >= 3 and (includes(window_line, ALLOWED_NUMS) or num_lines_ct >= int(NUM_LINES_SPLIT*TOTAL_LINES)):
                    num_lines_ct += 1
                    corpus.add(window_line)
                    if len(corpus) % 1_000 == 0 and len(corpus) >= 1_000:
                        print(len(corpus))

    # if we have reached our percentage of lines containing numbers we will break
    if num_lines_ct >= int(NUM_LINES_SPLIT*TOTAL_LINES) and len(corpus) >= TOTAL_LINES:
        break

print(len(corpus))

joined_corpus = " ".join(corpus)
with open("ara.txt", "w", encoding="utf-8") as file:
    for line in corpus:
        file.write(line+"\n")
# corpus = set(map(lambda x: get_display(arabic_reshaper.reshape(x)), corpus))
# generator = GeneratorFromStrings(
#     list(corpus),
#     blur=0,
#     random_blur=False,
#     fonts=["Arial"]
# )

# for i, (img, lbl) in enumerate(generator):
#     if img:
#         # print(type(img))
#         # print(lbl)
#         cv2.imwrite(f"out{i}.jpg", np.array(img))
# for text in corpus:
# print("*"*20)
# print(text)
#     print("*"*20)

# ALLOWED_PUNC = ["!", ".", "_",
#                 ")", "(", "-", '"', "'", "»", "«", "=", "]", "["]
