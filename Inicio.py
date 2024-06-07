import streamlit as st
# Configuración de la página
st.set_page_config(
    page_title="BloodHound: Track your Blood",
    page_icon=":🩸:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    pass
with col2:
    pass
with col3:
    pass
with col4:
    pass
with col5:
    if st.button("⮕"):
        st.switch_page("pages/1_Alta_Usuariopy")

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
