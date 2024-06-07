import time
import streamlit as st
from datetime import datetime
from funciones import insert_user, dni_exists, perfil_paciente
import pandas as pd

st.set_page_config(
    page_title="BloodHound: Track your Blood",
    page_icon=":🩸:",
    layout="wide",
    initial_sidebar_state="expanded",
)
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15 = st.columns(15)
with col1:
    if st.button("🡄"):
        st.switch_page("Inicio.py")

with col15:
    if st.button("🡆"):
        st.switch_page("pages/2_Cargar_Estudio.py")

archivo_csv = 'examination.csv'
df = pd.read_csv(archivo_csv)
st.title('Alta Usuario')
st.write("Por favor complete con la siguiente informacion:")
dni = st.text_input("DNI", placeholder="xxxxxxxx")
output_dni = st.empty()

password = st.text_input("Contraseña", value = '', type="password")
confirm_password = st.text_input("Confirmar Contraseña", value = '', type="password")
output_password = st.empty()
if password != '' and confirm_password != '' and password != confirm_password:
    output_password.error("Las contraseñas no coinciden")

if (password == confirm_password) and dni != '' and password != '':
    nombre = st.text_input("Nombre", "")
    output_nombre = st.empty()
    apellido = st.text_input("Apellido", "")
    output_apellido = st.empty()
    fecha_nacimiento = st.date_input("Selecciona tu fecha de nacimiento", min_value=datetime(1900, 1, 1), max_value=datetime.today(), value=None)
    output_fecha_nacimiento = st.empty()
    st.write("Genero")
    genero_aux = st.radio("Selecciona una opción:", ["Masculino", "Femenino"], key="genero", index = None)
    genero = 2 if genero_aux == "Femenino" else 1
    output_genero = st.empty()
    altura = st.text_input("Altura (cm)", value="", placeholder= f"Ingrese un valor entre {int(df['BMXHT'].min() / 10) * 10}  y {int(df['BMXHT'].max() / 10) * 10}")
    output_altura = st.empty()
    peso = st.text_input("Peso (kg)", value="", placeholder= f"Ingrese un valor entre {int(df['BMXWT'].min() / 10) * 10} y {int(df['BMXWT'].max() / 10) * 10}")
    output_peso = st.empty()

    # Preguntas, no = 0 y si = 1, ponemos 0 como valor si no contesta
    st.write("¿Alguna vez un médico u otro profesional de la salud te ha dicho que tu nivel de colesterol en la sangre estaba alto?")
    colesterol_aux = st.radio("Selecciona una opción:", ["No", "Si"], key="colesterol", index = None)
    colesterol = 1 if colesterol_aux == "Si" else 2
    output_colesterol = st.empty()

    st.write("Durante los últimos 3 meses, ¿has estado en tratamiento para la anemia, a veces llamada sangre cansada o sangre baja?")
    anemia_aux = st.radio("Selecciona una opción:", ["No", "Si"], key="anemia", index = None)
    anemia = 9 if anemia_aux == "Si" else 7
    output_anemia = st.empty()

    st.write("¿Alguna vez un médico u otro profesional de la salud te ha dicho que estabas con sobrepeso?")
    sobrepeso_aux = st.radio("Selecciona una opción:", ["No", "Si"], key="sobrepeso", index = None)
    sobrepeso = 1 if sobrepeso_aux == "Si" else 0
    output_sobrepeso = st.empty()

    st.write("¿Alguna vez un médico u otro profesional de la salud te ha dicho que tienes diabetes?")
    diabetes_aux = st.radio("Selecciona una opción:", ["No", "Si"], key="diabetes", index = None)
    diabetes = 1 if diabetes_aux == "Si" else 2
    output_diabetes = st.empty()

    # Preguntas fumadores, rtas distintas de 0 y 1
    st.write("¿Fumas o fumaste alguna vez en tu vida?")
    fumadoraux1 = st.radio("Selecciona una opción:", ["No", "Si"], key="fumador_pregunta", index = None)
    if fumadoraux1 == "Si":
        fumadoraux2 = st.radio("¿Dejaste de fumar regularmente en los ultimos 6 meses o menos?", ["No", "Si"], key="fumador_pregunta2", index = None)
        fumador = 1 if fumadoraux2 == "No" else 2
    else: fumador = 2
    output_fumador = st.empty()

    error_message = ""

    if st.button("Guardar"):
        dni_exists_q = dni_exists(dni)
        if dni_exists_q:
            output_dni.error("Error, este DNI ya está registrado en la base de datos.")
            error_message += "DNI, " 
        bar = st.progress(5, text = "Analizando existencia de DNI en la base de datos...")
        time.sleep(0.725)
        if not dni or not dni.isdigit():
            output_dni.error("Error, por favor completa este campo correctamente.")
            error_message += "DNI, "
        bar.progress(10, text = "Analizando si DNI es de tipo numerico...")
        time.sleep(0.725)
        if not password or not confirm_password or (password != confirm_password):
            output_password.error("Error, por favor completa este campo correctamente.")
            error_message += "Contraseña, "
        bar.progress(15, text = "Analizando si las contraseñas coinciden...")
        time.sleep(0.725)
        if not nombre or not nombre.isalpha():
            output_nombre.error("Error, por favor completa este campo correctamente.")
            error_message += "Nombre, "
        bar.progress(20, text = "Analizando si Nombre es de tipo caracter...")
        time.sleep(0.725)
        if not apellido or not apellido.isalpha():
            output_apellido.error("Error, por favor completa este campo correctamente.")
            error_message += "Apellido, "
        bar.progress(30, text = "Analizando si Apellido es de tipo caracter...")
        time.sleep(0.725)
        if not fecha_nacimiento:
            output_fecha_nacimiento.error("Error, por favor selecciona tu fecha de nacimiento.")
            error_message += "Fecha de Nacimiento, "
        bar.progress(40, text = "Analizando si se introdujo fecha de nacimiento...")
        time.sleep(0.725)
        if not genero_aux:
            output_genero.error("Error, por favor completa este campo correctamente.")
            error_message += "Genero, "
        bar.progress(50, text = "Analizando si se introdujo genero...")
        time.sleep(0.725)
        if not altura or not altura.isdigit():
            output_altura.error("Error, por favor completa este campo correctamente.")
            error_message += "Altura, "
        elif int(altura) > df['BMXHT'].max() :
            output_altura.error("El valor ingresado es mayor al maximo esperado, ¿esta seguro de que lo ha ingresado correctamente?")
            error_message += "Altura, "
        elif int(altura) < df['BMXHT'].min() :
            output_altura.error("El valor ingresado es menor al minimo esperado, ¿esta seguro de que lo ha ingresado correctamente?")
            error_message += "Altura, "
        bar.progress(60, text = "Analizando posibles errores al introducir Altura...")
        time.sleep(0.725)
        if not peso or not peso.isdigit():
            output_peso.error("Error, por favor completa este campo correctamente.")
            error_message += "Peso, "
        elif int(peso) < df['BMXWT'].min() :
            output_peso.error("El valor ingresado es menor al minimo esperado, ¿esta seguro de que lo ha ingresado correctamente?")
            error_message += "Peso, "
        elif int(peso) > df['BMXWT'].max() :
            output_peso.error("El valor ingresado es mayor al maximo esperado, ¿esta seguro de que lo ha ingresado correctamente?")
            error_message += "Peso, "
        bar.progress(65, text = "Analizando posibles errores al introducir Peso...")
        time.sleep(0.725)
        if not colesterol_aux:
            output_colesterol.error("Error, por favor completa este campo correctamente.")
            error_message += "Colesterol, "
        bar.progress(70, text = "Analizando posibles errores al introducir Colesterol...")
        time.sleep(0.725)
        if not anemia_aux:
            output_anemia.error("Error, por favor completa este campo correctamente.")
            error_message += "Anemia, "
        bar.progress(75, text = "Analizando posibles errores al introducir Anemia...")
        time.sleep(0.725)
        if not sobrepeso_aux:
            output_sobrepeso.error("Error, por favor completa este campo correctamente.")
            error_message += "Sobrepeso, "
        bar.progress(80, text = "Analizando posibles errores al introducir Sobrepeso...")
        time.sleep(0.725)
        if not diabetes_aux:
            output_diabetes.error("Error, por favor completa este campo correctamente.")
            error_message += "Diabetes, "
        bar.progress(85, text = "Analizando posibles errores al introducir Diabetes...")
        if not fumadoraux1:
            output_fumador.error("Error, por favor completa este campo correctamente.")
            error_message += "Fumador, "
        bar.progress(90, text = "Analizando posibles errores al introducir Fumador...")
        time.sleep(0.725)
        if fumadoraux1 == "Si" and not fumadoraux2:
            output_fumador.error("Error, por favor completa este campo correctamente.")
            error_message += "Fumador, "
        bar.progress(95, text = "Analizando posibles errores al introducir Fumador...")
        time.sleep(0.725)
        if error_message:
            st.sidebar.error("Error: Las siguientes variables no han sido completadas: " + error_message[:-2])  # Elimina la última coma y el espacio
            bar.progress(0)

        else:

            insert_user(dni, password, nombre, apellido, fecha_nacimiento, genero, altura, peso, colesterol, anemia, sobrepeso, diabetes, fumador,*perfil_paciente(fecha_nacimiento,altura,genero,peso,fumador,diabetes))
            bar.progress(100, text = "Exito...")
            bar.empty()
            st.success("¡Datos guardados exitosamente!")
            time.sleep(2.5)
            st.write("Aguarde unos instantes...")
            time.sleep(2.5)
            st.switch_page("pages/2_Cargar_Estudio.py")