import streamlit as st
import requests
import base64
import os
import json
import pandas as pd

def displayPDF(uploaded_file):
    
    # Read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode('utf-8')

    # Embed PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="600" type="application/pdf"></iframe>'

    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)


st.header("Prolaw Invoice Data Extraction Prototype")

# Create a file uploader in the Streamlit app
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    displayPDF(uploaded_file)

API_URL = os.getenv("API_URL") or  "https://vvnkofpgwi.execute-api.us-east-1.amazonaws.com/upload"

if uploaded_file is not None:
    # Read the file and encode it in base64
    file_bytes = uploaded_file.read()
    base64_encoded_file = base64.b64encode(file_bytes).decode()

    headers = {'Content-Type': 'application/json'}

    data = {
        "filename": uploaded_file.name,
        "doc": base64_encoded_file
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    # Get the JSON response from the API
    json_response = response.json()

    # Extract the ExpenseDocuments
    expense_documents = json_response['ExpenseDocuments']

    # Create a list to store the data for the DataFrame
    data = []

    # Go through the ExpenseDocuments
    for document in expense_documents:
        # Go through the SummaryFields
        for field in document['SummaryFields']:
            # Get the name of the value and the actual value
            name = field['Type']['Text']
            value = field['ValueDetection']['Text']
            # Add the data to the list
            data.append([name, value])

    st.subheader("Response")

    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=['Name', 'Value'])

    st.write(df)