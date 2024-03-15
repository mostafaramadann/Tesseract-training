## Setup:

1. Download data and unzip it in root directory.
2. Create dir tesstrain/data/DIN-ground-truth
3. Download base model (\*.traineddata) from [tessdata best](https://github.com/tesseract-ocr/tessdata_best)
4. Create a dir tesstrain/data/ara
5. Extract base model in the previous directory using command: combine_tessdata -u ara.traineddata dx

6. Copy traineddata file to tesstrain/tessdata
7. Make sure to install fonts used in split_training_text.py on local machine.

## Run:

```python
    python3 parse_xml.py
    python3 split_training_text.py
```

## Training and evaluation:

```shell
make training TESSDATA=tessdata GROUND_TRUTH_DIR=data/DIN-ground-truth MODEL_NAME=dx MAX_ITERATIONS=2500 START_MODEL=ara FINETUNE_TYPE=LAYER LANG_TYPE=RTL
```

## Load model:

```shell
sudo cp data/dx.traineddata /usr/share/tesseract-ocr/<tesseract_version>/tessdata/
```

## Inference:

```shell
tesseract image_file output.txt -l dx
```
