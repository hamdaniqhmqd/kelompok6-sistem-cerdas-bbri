import streamlit as st
from PIL import Image, ImageOps, ImageDraw

def about_us():
    # Menambahkan CSS untuk mempercantik tampilan
    st.markdown(
        """
        <style>
        .justify-text {
            text-align: justify;
            font-size: 18px;
            line-height: 1.6;
        }
        .center-text {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin-top: 10px;
        }
        .team-image {
            border-radius: 50%;
            width: 150px;
            height: 150px;
            object-fit: cover;
            margin: 10px auto;
            display: block;
        }
        .team-member {
            text-align: center;
            margin-top: 10px;
        }
        .section {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Tentang Kami")

    # Tentang Kami
    st.markdown(
        """
        <div class="section justify-text">
        Aplikasi ini dirancang untuk membantu Anda memprediksi tren harga saham Bank Rakyat Indonesia (BRI). Dengan menggunakan data historis dan algoritma machine learning yang canggih, kami memberikan visualisasi yang mudah dipahami dan prediksi yang akurat.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Manfaat Aplikasi
    st.header("Manfaat Aplikasi")
    st.markdown(
        """
        <div class="section justify-text">
        <ul>
            <li><strong>Pengambilan Keputusan:</strong> Membantu Anda mengambil keputusan investasi yang lebih informatif.</li>
            <li><strong>Analisis Pasar:</strong> Memahami tren pasar saham secara lebih mendalam.</li>
            <li><strong>Visualisasi yang Interaktif:</strong> Menyajikan data dalam bentuk grafik yang mudah dipahami.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.header("Tim Pengembang")
    st.markdown(
        """
        <div class="justify-text">
        Aplikasi ini dikembangkan oleh Kelompok 6 yang memiliki minat yang besar dalam bidang keuangan dan teknologi. Kami berkomitmen untuk terus mengembangkan aplikasi ini agar semakin bermanfaat bagi pengguna.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Daftar anggota tim dengan foto
    team_members = [
        {"name": "Ahmad Hamdani", "image": "ahmad.jpg"},
        {"name": "Bagas Yudha Ardiansyah", "image": "bagas.jpg"},
        {"name": "Triani Yuli Astutik", "image": "triani.jpg"},
        {"name": "Yola Septianingrum", "image": "yolaa.jpg"}
    ]

    # Menampilkan foto dan nama anggota tim dalam kolom
    col1, col2, col3, col4 = st.columns(4)

    for i, member in enumerate(team_members):
        col = eval(f"col{i+1}")
        with col:
            image_path = f"images/{member['image']}"  # Asumsi gambar ada di folder 'images'
            try:
                img = Image.open(image_path)
                # Membuat gambar menjadi bulat
                img = ImageOps.fit(img, (300, 300), Image.Resampling.LANCZOS)
                mask = Image.new('L', (300, 300), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 300, 300), fill=255)
                img.putalpha(mask)

                st.image(img, use_container_width=True, output_format="PNG")
            except FileNotFoundError:
                st.write(f"Gambar {member['image']} tidak ditemukan.")
            
            # Membuat nama anggota tim berada di tengah
            st.markdown(
                f"""
                <div class="center-text">
                {member['name']}
                </div>
                """,
                unsafe_allow_html=True
            )

# Memanggil fungsi about_us()
about_us()
