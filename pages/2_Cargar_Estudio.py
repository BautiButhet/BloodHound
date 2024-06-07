import time
import streamlit as st
from datetime import datetime
from funciones import dni_exists, get_nombre, insert_studio, password_exists

st.set_page_config(
    page_title="BloodHound: Track your Blood",
    page_icon=":🩸:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    if st.button("⬅"):
        st.switch_page("pages/1_Alta_Usuario.py")
with col2:
    pass
with col3:
    pass
with col4:
    pass
with col5:
    pass
with col6:
    if st.button("⮕"):
        st.switch_page("pages/3_Analisis_Estudio.py")

st.title('Carga de Estudios')
if 'estado' not in st.session_state:
    st.session_state['estado']= 'No Autorizado'

st.write("Iniciar Sesion:")
dni = st.text_input("DNI", value = '', placeholder="xxxxxxxx")
if not dni_exists(dni):
    st.session_state['estado'] = 'No Autorizado'
password = st.text_input("Contraseña", value = '', type="password")
output_error = st.empty()
if not password_exists(password):
    st.session_state['estado'] = 'No Autorizado'

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("Iniciar Sesión"):
        if dni_exists(dni) and password_exists(password):
            output_error.success("Inicio de sesión exitoso")
            st.session_state['estado'] = 'Autorizado'
        else:
            output_error.error("Usuario o Contraseña incorrectos")
            st.session_state['estado'] = 'No Autorizado'
with col2:
    pass
with col3:
    pass
with col4:
    pass
with col5:
    if st.button("Crear Usuario"):
        st.switch_page("pages/1_Alta_Usuario.py")


if st.session_state['estado'] == 'Autorizado':
    error_message = ""
    st.subheader(f"Bienvenido {get_nombre(dni)}, puede cargar sus datos")
    fecha = st.date_input("Indique fecha en que se realizo el estudio]", min_value=datetime(1900, 1, 1), max_value=datetime.today(), value=None)
    output_fecha_nacimiento = st.empty()
    red_blood_cc = st.text_input("Eritrocito (millon de celulas/uL) ", value=None, placeholder="0")
    output_red_blood = st.empty()
    hematocrit = st.text_input("Hematocrito (%)", value=None, placeholder="0")
    output_hematocrit = st.empty()
    insulin = st.text_input("Insulina (uU/mL)", value=None, placeholder="0")
    output_insulin = st.empty()
    two_hour_glucose = st.text_input("Glucosa a las dos horas", value=None, placeholder="0")
    output_two_hour_glucose = st.empty()
    triglyceride = st.text_input("Triglicerido (mg/dL)", value=None, placeholder="0")
    output_triglyceride = st.empty()
    total_cholesterol = st.text_input("Colesterol total( mg/dL)", value=None, placeholder="0")
    output_total_cholesterol = st.empty()
    direct_hdl_cholesterol = st.text_input("Colesterol-HDL directo (mg/dL)", value=None, placeholder="0")
    output_direct_hdl_cholesterol = st.empty()
    ldl_cholesterol = st.text_input("Colesterol-LDL (mg/dL)", value=None, placeholder="0")
    output_ldl_cholesterol = st.empty()
    uric_acid = st.text_input("Ácido urico (mg/dL)", value=None, placeholder="0")
    output_uric_acid = st.empty()
    blood_pressure_status = st.text_input("Estado de la presión arterial", value=None, placeholder="0")
    output_blood_pressure_status = st.empty()
    blood_pressure_time_seconds = st.text_input("Tiempo de la presión arterial en segundos", value=None, placeholder="0")
    output_blood_pressure_time_seconds = st.empty()

    if st.button("Guardar"):
        if not fecha:
            output_fecha_nacimiento.error("Error, por favor selecciona la fecha en l;a que se realizo el estudio.")
            error_message += "Fecha de Nacimiento, "

        if not red_blood_cc == None and not red_blood_cc.isdigit():
            output_red_blood.error("Error, por favor completa este campo correctamente.")
            error_message += "Eritrocitos, "

        if not hematocrit == None and not hematocrit.isdigit():
            output_hematocrit.error("Error, por favor completa este campo correctamente.")
            error_message += "Hematocrito, "

        if not insulin == None and not insulin.isdigit():
            output_insulin.error("Error, por favor completa este campo correctamente.")
            error_message += "Insulina, "

        if not two_hour_glucose == None and not two_hour_glucose.isdigit():
            output_two_hour_glucose.error("Error, por favor completa este campo correctamente.")
            error_message += "Glucosa a las dos horas, "

        if not triglyceride == None and not triglyceride.isdigit():
            output_triglyceride.error("Error, por favor completa este campo correctamente.")
            error_message += "Triglicerido, "

        if not total_cholesterol == None and not total_cholesterol.isdigit():
            output_total_cholesterol.error("Error, por favor completa este campo correctamente.")
            error_message += "Colesterol total, "

        if not direct_hdl_cholesterol == None and not direct_hdl_cholesterol.isdigit():
            output_direct_hdl_cholesterol.error("Error, por favor completa este campo correctamente.")
            error_message += "Colesterol-HDL directo, "

        if not ldl_cholesterol == None and not ldl_cholesterol.isdigit():
            output_ldl_cholesterol.error("Error, por favor completa este campo correctamente.")
            error_message += "Colesterol-LDL, "

        if not uric_acid == None and not uric_acid.isdigit():
            output_uric_acid.error("Error, por favor completa este campo correctamente.")
            error_message += "Ácido urico, "

        if not blood_pressure_status == None and not blood_pressure_status.isdigit():
            output_blood_pressure_status.error("Error, por favor completa este campo correctamente.")
            error_message += "Estado de la presión arterial, "

        if not blood_pressure_time_seconds == None and not blood_pressure_time_seconds.isdigit():
            output_blood_pressure_time_seconds.error("Error, por favor completa este campo correctamente.")
            error_message += "Tiempo de la presión arterial en segundos, "

        if error_message:
            st.sidebar.error("Error: Los siguientes campos no han sido completados correctamente: " + error_message[:-2])
        else:          
            # Insertar los datos en la base de datos
            st.toast('Procesando Informacion!')
            time.sleep(.75)
            st.toast('...')
            time.sleep(.75)
            st.toast('...')
            time.sleep(.75)
            st.toast("¡Datos guardados exitosamente!", icon='🎉')
            insert_studio(dni,red_blood_cc, hematocrit, insulin, two_hour_glucose, triglyceride, total_cholesterol, direct_hdl_cholesterol, ldl_cholesterol, uric_acid, blood_pressure_status, blood_pressure_time_seconds,fecha)
            st.success("Guardado exitoso! Aguarde unos instantes...")
            time.sleep(2.5)
            st.switch_page("pages/3_Analisis_Estudio.py")

