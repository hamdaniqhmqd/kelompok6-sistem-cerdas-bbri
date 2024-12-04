import streamlit as st
import pandas as pd

# Menampilkan logo bank sebagai gambar
st.image("bri.jpeg", width=800)

# Judul aplikasi
st.title("📊 *Visualisasi Tren Harga Saham Bank Rakyat Indonesia*")

# Menampilkan teks pengantar dengan gambar dan penjelasan
col1, col2 = st.columns([1.5, 2.5])
with col1:
    st.image("LogoBRI.png", width=800)
with col2:
    st.write("*Selamat datang di aplikasi visualisasi tren harga saham Bank Rakyat Indonesia (BRI).*\n", fontsize=20)
    st.write("""
    Pilih menu untuk memulai analisis harga saham berdasarkan periode waktu yang diinginkan. 
    Anda dapat memilih periode waktu yang berbeda dan memperoleh visualisasi data historis.
    """, text_align="justify")

st.write("Unggah dataset untuk memulai analisis.")

# Sidebar dengan pilihan periode waktu
menu = st.sidebar.selectbox(
    "Pilih Menu",
    ["Hari", "Minggu", "Bulan"]
)  # Pilihan periode untuk analisis

# Menampilkan data berdasarkan periode yang dipilih
if menu == "Hari":
    st.header("📅 Menampilkan per Hari")
    data = pd.read_csv("bri/bbri.csv")  # Membaca dataset harian
    st.dataframe(data)

elif menu == "Minggu":
    st.header("📅 Menampilkan per Minggu")
    data = pd.read_csv("bri/bbri_minggu.csv")  # Membaca dataset mingguan
    st.dataframe(data)

elif menu == "Bulan":
    st.header("📅 Menampilkan per Bulan")
    data = pd.read_csv("bri/bbri_bulan.csv")  # Membaca dataset bulanan
    st.dataframe(data)

# Validasi kolom 'Date' ada dalam dataset
if 'Date' not in data.columns:
    st.error("Dataset harus mengandung kolom 'Date'.")
else:
    # Membersihkan kolom dan konversi 'Date' ke datetime
    data.columns = [col.strip() for col in data.columns]
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    # Memeriksa kolom yang akan digunakan untuk visualisasi
    show_close = st.checkbox("Tampilkan Close", value=True)
    show_open = st.checkbox("Tampilkan Open", value=True)
    show_high = st.checkbox("Tampilkan High", value=True)
    show_low = st.checkbox("Tampilkan Low", value=True)

    # Membuat daftar kolom yang ditampilkan berdasarkan checkbox yang dipilih
    columns_to_display = ['Date']
    if show_close:
        columns_to_display.append('Close')
    if show_open:
        columns_to_display.append('Open')
    if show_high:
        columns_to_display.append('High')
    if show_low:
        columns_to_display.append('Low')

    # Menampilkan grafik tren harga saham berdasarkan kolom yang dipilih
    historical_chart = data[columns_to_display]
    st.line_chart(historical_chart.rename(columns={"Date": "index"}).set_index("index"))
