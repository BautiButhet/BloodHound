import streamlit as st
import streamlit.components.v1 as com
# Configuración de la página
#kjsdgkjsdk
st.set_page_config(
    page_title="BloodHound: Track your Blood",
    page_icon=":🩸:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15 = st.columns(15)
with col1:
    pass
with col15:
    if st.button("🡆"):
        st.switch_page("pages/1_Alta_Usuario.py")

import base64

com.iframe("https://lottie.host/embed/cc2e07bb-dd32-484b-933b-a71b7b7ecb5d/I3fXQsSh9W.json")

# Leer la imagen desde el archivo local y convertirla a base64
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

titulo_css = """
    <style>
        .titulo-custom {
            font-family: 'Poppins', sans-serif;
            text-align: center;
            font-size: 2.5em;
        }
        .subtitulo-custom {
            font-family: 'Poppins', sans-serif;
            text-align: center;
            font-size: 1.5em;
        }
    </style>
"""

# Aplicar el estilo CSS al título y subtítulo usando markdown
st.markdown(titulo_css, unsafe_allow_html=True)

# Mostrar el título y subtítulo con la clase CSS personalizada
st.markdown("<h1 class='titulo-custom'>BloodHound</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subtitulo-custom'>Track your blood</h3>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .custom-font {
        font-family: 'Poppins', sans-serif;
        font-size: 20px;
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <p class="custom-font">El propósito de esta aplicación es personalizar los
        datos hematológicos para que sean más comprensibles y accesibles para el paciente.
        Nuestro objetivo es simplificar los análisis de laboratorio, centrándonos principalmente
        en los estudios de sangre, con el fin de evitar confusiones, preocupaciones innecesarias
        y dudas. Para lograr esto, hemos desarrollado un algoritmo que personaliza los datos
        hematológicos según el perfil físico del usuario. De esta manera, el usuario puede ver cómo se
        comportan los análisis de sangre promedio de otros pacientes con características físicas o de salud similares.</i></h4>
    </div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#DC143C;'>Esta herramienta no está diseñada para "
            + "diagnosticar a los pacientes. Es fundamental contar con la participación de personal "
            + "médico antes de tomar decisiones relacionadas con la salud.</p>", unsafe_allow_html=True)

com.iframe("https://lottie.host/embed/962dbca4-1021-4512-87fd-79f6c30bde75/Mwbl6U1ODr.json")