import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from rowEquation import RowEquation
import random
import stream_app.parts as parts
from streamlit_plotly_events import plotly_events


st.set_page_config(layout="wide",
    page_title="Rower-Boat-Water 1D System",
    page_icon="assets/icon.png",   # puede ser .png, .ico, .jpg
)
# --------------------------------------------------
# LAYOUT
# --------------------------------------------------
st.title("Sistema Físico Remero–Barco–Agua 1D  ")

col_graficas, col_form, col_digram = st.columns([3, 1,1])   # Graficas a la izquierda, formulario estrecho a la derecha

# --------------------------------------------------
# FORMULARIO
# --------------------------------------------------
with col_form:
    st.header("Parámetros")

    with st.form("formulario_parametros"):

        grado = st.number_input("grado del polinomio", value=4, step=1, min_value=3,)
        M = st.number_input("M", value=20.0)
        m = st.number_input("m", value=80)
        L = st.number_input("L", value=-1.0)
        T = st.number_input("T", value=2.0)
        rho = st.number_input("rho", value=1.2)
        S = st.number_input("S", value=0.3)
        Cd = st.number_input("Cd", value=0.8)
        y0_dot = st.number_input("y0_dot", value=0.0)

        recalcular = st.form_submit_button("Recalcular")
        # Elegir la gráfica X(t) interactiva
        grafica_interactiva = st.selectbox("Elige la gráfica interactiva X(t)", 
                                        ["x(t) — Rower Position", 
                                            "x'(t) — Rower Speed", 
                                            "x''(t) — Rower Acceleration"])

        # N_puntos = st.number_input("Número de puntos a seleccionar", min_value=1, value=3, step=1)
# --------------------------------------------------
# RESULTADOS Y GRÁFICAS A LA IZQUIERDA
# --------------------------------------------------
with col_graficas:

    if recalcular:
        modelo = RowEquation(m, M, L, T, rho, S, Cd)
        high_coeffs = [random.uniform(-3, 3) for _ in range(grado - 3)]
        modelo.y0_dot = y0_dot
        modelo.set_rower_cinematic(high_coeffs)
        solution = modelo.solve_edo()

        st.subheader("Gráficas de resultados")

        nombres = [
            "x(t) — Rower Position", "x'(t) — Rower Speed", "x''(t) — Rower Acceleration",
            "y(t) — Boat Position", "y'(t) — Boat Speed", "y''(t) — Boat Acceleration"
        ]
        resultados = [
            solution['xx'], solution['xx_dot'], solution['xx_ddot'],
            solution['yy'], solution['yy_dot'], solution['yy_ddot']]
        # Crear mosaico 2x3 en Plotly
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=nombres
        )

        # Añadir series a subplots
        row = 1
        col = 1
        for i in range(6):
            fig.add_trace(
                go.Scatter(
                    x=solution['tt'],
                    y=resultados[i],
                    mode='lines',
                    name=nombres[i],
                    line=dict(color='black')  # <-- línea negra
                ),
                row=row,
                col=col
            )

            col += 1
            if col == 4:  # pasar a nueva fila
                col = 1
                row += 1

        fig.update_layout(height=900, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

         # -----------------------------
        # Gráfica interactiva para click
        # -----------------------------
        fig_click = go.Figure()
        fig_click.add_trace(go.Scatter(x=[1,2,3], y=[1,4,7], mode='lines', name=grafica_interactiva))

        puntos_seleccionados = plotly_events(fig_click, click_event=True, select_event=False, key="fig_click")

        if puntos_seleccionados:
            print(puntos_seleccionados)

with col_digram:
    if recalcular:
        parts.animar_bola_1d(solution['xx'], T = modelo.T, L = modelo.L)
        st.text("Funcion de posición x(t) del remero:")
        latex_str = rf"x(t) = {' + '.join(
            f'{c:.2f}t^{{{i}}}' if i > 1 else (f'{c:.2f}t' if i == 1 else f'{c:.2f}')
            for i, c in enumerate(modelo.coeffs) if c != 0
        )}"

        st.latex(latex_str)

    st.image("assets/diagram.png"
    )
