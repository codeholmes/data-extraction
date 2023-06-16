from calendar import c
from numpy import save
import streamlit as st
from app.extractor import Extractor
import os
import sys
from datetime import datetime

root_dir = os.path.dirname(os.path.realpath(__file__))
current_dir = os.getcwd()
sys.path.append(root_dir)


st.title("Data Extractor")
st.write(
    "This is a simple web app to extract data from PDF or image. This app is built using Streamlit, Pytesseract, and OpenCV."
)


# upload file
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    # directory to save uploaded file
    data_dir = os.path.join(current_dir, "resources/public")
    # create directory if not exist
    os.makedirs(data_dir, exist_ok=True)
    # save file
    file_name = uploaded_file.name.split('.')[0] + '-' + datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = file_name + '.' + uploaded_file.type.split('/')[1]
    save_path = os.path.join(data_dir, file_name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # invoke extractor based on file type
    if uploaded_file.type == "application/pdf":
        ex = Extractor()
        ex.extract_from_pdf(uploaded_file)
        ex.extract_table(file_name, "pdf")
    elif uploaded_file.type == "image/png" or uploaded_file.type == "image/jpg" or uploaded_file.type == "image/jpeg":
        ex = Extractor()
        ex.extract_from_img(uploaded_file)
        ex.extract_table(file_name, "image")
    else:
        st.write("File type not supported")