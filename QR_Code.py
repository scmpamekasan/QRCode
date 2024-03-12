import streamlit as st
import pandas as pd
from PIL import Image
import os
import qrcode

# Function to load image
def load_image(img):
    im = Image.open(img)
    return im

# Function to load data
@st.cache
def load_data():
    return pd.read_excel(
        io="List_QR.xlsx",
        engine="openpyxl",
        sheet_name="Customer",
        nrows=20000
    )

# Main Streamlit app
st.subheader("Create QR Code")
with st.form(key='myqr_form'):
    raw_text = st.text_area("Input Kode Outlet disini (Kode Huruf Menggunakan Huruf Kapital)", max_chars=8)
    submit_button = st.form_submit_button("Generate")

    # Load data
    df = load_data()

    # Drop unnecessary columns
    df1 = df.drop(['Alamat','Zona','Sektor','Tgl Process'], axis=1)

    # Filter DataFrame based on user input
    df2 = df1[df1["OutletID"].str.contains(raw_text)]

# Display QR code and store name if the form is submitted
if submit_button:
    col1, col2 = st.columns(2)
    with col1:
        if not df2.empty:
            # Generate QR code
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, 
                               box_size=10, border=14)
            df3 = df2.iloc[0].iloc[2]
            qr.add_data(df3)
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')

            # Save QR code image
            img_filename = "{}.png".format(raw_text)
            path_for_images = os.path.join(img_filename)
            img.save(path_for_images)

            # Display QR code image
            final_img = load_image(path_for_images)
            st.image(final_img)

    with col2:
        if not df2.empty:
            # Display store name
            st.info('Nama Toko')
            df4 = df2.iloc[0].iloc[1]
            st.write(df4)
        else:
            st.warning("No matching records found.")
