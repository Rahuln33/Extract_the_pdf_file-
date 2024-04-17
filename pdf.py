import os
import pdfplumber
import pandas as pd
import re

def extract_data_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text
def parse_data(text):
    data = {}
    # Regular expressions for extracting data points
    patterns = {
    "Name": r"Name: ([^\n]+)",
    "Invoice No.": r"Invoice No\.: (\S+)",
    "PNR": r"PNR: (\S+)",
    "GSTIN": r"GSTIN: (\S+)",
    "Amount": r"total\s*(.*)",
    "CGST": r"CGST\s+(?:Rate & Amount)\s+(\d+\.\d+)",
    "SGST": r"SGST\s+Rate total value and Amount Total value +(\d+\.\d+)",
    "IGST": r"IGST\s+Rate total value and Amount Total value +(\d+\.\d+)",
    "Total Invoice value Amount": r"Total\s*Invoice\s*Value\s*\(in\s*words\)\s*(.*)"


    }    
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            data[key] = match.group(1)
        else:
            data[key] = ""  # Set empty string if data not found
            print(f"Warning: {key} not found in the PDF")
    return data

def save_to_csv(data_list, output_csv):
    df = pd.DataFrame(data_list)
    df.to_csv(output_csv, index=False)
def main():
    input_folder = "C:\\Users\\RAHUL N\\OneDrive\\Desktop\\PDF\\input_pdfs"  # Update this path to the correct location
    output_csv = "pdf_data.csv"
    data_list = []
    
    # Loop through each PDF file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            text = extract_data_from_pdf(pdf_path)
            data = parse_data(text)
            data["PDF_File"] = filename
            data_list.append(data)
    
    # Save extracted data to CSV
    save_to_csv(data_list, output_csv)
    print("Data extraction completed. CSV file saved as", output_csv)

if __name__ == "__main__":
    main()
