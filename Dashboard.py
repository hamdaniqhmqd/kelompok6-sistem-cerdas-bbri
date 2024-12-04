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

    # Menambahkan kolom 'Day' berdasarkan selisih dengan tanggal minimum
    data['Day'] = (data['Date'] - data['Date'].min()).dt.days

    required_columns = ['Date', 'Close', 'Open', 'High', 'Low']
    if not all(col in data.columns for col in required_columns):
        st.error(f"Dataset harus mengandung kolom: {required_columns}")
    else:
        # Fitur untuk prediksi
        X = data[['Day', 'Open', 'High', 'Low']]
        y = data['Close']

        # Pembagian data untuk training dan testing (80% training, 20% testing)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Membuat dan melatih model Linear Regression
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Menyimpan model yang sudah dilatih
        if menu == "Hari":
            with open("bri_stock_model_hari.sav", "wb") as f:
                pickle.dump(model, f)
        elif menu == "Minggu":
            with open("bri_stock_model_minggu.sav", "wb") as f:
                pickle.dump(model, f)
        elif menu == "Bulan":
            with open("bri_stock_model_bulan.sav", "wb") as f:
                pickle.dump(model, f)

        # Prediksi dan evaluasi model
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # Menghitung Root Mean Squared Error

        st.subheader("Visualisasi Tren Harga Saham")

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

        # Prediksi harga saham masa depan
        days_future = st.slider("Prediksi untuk berapa hari ke depan?", min_value=1, max_value=365, value=30)

        # Membuat data untuk prediksi masa depan
        last_day = data['Day'].max()
        future_days = np.array(range(last_day + 1, last_day + 1 + days_future)).reshape(-1, 1)

        # Mengambil data terakhir untuk Open, High, Low
        last_row = data.iloc[-1]
        open_price = last_row['Open']
        high_price = last_row['High']
        low_price = last_row['Low']

        # Membuat data prediksi
        future_data = np.hstack([future_days, np.full((days_future, 3), [open_price, high_price, low_price])])
        future_predictions = model.predict(future_data)

        # Membuat tanggal untuk prediksi masa depan
        future_dates = pd.date_range(data['Date'].max() + pd.Timedelta(days=1), periods=days_future)
        future_df = pd.DataFrame({
            "Date": future_dates,
            "Predicted_Close": future_predictions
        })

        # Menampilkan hasil prediksi masa depan
        st.subheader("Hasil Prediksi")
        st.write(future_df)

        # Menampilkan grafik dengan data historis dan prediksi masa depan
        prediction_chart = pd.concat(
            [
                data[['Date', 'Close']],
                future_df.rename(columns={"Predicted_Close": "Close"})
            ],
            ignore_index=True
        )
        st.line_chart(prediction_chart.rename(columns={"Date": "index"}).set_index("index"))

#paling bawah

# Opsional: Simpan atau unduh prediksi sebagai file CSV
st.subheader("📥 *Unduh Prediksi Tren Masa Depan*")
csv = prediction_chart.to_csv(index=False)
st.download_button(
    label="Download Prediksi",
    data=csv,
    file_name="prediksi_harga_saham_bri.csv",
    mime="text/csv"
)
