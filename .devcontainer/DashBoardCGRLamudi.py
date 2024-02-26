import streamlit as st
import pandas as pd
import altair as alt
# from numerize import numerize

st.set_page_config(layout='wide')

# Judul
st.title('MENGHITUNG HARGA BANGUNAN DAN LAHAN PERUMAHAN DI DEPOK')

# BAGIAN CGR
df = pd.read_csv('perum_cgr_fix_2.csv')

def format_big_number(num):
    if num >= 1e9:
        return f"{num / 1e9:.2f} Milyar"
    elif num >= 1e6:
        return f"{num / 1e6:.2f} Juta"
    else:
        return f"{num:.2f}"

st.header("Data Perum CGR")
# 2 Kolom Harga Lahan @ CGR  
mx_hl2010, mx_hl2024, mx_delta_hl= st.columns(3)
with mx_hl2010 :
    # harga lahan permeter dari AJB
    hl2010 = 142160000/91
    st.metric('Harga Lahan 2010 / m2', format_big_number(hl2010), delta=None, delta_color="normal", help=None, label_visibility="visible")

with mx_hl2024 :
    hl2024 = (df['harga_kpr'].sum() - df['luas_bangunan'].sum() * 4921226.098787341) / df['luas_lahan'].sum()
    st.metric('Harga Lahan 2024 / m2', format_big_number(hl2024), delta=None, delta_color="normal", help=None, label_visibility="visible")   

with mx_delta_hl :
    selisih_hl = hl2024 - hl2010
    delta_hl = 100 * (hl2024 - hl2010) / hl2010
    st.metric('kenaikan', value=format_big_number(selisih_hl), delta=f'{delta_hl:.2f}%', delta_color="normal", help=None, label_visibility="visible")
    
 # Kolom Harga bangunan   
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
    width=800,
    height=400
)

# Display the chart
st.altair_chart(barchart)

# BAGIAN LAMUDI
st.header("Data lamudi.com")
df2 = pd.read_csv('lamudi_pentaho_transform_fix.csv')

def hld(kec):
    hl_lamudi_2 = (df2[df2['alamat']==kec]['harga'].sum() - df2[df2['alamat']==kec]['luas_bangunan'].sum() * 4921226.098787341) / df2[df2['alamat']==kec]['luas_lahan'].sum()
    return hl_lamudi_2

# Grafik harga lahan permeter berdasarkan kecamatan di depok
grafik = pd.DataFrame({
    "kecamatan": ["Sawangan, Depok","Sukmajaya, Depok","Cimanggis, Depok","Cilodong, Depok", "Depok Jaya, Depok","Tapos, Depok", "Depok, Depok", "Beji, Depok", "Cinere, Depok", "Sawangan Baru, Depok", "Pancoran Mas, Depok", "Cipayung, Depok", "Bojongsari Baru, Depok", "Limo, Depok"],
    "value": [hld("Sawangan, Depok"),hld("Sukmajaya, Depok"),hld("Cimanggis, Depok"),hld("Cilodong, Depok"), hld("Depok Jaya, Depok"),hld("Tapos, Depok"),hld("Depok, Depok"),hld("Beji, Depok"), hld("Cinere, Depok"), hld("Sawangan Baru, Depok"), hld("Pancoran Mas, Depok"), hld("Cipayung, Depok"), hld("Bojongsari Baru, Depok"), hld("Limo, Depok")]
})
st.bar_chart(data=grafik, x="kecamatan", y="value")

st.write(grafik.describe())

