import streamlit as st
import pandas as pd
import time
import pymongo
import plotly.express as px
import plotly.graph_objects as go

# Fungsi untuk terhubung ke MongoDB
def get_mongodb_collection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["seeforme"]
    collection = db["history"]
    return collection

# Fungsi untuk mengambil data dari MongoDB dan mengembalikan dataframe
def fetch_data():
    collection = get_mongodb_collection()
    data = list(collection.find({}, {'_id': 0}))  # Mengambil semua data tanpa '_id'
    return pd.DataFrame(data)

# Streamlit App
st.title("Visualisasi Deteksi Objek Real-Time")

# Sidebar untuk pengaturan refresh
refresh_interval = st.sidebar.slider("Interval Refresh (detik)", 1, 30, 5)

st.write("Data Deteksi Objek dari MongoDB:")

# Loop untuk real-time refresh
while True:
    # Ambil data dari MongoDB
    df = fetch_data()
    
    if df.empty:
        st.write("Belum ada data.")
    else:
        # Konversi waktu deteksi ke format datetime
        df['detection_time'] = pd.to_datetime(df['detection_time'])

        # Tampilkan tabel data
        st.dataframe(df)

        # Grafik 1: Deteksi Objek dari Waktu ke Waktu
        df['hour'] = df['detection_time'].dt.hour
        hourly_count = df.groupby(['hour', 'location']).size().reset_index(name='count')

        fig_line = px.line(hourly_count, x='hour', y='count', color='location', markers=True,
                           labels={'hour': 'Jam', 'count': 'Jumlah Deteksi'},
                           title="Deteksi Objek dari Waktu ke Waktu")
        st.plotly_chart(fig_line)

        # Grafik 2: Proporsi Deteksi Objek per Lokasi
        location_count = df['location'].value_counts().reset_index()
        location_count.columns = ['location', 'count']

        fig_pie = px.pie(location_count, values='count', names='location',
                         title="Proporsi Deteksi Objek per Lokasi")
        st.plotly_chart(fig_pie)

        # Grafik 3: Deteksi Objek Berdasarkan Lokasi dan Jenis
        obj_location_count = df.groupby(['object_name', 'location']).size().reset_index(name='count')

        fig_stacked = px.bar(obj_location_count, x='object_name', y='count', color='location',
                             title="Deteksi Objek Berdasarkan Lokasi dan Jenis",
                             labels={'object_name': 'Nama Objek', 'count': 'Jumlah'})
        st.plotly_chart(fig_stacked)

        # Grafik 4: Heatmap Waktu dan Deteksi
        df['date'] = df['detection_time'].dt.date
        df['time'] = df['detection_time'].dt.time
        heatmap_data = df.groupby(['date', 'hour']).size().reset_index(name='count')

        fig_heatmap = px.density_heatmap(heatmap_data, x='date', y='hour', z='count', 
                                         title="Heatmap Deteksi Berdasarkan Waktu dan Tanggal",
                                         labels={'date': 'Tanggal', 'hour': 'Jam', 'count': 'Jumlah Deteksi'})
        st.plotly_chart(fig_heatmap)

        # Informasi objek dominan dan tidak dominan
        obj_count = df['object_name'].value_counts()
        dominant_object = obj_count.idxmax()
        least_dominant_object = obj_count.idxmin()
        st.write(f"Objek Dominan: {dominant_object} ({obj_count[dominant_object]} kali)")
        st.write(f"Objek Tidak Dominan: {least_dominant_object} ({obj_count[least_dominant_object]} kali)")

        # Informasi berdasarkan lokasi
        st.write("Detail Deteksi Berdasarkan Lokasi:")
        for location, loc_df in df.groupby('location'):
            st.subheader(f"Lokasi: {location.capitalize()}")
            st.dataframe(loc_df)

            loc_obj_count = loc_df['object_name'].value_counts()
            fig_bar = px.bar(loc_obj_count, x=loc_obj_count.index, y=loc_obj_count.values,
                             title=f"Jumlah Objek Terdeteksi di {location.capitalize()}",
                             labels={'x': 'Nama Objek', 'y': 'Jumlah'})
            st.plotly_chart(fig_bar)

            dominant_object_loc = loc_obj_count.idxmax()
            least_dominant_object_loc = loc_obj_count.idxmin()
            st.write(f"Objek Dominan di {location.capitalize()}: {dominant_object_loc} ({loc_obj_count[dominant_object_loc]} kali)")
            st.write(f"Objek Tidak Dominan di {location.capitalize()}: {least_dominant_object_loc} ({loc_obj_count[least_dominant_object_loc]} kali)")

    # Tunggu sebelum refresh berikutnya
    time.sleep(refresh_interval)
    st.experimental_rerun()  # Refresh halaman Streamlit


# # *******************************************************************************

# import streamlit as st
# import pandas as pd
# import time
# import pymongo
# import plotly.express as px
# import plotly.graph_objects as go

# # Fungsi untuk terhubung ke MongoDB
# def get_mongodb_collection():
#     client = pymongo.MongoClient("mongodb://localhost:27017/")
#     db = client["seeforme"]
#     collection = db["seeformecoll"]
#     return collection

# # Fungsi untuk mengambil data dari MongoDB dan mengembalikan dataframe
# def fetch_data():
#     collection = get_mongodb_collection()
#     data = list(collection.find({}, {'_id': 0}))  # Mengambil semua data tanpa '_id'
#     return pd.DataFrame(data)

# # Streamlit App
# st.title("Visualisasi Deteksi Objek Real-Time")

# # Sidebar untuk pengaturan refresh
# refresh_interval = st.sidebar.slider("Interval Refresh (detik)", 1, 30, 5)

