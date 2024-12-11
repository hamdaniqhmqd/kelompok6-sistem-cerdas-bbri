import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("🔮 *Prediksi harga Saham Bank Rakyat Indonesia Untuk Beberapa Hari Kedepan*")

st.markdown("---")

# Langkah kerja penggunaan aplikasi
st.subheader("**Langkah Kerja:**")
st.write("""
1. **Pastikan Dataset Lengkap**: Dataset yang digunakan harus mengandung kolom seperti *Date*, *Open*, *High*, *Low*, dan *Close* (bisa di cek di bagian Menu Dataset).
2. **Pilih Periode Waktu**: Gunakan menu dropdown di sidebar untuk memilih periode waktu yang diinginkan seperti (Hari, Minggu, atau Bulan).
3. **Prediksi Harga Saham Masa Depan**: Tentukan jumlah hari yang ingin diprediksi dengan menggunakan slider. Aplikasi akan memproses prediksi harga saham BRI untuk periode tersebut.
4. **Visualisasi Hasil Prediksi**: Setelah prediksi dihitung, aplikasi akan menampilkan grafik yang menggambarkan harga saham historis dan harga prediksi untuk masa depan.
5. **Unduh Hasil Prediksi**: Setelah melihat hasil prediksi, Anda dapat mengunduhnya dalam format CSV untuk referensi lebih lanjut atau analisis tambahan.
""")

# Sidebar dengan pilihan kategori waktu
menu = st.sidebar.selectbox(
    "Pilih Kategori Waktu Dataset",
    ["Hari", "Minggu", "Bulan"]
)

# Menampilkan data berdasarkan periode yang dipilih
if menu == "Hari":
    data = pd.read_csv("bri/bbri.csv")  # Membaca dataset harian

elif menu == "Minggu":
    data = pd.read_csv("bri/bbri_minggu.csv")  # Membaca dataset mingguan

elif menu == "Bulan":
    data = pd.read_csv("bri/bbri_bulan.csv")  # Membaca dataset bulanan

st.markdown("---")

# Validasi kolom 'Date' ada dalam dataset
if 'Date' not in data.columns:
    st.error("Dataset harus mengandung kolom 'Date'.")
