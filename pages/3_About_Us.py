import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Menampilkan logo bank sebagai gambar
st.image("bri.jpeg", width=800)

# Judul aplikasi
st.title("🔮 *Prediksi dan Visualisasi Tren Harga Saham Bank Rakyat Indonesia*")

# Menampilkan teks pengantar dengan gambar dan penjelasan
col1, col2 = st.columns([1.5, 2.5])
with col1:
    st.image("LogoBRI.png", width=800)
with col2:
    st.write("*Selamat datang di aplikasi prediksi tren harga saham Bank Rakyat Indonesia (BRI).*\n", fontsize=20)
    st.write(""""
    Pilih menu untuk memulai analisis harga saham berdasarkan periode waktu yang diinginkan. Aplikasi ini dapat membantu memprediksi tren harga saham BRI berdasarkan data historis yang diunggah. 
    Anda dapat memilih periode waktu yang berbeda dan memperoleh visualisasi serta prediksi untuk masa depan.
    """, text_align="justify")

st.write("Unggah dataset untuk memulai analisis dan prediksi.")
