import streamlit as st
from streamlit_option_menu import option_menu
import altair as alt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

st.set_page_config(layout='wide')

# Judul
st.title('PROSPEK INVESTASI RUMAH DI KOTA DEPOK')

def format_big_number(num):
    if num >= 1e9:
        return f"{num / 1e9:.2f} Milyar"
    elif num >= 1e6:
        return f"{num / 1e6:.2f} Juta"
    else:
        return f"{num:.2f}"

with st.sidebar:
    selected = option_menu("Main Menu", ["Home", "Prediction", "Gallery"], 
        icons=['house', 'gear'], menu_icon="cast", default_index=0)
    #selected

if (selected == "Home") :

    st.header("I. Pendahuluan")

    st.markdown('<div style="text-align:justify">Depok sebagai salah satu kota di Jawa Barat yang berbatasan  langsung dengan selatan Jakarta,  memiliki lokasi strategis untuk perumahan . Sehingga  perumahan di Kota Depok  kian tumbuh setiap tahunnya, juga atas permintaan dan perkembangan kondisi sosial dan ekonomi masyarakat Depok yang kian intens. Oleh karena itu, pemerintah dan para pengembang perumahan berusaha untuk memenuhi kebutuhan akan perumahan dengan membangun berbagai jenis hunian, mulai dari perumahan subsidi hingga perumahan mewah. Capstone ini dibuat untuk mengetahui harga lahan dan bangunan permeter persegi saat membeli rumah tahun 2010 disuatu lokasi di Depok , setelah 15 tahun kemudian berdasarkan jumlah angsuran yang telah dibayar maka akan diketahui berapa kenaikan harga lahan dari suatu perumahan tersebut dengan ketentuan harga bangunan tetap. Kemudian angka yang diperoleh akan dibandingkan dengan nilai jual dari sebuah website jual beli properti/rumah. capstone ini sebagai bahan pertimbangan untuk calon pembeli rumah, bagi keluarga muda yang sedang mempertimbangkan untuk membeli rumah antara harga real dan harga penawaran.</div>', unsafe_allow_html=True)

    # BAGIAN CGR
    df = pd.read_csv('perum_cgr_fix_2.csv')

    st.header("II. Pengolahan Data dan Visualisasi")

    st.subheader("A. Data Perum CGR")
    st.markdown('<div style="text-align:justify">Data ini adalah data Real Developer dari perumahan dimana saya bermukim, data fix yang bisa langsung diexplore dengan menggunakan SQL, seperti berikut ini: <br> <br> </div>',unsafe_allow_html=True)
    st.text('## harga lahan permeter persegi 2010 : 1,672,087.91 (AJB)')
    st.text('## harga_rumah_dev = (sum luas_bangunan * harga_bangunan) + (sum luas_lahan * harga_lahan_2010)')
    st.text('## formula mencari harga bangunan permeter persegi')
    st.code('SELECT (sum(harga_dev)-sum(luas_lahan)* 1672087.91 )/sum(luas_bangunan) AS harga_bangunan_per_m FROM perum_cgr_fix;')
    st.text('## formula mencari harga lahan 2024 dengan asumsi harga bangunan tetap') 
    st.code('SELECT (sum(harga_kpr)-sum(luas_bangunan)* 4921226.104182 )/sum(luas_lahan) AS harga_lahan_per_m FROM perum_cgr_fix;')

    #  Kolom Harga  @ CGR  
    mx_hl2010, mx_hl2024, mx_delta_hl, mx_hb= st.columns(4)
    with mx_hl2010 :
        # harga lahan permeter dari AJB
        hl2010 = 152160000/91
        st.metric('Harga Lahan 2010 / m2', format_big_number(hl2010), delta=None, delta_color="normal", help=None, label_visibility="visible")

    with mx_hl2024 :
        hl2024 = (df['harga_kpr'].sum() - df['luas_bangunan'].sum() * 4921226.098787341) / df['luas_lahan'].sum()
        st.metric('Harga Lahan 2024 / m2', format_big_number(hl2024), delta=None, delta_color="normal", help=None, label_visibility="visible")   

    with mx_delta_hl :
        selisih_hl = hl2024 - hl2010
        delta_hl = 100 * (hl2024 - hl2010) / hl2010
        st.metric('kenaikan harga lahan', value=format_big_number(selisih_hl), delta=f'{delta_hl:.2f}%', delta_color="normal", help=None, label_visibility="visible")

    # Kolom Harga bangunan    
    with mx_hb :
        hb = (df['harga_dev'].sum() - df['luas_lahan'].sum() * 1672087.912087912 )/df['luas_bangunan'].sum()
        st.metric('Harga bangunan / m2', format_big_number(hb), delta=None, delta_color="normal", help=None, label_visibility="visible")

    # Create the DataFrame
    data = pd.DataFrame({
        "Category": ["Harga Bangunan", "Harga Lahan"],
        "2010": [hb, (hl2010)],
        "2011": [hb, (hl2010) + (hl2024-hl2010)/14],
        "2012": [hb, (hl2010) + 2*(hl2024-hl2010)/14],
        "2013": [hb, (hl2010) + 3*(hl2024-hl2010)/14],
        "2014": [hb, (hl2010) + 4*(hl2024-hl2010)/14],
        "2014": [hb, (hl2010) + 5*(hl2024-hl2010)/14],
        "2016": [hb, (hl2010) + 6*(hl2024-hl2010)/14],
        "2017": [hb, (hl2010) + 7*(hl2024-hl2010)/14],
        "2018": [hb, (hl2010) + 8*(hl2024-hl2010)/14],
        "2019": [hb, (hl2010) + 9*(hl2024-hl2010)/14],
        "2020": [hb, (hl2010) + 10*(hl2024-hl2010)/14],
        "2021": [hb, (hl2010) + 11*(hl2024-hl2010)/14],
        "2022": [hb, (hl2010) + 12*(hl2024-hl2010)/14],
        "2023": [hb, (hl2010) + 13*(hl2024-hl2010)/14],
        "2024": [hb, (hl2010) + 14*(hl2024-hl2010)/14]
    })

    # Melt the DataFrame to create long format data for the chart
    melted_data = data.melt(id_vars="Category", var_name="Tahun", value_name="Harga")

    # Create the chart
    barchart = alt.Chart(melted_data).mark_bar().encode(
        x="Tahun:N",
        y="Harga:Q",
        color="Category:N",
        tooltip=["Category:N", "Tahun:N", "Harga:Q"]
    ).properties(
        title="HARGA LAHAN DAN BANGUNAN PER M2",
        width=1100,
        height=400
    )

    # Display the chart
    st.altair_chart(barchart)

    # BAGIAN LAMUDI
    st.subheader("B. Data lamudi.com")
    st.text("Disclaimer : Data ini digunakan untuk model pembelajaran Data Analysis")
    st.text('untuk Data collection, integration dan cleansing menggunakan Octoparse dan Pentaho serta di explore dengan SQL sebagai berikut :') 

    g1, g2, g3 = st.columns([1,5,2])
    with g1:
        st.write(" ")
    with g3:
        st.write(" ")
    with g2:
        st.image("Data_Cleansing.png", width=800)

    formula_SQL ='''
    WITH fix_lamudi AS (
        SELECT alamat AS alamat, REGEXP_REPLACE (harga, 'Rp','') AS harga, REGEXP_REPLACE(luas_bangunan, 'm²','') AS luas_bangunan, REGEXP_REPLACE(luas_lahan, 'm²','') AS luas_lahan FROM lamudi) 
    SELECT 
        alamat, CAST(luas_bangunan AS signed)AS luas_bangunan, CAST(luas_lahan AS signed) AS luas_lahan, CAST(replace(harga,'.','') AS signed) AS harga FROM fix_lamudi; '''
    st.code(formula_SQL)

    df2 = pd.read_csv('lamudi_pentaho_transform_fix.csv')

    def hld(kec):
        hl_lamudi_2 = (df2[df2['alamat']==kec]['harga'].sum() - df2[df2['alamat']==kec]['luas_bangunan'].sum() * 4921226.098787341) / df2[df2['alamat']==kec]['luas_lahan'].sum()
        return hl_lamudi_2

    # Grafik harga lahan permeter berdasarkan kecamatan di depok
    grafik = pd.DataFrame({
        "kecamatan": ["Sawangan, Depok","Sukmajaya, Depok","Cimanggis, Depok","Cilodong, Depok","Tapos, Depok", "Beji, Depok", "Cinere, Depok", "Pancoran Mas, Depok", "Cipayung, Depok", "Bojongsari, Depok", "Limo, Depok"],
        "harga_lahan": [hld("Sawangan, Depok"),hld("Sukmajaya, Depok"),hld("Cimanggis, Depok"),hld("Cilodong, Depok"), hld("Tapos, Depok"), hld("Beji, Depok"), hld("Cinere, Depok"), hld("Pancoran Mas, Depok"), hld("Cipayung, Depok"), hld("Bojongsari, Depok"), hld("Limo, Depok")]
    })

    # Barchat Lamudi with sorted
    sorted_grafik = grafik.sort_values(by='harga_lahan', ascending =True)
    average_values = grafik["harga_lahan"].mean()
    st.write("avg harga lahan :", average_values)

    chart_lamudi = (
        alt.Chart(sorted_grafik)
        .mark_bar()
        .encode(x= alt.X("kecamatan",sort = None), y="harga_lahan")
        .properties(width = 1100, height = 500)
    ) 
    chart_lamudi 
    
    st.header("III. Insight Analysis")
    st.markdown('<div style="text-align:justify">1. Dari data menunjukan bahwa kenaikan harga lahan dalam periode 15 tahun adalah 118.94%, Tren kenaikan harga lahan Linier terhadap waktu yaitu semakin lama semakin mahal, dengan demikian harga jual rumah kembali semakin tinggi <br>2. Harga diatas adalah salah satu alasan mengapa  Perumahan di Depok Cocok untuk Investasi</div>', unsafe_allow_html=True)

