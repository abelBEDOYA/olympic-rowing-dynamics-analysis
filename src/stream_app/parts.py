import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

def animar_bola_1d(x_positions, L, T):
    x_positions = x_positions[::20]  # reducir cantidad de frames para mejor rendimiento
    N = len(x_positions)
    dt = T / N   # tiempo entre frames en segundos

    # Figura base
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[x_positions[0]], y=[0], mode="markers", marker=dict(size=20), name="Bola"))
    fig.add_trace(go.Scatter(x=[0, L], y=[0, 0], mode="markers", marker=dict(size=12, color="green"), name="Ref"))

    fig.update_layout(
        xaxis=dict(range=[np.min(x_positions), np.max(x_positions)]),
        yaxis=dict(range=[-1, 1]),
    )

    # Contenedor único con key
    container = st.empty()
    container.plotly_chart(fig, use_container_width=True, key="anim_bola")  # key solo aquí

    # Animación en tiempo real
    for x in x_positions:
        fig.data[0].x = [x]   # actualizar la posición
        container.plotly_chart(fig, use_container_width=True)  # actualizar contenido del mismo contenedor
        time.sleep(dt)
