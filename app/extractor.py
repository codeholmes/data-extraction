import pytesseract
import cv2
from app.preprocessor import Preprocessing
import streamlit as st
import numpy as np
from pdf2image import convert_from_bytes
from img2table.ocr import TesseractOCR
from img2table.document import Image, PDF
import os
import pandas as pd
import io

# path to public folder
current_dir = os.getcwd()
public_folder_path = os.path.join(current_dir, "resources/public")

class Extractor:


    def extract_from_pdf(self, uploaded_file):
         """Function for extracting text from PDF file"""
         pages = convert_from_bytes(uploaded_file.read())
         
         for i, page in enumerate(pages):
            st.subheader(f"PDF Page - {i+1}")
            st.image(page, caption=f"Page {i+1}", use_column_width=True)
            # file_bytes = np.asarray(bytearray(page), dtype=np.uint8)
            grey_page = Preprocessing.grayscale(np.array(page))
            text = pytesseract.image_to_string(grey_page)
            st.subheader("Extracted Data")
            st.subheader(text)

    def extract_from_img(self, uploaded_file):
        """Function for extracting text from Image"""
        st.subheader("Image")
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        # st.write(image)
        st.image(image, channels="BGR")
        grey_img = Preprocessing.grayscale(image)
        text = pytesseract.image_to_string(grey_img)
        st.write("Extracted Data")
        st.write(text)
        # self.extract_table(image)

    def extract_table(self, file_name, file_type):
        """Function for extracting table from PDF or Image"""
        st.subheader("Extracted table from PDF or Image")

        file_path = os.path.join(public_folder_path, file_name)
        excel_path = os.path.join(public_folder_path, file_name.split('.')[0] + '.xlsx')

        ocr = TesseractOCR(n_threads=1, lang="eng")

        doc = PDF(file_path)
        if file_type == "image":
            doc = Image(file_path)
        elif file_type == "pdf":
            doc = PDF(file_path)

        doc.to_xlsx(dest=excel_path, ocr=ocr,
                                            implicit_rows=False,
                                            borderless_tables=True,
                                            min_confidence=50)
        df = pd.read_excel(excel_path, engine='openpyxl')
        st.table(df)
        
        # invoke download csv
        if df is not None:
            self.download_csv(df, file_name)

    def download_csv(self, df, file_name):
        """Function for downloading csv file"""
        buffer = io.BytesIO()
        df.to_csv(buffer, index=False)
        file_name = file_name.split('.')[0] + '.csv'
        buffer.seek(0)
        st.download_button(
            label="Download CSV",
            data=buffer,
            file_name=file_name,
        )