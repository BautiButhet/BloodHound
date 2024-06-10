import streamlit as st
import pandas as pd
import altair as alt
from funciones import dni_exists,password_exists,consultar_estudios,consultar_estudios_fecha,highlight_valor_real,check_range
import base64

st.set_page_config(
    page_title="BloodHound: Track your Blood",
    page_icon=":🩸:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15 = st.columns(15)
with col1:
    if st.button("🡄"):
        st.switch_page("pages/2_Cargar_Estudio.py")

with col15:
    if st.button("🏠"):
        st.switch_page("Inicio.py")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Ruta a tu imagen local
img_path = "papers.co-sm55-pastel-blue-red-morning-blur-gradation-28-wallpaper.jpg"

# Convertir la imagen a base64
img_base64 = get_base64_of_bin_file(img_path)

# Crear el estilo CSS con la imagen base64
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img_base64}");
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""
# Insertar el estilo CSS en la aplicación de Streamlit
st.markdown(page_bg_img, unsafe_allow_html=True)

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
            
           # Función para aplicar el estilo condiciona


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
            valor_ideal = filtered_data.loc[filtered_data['variable'] == variable, 'valor_ideal'].values[0]
            
            valor_ideal_mayor = valor_ideal + 0.1*valor_ideal
            valor_ideal_menor = valor_ideal - 0.1*valor_ideal
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
            mean_line_mayor = alt.Chart(pd.DataFrame({'y': [valor_ideal_mayor]})).mark_rule(color='red').encode(
                y='y:Q'
            )
            mean_line_menor = alt.Chart(pd.DataFrame({'y': [valor_ideal_menor]})).mark_rule(color='red').encode(
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
            chart = (line + points + mean_line_mayor + mean_line_menor + text).properties(
                title=f'Evolución de {variable}'
            )

            # Mostrar el gráfico en Streamlit
            st.altair_chart(chart, use_container_width=True)
    else:
        st.write("No hay datos para mostrar, por favor cargue estudio")
        if st.button('Cargar Estudio'):
            st.switch_page("pages/2_Cargar_Estudio.py")