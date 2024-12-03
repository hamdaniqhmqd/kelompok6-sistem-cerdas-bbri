import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Title aplikasi
st.title("Prediksi dan Visualisasi Tren Harga Saham Bank Rakyat Indonesia")
st.write("Unggah dataset untuk memulai analisis dan prediksi.")

menu = st.sidebar.selectbox(
    "Pilih Menu",
    ["Hari", "Minggu", "Bulan"]
)

if menu == "Hari":
    # Menampilkan gambar
    st.header("Menampilkan per Hari")
    data = pd.read_csv("bri/bbri.csv")
    st.dataframe(data)

elif menu == "Minggu":
    # Menampilkan dataset
    st.header("Menampilkan per Minggu")
    data = pd.read_csv("bri/bbri_minggu.csv")
    st.dataframe(data)

elif menu == "Bulan":
    st.header("Menampilkan per Bulan")
    data = pd.read_csv("bri/bbri_bulan.csv")
    st.dataframe(data)

required_columns = ['Date', 'Close']

if not all(col in data.columns for col in required_columns):
    st.error(f"Dataset harus mengandung kolom: {required_columns}")
else:
    data['Date'] = pd.to_datetime(data['Date'])
    data['Day'] = (data['Date'] - data['Date'].min()).dt.days
    X = data[['Day']]
    y = data['Close']
        
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)
        
    with open("bri_stock_model.pkl", "wb") as f:
        pickle.dump(model, f)

        # Predictions
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

     
        # Visualize historical data
    st.subheader("Visualisasi Tren Harga Saham")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data['Date'], data['Close'], label='Harga Historis')
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Harga Penutupan (Close)")
    ax.legend()
    st.pyplot(fig)

        # Predict future trends
    st.subheader("Prediksi Tren Masa Depan")
    days_future = st.slider("Prediksi untuk berapa hari ke depan?", min_value=1, max_value=365, value=30)
    future_days = np.array(range(data['Day'].max() + 1, data['Day'].max() + 1 + days_future)).reshape(-1, 1)
    future_predictions = model.predict(future_days)
    
    future_dates = pd.date_range(data['Date'].max() + pd.Timedelta(days=1), periods=days_future)
    future_df = pd.DataFrame({"Date": future_dates, "Predicted_Close": future_predictions})
        
    st.write(future_df)

        # Plot predictions
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data['Date'], data['Close'], label='Harga Historis')
    ax.plot(future_df['Date'], future_df['Predicted_Close'], label='Prediksi', linestyle='--')
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Harga Penutupan (Close)")
    ax.legend()
    st.pyplot(fig)
      