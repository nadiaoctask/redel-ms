import streamlit as st
from supabase import create_client, Client
from datetime import date
import pandas as pd

st.set_page_config(page_title="Redelivery Management System", layout="wide")

SUPABASE_URL = "https://rmlxzhhsvcgadzcjpyxm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJtbHh6aGhzdmNnYWR6Y2pweXhtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzOTE2NzAsImV4cCI6MjEwMDk2NzY3MH0.Ft0tKwqmwyNdAChPombLj3Og7QIE_1vix24V3JUmNw8"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase: Client = init_supabase()
except Exception as e:
    st.error(f"Gagal koneksi Supabase: {e}")

# ==========================================
# 1. KONFIGURASI LAYAR & CUSTOM CSS (FULL CANVA MATCH)
# ==========================================
st.set_page_config(
    page_title="Redelivery Management System - WINGS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load FontAwesome & Font Poppins lewat CDN untuk Icon & Tipografi Presisi
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
    /* Reset & Prevent Scrolling untuk Pas 1 Layar */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Poppins', sans-serif !important;
        background-color: #F4F7FA !important;
        overflow: hidden !important; /* Mencegah scroll */
    }
    
    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 0rem !important;
        max-width: 98% !important;
    }

    /* --- SIDEBAR NAVBAR CUSTOM --- */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        padding-top: 1rem;
    }
    
    /* Styling Tombol Navigasi Samping */
    div.stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }

    /* Top Banner Header */
    .header-title {
        color: #0E4A6E;
        font-weight: 700;
        font-size: 28px;
        margin-bottom: 0px;
    }
    
    /* --- METRIC CARDS (3 STATUS TOP) --- */
    .status-card-container {
        background: white;
        border-radius: 14px;
        padding: 15px 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #EAEFF4;
        margin-bottom: 15px;
    }
    
    .status-item {
        display: flex;
        align-items: center;
        gap: 20px;
        flex: 1;
        justify-content: center;
    }
    
    .status-bar {
        width: 6px;
        height: 55px;
        border-radius: 10px;
    }
    
    .status-number {
        font-size: 42px;
        font-weight: 700;
        color: #0E4A6E;
        line-height: 1;
    }
    
    .status-label {
        font-size: 13px;
        font-weight: 600;
        color: #475569;
        max-width: 120px;
    }

    /* --- DARK AZURE ACTION BUTTONS --- */
    .azure-btn {
        background-color: #0E4A6E !important;
        color: white !important;
        border-radius: 14px !important;
        padding: 35px 20px !important;
        font-size: 22px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 6px 16px rgba(14, 74, 110, 0.25) !important;
    }

    .green-btn {
        background-color: #2D8A56 !important;
        color: white !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border: none !important;
    }

    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Supabase Client Init
SUPABASE_URL = "https://rmlxzhhsvcgadzcjpyxm.supabase.co"
SUPABASE_KEY = "PASTE_ANON_KEY_KAMU_DISINI_YANG_AWALAN_eyJhbG"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase: Client = init_supabase()
except Exception as e:
    st.error(f"Koneksi error: {e}")

# Session State untuk Active Menu (Ganti Radio dengan Tab Klik murni)
if 'active_nav' not in st.session_state:
    st.session_state['active_nav'] = "Dashboard"

