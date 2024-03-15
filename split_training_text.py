import os
import random
import pathlib
import subprocess

training_text_file = 'ara.txt'

lines = []
FONTS = ["Arial", "DIN Next LT Arabic", "Arial,Bold",
         "DIN Next LT Arabic,Medium", "Frutiger LT Arabic Bold Condensed"]

DIMS = [["3800", "480"]]

# DIMS = [["2000", "300"]]

with open(training_text_file, 'r') as input_file:
    for line in input_file.readlines():
        lines.append(line.strip())

output_directory = 'tesstrain/data/DIN-ground-truth'

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

random.shuffle(lines)

count = 4000

lines = lines[:count]

line_count = 0
for line in lines:
    training_text_file_name = pathlib.Path(training_text_file).stem
    line_training_text = os.path.join(
        output_directory, f'{training_text_file_name}_{line_count}.gt.txt')
    with open(line_training_text, 'w') as output_file:
        output_file.writelines([line])

    file_base_name = f'ara_{line_count}'
    random_index = random.Random().randint(0, len(FONTS)-1)
    random_font = FONTS[random_index]
    random_index = random.Random().randint(0, len(DIMS)-1)
    random_dim = DIMS[random_index]

    text_file = open(line_training_text)
    word_ct = len(text_file.readline())
    text_file.close()

    # zoom control
    # factor = 100
    # factor = random.randint(250, 500)
    # constant = 100
    # x_length = word_ct*factor + constant
    # print(random_font)
    # --ptsize
    # font_sizes []
    subprocess.run([
        'text2image',
        f'--font={random_font}',
        f'--text={line_training_text}',
        f'--outputbase={output_directory}/{file_base_name}',
        '--max_pages=1',
        '--strip_unrenderable_words',
        '--leading=0',
        f'--xsize={random_dim[0]}',
        f'--ysize={random_dim[1]}',
        '--char_spacing=0.2',
        '--resolution=600',
        '--ptsize=14',
        '--exposure=0',
        '--unicharset_file=langdata/ara.unicharset'
    ])

    line_count += 1
