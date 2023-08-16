
## Description

[Python]- This Python script extracts text data from documents, creates JSONL files, and fine-tunes an OpenAI language model using the extracted data.

## Installation

```bash
$ pip install -r requirements.txt
```

## Dependencies

```bash
$ os
$ docx
$ pandas
$ jsonlines
$ tiktoken
$ openai
$ time
$ progress
$ pyfiglet
$ click
```

## Running the script

```bash
# production mode
$ python .\extraction.py

```

## Acknowledgments

OpenAI API documentation for providing instructions on how to use the API = https://beta.openai.com/docs/api-reference/introduction.
click for providing a command line interface for the script = https://click.palletsprojects.com/en/7.x/.
docx for providing the ability to read and write .docx files = https://python-docx.readthedocs.io/en/latest/.
