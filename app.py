import pandas as pd
import scipy.stats
import streamlit as st
import time

# Variables que se conservan entre ejecuciones
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'iteraciones', 'media']
    )

# Título de la aplicación
st.header('Lanzar una moneda')

# Crear gráfico inicial con línea base en 0.5
chart = st.line_chart([0.5])

# Función que simula lanzar una moneda n veces
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1

        if r == 1:
            outcome_1_count += 1

        mean = outcome_1_count / outcome_no

        # Agregar punto al gráfico
        chart.add_rows([mean])

        # Pausa para ver la animación
        time.sleep(0.05)

    return mean

# Slider para elegir número de intentos
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)

# Botón para iniciar el experimento
start_button = st.button('Ejecutar')

# Si se presiona el botón
if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')

    # Incrementar número de experimento
    st.session_state['experiment_no'] += 1

    # Ejecutar simulación
    mean = toss_coin(number_of_trials)

    # Guardar resultado en la tabla
    st.session_state['df_experiment_results'] = pd.concat(
        [
            st.session_state['df_experiment_results'],
            pd.DataFrame(
                data=[[
                    st.session_state['experiment_no'],
                    number_of_trials,
                    mean
                ]],
                columns=['no', 'iteraciones', 'media']
            )
        ],
        axis=0
    )

    # Reiniciar índices
    st.session_state['df_experiment_results'] = (
        st.session_state['df_experiment_results']
        .reset_index(drop=True)
    )

# Mostrar tabla de resultados
st.write(st.session_state['df_experiment_results'])