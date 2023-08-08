# PDF2OCR - Client

This is an example client in python of how to use the PDF to OCR Api provided by rapidApi:

https://rapidapi.com/globalw/api/pdf-to-ocr

## Precompiled Binary Usage

In order to use the client without installation, we have added a precompiled executable:

Windows:

```bash

```

## Installation from Source

```bash
pip install -r requirements.txt
```

## Usage

Specify YOUR-API-KEY in the command options by using the parameter ```--api-key```
Specify YOUR-API-HOST in the command options by using the parameter ```--api-host```
Specify the input folder with parameter ```--input-folder-path``` 
Specify the output folder with parameter ```--output-folder-path```

Example Windows:

```bash
python .\client\client.py --api-key <YOUR-API-KEY> --api-host <YOUR-API-HOST> --input-folder-path .\bin\input --output-folder-path .\bin\output
```

Example Linux:

```bash
python .\client\client.py --api-key <YOUR-API-KEY> --api-host <YOUR-API-HOST> --input-folder-path .\bin\input --output-folder-path .\bin\output
```

