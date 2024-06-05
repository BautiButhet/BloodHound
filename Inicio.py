import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="BloodHound: Track your Blood",
    page_icon=":🩸:",
    layout="wide",
    initial_sidebar_state="expanded",
)
#######para meterle un fondo###########
import base64

# Leer la imagen desde el archivo local y convertirla a base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Ruta a tu imagen local
img_path = 'fondo-medico-abstracto-iconos-simbolos-planos-diseno-plantillas-concepto-e-idea-tecnologia-sanitaria-medicina-innovacion-salud-ciencia-e-investigacion_120542-693.avif'

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

st.markdown("<h1 style='text-align:center;'>BloodHound</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>Track your blood</h3>", unsafe_allow_html=True)

st.markdown("""
    <div style='border: 2px solid #DC143C; padding: 10px; border-radius: 5px; background-color: rgba(255, 255, 255, 0.8);'>
        <h5 style='text-align:justify;'><i>El propósito de esta aplicación es personalizar los
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
