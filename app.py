import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Redelivery Management System", layout="wide")

SUPABASE_URL = "https://rmlxzhhsvcgadzcjpyxm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJtbHh6aGhzdmNnYWR6Y2pweXhtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzOTE2NzAsImV4cCI6MjEwMDk2NzY3MH0.Ft0tKwqmwyNdAChPombLj3Og7QIE_1vix24V3JUmNw8"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_supabase()

st.title("Redelivery Management System")
st.write("Data Palet")

# 4. Fungsi Ambil Data Palet
def get_palet_data():
    response = supabase.table("palet").select("*").execute()
    return response.data

# 5. Tampilkan Data di UI Streamlit
st.subheader("Data Palet")

try:
    data_palet = get_palet_data()
    
    if data_palet:
        # Menampilkan data dalam bentuk Tabel Interaktif Streamlit
        st.dataframe(data_palet, use_container_width=True)
        
        # Tampilkan Summary Ringkas
        total_palet = len(data_palet)
        in_use = sum(1 for p in data_palet if p['status_palet'] == 'In Use')
        available = sum(1 for p in data_palet if p['status_palet'] == 'Available')
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Palet", total_palet)
        col2.metric("Palet Available", available)
        col3.metric("Palet In Use", in_use)
    else:
        st.info("Belum ada data palet di database.")

except Exception as e:
    st.error(f"Gagal terhubung ke Supabase: {e}")