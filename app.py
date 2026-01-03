import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="Simulador: Oscilador Longitudinal")

# Forzar estilo oscuro en Matplotlib para que coincida con Python local
plt.style.use('dark_background')

# --- BARRA LATERAL (CONTROLES) ---
with st.sidebar:
    st.header("Controles del Sistema")
    m_v = st.slider('Masa m', 0.1, 5.0, 1.0, step=0.1)
    k1_v = st.slider('k1 (Izq)', 0.5, 30.0, 5.0, step=0.5)
    k2_v = st.slider('k2 (Der)', 0.5, 30.0, 5.0, step=0.5)
    t_sim = st.slider('Tiempo de Simulación (s)', 2.0, 20.0, 10.0)
    
    if st.button('RESTART SIMULATION'):
        st.rerun()

# --- PARÁMETROS FÍSICOS ---
L = 2.0
dt = 0.01
initial_x = 0.8
T_MAX = t_sim
w = np.sqrt((k1_v + k2_v) / m_v)

# --- NÚCLEO DE CÁLCULO (RK4) ---
def get_accel(p, k1, k2, m):
    return (-(k1 + k2) * p) / m

def simulate():
    t_vals = np.arange(0, T_MAX, dt)
    x_vals, v_vals, a_vals = [], [], []
    curr_x, curr_v = initial_x, 0.0
    
    for t in t_vals:
        x_vals.append(curr_x)
        v_vals.append(curr_v)
        a_vals.append(get_accel(curr_x, k1_v, k2_v, m_v))
        
        # RK4 Step
        k1_v_rk = get_accel(curr_x, k1_v, k2_v, m_v)
        k1_x_rk = curr_v
        k2_v_rk = get_accel(curr_x + 0.5*dt*k1_x_rk, k1_v, k2_v, m_v)
        k2_x_rk = curr_v + 0.5*dt*k1_v_rk
        k3_v_rk = get_accel(curr_x + 0.5*dt*k2_x_rk, k1_v, k2_v, m_v)
        k3_x_rk = curr_v + 0.5*dt*k2_v_rk
        k4_v_rk = get_accel(curr_x + dt*k3_x_rk, k1_v, k2_v, m_v)
        k4_x_rk = curr_v + dt*k3_v_rk
        
        curr_v += (dt/6)*(k1_v_rk + 2*k2_v_rk + 2*k3_v_rk + k4_v_rk)
        curr_x += (dt/6)*(k1_x_rk + 2*k2_x_rk + 2*k3_x_rk + k4_x_rk)
        
    return t_vals, x_vals, v_vals, a_vals

t_axis, h_x, h_v, h_a = simulate()

# --- GEOMETRÍA DEL RESORTE ---
def get_zigzag_spring(start, end, nodes=15, width=0.1):
    t = np.linspace(0, 1, nodes)
    start = np.array(start); end = np.array(end)
    direction = end - start
    dist = np.linalg.norm(direction)
    x = start[0] + t * direction[0]
    y = start[1] + t * direction[1]
    if dist > 0:
        perp = np.array([-direction[1], direction[0]]) / dist
    else:
        perp = np.array([0, 1])
    for i in range(1, nodes-1):
        offset = width if i % 2 == 0 else -width
        x[i] += perp[0] * offset
        y[i] += perp[1] * offset
    return x, y

# --- CONSTRUCCIÓN DE LA FIGURA (Misma Estética) ---
fig = plt.figure(figsize=(15, 10))
gs = fig.add_gridspec(6, 2, hspace=1.2, wspace=0.25, width_ratios=[1, 1])
fig.patch.set_facecolor('#0E1117') # Fondo exacto de Streamlit Dark

# Subplots de Gráficos
ax_p = fig.add_subplot(gs[0:2, 1])
ax_v = fig.add_subplot(gs[2:4, 1])
ax_a = fig.add_subplot(gs[4:6, 1])

# Simulación Física
ax_sim = fig.add_subplot(gs[0:3, 0])
ax_sim.set_xlim(-L-0.5, L+0.5); ax_sim.set_ylim(-1, 1); ax_sim.set_aspect('equal')
ax_sim.set_title("Oscilación Longitudinal", fontsize=12, fontweight='bold', pad=15)

# Dibujar estado final (Snapshot)
curr_x = h_x[-1]
zx1, zy1 = get_zigzag_spring([-L, 0], [curr_x, 0])
zx2, zy2 = get_zigzag_spring([L, 0], [curr_x, 0])
ax_sim.plot(zx1, zy1, 'silver', lw=2)
ax_sim.plot(zx2, zy2, 'silver', lw=2)
ax_sim.plot([curr_x], [0], 'cyan', marker='o', ms=20, markeredgecolor='white', zorder=5)
ax_sim.axvline(-L, color='gray', lw=8)
ax_sim.axvline(L, color='gray', lw=8)

# Box de Frecuencia
ax_sim.text(0.5, -0.32, f"FRECUENCIA PROPIA:\nω0 = {w:.3f} rad/s", 
            transform=ax_sim.transAxes, fontsize=10, color='cyan', 
            fontweight='bold', ha='center',
            bbox=dict(facecolor='#151515', alpha=0.9, edgecolor='gray', pad=8))

# Llenar Gráficos
axes = [ax_p, ax_v, ax_a]
data = [h_x, h_v, h_a]
titles = ["Posición (x) vs Tiempo", "Velocidad (v) vs Tiempo", "Aceleración (a) vs Tiempo"]
ylabels = ["x (m)", "v (m/s)", "a (m/s²)"]
colors = ['#00FF7F', '#FFD700', '#FF4500']

for i in range(3):
    axes[i].plot(t_axis, data[i], color=colors[i], lw=2)
    axes[i].set_title(titles[i], fontweight='bold', fontsize=10)
    axes[i].set_ylabel(ylabels[i], fontsize=9)
    axes[i].set_xlabel("t (s)", fontsize=9)
    axes[i].grid(color='gray', linestyle=':', alpha=0.3)

# --- RENDER EN STREAMLIT ---
st.pyplot(fig)