else:
    # Membersihkan kolom dan konversi 'Date' ke datetime
    data.columns = [col.strip() for col in data.columns]
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    # Menambahkan kolom 'Day' berdasarkan selisih dengan tanggal minimum
    data['Day'] = (data['Date'] - data['Date'].min()).dt.days

    required_columns = ['Date', 'Close', 'Open', 'High', 'Low', 'Volume']
    if not all(col in data.columns for col in required_columns):
        st.error(f"Dataset harus mengandung kolom: {required_columns}")
    else:
        # Fitur untuk prediksi
        X = data[['Day', 'Open', 'High', 'Low', 'Volume']]  # Menambahkan kolom 'Volume'
        y = data['Close']

        # Pembagian data untuk training dan testing (80% training, 20% testing)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Membuat dan melatih model Linear Regression
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Menyimpan model yang sudah dilatih sesuai dengan periode
        if menu == "Hari":
            with open("bri_stock_model_hari.sav", "wb") as prediksi:
                pickle.dump(model, prediksi)
        elif menu == "Minggu":
            with open("bri_stock_model_minggu.sav", "wb") as prediksi:
                pickle.dump(model, prediksi)
        elif menu == "Bulan":
            with open("bri_stock_model_bulan.sav", "wb") as prediksi:
                pickle.dump(model, prediksi)

        # Mengambil data terakhir untuk Open, High, Low
        last_row = data.iloc[-1]
        open_price = last_row['Open']
        high_price = last_row['High']
        low_price = last_row['Low']
        volume = last_row['Volume']

        # Membuat tanggal untuk prediksi masa depan
        if menu == "Hari":
            # Prediksi berdasarkan hari
            st.subheader("📝 Prediksi Harga Saham untuk berapa hari ke depan.")
            days_future = st.slider("🗓️ Geser slider untuk prediksi harga saham untuk berapa hari kedepan.", min_value=1, max_value=365, value=64)

            # Membuat data prediksi harian
            future_days = np.array(range(data['Day'].max() + 1, data['Day'].max() + 1 + days_future)).reshape(-1, 1)
            future_data = np.hstack([future_days, np.full((len(future_days), 4), [open_price, high_price, low_price, volume])])
            future_predictions = model.predict(future_data)
            future_dates = pd.date_range(data['Date'].max() + pd.Timedelta(days=1), periods=days_future, freq='D')  # Frekuensi harian


        elif menu == "Minggu":
            # Prediksi berdasarkan minggu
            st.subheader("📝 Prediksi Harga Saham untuk berapa minggu ke depan.")
            weeks_future = st.slider("📅 Geser slider untuk prediksi harga saham untuk berapa minggu kedepan.", min_value=1, max_value=52, value=24)

            # Membuat data prediksi mingguan
            future_weeks = np.array(range(data['Day'].max() // 7 + 1, data['Day'].max() // 7 + weeks_future + 1)).reshape(-1, 1) * 7
            future_data = np.hstack([future_weeks, np.full((len(future_weeks), 4), [open_price, high_price, low_price, volume])])
            future_predictions = model.predict(future_data)
            future_dates = pd.date_range(data['Date'].max() + pd.Timedelta(weeks=1), periods=weeks_future, freq='W')  # Frekuensi mingguan (setiap minggu)


        elif menu == "Bulan":
            # Prediksi berdasarkan bulan
            st.subheader("📝 Prediksi Harga Saham untuk berapa bulan ke depan.")
            months_future = st.slider("📅 Geser slider untuk prediksi harga saham untuk berapa bulan kedepan.", min_value=1, max_value=12, value=6)

            # Membuat data prediksi bulanan
            future_months = np.array(range(data['Day'].max() // 30 + 1, data['Day'].max() // 30 + months_future + 1)).reshape(-1, 1) * 30
            future_data = np.hstack([future_months, np.full((len(future_months), 4), [open_price, high_price, low_price, volume])])
            future_predictions = model.predict(future_data)
            future_dates = pd.date_range(data['Date'].max() + pd.DateOffset(months=1), periods=months_future, freq='M')  # Frekuensi bulanan (akhir bulan)


        future_df = pd.DataFrame({
            "Date": future_dates,
            "Predicted_Close": future_predictions
        })

        # Menambahkan status prediksi: Naik, Turun, atau Tetap
        future_df['Status'] = future_df['Predicted_Close'].diff().apply(
            lambda x: 'Naik' if x > 0 else ('Turun' if x < 0 else 'Tetap')
        )

        # Menampilkan hasil prediksi masa depan beserta statusnya
        st.write(f"📊 Hasil Prediksi Harga Saham Untuk {len(future_df)} Periode Kedepan")
        
        # Menggunakan st.dataframe untuk tampilan yang lebih interaktif dan bisa digulir
        st.dataframe(future_df, use_container_width=True)

        # Menyiapkan data untuk grafik dengan memastikan tipe data yang tepat
        prediction_chart = pd.concat(
            [
                data[['Date', 'Close']],
                future_df.rename(columns={"Predicted_Close": "Close"})
            ],
            ignore_index=True
        )

        # Pastikan kolom 'Date' bertipe datetime
        prediction_chart['Date'] = pd.to_datetime(prediction_chart['Date'], errors='coerce')

        # Pastikan kolom 'Close' bertipe numerik
        prediction_chart['Close'] = pd.to_numeric(prediction_chart['Close'], errors='coerce')

        # Menampilkan grafik dengan data yang sudah diperbaiki
        st.write(f"📊 Hasil Visualisasi Grafik Harga Saham Untuk {len(future_df)} Periode Kedepan")
        st.line_chart(prediction_chart.set_index('Date')['Close'])
        
        # Menampilkan hasil evaluasi
        st.markdown("---")
        
        # Prediksi dan evaluasi model
        y_pred = model.predict(X_test)

        # Menghitung MSE, MAE, dan RMSE
        mse = mean_squared_error(y_test, y_pred) 
        mae = np.mean(np.abs(y_test - y_pred))   
        rmse = np.sqrt(mse)                      

        st.subheader("🗃️ Hasil Evaluasi")
        st.write("Hasil Evaluasi harga saham secara keseluruhan.")

        st.write(f"Mean Absolute Error (MAE): {mae:.2f}")
        st.write(f"Mean Squared Error (MSE): {mse:.2f}")
        st.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
                
        
# Opsional: Simpan atau unduh prediksi sebagai file CSV
st.markdown("---")
st.subheader("📥 Unduh Prediksi Harga Saham Bang Rakyat Indonesia Kedepannya")
st.write("Unduh Data hasil prediksi untuk referensi harga saham kedepannya. Unduh data tersebut dengan format CSV")
csv = prediction_chart.to_csv(index=False)
st.download_button(
    label="Download Prediksi",
    data=csv,
    file_name="prediksi_harga_saham_bri.csv",
    mime="text/csv"
)

# Metode yang Digunakan
st.markdown("---")
st.subheader("Metode Prediksi Harga")
st.write("""
Pada program prediksi harga saham, menggunakan metode **Regresi Linear** untuk memprediksi harga penutupan saham (Close) berdasarkan hubungan variabel independen seperti Day, Open, High, Low, dan Volume. Data historis diolah menjadi fitur numerik, dilatih dengan Linear Regression, dan dievaluasi menggunakan Mean Squared Error (MSE), Mean Absolute Error (MAE), dan Root Mean Squared Error (RMSE).
Prediksi masa depan dilakukan secara progresif (1 hari, 7 hari, atau 30 hari), dengan hasil berupa tabel prediksi yang mencakup tanggal dan status harga (Naik, Turun, atau Tetap).
""")

# Footer dengan kesimpulan
st.markdown("---")
st.subheader("**Kesimpulan:**")
st.write("""
Aplikasi ini menyediakan solusi praktis untuk memprediksi dan menganalisis tren harga saham Bank Rakyat Indonesia. Dengan fitur prediksi yang didukung algoritma regresi linear dan visualisasi data yang interaktif, Anda dapat membuat keputusan yang lebih baik berdasarkan tren pasar. Jangan lupa untuk mengunduh hasil prediksi untuk referensi di masa depan.
Dari hasil prediksi tersebut, menggunakan metode **Regresi Linear**, evaluasi dengan MSE, MAE, dan RMSE.
""")

# selesai