# st.write("Data Deteksi Objek dari MongoDB:")

# # Loop untuk real-time refresh
# while True:
#     # Ambil data dari MongoDB
#     df = fetch_data()
    
#     if df.empty:
#         st.write("Belum ada data.")
#     else:
#         # Tampilkan tabel data
#         st.dataframe(df)

#         # Grafik 1: Deteksi Objek dari Waktu ke Waktu
#         df['detection_time'] = pd.to_datetime(df['detection_time'])
#         df['hour'] = df['detection_time'].dt.hour
#         hourly_count = df.groupby(['hour', 'location']).size().reset_index(name='count')

#         fig_line = px.line(hourly_count, x='hour', y='count', color='location', markers=True,
#                            labels={'hour': 'Jam', 'count': 'Jumlah Deteksi'},
#                            title="Deteksi Objek dari Waktu ke Waktu")
#         st.plotly_chart(fig_line)

#         # Grafik 2: Proporsi Deteksi Objek per Lokasi
#         location_count = df['location'].value_counts().reset_index()
#         location_count.columns = ['location', 'count']

#         fig_pie = px.pie(location_count, values='count', names='location',
#                          title="Proporsi Deteksi Objek per Lokasi")
#         st.plotly_chart(fig_pie)

#         # Grafik 3: Deteksi Objek Berdasarkan Lokasi dan Jenis
#         obj_location_count = df.groupby(['object_name', 'location']).size().reset_index(name='count')

#         fig_stacked = px.bar(obj_location_count, x='object_name', y='count', color='location',
#                              title="Deteksi Objek Berdasarkan Lokasi dan Jenis",
#                              labels={'object_name': 'Nama Objek', 'count': 'Jumlah'})
#         st.plotly_chart(fig_stacked)

#         # Grafik 4: Heatmap Waktu dan Deteksi
#         df['date'] = df['detection_time'].dt.date
#         df['time'] = df['detection_time'].dt.time
#         heatmap_data = df.groupby(['date', 'hour']).size().reset_index(name='count')

#         fig_heatmap = px.density_heatmap(heatmap_data, x='date', y='hour', z='count', 
#                                          title="Heatmap Deteksi Berdasarkan Waktu dan Tanggal",
#                                          labels={'date': 'Tanggal', 'hour': 'Jam', 'count': 'Jumlah Deteksi'})
#         st.plotly_chart(fig_heatmap)

#         # Informasi objek dominan dan tidak dominan
#         obj_count = df['object_name'].value_counts()
#         dominant_object = obj_count.idxmax()
#         least_dominant_object = obj_count.idxmin()
#         st.write(f"Objek Dominan: {dominant_object} ({obj_count[dominant_object]} kali)")
#         st.write(f"Objek Tidak Dominan: {least_dominant_object} ({obj_count[least_dominant_object]} kali)")

#         # Informasi berdasarkan lokasi
#         st.write("Detail Deteksi Berdasarkan Lokasi:")
#         for location, loc_df in df.groupby('location'):
#             st.subheader(f"Lokasi: {location.capitalize()}")
#             st.dataframe(loc_df)

#             loc_obj_count = loc_df['object_name'].value_counts()
#             fig_bar = px.bar(loc_obj_count, x=loc_obj_count.index, y=loc_obj_count.values,
#                              title=f"Jumlah Objek Terdeteksi di {location.capitalize()}",
#                              labels={'x': 'Nama Objek', 'y': 'Jumlah'})
#             st.plotly_chart(fig_bar)

#             dominant_object_loc = loc_obj_count.idxmax()
#             least_dominant_object_loc = loc_obj_count.idxmin()
#             st.write(f"Objek Dominan di {location.capitalize()}: {dominant_object_loc} ({loc_obj_count[dominant_object_loc]} kali)")
#             st.write(f"Objek Tidak Dominan di {location.capitalize()}: {least_dominant_object_loc} ({loc_obj_count[least_dominant_object_loc]} kali)")

#     # Tunggu sebelum refresh berikutnya
#     time.sleep(refresh_interval)
#     st.experimental_rerun()  # Refresh halaman Streamlit
# # *******************************************************************************





# # =================================================================================
# import streamlit as st
# import pandas as pd
# import time
# import pymongo

# # Fungsi untuk terhubung ke MongoDB
# def get_mongodb_collection():
#     client = pymongo.MongoClient("mongodb://localhost:27017/")
#     db = client["see4me"]
#     collection = db["see4mecoll"]
#     return collection

# # Fungsi untuk mengambil data dari MongoDB dan mengembalikan dataframe
# def fetch_data():
#     collection = get_mongodb_collection()
#     data = list(collection.find({}, {'_id': 0}))  # Mengambil semua data tanpa '_id'
#     return pd.DataFrame(data)

# # Streamlit App
# st.title("Visualisasi Deteksi Objek Real-Time")

# # Sidebar untuk pengaturan refresh
# refresh_interval = st.sidebar.slider("Interval Refresh (detik)", 1, 30, 5)

# st.write("Data Deteksi Objek dari MongoDB:")

# # Loop untuk real-time refresh
# while True:
#     # Ambil data dari MongoDB
#     df = fetch_data()
    
#     if df.empty:
#         st.write("Belum ada data.")
#     else:
#         # Tampilkan tabel data
#         st.dataframe(df)

#         # Tampilkan bar chart dari jumlah objek terdeteksi
#         obj_count = df['object_name'].value_counts()
#         st.bar_chart(obj_count)

#     # Tunggu sebelum refresh berikutnya
#     time.sleep(refresh_interval)
# # =================================================================================