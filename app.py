import streamlit as st
import segyio
import numpy as np
import matplotlib.pyplot as plt

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Visualisasi Seismik SEG-Y",
    layout="wide"
)

st.title("📊 Visualisasi Data Seismik SEG-Y")
st.markdown("Aplikasi sederhana untuk menampilkan penampang seismik post-stack")

# =========================
# SIDEBAR - PENGATURAN
# =========================
st.sidebar.header("⚙ Pengaturan Visualisasi")

# 1. Colormap
colormap = st.sidebar.selectbox(
    "Pilih Colormap",
    ["gray", "seismic", "viridis", "plasma"]
)

# 2. Balik sumbu waktu
invert_time = st.sidebar.checkbox("Balik Sumbu Waktu")

# 3. Mode skala amplitudo
scale_mode = st.sidebar.radio(
    "Mode Skala Amplitudo",
    ["Auto", "Manual"]
)

# 4. Slider vmin & vmax (dipakai kalau Manual)
vmin = st.sidebar.slider(
    "vmin (amplitudo minimum)",
    -5000, 5000, -1000
)

vmax = st.sidebar.slider(
    "vmax (amplitudo maksimum)",
    -5000, 5000, 1000
)
plot_type = st.sidebar.selectbox(
    "Tipe Plot",
    ["Image", "Wiggle"]
)
# =========================
# LOAD FILE SEG-Y
# =========================
file_segy = "Test_post stack small.sgy"

with segyio.open(file_segy, "r", ignore_geometry=True) as f:
    seismic_data = segyio.tools.collect(f.trace[:])

# 👉 AMBIL SATU PENAMPANG
seismic_section = seismic_data
if invert_time:
    seismic_section = np.flipud(seismic_section)
    
def wiggle_plot(ax, data, scale=1.0):
    n_traces, n_samples = data.shape
    t = np.arange(n_samples)

    for i in range(n_traces):
        trace = data[i] / np.max(np.abs(data[i]))
        ax.plot(i + trace * scale, t, color="black", linewidth=0.5)

    ax.invert_yaxis()
    ax.set_xlabel("Trace")
    ax.set_ylabel("Time Sample")

# =========================
# PLOT SEISMIK
# =========================
fig, ax = plt.subplots(figsize=(10, 6))

if plot_type == "Image":
    im = ax.imshow(
        seismic_section.T,
        cmap=colormap,
        aspect="auto"
    )
    plt.colorbar(im, ax=ax, label="Amplitude")
else:
    wiggle_plot(ax, seismic_section)

ax.set_title("Penampang Seismik")
st.pyplot(fig)