if (selected == "Prediction") :
    df2 = pd.read_csv('lamudi_pentaho_transform_fix.csv', usecols=['harga','luas_bangunan', 'luas_lahan'])
    
    st.write('Korelasi harga rumah dengan luas bangunan dan luas tanah')
    
    #Mengetahui nilai korelasi dari independent variable dan dependent variable.
    st.write(df2.corr().style.background_gradient())

    #Pertama, buat variabel x dan y.
    feature = df2.drop(columns='harga')
    target = df2['harga']
    #Kedua,  split data menjadi training and testing dengan porsi 80:20.
    ftr_train, ftr_test, tgt_train, tgt_test = train_test_split(feature, target, test_size=0.2, random_state=42)
    #convert data ke numpy arrays
    x_harga_train = feature.to_numpy()
    y_harga_train = target.to_numpy().ravel()
    #Ketiga,  bikin object linear regresi.
    model = LinearRegression()
    
    lin_reg = model.fit(x_harga_train, y_harga_train)

    def predict(building_area, land_area):
        """Makes a prediction using the linear regression model."""
        if lin_reg is None:
            st.error("Please upload a trained linear regression model.")
            return None

        # Create a DataFrame from the input values
        data = pd.DataFrame({
            "building_area": [building_area],
            "land_area": [land_area]
        })

        # Make the prediction
        prediction = lin_reg.predict(data)[0]
        return prediction

    st.title("Linear Regression Prediction App")

    # Text input fields for user input
    building_area = st.number_input("Luas Bangunan (sq m)", min_value=0.0)
    land_area = st.number_input("Luas Lahan (sq m)", min_value=0.0)

    # Button to trigger prediction
    if st.button("Predict"):
        # Make the prediction
        prediction = predict(building_area, land_area)

        if prediction is not None:
            st.success(f"Predicted value   :  {format_big_number(prediction)}")
        else:
            st.warning("Prediction could not be made.")

if (selected == "Gallery") :
    tab1, tab2, tab3, tab4 = st.tabs(['Rumah1', 'Rumah2', 'Rumah3','Rumah4'])
    with tab1 :
        st.header("Brosur")
        st.image("cgr3.PNG")
    with tab2 :
        st.header("Tahap Pengerjaan")
        st.image("cgr6.PNG")
    with tab3 :
        st.header("Rumah Contoh")
        st.image("cgr2.PNG")
    with tab4 :
        st.header("Rumah Contoh")
        st.image("cgr1.PNG")
