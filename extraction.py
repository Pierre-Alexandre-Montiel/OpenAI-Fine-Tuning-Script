import os
from click import progressbar
import docx
import pandas as pd
import jsonlines
import tiktoken
import openai
import config
import time
from progress.bar import IncrementalBar
import pyfiglet

def jsonl_creation(filename, core, output_file):
    with jsonlines.open(output_file, mode='a') as writer:
        data = {'prompt': "name: " + filename + "\n\n###\n\n", 'completion': " ".join(core)}
        writer.write(data)

def token_amount(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def extraction():
    initial_count = 0
    len = 0;
    dir = "C:/Users/p.a.montiel/OpenAI_contrats/datasets"
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            initial_count += 1
    files = os.listdir(dir)
    output_file = 'training_data.jsonl'
    bar = IncrementalBar('Documents extraction', max = initial_count)
    while len < initial_count :
        file_path = dir + '/' + files[len]
        doc = docx.Document(file_path)
        text = ([paragraph.text for paragraph in doc.paragraphs])

        jsonl_creation(files[len], text, output_file)
        len += 1
        bar.next()
        time.sleep(1)
    bar.finish()

def fine_tuning(id):
    params = {
    "training_file": id,
    "model": "curie",
    "suffix": "Demo",
    "n_epochs": 1
    }
    wip = openai.FineTune.create(**params)
    bar = IncrementalBar('Model Fine-tuning', max = 1000)
    print("\033[92m { Fine tuning model created with id }=> \033[00m", wip.id)
    status = openai.FineTune.retrieve(id=wip.id)["status"]
    if status not in ["succeeded", "failed"]:
        print(f'Job not in terminal status: {status}. Waiting.')
        while status not in ["succeeded", "failed"]:
            time.sleep(8)
            status = openai.FineTune.retrieve(id=wip.id)["status"]
            print(f' Status: {status}')
            bar.next()
            time.sleep(1)
    else:
        print(f'Fine-tune job {wip.id} finished with status: {status}')
    bar.finish()

def data_upload(filepath):
    openai.api_key = config.api_key
    response = openai.File.create(
    purpose="fine-tune",
    file=open(filepath, 'rb'),
    )
    bar = IncrementalBar('Data upload', max = 3)
    i = 0
    while i < 3:
        bar.next()
        time.sleep(1)
        i += 1
    bar.finish()
    print("\033[92m { file create and upload with id }=> \033[00m", response.id)
    fine_tuning(response.id)

if __name__ == '__main__':
    ascii_banner = pyfiglet.figlet_format("Extraction")
    print(ascii_banner)
    time.sleep(2)
    extraction()
    time.sleep(3)
    tmp1 = time.time()
    data_upload('C:/Users/p.a.montiel/OpenAI_contrats/training_data.jsonl')
    tmp2 = time.time()
    print("Global creation time: \033[96m{:.2f}\033[00m seconds".format(tmp2 - tmp1))
   # text = """The OpenAI API can be applied to virtually any task that involves understanding or generating natural language or code. We offer a spectrum of models with different levels of power suitable for different tasks, as well as the ability to fine-tune your own custom models. These models can be used for everything from content generation to semantic search and classification."""
   #num_tokens = token_amount(text, "gpt2")
   # print(num_tokens)