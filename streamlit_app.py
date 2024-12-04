import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt


# Judul aplikasi
st.markdown("""
<div style="text-align: center; font-size: 38px; font-weight: bold;">
            PREDIKSI DAN VISUALISASI SAHAM BANK RAKYAT INDONESIA
</div>
""", unsafe_allow_html=True )

# Menampilkan logo bank sebagai gambar
st.image("bri.jpeg", width=750)

# Menampilkan teks pengantar dengan gambar dan penjelasan
col1, col2 = st.columns([1.5, 2.5])
with col1:
    st.image("LogoBRI.png", width=800)
with col2:
    st.markdown(
        """
        *Selamat datang di aplikasi prediksi tren harga saham Bank Rakyat Indonesia (BBRI)!*
        
        "Pilih menu untuk memulai analisis harga saham berdasarkan periode waktu yang diinginkan. Aplikasi ini dapat membantu memprediksi tren harga saham BRI berdasarkan data historis yang diunggah. 
        Anda dapat memilih periode waktu yang berbeda dan memperoleh visualisasi serta prediksi untuk masa depan".
        """
    )

# Tambahan penjelasan
st.markdown(
    """
            
        Aplikasi ini dirancang untuk membantu Anda memahami pergerakan harga saham **Bank Rakyat Indonesia (BBRI)** secara mudah dan interaktif. 
        Dengan memanfaatkan teknologi **Machine Learning**, aplikasi ini memungkinkan Anda untuk:
        - **Melihat Visualisasi Tren Harga Saham**: Menampilkan data historis dan pola harga saham dari waktu ke waktu.
        - **Prediksi Harga Saham**: Memperkirakan harga saham BBRI di masa depan berdasarkan data historis.
        - **Analisis Mendalam**: Memberikan wawasan yang lebih detail untuk mendukung keputusan investasi.
    """
)


# Menambahkan penjelasan detail fitur aplikasi
st.subheader("✨ **Fitur Utama**")
st.markdown(
    """
    - **Dashboard Interaktif**: Grafik yang informatif dan mudah dipahami.
    - **Prediksi Masa Depan**: Menggunakan model *Machine Learning* untuk prediksi harga saham berdasarkan pola data historis.
    - **Pemrosesan Data yang Akurat**: Data historis diambil langsung dari sumber terpercaya untuk memastikan keakuratan analisis.
    """
)

# Menjelaskan cara menggunakan aplikasi
st.subheader("📖 **Cara Menggunakan**")
st.markdown(
    """
    1. Pilih menu **Dataset** untuk melihat grafik pergerakan harga saham BBRI secara historis.
    2. Gunakan menu **Prediksi** untuk mendapatkan estimasi harga saham di masa depan.
    3. Jelajahi menu **About Us** untuk memahami teknologi dan metodologi yang digunakan dalam aplikasi ini.
    """
)

# Menambahkan tujuan aplikasi
st.subheader("🎯 **Tujuan Aplikasi**")
st.markdown(
    """
    Aplikasi ini bertujuan untuk membantu pengguna, baik investor pemula maupun profesional, dalam:
    - Mengambil keputusan investasi yang lebih baik.
    - Memahami tren harga saham secara komprehensif.
    - Meningkatkan wawasan tentang analisis data dalam sektor keuangan.
    """
)

# Menutup halaman dengan ucapan semangat
st.markdown(
    """
    ---
    <div style="text-align: center; font-size: 18px; color: #007BFF;">
        Selamat menjelajahi aplikasi ini, dan semoga bermanfaat untuk investasi Anda! 💹
    </div>
    """,unsafe_allow_html=True)
    

