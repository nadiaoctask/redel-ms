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

# Inject Custom CSS (Sesuai Color Palette UI Gambar Canva)
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background-color: #F2F5F8;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Custom Card Style */
    .metric-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.04);
        border-left: 6px solid #114B73;
        margin-bottom: 10px;
    }
    
    /* Custom Big Action Buttons */
    .action-button-main {
        background-color: #114B73;
        color: white;
        padding: 30px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        font-size: 22px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        cursor: pointer;
    }
    
    /* Status Badge Styling */
    .badge-menunggu {
        background-color: #FFECEB;
        color: #D9381E;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
    .badge-parsial {
        background-color: #FFF8E6;
        color: #D99B00;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
    .badge-selesai {
        background-color: #E6F6EC;
        color: #00875A;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. POP-UP MODAL: TAMBAH PALET BARU (NO REDIRECT)
# ==========================================
@st.dialog("➕ Buat Palet Baru")
def modal_tambah_palet():
    st.write("Sistem akan menambahkan data master Palet baru:")
    
    col_a, col_b = st.columns(2)
    with col_a:
        nomor_palet_input = st.text_input("Nomor Palet Baru", placeholder="Contoh: 17 atau TURUN-01")
    with col_b:
        jenis_palet_input = st.selectbox("Jenis Palet", ["Bin", "Turun palet"])
        
    st.write("")
    if st.button("💾 Simpan Palet Baru", type="primary", use_container_width=True):
        if not nomor_palet_input:
            st.error("Nomor palet wajib diisi!")
        else:
            try:
                supabase.table("palet").insert({
                    "nomor_palet": nomor_palet_input,
                    "jenis_palet": jenis_palet_input,
                    "status_palet": "Available"
                }).execute()
                st.toast(f"Palet {nomor_palet_input} berhasil ditambahkan!", icon="✅")
                st.rerun()
            except Exception as e:
                st.error(f"Gagal menyimpan: {e}")

# ==========================================
# 3. SIDEBAR NAVIGATION (LOGIKA NAVBAR UI)
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/47/Wings_Logo.svg", width=120)
    st.markdown("### **Redelivery Management System**")
    st.caption("Supervisor Panel: **Suliadi**")
    st.divider()
    
    menu = st.radio(
        "NAVIGASI UTAMA",
        [
            "🏠 Dashboard",
            "📥 Penerimaan SKR",
            "🚚 Redelivery",
            "📊 Data SKR Redel",
            "📦 Data Palet",
            "📄 Laporan Rekap"
        ],
        index=0
    )
    
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.info("Logout berhasil")

# ==========================================
# 4. HALAMAN 1: DASHBOARD UTAMA
# ==========================================
if menu == "🏠 Dashboard":
    st.title("Redelivery Management System")
    st.caption("Selamat Datang, Suliadi (Supervisor)")
    st.write("")
    
    # --- FETCH RINGKASAN METRIK ---
    try:
        res_skr = supabase.table("skr_redel").select("status_skr").execute().data
        cnt_menunggu = sum(1 for item in res_skr if item['status_skr'] == 'Menunggu shipment baru')
        cnt_parsial = sum(1 for item in res_skr if item['status_skr'] == 'Parsial')
        cnt_selesai = sum(1 for item in res_skr if item['status_skr'] == 'Selesai')
    except:
        cnt_menunggu, cnt_parsial, cnt_selesai = 0, 0, 0

    # --- METRIC CARDS (SESUAI GAMBAR CANVA) ---
    st.subheader("Status SKR Redelivery")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #D9381E;">
            <p style="color:#666; font-size:14px; margin:0;">Menunggu Shipment Redelivery</p>
            <h1 style="color:#114B73; margin:10px 0;">{cnt_menunggu} <span style="font-size:16px; color:#888;">SKR</span></h1>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #D99B00;">
            <p style="color:#666; font-size:14px; margin:0;">Redelivery Parsial</p>
            <h1 style="color:#114B73; margin:10px 0;">{cnt_parsial} <span style="font-size:16px; color:#888;">SKR</span></h1>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #00875A;">
            <p style="color:#666; font-size:14px; margin:0;">Selesai Redelivery</p>
            <h1 style="color:#114B73; margin:10px 0;">{cnt_selesai} <span style="font-size:16px; color:#888;">SKR</span></h1>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # --- CARI SHIPMENT SEARCH BAR (SESUAI GAMBAR CANVA) ---
    st.markdown("### 🔍 Cari Data Shipment")
    col_s1, col_s2 = st.columns([5, 1])
    with col_s1:
        search_no_shipment = st.text_input("", placeholder="Masukkan Nomor Shipment...", label_visibility="collapsed")
    with col_s2:
        btn_cari = st.button("Cari", type="primary", use_container_width=True)

    # AKSI CARI SHIPMENT: Tampilkan data jika ditekan
    if search_no_shipment or btn_cari:
        if search_no_shipment:
            res_search = supabase.table("skr_redel").select("*, penempatan(nomor_palet)").eq("no_shipment", search_no_shipment.strip()).execute().data
            if res_search:
                data_item = res_search[0]
                palet_list = [p['nomor_palet'] for p in data_item.get('penempatan', [])]
                palet_str = ", ".join(palet_list) if palet_list else "-"
                
                st.success(f"✅ Data Shipment ditemukan untuk No: **{data_item['no_shipment']}**")
                
                c_a, c_b, c_c, c_d = st.columns(4)
                c_a.metric("Nama Delman", data_item['nama_delman'])
                c_b.metric("Nopol Kendaraan", data_item['nopol_kendaraan'])
                c_c.metric("Jenis GR", data_item['jenis_gr'])
                c_d.metric("Status SKR", data_item['status_skr'])
                
                st.info(f"📦 **Lokasi Penempatan Palet:** {palet_str}")
            else:
                st.warning(f"❌ Nomor Shipment '{search_no_shipment}' tidak ditemukan di database.")

    st.divider()

    # --- BUTTON TOMBOL BESAR DASHBOARD ---
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("📦 Penerimaan SKR", use_container_width=True, type="primary"):
            st.session_state['menu_target'] = "📥 Penerimaan SKR"
            st.info("Buka menu 'Penerimaan SKR' di navigasi samping.")
            
    with col_btn2:
        if st.button("🚛 Redelivery", use_container_width=True, type="primary"):
            st.session_state['menu_target'] = "🚚 Redelivery"
            st.info("Buka menu 'Redelivery' di navigasi samping.")

    st.write("")
    st.button("📥 Download Laporan Rekapitulasi Hari Ini", use_container_width=True)

# ==========================================
# 5. HALAMAN 2: FORM PENERIMAAN SKR
# ==========================================
elif menu == "📥 Penerimaan SKR":
    st.title("📥 Form Input Penerimaan SKR")
    st.caption("Masukkan Data Penerimaan SKR Baru & Plotting Ke Palet")
    
    # Ambil data palet yang ada
    palet_data = supabase.table("palet").select("nomor_palet, jenis_palet").execute().data
    list_palet_options = [p['nomor_palet'] for p in palet_data] if palet_data else []

    with st.container(border=True):
        st.subheader("Masukkan Data Shipment (1 Card)")
        
        c1, c2 = st.columns(2)
        with c1:
            no_shipment = st.text_input("No. Shipment *", placeholder="Masukkan Nomor Shipment")
            nama_delman = st.text_input("Nama Delman", placeholder="Nama Driver / Sopir")
            nopol_kendaraan = st.text_input("Nopol Kendaraan", placeholder="B 1234 XYZ")
        
        with c2:
            jenis_gr = st.radio("Jenis GR", ["Sistem", "Turun gudang"], horizontal=True)
            tanggal_penerimaan = st.date_input("Tanggal Penerimaan", value=date.today(), disabled=True)
            
            col_p1, col_p2 = st.columns([3, 2])
            with col_p1:
                selected_palet = st.selectbox("Pilih Palet", options=list_palet_options if list_palet_options else ["Belum ada palet"])
            with col_p2:
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
                    # 1. Insert SKR
                    supabase.table("skr_redel").insert({
                        "no_shipment": no_shipment.strip(),
                        "nama_delman": nama_delman,
                        "nopol_kendaraan": nopol_kendaraan,
                        "jenis_gr": jenis_gr,
                        "tanggal_penerimaan": str(tanggal_penerimaan),
                        "status_skr": "Menunggu shipment baru"
                    }).execute()
                    
                    # 2. Insert Penempatan Palet
                    if selected_palet and selected_palet != "Belum ada palet":
                        supabase.table("penempatan").insert({
                            "nomor_palet": selected_palet,
                            "no_shipment": no_shipment.strip()
                        }).execute()
                        
                        # Set status palet jadi 'In Use'
                        supabase.table("palet").update({"status_palet": "In Use"}).eq("nomor_palet", selected_palet).execute()

                    st.success(f"✅ Data Penerimaan SKR {no_shipment} Berhasil Disimpan!")
                except Exception as e:
                    st.error(f"Gagal menyimpan data: {e}")

# ==========================================
# 6. HALAMAN 3: FORM REDELIVERY
# ==========================================
elif menu == "🚚 Redelivery":
    st.title("🚚 Form Redelivery (Pengeluaran Barang)")
    st.caption("Input Pengiriman Ulang (Redelivery) untuk SKR yang ada di Gudang")

    # Ambil SKR yang bisa di-redel (yang durasi statusnya bukan 'Selesai')
    skr_available = supabase.table("skr_redel").select("no_shipment").neq("status_skr", "Selesai").execute().data
    list_skr_options = [s['no_shipment'] for s in skr_available] if skr_available else []

    with st.container(border=True):
        st.subheader("Masukkan Data Redelivery")
        rc1, rc2 = st.columns(2)
        with rc1:
            no_shipment_redel = st.text_input("No. Shipment Baru *", placeholder="Input Nomor Redelivery Baru")
            nama_delman_redel = st.text_input("Nama Delman", placeholder="Nama Driver Redel")
        with rc2:
            nopol_redel = st.text_input("Nopol Kendaraan", placeholder="B 9999 RED")
            tgl_pengiriman = st.date_input("Tanggal Pengiriman", value=date.today(), disabled=True)

    st.write("")
    
    with st.container(border=True):
        st.subheader("Masukkan Data SKR yang Diangkut")
        
        # State Manajemen Baris SKR Dinamis
        if 'redel_items_count' not in st.session_state:
            st.session_state['redel_items_count'] = 1

        items_to_save = []

        for i in range(st.session_state['redel_items_count']):
            st.markdown(f"**Item SKR #{i+1}**")
            col_i1, col_i2, col_i3, col_i4 = st.columns([3, 2, 2, 1])
            
            with col_i1:
                skr_selected = st.selectbox(f"No. SKR", options=list_skr_options, key=f"skr_select_{i}")
            with col_i2:
                jenis_redel = st.radio(f"Jenis Redel", ["Parsial", "Full"], key=f"jenis_redel_{i}", horizontal=True)
            with col_i3:
                # LOGIKA: Kalau pilih Full, checkbox 'Kiriman Terakhir' hilang/otomatis True
                if jenis_redel == "Parsial":
                    is_final = st.checkbox("Kiriman Terakhir? (Selesai)", key=f"final_{i}")
                else:
                    is_final = True
                    st.info("✓ Otomatis Selesai (Full)")
            with col_i4:
                st.write("")
                st.write("")
                if i > 0: # Button Hapus Baris
                    if st.button("🗑️", key=f"del_item_{i}"):
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
                # 1. Insert Master Redelivery
                supabase.table("redelivery").insert({
                    "no_shipment_redel": no_shipment_redel.strip(),
                    "nama_delman": nama_delman_redel,
                    "nopol_kendaraan": nopol_redel,
                    "tanggal_pengiriman": str(tgl_pengiriman)
                }).execute()
                
                # 2. Insert Detail Redelivery & Update Status SKR
                for item in items_to_save:
                    if item["no_shipment"]:
                        supabase.table("detail_redel").insert({
                            "no_shipment_redel": no_shipment_redel.strip(),
                            "no_shipment": item["no_shipment"],
                            "jenis_redel": item["jenis_redel"],
                            "is_final_delivery": item["is_final_delivery"]
                        }).execute()
                        
                        # Update status SKR
                        new_status = "Selesai" if item["is_final_delivery"] else "Parsial"
                        supabase.table("skr_redel").update({"status_skr": new_status}).eq("no_shipment", item["no_shipment"]).execute()

                st.success(f"✅ Data Redelivery {no_shipment_redel} Berhasil Disimpan!")
            except Exception as e:
                st.error(f"Gagal menyimpan data Redelivery: {e}")

# ==========================================
# 7. HALAMAN 4: MONITORING (DATA SKR REDEL)
# ==========================================
elif menu == "📊 Data SKR Redel":
    st.title("Data SKR Redelivery")
    
    tab1, tab2 = st.tabs(["📥 TAB 1: PENERIMAAN SKR (IN)", "📤 TAB 2: REDELIVERY / KIRIM ULANG (OUT)"])
    
    # ---------------- TAB 1: PENERIMAAN SKR ----------------
    with tab1:
        c_f1, c_f2, c_f3 = st.columns([3, 2, 2])
        with c_f1:
            search_skr = st.text_input("🔍 CARI DATA", placeholder="Input No SKR / Nama Delman / ID Palet...")
        with c_f2:
            filter_gr = st.radio("📦 JENIS GR", ["Semua GR", "GR Sistem", "GR Turun Gudang"], horizontal=True)
        with c_f3:
            filter_status = st.selectbox("🟢 STATUS SKR", ["Semua Status", "Menunggu shipment baru", "Parsial", "Selesai"])

        # Fetch Data SKR & Penempatan
        data_skr = supabase.table("skr_redel").select("*, penempatan(nomor_palet), detail_redel(*)").execute().data
        
        # Apply Filters
        if data_skr:
            filtered_skr = data_skr
            if search_skr:
                filtered_skr = [s for s in filtered_skr if search_skr.lower() in s['no_shipment'].lower() or search_skr.lower() in (s['nama_delman'] or '').lower()]
            if filter_gr != "Semua GR":
                gr_val = "Sistem" if filter_gr == "GR Sistem" else "Turun gudang"
                filtered_skr = [s for s in filtered_skr if s['jenis_gr'] == gr_val]
            if filter_status != "Semua Status":
                filtered_skr = [s for s in filtered_skr if s['status_skr'] == filter_status]

            # Render Table
            for item in filtered_skr:
                palet_list = [p['nomor_palet'] for p in item.get('penempatan', [])]
                palet_str = ", ".join(palet_list) if palet_list else "-"
                
                # Expandable Row untuk Histori Redel
                with st.expander(f"▶ {item['no_shipment']} | GR: {item['jenis_gr']} | Palet: {palet_str} | Status: {item['status_skr']}"):
                    col_det1, col_det2 = st.columns([3, 1])
                    with col_det1:
                        st.write(f"**Nama Delman:** {item['nama_delman']} | **Nopol:** {item['nopol_kendaraan']}")
                        st.write(f"**Tanggal Masuk:** {item['tanggal_penerimaan']}")
                        
                        # Detail Histori Redel
                        details = item.get('detail_redel', [])
                        if details:
                            st.markdown("**🚚 Detail Histori Redelivery:**")
                            for d in details:
                                st.caption(f"• Redel No: `{d['no_shipment_redel']}` | Jenis: {d['jenis_redel']} | Final: {'✅ Ya' if d['is_final_delivery'] else '❌ Tidak'}")
                        else:
                            st.caption("Belum ada riwayat Redelivery.")
                            
                    with col_det2:
                        if st.button("✏️ Edit", key=f"edit_skr_{item['no_shipment']}"):
                            st.info("Fitur Edit Modal")
                        
                        # Kunci tombol hapus jika status Selesai/Parsial
                        if item['status_skr'] == 'Menunggu shipment baru':
                            if st.button("🗑️ Hapus", key=f"del_skr_{item['no_shipment']}"):
                                supabase.table("skr_redel").delete().eq("no_shipment", item['no_shipment']).execute()
                                st.success("Data berhasil dihapus!")
                                st.rerun()
                        else:
                            st.button("🔒 Terkunci", disabled=True, key=f"lock_skr_{item['no_shipment']}")
        else:
            st.info("Tidak ada data SKR ditemukan.")

    # ---------------- TAB 2: REDELIVERY ----------------
    with tab2:
        rc_f1, rc_f2 = st.columns([3, 2])
        with rc_f1:
            search_redel = st.text_input("🔍 CARI REDEL", placeholder="Input No Redel Baru / Nama Driver / Nopol...")
        with rc_f2:
            st.write("📅 TANGGAL KIRIM")
            st.date_input("Filter Tanggal", value=(date.today(), date.today()), label_visibility="collapsed")

        # Fetch Data Redelivery
        data_redel = supabase.table("redelivery").select("*, detail_redel(*)").execute().data
        
        if data_redel:
            for redel in data_redel:
                details = redel.get('detail_redel', [])
                total_skr = len(details)
                
                with st.expander(f"▼ {redel['no_shipment_redel']} | Delman: {redel['nama_delman']} ({redel['nopol_kendaraan']}) | Tgl: {redel['tanggal_pengiriman']} | Total: {total_skr} SKR"):
                    st.markdown("**📦 Daftar SKR Yang Diangkut pada Surat Jalan Ini:**")
                    for d in details:
                        st.write(f"- **No. SKR:** `{d['no_shipment']}` | **Jenis:** {d['jenis_redel']} | **Flag Final:** {'✅ Selesai' if d['is_final_delivery'] else '❌ Belum Habis'}")
                    
                    st.divider()
                    col_ra1, col_ra2 = st.columns([1, 1])
                    with col_ra1:
                        if st.button("✏️ Edit Redel", key=f"edit_redel_{redel['no_shipment_redel']}"):
                            st.info("Edit Redelivery Modal")
                    with col_ra2:
                        if st.button("🗑️ Hapus Redel", key=f"del_redel_{redel['no_shipment_redel']}"):
                            supabase.table("redelivery").delete().eq("no_shipment_redel", redel['no_shipment_redel']).execute()
                            st.success("Redelivery dihapus")
                            st.rerun()
        else:
            st.info("Belum ada data Redelivery.")

# ==========================================
# 8. HALAMAN SISA (DATA PALET & LAPORAN)
# ==========================================
elif menu == "📦 Data Palet":
    st.title("📦 Master Data Palet")
    if st.button("➕ BUAT PALET BARU"):
        modal_tambah_palet()
    
    palets = supabase.table("palet").select("*").execute().data
    if palets:
        st.dataframe(pd.DataFrame(palets), use_container_width=True)

elif menu == "📄 Laporan Rekap":
    st.title("📄 Laporan Rekapitulasi Gudang")
    st.button("📥 Export CSV / Excel Laporan Hari Ini", type="primary")