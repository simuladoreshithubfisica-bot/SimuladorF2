import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Laboratorio Virtual de Física II", layout="wide")

# Título y Menú Lateral
st.sidebar.title("🛠️ Configuración del Laboratorio")
simulador_principal = st.sidebar.selectbox(
    "Selecciona el Experimento",
    ["Red de Reflexión Tallada", "Modos Normales: Osciladores Acoplados", "Modos Normales: Cuerdas Vibrantes"]
)

# --- 1. SIMULADOR: RED DE REFLEXIÓN (Tu código original) ---
if simulador_principal == "Red de Reflexión Tallada":
    st.title("🛡️ Red de Reflexión Tallada (Blazed Grating)")
    # (Aquí va el código que ya tienes funcionando para la red)
    st.info("Este es el simulador que ya tenías configurado.")

# --- 2. SIMULADOR: OSCILADORES ACOPLADOS (Mejorado con Sliders) ---
elif simulador_principal == "Modos Normales: Osciladores Acoplados":
    st.title("🧶 Modos Normales en Osciladores Acoplados")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Parámetros")
        n_masas = st.selectbox("Escenario (Número de masas)", [2, 3], index=0)
        k = st.slider("Constante elástica k (N/m)", 1, 100, 20)
        m = st.slider("Masa m (kg)", 0.1, 5.0, 1.0)
        modo = st.radio("Seleccionar Modo", [f"Modo {i+1}" for i in range(n_masas)])

    with col2:
        t = np.linspace(0, 10, 500)
        # Lógica simplificada para 2 masas
        if n_masas == 2:
            w = np.sqrt(k/m) if modo == "Modo 1" else np.sqrt(3*k/m)
            x1 = np.cos(w * t)
            x2 = np.cos(w * t) if modo == "Modo 1" else -np.cos(w * t)
            
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(t, x1, label="Masa 1")
            ax.plot(t, x2, label="Masa 2", linestyle="--")
            ax.set_title(f"Oscilación en {modo} (ω = {w:.2f} rad/s)")
            ax.legend()
            st.pyplot(fig)

# --- 3. SIMULADOR: CUERDAS VIBRANTES (Mejorado con Selectores) ---
elif simulador_principal == "Modos Normales: Cuerdas Vibrantes":
    st.title("🎻 Modos Normales en Cuerdas (Continuo)")
    
    st.sidebar.subheader("Ajustes de la Cuerda")
    L = st.sidebar.slider("Longitud L (m)", 0.5, 5.0, 1.0)
    tension = st.sidebar.slider("Tensión T (N)", 10, 500, 100)
    mu = st.sidebar.slider("Densidad lineal μ (kg/m)", 0.01, 0.5, 0.1)
    n_armonico = st.sidebar.number_input("Número de Armónico (n)", 1, 10, 1)

    v = np.sqrt(tension / mu)
    frecuencia = (n_armonico * v) / (2 * L)
    
    x = np.linspace(0, L, 1000)
    y = np.sin(n_armonico * np.pi * x / L)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, y, color="cyan", lw=2)
    ax.fill_between(x, y, -y, alpha=0.1, color="cyan")
    ax.set_title(f"Armónico n={n_armonico} - Frecuencia: {frecuencia:.2f} Hz")
    ax.set_xlim(0, L)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig)
    
    st.latex(r"f_n = \frac{n}{2L} \sqrt{\frac{T}{\mu}}")
