import streamlit as st
import streamlit.components.v1 as components
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
# 1. KONFIGURASI HALAMAN & CUSTOM CSS SYSTEM
# ==========================================
st.set_page_config(
    page_title="Redelivery Management System - WINGS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS & CDN FontAwesome
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
    /* Reset Layout Biar Pas 1 Layar (No Scroll) */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Poppins', sans-serif !important;
        background-color: #F4F7FA !important;
        overflow-x: hidden;
    }
    
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 98% !important;
    }

    /* Sidebar Styling Smooth */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* Tombol Navigasi Custom (Tanpa Border Kaku) */
    div[data-testid="stSidebar"] div.stButton > button {
        background-color: transparent !important;
        color: #475569 !important;
        border: none !important;
        border-radius: 8px !important;
        text-align: left !important;
        padding: 10px 16px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        box-shadow: none !important;
        transition: all 0.2s ease-in-out !important;
    }

    div[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #F1F5F9 !important;
        color: #0E4A6E !important;
    }

    div[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
        background-color: #0E4A6E !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Primary Button Dark Azure (#0E4A6E) */
    div.stButton > button[kind="primary"] {
        background-color: #0E4A6E !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 12px rgba(14, 74, 110, 0.2) !important;
    }

    /* Card Metrics Styling Presisi Canva */
    .metric-container {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 16px 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        border: 1px solid #E2E8F0;
        display: flex;
        align-items: center;
    }

    .metric-value {
        font-size: 38px;
        font-weight: 700;
        color: #0E4A6E;
        line-height: 1;
    }

    .metric-label {
        font-size: 13px;
        font-weight: 600;
        color: #475569;
    }

    /* Hide Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Session State Navigasi
if 'active_nav' not in st.session_state:
    st.session_state['active_nav'] = "Dashboard"

# ==========================================
# 2. POP-UP MODAL: TAMBAH PALET BARU
# ==========================================
@st.dialog("➕ Buat Palet Baru")
def modal_tambah_palet():
    st.write("Sistem akan menambahkan data master Palet baru:")
    col_a, col_b = st.columns(2)
    with col_a:
        nomor_palet_input = st.text_input("Nomor Palet Baru *", placeholder="Contoh: 17 atau TURUN-01")
    with col_b:
        jenis_palet_input = st.selectbox("Jenis Palet", ["Bin", "Turun palet"])
        
    st.write("")
    if st.button("💾 Simpan Palet Baru", type="primary", use_container_width=True):
        if not nomor_palet_input:
            st.error("Nomor palet wajib diisi!")
        else:
            try:
                supabase.table("palet").insert({
                    "nomor_palet": nomor_palet_input.strip(),
                    "jenis_palet": jenis_palet_input,
                    "status_palet": "Available"
                }).execute()
                st.toast(f"Palet {nomor_palet_input} berhasil ditambahkan!", icon="✅")
                st.rerun()
            except Exception as e:
                st.error(f"Gagal menyimpan: {e}")

# ==========================================
# 3. SIDEBAR NAVBAR (NAVIGASI SMOOTH)
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/47/Wings_Logo.svg", width=110)
    st.markdown("<h4 style='color:#0E4A6E; margin-bottom:20px;'>Redelivery System</h4>", unsafe_allow_html=True)
    
    def nav_item(label, nav_key):
        is_active = st.session_state['active_nav'] == nav_key
        btn_type = "primary" if is_active else "secondary"
        if st.button(f"{label}", key=f"nav_{nav_key}", use_container_width=True, type=btn_type):
            st.session_state['active_nav'] = nav_key
            st.rerun()

    st.caption("MAIN MENU")
    nav_item("Dashboard", "Dashboard")
    
    st.caption("FORMULIR")
    nav_item("Penerimaan SKR", "Penerimaan SKR")
    nav_item("Redelivery", "Redelivery")
    
    st.caption("DATA")
    nav_item("Data SKR Redel", "Data SKR Redel")
    nav_item("Data Palet", "Data Palet")
    nav_item("Laporan Rekap", "Laporan Rekap")
    
    st.divider()
    if st.button("Logout", key="btn_logout", use_container_width=True):
        st.toast("Logout berhasil")

# Header User Info Atas Kanan
c_head1, c_head2 = st.columns([4, 1])
with c_head1:
    st.markdown("<h2 style='color:#0E4A6E; font-weight:700; margin:0;'>Redelivery Management System</h2>", unsafe_allow_html=True)
with c_head2:
    st.markdown("""
        <div style="text-align: right; font-size: 13px; color: #334155;">
            <b>Suliadi</b><br><span style="color: #64748B;">Supervisor</span>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# ==========================================
# 4. PAGE 1: DASHBOARD UTAMA (PRESISI CANVA)
# ==========================================
if st.session_state['active_nav'] == "Dashboard":
    
    # Fetch Data Realtime
    try:
        res_skr = supabase.table("skr_redel").select("status_skr").execute().data
        cnt_menunggu = sum(1 for item in res_skr if item['status_skr'] == 'Menunggu shipment baru')
        cnt_parsial = sum(1 for item in res_skr if item['status_skr'] == 'Parsial')
        cnt_selesai = sum(1 for item in res_skr if item['status_skr'] == 'Selesai')
    except:
        cnt_menunggu, cnt_parsial, cnt_selesai = 28, 10, 99

    st.markdown("##### **Status SKR Redelivery**")
    
    # 3 Metrics Card Canva Design
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class="metric-container" style="border-left: 6px solid #C0392B;">
                <div style="flex:1;">
                    <div class="metric-label">Menunggu Shipment Redelivery</div>
                    <div class="metric-value">{cnt_menunggu} <span style="font-size:14px; color:#94A3B8;">SKR</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="metric-container" style="border-left: 6px solid #F1C40F;">
                <div style="flex:1;">
                    <div class="metric-label">Redelivery Parsial</div>
                    <div class="metric-value">{cnt_parsial} <span style="font-size:14px; color:#94A3B8;">SKR</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="metric-container" style="border-left: 6px solid #27AE60;">
                <div style="flex:1;">
                    <div class="metric-label">Selesai Redelivery</div>
                    <div class="metric-value">{cnt_selesai} <span style="font-size:14px; color:#94A3B8;">SKR</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # Search Bar Shipment
    col_s1, col_s2 = st.columns([5, 1])
    with col_s1:
        search_input = st.text_input("", placeholder="Masukkan Nomor Shipment...", label_visibility="collapsed")
    with col_s2:
        btn_cari = st.button("Cari", type="primary", use_container_width=True)

    if search_input or btn_cari:
        if search_input:
            res = supabase.table("skr_redel").select("*, penempatan(nomor_palet)").eq("no_shipment", search_input.strip()).execute().data
            if res:
                d = res[0]
                palet_list = [p['nomor_palet'] for p in d.get('penempatan', [])]
                st.success(f"Shipment Ditemukan: **{d['no_shipment']}** | Delman: {d['nama_delman']} | Nopol: {d['nopol_kendaraan']} | Status: {d['status_skr']}")
                st.info(f"Lokasi Palet: {', '.join(palet_list) if palet_list else '-'}")
            else:
                st.warning("Data Shipment tidak ditemukan.")

    st.write("")
    
    # 2 Tombol Utama Dark Azure (#0E4A6E)
    cb1, cb2 = st.columns(2)
    with cb1:
        if st.button("Penerimaan SKR", key="btn_main_in", use_container_width=True, type="primary"):
            st.session_state['active_nav'] = "Penerimaan SKR"
            st.rerun()
    with cb2:
        if st.button("Redelivery", key="btn_main_out", use_container_width=True, type="primary"):
            st.session_state['active_nav'] = "Redelivery"
            st.rerun()

    st.write("")
    # Tombol Download Hijau
    st.markdown("""
        <style>
        div.stButton > button[key="btn_dl"] {
            background-color: #27AE60 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
    st.button("Download Laporan Rekapitulasi Hari Ini", key="btn_dl", use_container_width=True)

# ==========================================
# 5. PAGE 2: FORM PENERIMAAN SKR
# ==========================================
elif st.session_state['active_nav'] == "Penerimaan SKR":
    st.subheader("Penerimaan SKR (Inbound)")
    
    # Ambil Palet Realtime
    try:
        palet_db = supabase.table("palet").select("nomor_palet").execute().data
        list_palet_options = [p['nomor_palet'] for p in palet_db] if palet_db else []
    except:
        list_palet_options = []

    with st.container(border=True):
        st.markdown("##### **Masukkan Data Shipment**")
        c1, c2 = st.columns(2)
        with c1:
            no_shipment = st.text_input("No. Shipment *", placeholder="Masukkan Nomor Shipment")
            nama_delman = st.text_input("Nama Delman", placeholder="Nama Driver / Sopir")
            nopol_kendaraan = st.text_input("Nopol Kendaraan", placeholder="B 1234 XYZ")
        with c2:
            jenis_gr = st.radio("Jenis GR", ["Sistem", "Turun gudang"], horizontal=True)
            tanggal_penerimaan = st.date_input("Tanggal Penerimaan", value=date.today(), disabled=True)
            
            cp1, cp2 = st.columns([3, 2])
            with cp1:
                selected_palet = st.selectbox("Pilih Palet", options=list_palet_options if list_palet_options else ["Belum ada palet"])
            with cp2:
                st.write("")
                st.write("")
                if st.button("➕ BUAT PALET BARU", use_container_width=True):
                    modal_tambah_palet()

        st.divider()
        if st.button("💾 SIMPAN PENERIMAAN", type="primary", use_container_width=True):
            if not no_shipment:
                st.error("No. Shipment wajib diisi!")
            else:
                try:
                    supabase.table("skr_redel").insert({
                        "no_shipment": no_shipment.strip(),
                        "nama_delman": nama_delman,
                        "nopol_kendaraan": nopol_kendaraan,
                        "jenis_gr": jenis_gr,
                        "tanggal_penerimaan": str(tanggal_penerimaan),
                        "status_skr": "Menunggu shipment baru"
                    }).execute()
                    
                    if selected_palet and selected_palet != "Belum ada palet":
                        supabase.table("penempatan").insert({
                            "nomor_palet": selected_palet,
                            "no_shipment": no_shipment.strip()
                        }).execute()
                        supabase.table("palet").update({"status_palet": "In Use"}).eq("nomor_palet", selected_palet).execute()

                    st.success(f"✅ Penerimaan SKR {no_shipment} Berhasil Disimpan!")
                except Exception as e:
                    st.error(f"Gagal menyimpan data: {e}")

# ==========================================
# 6. PAGE 3: FORM REDELIVERY
# ==========================================
elif st.session_state['active_nav'] == "Redelivery":
    st.subheader("Redelivery (Outbound)")
    
    try:
        skr_db = supabase.table("skr_redel").select("no_shipment").neq("status_skr", "Selesai").execute().data
        list_skr_options = [s['no_shipment'] for s in skr_db] if skr_db else []
    except:
        list_skr_options = []

    with st.container(border=True):
        st.markdown("##### **Masukkan Data Redelivery**")
        rc1, rc2 = st.columns(2)
        with rc1:
            no_shipment_redel = st.text_input("No. Shipment Baru *", placeholder="Input Nomor Redelivery Baru")
            nama_delman_redel = st.text_input("Nama Delman", placeholder="Nama Driver Redel")
        with rc2:
            nopol_redel = st.text_input("Nopol Kendaraan", placeholder="B 9999 RED")
            tgl_pengiriman = st.date_input("Tanggal Pengiriman", value=date.today(), disabled=True)

    st.write("")
    with st.container(border=True):
        st.markdown("##### **Masukkan Data SKR yang Diangkut**")
        
        if 'redel_items_count' not in st.session_state:
            st.session_state['redel_items_count'] = 1

        items_to_save = []
        for i in range(st.session_state['redel_items_count']):
            col_i1, col_i2, col_i3, col_i4 = st.columns([3, 2, 2, 1])
            with col_i1:
                skr_selected = st.selectbox(f"No. SKR #{i+1}", options=list_skr_options, key=f"skr_sel_{i}")
            with col_i2:
                jenis_redel = st.radio("Jenis Redel", ["Parsial", "Full"], key=f"j_redel_{i}", horizontal=True)
            with col_i3:
                if jenis_redel == "Parsial":
                    is_final = st.checkbox("Kiriman Terakhir? (Selesai)", key=f"fin_{i}")
                else:
                    is_final = True
                    st.caption("✓ Otomatis Selesai (Full)")
            with col_i4:
                st.write("")
                st.write("")
                if i > 0:
                    if st.button("🗑️", key=f"btn_del_row_{i}"):
                        st.session_state['redel_items_count'] -= 1
                        st.rerun()

            items_to_save.append({
                "no_shipment": skr_selected,
                "jenis_redel": jenis_redel,
                "is_final_delivery": is_final
            })

        if st.button("➕ Tambah SKR Lain Ke Pengiriman Ini"):
            st.session_state['redel_items_count'] += 1
            st.rerun()

    st.divider()
    if st.button("💾 SIMPAN REDELIVERY", type="primary", use_container_width=True):
        if not no_shipment_redel:
            st.error("No. Shipment Baru wajib diisi!")
        else:
            try:
                supabase.table("redelivery").insert({
                    "no_shipment_redel": no_shipment_redel.strip(),
                    "nama_delman": nama_delman_redel,
                    "nopol_kendaraan": nopol_redel,
                    "tanggal_pengiriman": str(tgl_pengiriman)
                }).execute()
                
                for item in items_to_save:
                    if item["no_shipment"]:
                        supabase.table("detail_redel").insert({
                            "no_shipment_redel": no_shipment_redel.strip(),
                            "no_shipment": item["no_shipment"],
                            "jenis_redel": item["jenis_redel"],
                            "is_final_delivery": item["is_final_delivery"]
                        }).execute()
                        
                        new_status = "Selesai" if item["is_final_delivery"] else "Parsial"
                        supabase.table("skr_redel").update({"status_skr": new_status}).eq("no_shipment", item["no_shipment"]).execute()

                st.success(f"✅ Redelivery {no_shipment_redel} Berhasil Disimpan!")
            except Exception as e:
                st.error(f"Gagal menyimpan data Redelivery: {e}")

# ==========================================
# 7. HALAMAN 4: MONITORING (DATA SKR REDEL)
# ==========================================
elif st.session_state['active_nav'] == "Data SKR Redel":
    st.subheader("Data SKR Redelivery")
    tab1, tab2 = st.tabs(["TAB 1: PENERIMAAN SKR (IN)", "TAB 2: REDELIVERY (OUT)"])
    
    with tab1:
        c_f1, c_f2, c_f3 = st.columns([3, 2, 2])
        with c_f1:
            search_skr = st.text_input("CARI DATA", placeholder="Input No SKR / Nama Delman / ID Palet...")
        with c_f2:
            filter_gr = st.radio("JENIS GR", ["Semua GR", "GR Sistem", "GR Turun Gudang"], horizontal=True)
        with c_f3:
            filter_status = st.selectbox("STATUS SKR", ["Semua Status", "Menunggu shipment baru", "Parsial", "Selesai"])

        data_skr = supabase.table("skr_redel").select("*, penempatan(nomor_palet), detail_redel(*)").execute().data
        
        if data_skr:
            filtered_skr = data_skr
            if search_skr:
                filtered_skr = [s for s in filtered_skr if search_skr.lower() in s['no_shipment'].lower() or search_skr.lower() in (s['nama_delman'] or '').lower()]
            if filter_gr != "Semua GR":
                gr_val = "Sistem" if filter_gr == "GR Sistem" else "Turun gudang"
                filtered_skr = [s for s in filtered_skr if s['jenis_gr'] == gr_val]
            if filter_status != "Semua Status":
                filtered_skr = [s for s in filtered_skr if s['status_skr'] == filter_status]

            for item in filtered_skr:
                palet_list = [p['nomor_palet'] for p in item.get('penempatan', [])]
                palet_str = ", ".join(palet_list) if palet_list else "-"
                
                with st.expander(f"{item['no_shipment']} | GR: {item['jenis_gr']} | Palet: {palet_str} | Status: {item['status_skr']}"):
                    st.write(f"**Delman:** {item['nama_delman']} | **Nopol:** {item['nopol_kendaraan']} | **Tgl Masuk:** {item['tanggal_penerimaan']}")
                    details = item.get('detail_redel', [])
                    if details:
                        st.markdown("**Detail Histori Redelivery:**")
                        for d in details:
                            st.caption(f"• Redel No: `{d['no_shipment_redel']}` | Jenis: {d['jenis_redel']} | Final: {'Ya' if d['is_final_delivery'] else 'Tidak'}")
                    else:
                        st.caption("Belum ada riwayat Redelivery.")
        else:
            st.info("Tidak ada data SKR ditemukan.")

    with tab2:
        data_redel = supabase.table("redelivery").select("*, detail_redel(*)").execute().data
        if data_redel:
            for redel in data_redel:
                details = redel.get('detail_redel', [])
                with st.expander(f"{redel['no_shipment_redel']} | Delman: {redel['nama_delman']} ({redel['nopol_kendaraan']}) | Tgl: {redel['tanggal_pengiriman']}"):
                    st.markdown("**Daftar SKR Yang Diangkut:**")
                    for d in details:
                        st.write(f"- **No. SKR:** `{d['no_shipment']}` | **Jenis:** {d['jenis_redel']} | **Flag Final:** {'Selesai' if d['is_final_delivery'] else 'Belum Habis'}")
        else:
            st.info("Belum ada data Redelivery.")

# ==========================================
# 8. HALAMAN 5: DATA PALET (REALTIME)
# ==========================================
elif st.session_state['active_nav'] == "Data Palet":
    st.subheader("Master Data Palet")
    if st.button("➕ BUAT PALET BARU", type="primary"):
        modal_tambah_palet()
        
    st.write("")
    palets = supabase.table("palet").select("*").order("nomor_palet").execute().data
    if palets:
        st.dataframe(pd.DataFrame(palets), use_container_width=True)
    else:
        st.info("Belum ada data palet di database.")

# ==========================================
# 9. HALAMAN 6: LAPORAN REKAP
# ==========================================
elif st.session_state['active_nav'] == "Laporan Rekap":
    st.subheader("Laporan Rekapitulasi Gudang")
    st.button("Export CSV Laporan Hari Ini", type="primary")