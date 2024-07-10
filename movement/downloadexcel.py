from flask import Flask, send_file
import pandas as pd

def download_excel():
    # Create a sample DataFrame
    data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
    df = pd.DataFrame(data)

    # Generate Excel file
    excel_file_path = 'sample.xlsx'
    df.to_excel(excel_file_path, index=False)

    # Send the file as a response
    return send_file(excel_file_path, as_attachment=True)
