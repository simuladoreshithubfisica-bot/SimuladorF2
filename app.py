import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la página (esto debe ir primero)
st.set_page_config(page_title="Simulador de Red de Reflexión", layout="centered")

st.title("🛡️ Red de Reflexión Tallada (Blazed Grating)")
st.markdown("""
Esta aplicación simula cómo el ángulo de las facetas de una red de reflexión permite concentrar la energía en un orden de difracción específico. 
""")

# 2. Parámetros en la barra lateral
st.sidebar.header("Configuración del Experimento")
phi_deg = st.sidebar.slider('Ángulo de Faceta (phi) [°]', 0.0, 30.0, 8.35)
wav = st.sidebar.slider('Longitud de onda (λ) [nm]', 400, 750, 600)
N = st.sidebar.number_input('Número de rendijas (N)', value=20, min_value=2)
d = 2000  # nm (Paso de la red fijo)

# 3. Lógica matemática
phi = np.radians(phi_deg)
theta = np.linspace(-np.radians(60), np.radians(60), 2000)

# Término de interferencia de la red
gamma = (np.pi * d * np.sin(theta)) / wav
with np.errstate(divide='ignore', invalid='ignore'):
    interf = (np.sin(N * gamma) / np.sin(gamma))**2
    interf /= N**2
    interf = np.nan_to_num(interf, nan=1.0) # Manejo de indeterminaciones en el centro

# Envolvente de difracción de la faceta (Blazing)
beta = (np.pi * d * np.cos(phi) * np.sin(theta - 2*phi)) / wav
env = (np.sinc(beta/np.pi))**2

I_total = interf * env

# 4. Creación de los gráficos con Matplotlib
plt.style.use('dark_background')
fig, (ax_geom, ax_plot) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [1, 2]})
plt.subplots_adjust(hspace=0.4)

# Esquema Geométrico
for i in range(5):
    x_base = i * d
    ax_geom.plot([x_base, x_base + d*np.cos(phi)**2], [0, d*np.sin(phi)*np.cos(phi)], 'cyan', lw=2)
ax_geom.set_title(f"Geometría de las Facetas (Phi: {phi_deg}°) ", color='cyan')
ax_geom.axis('off')

# Gráfico de Intensidad
ax_plot.plot(np.degrees(theta), I_total, color='white', lw=1.5, label='Intensidad Total')
ax_plot.plot(np.degrees(theta), env, 'r--', alpha=0.5, label='Envolvente (Blazing)')
ax_plot.fill_between(np.degrees(theta), I_total, color='cyan', alpha=0.2)
ax_plot.set_xlim(-60, 60)
ax_plot.set_ylim(0, 1.1)
ax_plot.set_title("Patrón de Difracción Intensificado", color='white')
ax_plot.set_xlabel("Ángulo de Emergencia (°)")
ax_plot.set_ylabel("I / I_max")
ax_plot.legend()
ax_plot.grid(alpha=0.1)

# 5. Renderizado en Streamlit
st.pyplot(fig)

# Información adicional opcional
st.info(f"💡 El máximo de la envolvente se encuentra en el ángulo de reflexión especular: {2*phi_deg:.2f}°")