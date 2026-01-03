import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Laboratorio de Física II", layout="wide")

# MENU LATERAL
st.sidebar.title("Menú de Experimentos")
modo_seleccionado = st.sidebar.selectbox("Seleccione el Simulador", 
                                        ["2 Masas Acopladas", "Red de Difracción"])

# --- EXPERIMENTO 1: 2 MASAS ACOPLADAS (ANIMADO) ---
if modo_seleccionado == "2 Masas Acopladas":
    st.title("🧶 Modos Normales: 2 Masas Acopladas")
    
    # Parámetros Interactivos
    col_param, col_graf = st.columns([1, 2])
    
    with col_param:
        st.subheader("Configuración")
        k = st.slider("Constante elástica k (N/m)", 1, 100, 20)
        m = st.slider("Masa m (kg)", 0.5, 5.0, 1.0)
        tipo_modo = st.radio("Modo de Oscilación", ["Simétrico (Modo 1)", "Antisimétrico (Modo 2)"])
        animar = st.checkbox("▶️ Iniciar Animación", value=True)

    with col_graf:
        # Frecuencias naturales
        w1 = np.sqrt(k / m)
        w2 = np.sqrt(3 * k / m)
        w = w1 if "Simétrico" in tipo_modo else w2
        
        st.latex(r"\omega = " + f"{w:.2f} " + r"\text{ rad/s}")
        
        # Placeholder para la animación
        plot_spot = st.empty()

        # Bucle de Animación
        t = 0
        while animar:
            # Calculamos posiciones de las masas
            # x = A * cos(w*t)
            pos1 = np.cos(w * t)
            pos2 = np.cos(w * t) if "Simétrico" in tipo_modo else -np.cos(w * t)
            
            # Crear la figura (estilo dibujo técnico)
            fig, ax = plt.subplots(figsize=(8, 3))
            
            # Dibujar "Paredes"
            ax.axvline(-2, color="black", lw=3)
            ax.axvline(2, color="black", lw=3)
            
            # Dibujar Masas (como círculos)
            ax.plot(pos1 - 0.7, 0, 'ro', markersize=20, label="Masa 1")
            ax.plot(pos2 + 0.7, 0, 'bo', markersize=20, label="Masa 2")
            
            # Dibujar "Resortes" (líneas simples que se estiran)
            ax.plot([-2, pos1 - 0.7], [0, 0], 'k-', lw=1, alpha=0.5) # Resorte 1
            ax.plot([pos1 - 0.7, pos2 + 0.7], [0, 0], 'k-', lw=1, alpha=0.5) # Resorte 2
            ax.plot([pos2 + 0.7, 2], [0, 0], 'k-', lw=1, alpha=0.5) # Resorte 3
            
            ax.set_xlim(-2.5, 2.5)
            ax.set_ylim(-1, 1)
            ax.get_yaxis().set_visible(False)
            ax.set_title(f"Tiempo: {t:.1f}s")
            
            plot_spot.pyplot(fig)
            plt.close(fig)
            
            t += 0.1
            time.sleep(0.05) # Controla la fluidez

# --- EXPERIMENTO 2: RED DE DIFRACCIÓN (Tu código original) ---
elif modo_seleccionado == "Red de Difracción":
    st.title("🛡️ Red de Difracción")
    # Pega aquí el código que ya te funcionaba de la Red
    st.write("Aquí se mostrará tu simulador de Red de Difracción.")

