import streamlit as st
import pandas as pd
import altair as alt
from funciones import dni_exists,password_exists,consultar_estudios,consultar_estudios_fecha

st.set_page_config(
    page_title="BloodHound: Track your Blood",
    page_icon=":🩸:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14 = st.columns(14)
with col1:
    if st.button("🡄"):
        st.switch_page("pages/2_Cargar_Estudio.py")

with col14:
    if st.button("Inicio"):
        st.switch_page("Inicio.py")

st.title('Visualización de Estudios')
if 'estado' not in st.session_state:
    st.session_state['estado']= 'No Autorizado'

st.write("Iniciar Sesion:")
dni = st.text_input("DNI", value = '', placeholder="xxxxxxxx")
if not dni_exists(dni):
    st.session_state['estado'] = 'No Autorizado'
password = st.text_input("Contraseña", value = '', type="password")
if not password_exists(password):
    st.session_state['estado'] = 'No Autorizado'

if st.button("Iniciar Sesión"):
    if dni_exists(dni) and password_exists(password):
        st.success("Inicio de sesión exitoso")
        st.session_state['estado'] = 'Autorizado'
    else:
        st.error("Usuario o contraseña incorrectos")
if st.session_state['estado'] == 'Autorizado':
    data = consultar_estudios(dni)
    if not data.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Estudios anteriores')
            data['fecha'] = pd.to_datetime(data['fecha'])
            data = data.sort_values(by='fecha')
            options = list(data['fecha'].dt.strftime('%Y-%m-%d'))
            option = st.selectbox("*Seleccione la fecha del estudio*", options)
            selected_date = pd.to_datetime(option)
            filtered_data = consultar_estudios_fecha(dni, selected_date)
                # Definir la función para verificar si el valor está dentro del rango del 10% alrededor del valor ideal
            def check_range(value_real, value_ideal):
                if pd.isna(value_ideal) or pd.isna(value_real):
                    return False
                try:
                    min_val = value_ideal * 0.9
                    max_val = value_ideal * 1.1
                    return min_val <= value_real <= max_val
                except:
                    return False

            # Función para aplicar el estilo condicional
            def highlight_valor_real(row):
                val_real = row['valor_real']
                val_ideal = row['valor_ideal']
                if pd.isna(val_real) or pd.isna(val_ideal):
                    return ['' for col in row.index]
                
                try:
                    min_val = val_ideal * 0.9
                    max_val = val_ideal * 1.1
                    
                    if min_val <= val_real <= max_val:
                        # Calculate the percentage difference within the range (0 to 1)
                        percentage_diff = (val_real - min_val) / (max_val - min_val)
                        # Convert the percentage difference into a green shade (from light green to dark green)
                        green_intensity = int(200 * (1 - percentage_diff)) + 55  # softer green
                        alpha = 0.5 + 0.5 * percentage_diff  # adjust transparency
                        color = f'background-color: rgba(0, {green_intensity}, 0, {alpha})'
                        return [color if col == 'valor_real' else '' for col in row.index]
                    else:
                        # Calculate the percentage difference from the nearest bound (min_val or max_val)
                        if val_real < min_val:
                            percentage_diff = (min_val - val_real) / val_ideal
                        else:
                            percentage_diff = (val_real - max_val) / val_ideal
                        
                        # Cap the percentage_diff at 1 (100%) for the gradient calculation
                        percentage_diff = min(percentage_diff, 1.0)
                        
                        # Convert the percentage difference into a red shade (from light red to dark red)
                        red_intensity = int(200 * percentage_diff) + 55  # softer red
                        alpha = 0.5 + 0.5 * percentage_diff  # adjust transparency
                        color = f'background-color: rgba({red_intensity}, 0, 0, {alpha})'
                        return [color if col == 'valor_real' else '' for col in row.index]
                except Exception as e:
                    return ['' for col in row.index]

            # Cargar los datos
            # Aquí iría tu código para cargar el DataFrame `filtered_data`

            # Aplicar los estilos fila por fila
            styled_df = filtered_data.style.apply(highlight_valor_real, axis=1)

            # Mostrar el DataFrame en Streamlit
            st.dataframe(styled_df, height=filtered_data.shape[0] * 35 + 50, hide_index=True)
        with col2:
            st.subheader('Gráficos')
            variable = st.selectbox('*Selecciona la variable que quieras analizar*', (
                'red_blood_cc', 'hematocrit', 'insulin', 'fasting_glucose', 
                'triglyceride', 'total_cholesterol', 'direct_hdl_cholesterol', 
                'ldl_cholesterol', 'uric_acid', 'blood_pressure_status', 
                'blood_pressure_time_seconds'
            ))

            # Asegurarse de que la columna 'fecha' esté en formato datetime
            data['fecha'] = pd.to_datetime(data['fecha']) + pd.DateOffset(days=1)
            data = data.dropna(subset=[variable])

            # Obtener el valor medio (valor ideal) de la variable seleccionada
            valor_ideal = filtered_data.loc[filtered_data['parametro'] == variable, 'valor_ideal'].values[0]

            # Crear el gráfico de líneas
            line = alt.Chart(data).mark_line().encode(
                x=alt.X('fecha:T', axis=alt.Axis(title='Fecha de estudio', format='%d/%m/%Y')),
                y=alt.Y(variable, axis=alt.Axis(title=variable))
            )

            # Crear los puntos en el gráfico
            points = alt.Chart(data).mark_point(color='red', size=60).encode(
                x='fecha:T',
                y=variable,
                tooltip=[
                    alt.Tooltip('fecha:T', title='Fecha del Estudio', format='%d/%m/%Y'), 
                    alt.Tooltip(variable, title=variable)
                ]
            )

            # Crear la línea horizontal para el valor medio
            mean_line = alt.Chart(pd.DataFrame({'y': [valor_ideal]})).mark_rule(color='blue').encode(
                y='y:Q'
            )

            # Crear el texto para la línea de valor ideal
            text = alt.Chart(pd.DataFrame({
                'y': [valor_ideal], 
                'text': ['Valor Ideal'],
                'x': [data['fecha'].min()]  # Colocar el texto al inicio del eje X
            })).mark_text(
                align='left', 
                baseline='bottom',  # Colocar el texto por encima de la línea
                dx=5  # Desplazamiento horizontal (opcional)
            ).encode(
                x='x:T',
                y='y:Q',
                text='text:N'
            )

            # Combinar línea, puntos, línea de media y texto en un solo gráfico
            chart = (line + points + mean_line + text).properties(
                title=f'Evolución de {variable}'
            )

            # Mostrar el gráfico en Streamlit
            st.altair_chart(chart, use_container_width=True)
    else:
        st.write("No hay datos para mostrar, por favor cargue estudio")
        if st.button('Cargar Estudio'):
            st.switch_page("pages/2_Cargar_Estudio.py")