# ==========================================
# 2. SIDEBAR NAVBAR (ICON CDN + TANPA RADIO)
# ==========================================
with st.sidebar:
    # Logo Wings & Title
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/47/Wings_Logo.svg" width="110">
        </div>
    """, unsafe_allow_html=True)
    
    # Custom Menu Buttons dengan FontAwesome Icons (No Radio)
    def nav_button(label, icon_class, key_name):
        is_active = st.session_state['active_nav'] == key_name
        btn_style = "primary" if is_active else "secondary"
        if st.button(f"{label}", key=f"nav_{key_name}", use_container_width=True, type=btn_style):
            st.session_state['active_nav'] = key_name
            st.rerun()

    st.caption("MAIN MENU")
    nav_button(" Dashboard", "fa-solid fa-house", "Dashboard")
    
    st.caption("FORMULIR")
    nav_button(" Penerimaan SKR", "fa-solid fa-boxes-packing", "Penerimaan SKR")
    nav_button(" Redelivery", "fa-solid fa-truck-ramp-box", "Redelivery")
    
    st.caption("DATA")
    nav_button(" Data SKR Redel", "fa-solid fa-database", "Data SKR Redel")
    nav_button(" Data Palet", "fa-solid fa-pallet", "Data Palet")
    nav_button(" Laporan Rekap", "fa-solid fa-chart-column", "Laporan Rekap")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button(" Logout", key="btn_logout", use_container_width=True):
        st.toast("Berhasil Logout")

# Header User Info Atas Kanan
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <h2 class="header-title">Redelivery Management System</h2>
        <div style="text-align: right; font-size: 13px; color: #334155;">
            <b>Suliadi</b><br><span style="color: #64748B;">Supervisor</span>
            <i class="fa-solid fa-circle-user fa-2x" style="vertical-align: middle; margin-left: 8px; color: #0E4A6E;"></i>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 3. PAGE 1: DASHBOARD (PRESISI CANVA)
# ==========================================
if st.session_state['active_nav'] == "Dashboard":
    
    # Fetch Data Realtime
    try:
        res_skr = supabase.table("skr_redel").select("status_skr").execute().data
        cnt_menunggu = sum(1 for item in res_skr if item['status_skr'] == 'Menunggu shipment baru')
        cnt_parsial = sum(1 for item in res_skr if item['status_skr'] == 'Parsial')
        cnt_selesai = sum(1 for item in res_skr if item['status_skr'] == 'Selesai')
    except:
        cnt_menunggu, cnt_parsial, cnt_selesai = 28, 10, 99 # Fallback display
    
    # --- METRIC CARDS TOP (WARNA DARK AZURE, RED, YELLOW, GREEN) ---
    st.markdown(f"""
        <div class="status-card-container">
            <div class="status-item">
                <div class="status-bar" style="background-color: #C0392B;"></div>
                <div class="status-label">Menunggu Shipment Redelivery</div>
                <div class="status-number">{cnt_menunggu}</div>
                <span style="font-size:12px; color:#94A3B8; font-weight:600;">SKR</span>
            </div>
            <div style="width: 1px; height: 40px; background: #E2E8F0;"></div>
            <div class="status-item">
                <div class="status-bar" style="background-color: #F1C40F;"></div>
                <div class="status-label">Redelivery Parsial</div>
                <div class="status-number">{cnt_parsial}</div>
                <span style="font-size:12px; color:#94A3B8; font-weight:600;">SKR</span>
            </div>
            <div style="width: 1px; height: 40px; background: #E2E8F0;"></div>
            <div class="status-item">
                <div class="status-bar" style="background-color: #27AE60;"></div>
                <div class="status-label">Selesai Redelivery</div>
                <div class="status-number">{cnt_selesai}</div>
                <span style="font-size:12px; color:#94A3B8; font-weight:600;">SKR</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # --- CARI SHIPMENT SEARCH BAR ---
    with st.container():
        col_s1, col_s2 = st.columns([5, 1])
        with col_s1:
            search_input = st.text_input("", placeholder="🔍  Masukkan Nomor Shipment...", label_visibility="collapsed")
        with col_s2:
            btn_cari = st.button("Cari", type="primary", use_container_width=True)

    if search_input or btn_cari:
        if search_input:
            res = supabase.table("skr_redel").select("*, penempatan(nomor_palet)").eq("no_shipment", search_input.strip()).execute().data
            if res:
                d = res[0]
                st.success(f"Shipment Ditemukan: **{d['no_shipment']}** | Delman: {d['nama_delman']} | Nopol: {d['nopol_kendaraan']} | Status: {d['status_skr']}")
            else:
                st.warning("Data Shipment tidak ditemukan.")

    st.write("")
    
    # --- 2 TOMBOL UTAMA DARK AZURE (`#0E4A6E`) ---
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("📦   Penerimaan SKR", key="main_btn_in", use_container_width=True, type="primary"):
            st.session_state['active_nav'] = "Penerimaan SKR"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_b2:
        if st.button("🚚   Redelivery", key="main_btn_out", use_container_width=True, type="primary"):
            st.session_state['active_nav'] = "Redelivery"
            st.rerun()

    st.write("")
    # --- GREEN DOWNLOAD BUTTON ---
    st.button("📥   Download Laporan Rekapitulasi Hari Ini", key="btn_download_main", use_container_width=True)

# ==========================================
# 4. PAGE 2: FORM PENERIMAAN SKR
# ==========================================
elif st.session_state['active_nav'] == "Penerimaan SKR":
    st.subheader("Penerimaan SKR (Inbound)")
    with st.container(border=True):
        st.markdown("##### **Masukkan Data Shipment**")
        c1, c2 = st.columns(2)
        with c1:
            no_shipment = st.text_input("No. Shipment *", placeholder="Masukkan Nomor Shipment")
            nama_delman = st.text_input("Nama Delman", placeholder="Nama Driver / Sopir")
            nopol = st.text_input("Nopol Kendaraan", placeholder="B 1234 XYZ")
        with c2:
            jenis_gr = st.radio("Jenis GR", ["Sistem", "Turun gudang"], horizontal=True)
            tgl = st.date_input("Tanggal Penerimaan", value=date.today(), disabled=True)
            
            palet_res = supabase.table("palet").select("nomor_palet").execute().data
            opts = [p['nomor_palet'] for p in palet_res] if palet_res else []
            
            cp1, cp2 = st.columns([3, 2])
            with cp1:
                p_selected = st.selectbox("Pilih Palet", options=opts if opts else ["Tidak ada palet"])
            with cp2:
                st.write("")
                st.write("")
                if st.button("➕ Buat Palet Baru", use_container_width=True):
                    st.toast("Buka Pop-up Buat Palet")

        st.divider()
        if st.button("💾 SIMPAN PENERIMAAN", type="primary", use_container_width=True):
            if no_shipment:
                supabase.table("skr_redel").insert({
                    "no_shipment": no_shipment.strip(),
                    "nama_delman": nama_delman,
                    "nopol_kendaraan": nopol,
                    "jenis_gr": jenis_gr,
                    "tanggal_penerimaan": str(tgl),
                    "status_skr": "Menunggu shipment baru"
                }).execute()
                st.success("Berhasil Disimpan!")

# ==========================================
# 5. PAGE 3: REDELIVERY
# ==========================================
elif st.session_state['active_nav'] == "Redelivery":
    st.subheader("Redelivery (Outbound)")
    st.info("Form Input Redelivery Pengeluaran Barang")

# ==========================================
# 6. PAGE 4: DATA SKR REDEL (MONITORING)
# ==========================================
elif st.session_state['active_nav'] == "Data SKR Redel":
    st.subheader("Data SKR Redelivery")
    tab1, tab2 = st.tabs(["📥 TAB 1: PENERIMAAN SKR (IN)", "📤 TAB 2: REDELIVERY (OUT)"])
    
    with tab1:
        st.write("Monitoring Data SKR Inbound")
    with tab2:
        st.write("Monitoring Data Redelivery Outbound")

elif st.session_state['active_nav'] == "Data Palet":
    st.subheader("Master Data Palet")
    
elif st.session_state['active_nav'] == "Laporan Rekap":
    st.subheader("Laporan Rekapitulasi")