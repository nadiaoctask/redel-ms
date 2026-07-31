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

st.markdown("""
<style>
    /* Background Utama */
    .stApp {
        background-color: #F2F5F8;
    }
    
    /* Custom Card Style untuk Dashboard */
    .kanban-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 15px 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        border: 1px solid #E2E8F0;
    }
    
    /* Tombol Utama Dark Azure */
    div.stButton > button[kind="primary"] {
        background-color: #0E4A6E !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# Session State untuk Navigasi Samping
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
# 3. SIDEBAR NAVBAR (NAVIGASI CUSTOM)
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/47/Wings_Logo.svg", width=120)
    st.markdown("### **Redelivery Management System**")
    st.caption("Supervisor Panel: **Suliadi**")
    st.divider()
    
    def menu_item(label, icon_name, nav_key):
        is_active = st.session_state['active_nav'] == nav_key
        btn_type = "primary" if is_active else "secondary"
        if st.button(f"{icon_name}  {label}", key=f"nav_{nav_key}", use_container_width=True, type=btn_type):
            st.session_state['active_nav'] = nav_key
            st.rerun()

    st.caption("MAIN MENU")
    menu_item("Dashboard", "🏠", "Dashboard")
    
    st.caption("FORMULIR")
    menu_item("Penerimaan SKR", "📥", "Penerimaan SKR")
    menu_item("Redelivery", "🚚", "Redelivery")
    
    st.caption("DATA")
    menu_item("Data SKR Redel", "📊", "Data SKR Redel")
    menu_item("Data Palet", "📦", "Data Palet")
    menu_item("Laporan Rekap", "📄", "Laporan Rekap")
    
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.info("Logout berhasil")

# ==========================================
# 4. HALAMAN 1: DASHBOARD UTAMA
# ==========================================
if st.session_state['active_nav'] == "Dashboard":
    # Header Atas
    c_h1, c_h2 = st.columns([4, 1])
    with c_h1:
        st.title("Redelivery Management System")
    with c_h2:
        st.markdown("<div style='text-align:right;'><b>Suliadi</b><br><span style='color:#666;'>Supervisor</span></div>", unsafe_allow_html=True)

    # Fetch Realtime Data untuk Metric Cards
    try:
        res_skr = supabase.table("skr_redel").select("status_skr").execute().data
        cnt_menunggu = sum(1 for item in res_skr if item['status_skr'] == 'Menunggu shipment baru')
        cnt_parsial = sum(1 for item in res_skr if item['status_skr'] == 'Parsial')
        cnt_selesai = sum(1 for item in res_skr if item['status_skr'] == 'Selesai')
    except:
        cnt_menunggu, cnt_parsial, cnt_selesai = 28, 10, 99

    # Metrics Card Layout (Dark Azure Theme)
    st.markdown("##### **Status SKR Redelivery**")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class="kanban-card" style="border-left: 6px solid #C0392B;">
                <p style="color:#64748B; font-weight:600; margin:0;">Menunggu Shipment Redelivery</p>
                <h1 style="color:#0E4A6E; margin:10px 0; font-size:42px;">{cnt_menunggu} <span style="font-size:16px; color:#94A3B8;">SKR</span></h1>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="kanban-card" style="border-left: 6px solid #F1C40F;">
                <p style="color:#64748B; font-weight:600; margin:0;">Redelivery Parsial</p>
                <h1 style="color:#0E4A6E; margin:10px 0; font-size:42px;">{cnt_parsial} <span style="font-size:16px; color:#94A3B8;">SKR</span></h1>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="kanban-card" style="border-left: 6px solid #27AE60;">
                <p style="color:#64748B; font-weight:600; margin:0;">Selesai Redelivery</p>
                <h1 style="color:#0E4A6E; margin:10px 0; font-size:42px;">{cnt_selesai} <span style="font-size:16px; color:#94A3B8;">SKR</span></h1>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # Cari Data Shipment Search Bar
    with st.container():
        col_s1, col_s2 = st.columns([5, 1])
        with col_s1:
            search_no_shipment = st.text_input("", placeholder="🔍  Masukkan Nomor Shipment...", label_visibility="collapsed")
        with col_s2:
            btn_cari = st.button("Cari", type="primary", use_container_width=True)

    if search_no_shipment or btn_cari:
        if search_no_shipment:
            res_search = supabase.table("skr_redel").select("*, penempatan(nomor_palet)").eq("no_shipment", search_no_shipment.strip()).execute().data
            if res_search:
                data_item = res_search[0]
                palet_list = [p['nomor_palet'] for p in data_item.get('penempatan', [])]
                palet_str = ", ".join(palet_list) if palet_list else "-"
                
                st.success(f"✅ Data Shipment Ditemukan: **{data_item['no_shipment']}**")
                c_a, c_b, c_c, c_d = st.columns(4)
                c_a.metric("Nama Delman", data_item['nama_delman'])
                c_b.metric("Nopol Kendaraan", data_item['nopol_kendaraan'])
                c_c.metric("Jenis GR", data_item['jenis_gr'])
                c_d.metric("Status SKR", data_item['status_skr'])
                st.info(f"📦 **Lokasi Penempatan Palet:** `{palet_str}`")
            else:
                st.warning(f"❌ Nomor Shipment '{search_no_shipment}' tidak ditemukan di database.")

    st.write("")
    
    # 2 Tombol Aksi Utama (Dark Azure Color #0E4A6E)
    cb1, cb2 = st.columns(2)
    with cb1:
        if st.button("📦   Penerimaan SKR", key="btn_main_in", use_container_width=True, type="primary"):
            st.session_state['active_nav'] = "Penerimaan SKR"
            st.rerun()
    with cb2:
        if st.button("🚚   Redelivery", key="btn_main_out", use_container_width=True, type="primary"):
            st.session_state['active_nav'] = "Redelivery"
            st.rerun()

    st.write("")
    st.button("📥   Download Laporan Rekapitulasi Hari Ini", use_container_width=True)

# ==========================================
# 5. HALAMAN 2: FORM PENERIMAAN SKR
# ==========================================
elif st.session_state['active_nav'] == "Penerimaan SKR":
    st.title("📥 Form Input Penerimaan SKR")
    
    # AMBIL DATA PALET REALTIME DARI DATABASE SUPABASE
    try:
        palet_db = supabase.table("palet").select("nomor_palet").execute().data
        list_palet_options = [p['nomor_palet'] for p in palet_db] if palet_db else []
    except Exception as e:
        list_palet_options = []
        st.error(f"Gagal memuat data palet: {e}")

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
                    # Insert data SKR
                    supabase.table("skr_redel").insert({
                        "no_shipment": no_shipment.strip(),
                        "nama_delman": nama_delman,
                        "nopol_kendaraan": nopol_kendaraan,
                        "jenis_gr": jenis_gr,
                        "tanggal_penerimaan": str(tanggal_penerimaan),
                        "status_skr": "Menunggu shipment baru"
                    }).execute()
                    
                    # Insert Penempatan Palet & Update Status Palet jadi In Use
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
# 6. HALAMAN 3: FORM REDELIVERY
# ==========================================
elif st.session_state['active_nav'] == "Redelivery":
    st.title("🚚 Form Redelivery (Pengeluaran Barang)")
    
    # Fetch SKR yang belum selesai
    try:
        skr_db = supabase.table("skr_redel").select("no_shipment").neq("status_skr", "Selesai").execute().data
        list_skr_options = [s['no_shipment'] for s in skr_db] if skr_db else []
    except Exception as e:
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
                # KONDISIONAL: Jika Full, checkbox hilang & otomatis True
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
                # Insert Redelivery Master
                supabase.table("redelivery").insert({
                    "no_shipment_redel": no_shipment_redel.strip(),
                    "nama_delman": nama_delman_redel,
                    "nopol_kendaraan": nopol_redel,
                    "tanggal_pengiriman": str(tgl_pengiriman)
                }).execute()
                
                # Insert Detail & Update Status SKR
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
# 7. HALAMAN 4: DATA SKR REDEL (MONITORING)
# ==========================================
elif st.session_state['active_nav'] == "Data SKR Redel":
    st.title("Data SKR Redelivery")
    tab1, tab2 = st.tabs(["📥 TAB 1: PENERIMAAN SKR (IN)", "📤 TAB 2: REDELIVERY / KIRIM ULANG (OUT)"])
    
    with tab1:
        c_f1, c_f2, c_f3 = st.columns([3, 2, 2])
        with c_f1:
            search_skr = st.text_input("🔍 CARI DATA", placeholder="Input No SKR / Nama Delman / ID Palet...")
        with c_f2:
            filter_gr = st.radio("📦 JENIS GR", ["Semua GR", "GR Sistem", "GR Turun Gudang"], horizontal=True)
        with c_f3:
            filter_status = st.selectbox("🟢 STATUS SKR", ["Semua Status", "Menunggu shipment baru", "Parsial", "Selesai"])

        # Fetch Data SKR Realtime
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
                
                with st.expander(f"▼ {item['no_shipment']} | GR: {item['jenis_gr']} | Palet: {palet_str} | Status: {item['status_skr']}"):
                    st.write(f"**Delman:** {item['nama_delman']} | **Nopol:** {item['nopol_kendaraan']} | **Tgl Masuk:** {item['tanggal_penerimaan']}")
                    details = item.get('detail_redel', [])
                    if details:
                        st.markdown("**🚚 Detail Histori Redelivery:**")
                        for d in details:
                            st.caption(f"• Redel No: `{d['no_shipment_redel']}` | Jenis: {d['jenis_redel']} | Final: {'✅ Ya' if d['is_final_delivery'] else '❌ Tidak'}")
                    else:
                        st.caption("Belum ada riwayat Redelivery.")
        else:
            st.info("Tidak ada data SKR ditemukan.")

    with tab2:
        search_redel = st.text_input("🔍 CARI REDEL", placeholder="Input No Redel Baru / Nama Driver / Nopol...")
        data_redel = supabase.table("redelivery").select("*, detail_redel(*)").execute().data
        
        if data_redel:
            for redel in data_redel:
                details = redel.get('detail_redel', [])
                with st.expander(f"▼ {redel['no_shipment_redel']} | Delman: {redel['nama_delman']} ({redel['nopol_kendaraan']}) | Tgl: {redel['tanggal_pengiriman']}"):
                    st.markdown("**📦 Daftar SKR Yang Diangkut:**")
                    for d in details:
                        st.write(f"- **No. SKR:** `{d['no_shipment']}` | **Jenis:** {d['jenis_redel']} | **Flag Final:** {'✅ Selesai' if d['is_final_delivery'] else '❌ Belum Habis'}")
        else:
            st.info("Belum ada data Redelivery.")

# ==========================================
# 8. HALAMAN 5: DATA PALET (FETCH REALTIME)
# ==========================================
elif st.session_state['active_nav'] == "Data Palet":
    st.title("📦 Master Data Palet")
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
    st.title("📄 Laporan Rekapitulasi Gudang")
    st.button("📥 Export CSV Laporan Hari Ini", type="primary")