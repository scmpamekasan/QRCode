import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import os
import time
import qrcode

timestr = time.strftime("%Y%m%d-%H%M%S")
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, 
                   box_size=10, border=14)

def load_image(img):
    im = Image.open(img)
    return im

@st.cache
def load_data():
    return pd.read_excel(
        io="List_QR.xlsx",
        engine="openpyxl",
        sheet_name="Customer",
        nrows=20000
    )

st.subheader("Create QR Code")
with st.form(key='myqr_form'):
    raw_text = st.text_area("Input Kode Outlet disini (Kode Huruf Menggunakan Huruf Kapital)", max_chars=8)
    submit_button = st.form_submit_button("Generate")
    df = pd.read_excel(
        io="List_QR.xlsx",
        engine="openpyxl",
        sheet_name="Customer",
        usecols="B:H",
        nrows=20000,
    )

    df1 = df.drop(['Alamat','Zona','Sektor','Tgl Process'], axis=1)

    df2 = df1[df1["OutletID"].str.contains(raw_text)]

if submit_button:
    col1, col2 = st.columns(2)
    with col1:
        if not df2.empty:
            df3 = df2.iloc[0].iloc[2]
            qr.add_data(df3)
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')

            img_filename = "{}.png".format(raw_text)
            path_for_images = os.path.join(img_filename)
            img.save(path_for_images)

            final_img = load_image(path_for_images)
            st.image(final_img)

    with col2:
        if not df2.empty:
            st.info('Nama Toko')
            df4 = df2.iloc[0].iloc[1]
            st.write(df4)
        else:
            st.warning("No matching records found.")
