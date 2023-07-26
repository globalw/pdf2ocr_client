import argparse
import concurrent.futures
import random
from PIL import Image
import img2pdf
import base64
import requests
import time
import os
from PyPDF2 import PdfWriter, PdfReader

SLEEP_TIME = 0.5

parser = argparse.ArgumentParser(description='Convert pdf to pdf with text-layer')

parser.add_argument("--api-key", type=str, default=os.getcwd(),
                    help="Get your API key at https://rapidapi.com/globalw/api/pdf-to-ocr")

parser.parse_args(args)

def merge_pdfs_in_folder(input_folder_path, output_folder_path, min_pages=1, max_pages=20):
    pdf_writer = PdfWriter()
    output_pdf_path = os.path.join(output_folder_path, "merged_0.pdf")
    count = 0
    total_pages = 0
    pdf_count = 0

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(input_folder_path):
        if filename.endswith(".pdf"):
            pdf_reader = PdfReader(os.path.join(input_folder_path, filename))
            num_pages = len(pdf_reader.pages)

            for page in range(num_pages):
                pdf_writer.add_page(pdf_reader.pages[page])
                total_pages += 1
                count += 1

                if count >= max_pages:
                    with open(output_pdf_path, "wb") as output_pdf:
                        pdf_writer.write(output_pdf)
                    pdf_writer = PdfWriter()
                    pdf_count += 1
                    output_pdf_path = os.path.join(output_folder_path, f"merged_{str(random.uniform(1000, 9999))}_{pdf_count}.pdf")
                    count = 0

    # Output remaining pages
    if min_pages <= total_pages % max_pages <= max_pages:
        with open(output_pdf_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)


def request_ocr_pdf(base_url, uuid):
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "4bdc73fb5amsha5f27ff6dc57bdfp186d43jsnf051e8c3909f",
        "X-RapidAPI-Host": "pdf-to-ocr.p.rapidapi.com"
    }
    payload = {"uuid": uuid}
    return requests.post(base_url + "/ocr-pdf", json=payload, headers=headers)


def request_process_pdf(base_url, base64_file):
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "4bdc73fb5amsha5f27ff6dc57bdfp186d43jsnf051e8c3909f",
        "X-RapidAPI-Host": "pdf-to-ocr.p.rapidapi.com"
    }
    payload = {"base64_file": base64_file}
    return requests.post(base_url + "/process-pdf", json=payload, headers=headers)


def run_conversion(base_url, input_folder_path, output_folder_path):
    url_process = base_url + "/process-pdf"
    url_ocr = base_url + "/ocr-pdf"

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "4bdc73fb5amsha5f27ff6dc57bdfp186d43jsnf051e8c3909f",
        "X-RapidAPI-Host": "pdf-to-ocr.p.rapidapi.com"
    }
    uuid_list = []
    filename_list = []
    for filename in os.listdir(input_folder_path):
        if filename.endswith(".pdf"):
            with open(os.path.join(input_folder_path, filename), "rb") as file:
                encoded_pdf = base64.b64encode(file.read()).decode('utf-8')
                payload = {"base64_file": encoded_pdf}
                while True:
                    response = requests.post(url_process, json=payload, headers=headers)
                    if response.status_code == 201:  # Successfully processed
                        print(f"response code {response.status_code}")
                        uuid = response.json().get('uuid')
                        print(f"Processing {filename}...")
                        print(f"UUID: {uuid}")
                        uuid_list.append(uuid)
                        filename_list.append(filename)
                        break
                    else:
                        print(f"Unexpected status code {response.status_code} when uploading {filename}. Retrying in {SLEEP_TIME} seconds...")
                        print(f"response content: {response.content}")
                        time.sleep(SLEEP_TIME)

    for i in range(len(uuid_list)):
        while True:
            time.sleep(SLEEP_TIME)
            print(f"Requesting OCR for filename: {filename_list[i]}, uuid: {uuid_list[i]}")
            response_ocr = requests.post(url_ocr, json={"uuid": uuid_list[i]}, headers=headers)
            if response_ocr.status_code == 200:

                print(f"response code {response_ocr.status_code}")

                data_ocr = response_ocr.json()
                if 'ocr_file' in data_ocr:
                    decoded_pdf = base64.b64decode(data_ocr['ocr_file'])
                    print(f"filename: {filename_list[i]} , uuid: {uuid_list[i]} RECEIVED")
                    with open(os.path.join(output_folder_path, uuid + "_" + filename_list[i]), "wb") as output_file:
                        output_file.write(decoded_pdf)
                    break
                else:
                    print(f"OCR processing not yet finished for {filename_list[i]}. Retrying in {SLEEP_TIME} seconds...")
                    time.sleep(SLEEP_TIME)
            elif response_ocr.status_code in range(400, 500):  # Client errors
                print(f"response code {response_ocr.status_code}")
                print(f"response content: {response_ocr.content}")
                print(
                    f"Client error with status code {response_ocr.status_code} when retrieving {filename_list[i]}. Retrying in {SLEEP_TIME} seconds...")
                time.sleep(SLEEP_TIME)
            elif response_ocr.status_code == 500:  # Server error
                print(f"response code {response_ocr.status_code}")
                print(f"response content: {response_ocr.content}")
                print(f"Server error when retrieving {filename_list[i]}. Retrying in {SLEEP_TIME} seconds...")
                time.sleep(SLEEP_TIME)
            else:
                print(f"Unexpected status code {response_ocr.status_code} when retrieving {filename_list[i]}. Retrying in 5 seconds...")
                time.sleep(SLEEP_TIME)


def convert_png_to_pdf(input_folder_path, output_folder_path):
    # Ensure the output directory exists
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Iterate over PNG files in the input directory
    for filename in os.listdir(input_folder_path):
        if filename.endswith(".png"):
            # Open the image file
            img_path = os.path.join(input_folder_path, filename)
            img = Image.open(img_path)

            # Convert image to PDF
            pdf_bytes = img2pdf.convert(img.filename)

            # Write the PDF to a file
            pdf_path = os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}.pdf")
            file = open(pdf_path, "wb")
            file.write(pdf_bytes)
            file.close()


if __name__ == "__main__":

    localhost = "http://localhost:8001"
    rapidapi = "https://pdf-to-ocr.p.rapidapi.com"

    # Define your arguments for each function call
    args = [(rapidapi, "input", "output") for _ in range(1)]
    for i in range(1):
        # Create a ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            # Use executor.map() to start each instance of the function in its own thread
            results = executor.map(lambda p: run_conversion(*p), args)


