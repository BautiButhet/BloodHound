import streamlit as st
import psycopg2
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text


def get_db_connection():
    user = 'qhjbupnh'
    password = 'w6veIInjps-hA3WDVpV4HRWTwnmNoyJb'
    host = 'isilo.db.elephantsql.com'
    port = '5432'
    dbname = 'qhjbupnh'
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return conn

def insert_user(dni, password, nombre, apellido, fecha_nacimiento, genero, altura, peso, colesterol, anemia, sobrepeso, diabetes, fumador,media_red_blood_cc, media_hematocrit, media_insulin, media_two_hour_glucose, media_triglyceride, media_total_cholesterol, media_direct_hdl_cholesterol, media_ldl_cholesterol, media_uric_acid, media_blood_pressure_status, media_blood_pressure_time_seconds):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = query = "INSERT INTO usuarios.pacientes(dni, password, nombre, apellido, fecha_nacimiento, genero, altura, peso, colesterol, anemia, sobrepeso, diabetes, fumador,media_red_blood_cc, media_hematocrit, media_insulin, media_two_hour_glucose, media_triglyceride, media_total_cholesterol, media_direct_hdl_cholesterol, media_ldl_cholesterol, media_uric_acid, media_blood_pressure_status, media_blood_pressure_time_seconds) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query, (dni, password, nombre, apellido, fecha_nacimiento, genero, altura, peso, colesterol, anemia, sobrepeso, diabetes, fumador,media_red_blood_cc, media_hematocrit, media_insulin, media_two_hour_glucose, media_triglyceride, media_total_cholesterol, media_direct_hdl_cholesterol, media_ldl_cholesterol, media_uric_acid, media_blood_pressure_status, media_blood_pressure_time_seconds))
            conn.commit()
    except psycopg2.Error as e:
        st.error(f"Se produjo un error al guardar el usuario: {e}")
    finally:
        conn.close()

def insert_studio(dni, red_blood_cc, hematocrit, insulin, two_hour_glucose, triglyceride, total_cholesterol, direct_hdl_cholesterol, ldl_cholesterol, uric_acid, blood_pressure_status, blood_pressure_time_seconds,fecha):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "INSERT INTO usuarios.estudios(dni, red_blood_cc, hematocrit, insulin, two_hour_glucose, triglyceride, total_cholesterol, direct_hdl_cholesterol, ldl_cholesterol, uric_acid, blood_pressure_status, blood_pressure_time_seconds,fecha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
            cur.execute(query, (dni, red_blood_cc, hematocrit, insulin, two_hour_glucose, triglyceride, total_cholesterol, direct_hdl_cholesterol, ldl_cholesterol, uric_acid, blood_pressure_status, blood_pressure_time_seconds,fecha))
            conn.commit()
    except psycopg2.Error as e:
        st.error(f"Se produjo un error al guardar el usuario: {e}")
    finally:
        conn.close()


def dni_exists(dni):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM usuarios.pacientes WHERE dni = %s"
            cur.execute(query, (dni,))
            result = cur.fetchone()
            return result is not None
    finally:
        conn.close()

def password_exists(password):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM usuarios.pacientes WHERE password = %s"
            cur.execute(query, (password,))
            result = cur.fetchone()
            return result is not None
    finally:
        conn.close()

def get_nombre(dni):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT nombre FROM usuarios.pacientes WHERE dni = %s"
            cur.execute(query, (dni,))
            result = cur.fetchone()
            return result[0] if result else None
    finally:
        conn.close()

def consultar_estudios(dni):
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:

        query = """
        SELECT 
        usuarios.estudios.*,
        usuarios.pacientes.media_red_blood_cc,
        usuarios.pacientes.media_hematocrit,
        usuarios.pacientes.media_insulin,
        usuarios.pacientes.media_two_hour_glucose,
        usuarios.pacientes.media_triglyceride,
        usuarios.pacientes.media_total_cholesterol,
        usuarios.pacientes.media_direct_hdl_cholesterol,
        usuarios.pacientes.media_ldl_cholesterol,
        usuarios.pacientes.media_uric_acid,
        usuarios.pacientes.media_blood_pressure_status,
        usuarios.pacientes.media_blood_pressure_time_seconds
        FROM 
        usuarios.estudios
        INNER JOIN 
        usuarios.pacientes ON usuarios.estudios.dni = usuarios.pacientes.dni
        WHERE 
        usuarios.estudios.dni = %s;
        """
        df = pd.read_sql(query, conn, params=(dni,))
        return df
    except Exception as e:
        print(f"Error al realizar la consulta: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def color_cells(val, min_val, max_val):
    """Aplica un color basado en el valor, usando una escala de rojo a verde"""
    try:
        val = float(val)
        min_val = float(min_val)
        max_val = float(max_val)
    except ValueError:
        return ''  # Devuelve vacío si hay un error en la conversión

    if min_val <= val <= max_val:
        color = 'background-color: green'
    else:
        distance = min(abs(val - min_val), abs(val - max_val))
        max_distance = max(abs(val - min_val), abs(val - max_val))
        intensity = int(255 * (distance / max_distance))
        color = f'background-color: rgb(255,{255 - intensity},{255 - intensity})'
    return color

def consultar_estudios_fecha(dni, fecha):
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        query = """SELECT 
    'red_blood_cc' AS variable,
    usuarios.estudios.red_blood_cc AS valor_real,
    usuarios.pacientes.media_red_blood_cc AS valor_ideal,
    CONCAT(
        ROUND(CAST(usuarios.pacientes.media_red_blood_cc * 0.9 AS numeric), 2),
        ' - ',
        ROUND(CAST(usuarios.pacientes.media_red_blood_cc * 1.1 AS numeric), 2)
    ) AS rangos
FROM 
    usuarios.estudios
INNER JOIN 
    usuarios.pacientes ON usuarios.estudios.dni = usuarios.pacientes.dni
WHERE 
    usuarios.estudios.dni = %s AND usuarios.estudios.fecha = %s

UNION ALL

SELECT
    'hematocrit' AS variable,
    usuarios.estudios.hematocrit AS valor_real,
    usuarios.pacientes.media_hematocrit AS valor_ideal,
    CONCAT(
        ROUND(CAST(usuarios.pacientes.media_hematocrit * 0.9 AS numeric), 2),
        ' - ',
        ROUND(CAST(usuarios.pacientes.media_hematocrit * 1.1 AS numeric), 2)
    ) AS rangos
FROM
    usuarios.estudios
INNER JOIN
    usuarios.pacientes ON usuarios.estudios.dni = usuarios.pacientes.dni
WHERE
    usuarios.estudios.dni = %s AND usuarios.estudios.fecha = %s

UNION ALL

SELECT
    'insulin' AS variable,
    usuarios.estudios.insulin AS valor_real,
    usuarios.pacientes.media_insulin AS valor_ideal,
    CONCAT(
        ROUND(CAST(usuarios.pacientes.media_insulin * 0.9 AS numeric), 2),
        ' - ',
        ROUND(CAST(usuarios.pacientes.media_insulin * 1.1 AS numeric), 2)
    ) AS rangos
FROM
    usuarios.estudios
INNER JOIN
    usuarios.pacientes ON usuarios.estudios.dni = usuarios.pacientes.dni
WHERE
    usuarios.estudios.dni = %s AND usuarios.estudios.fecha = %s

UNION ALL

SELECT
    'two_hour_glucose' AS variable,
    usuarios.estudios.two_hour_glucose AS valor_real,
    usuarios.pacientes.media_two_hour_glucose AS valor_ideal,
    CONCAT(
        ROUND(CAST(usuarios.pacientes.media_two_hour_glucose * 0.9 AS numeric), 2),
        ' - ',
        ROUND(CAST(usuarios.pacientes.media_two_hour_glucose * 1.1 AS numeric), 2)
    ) AS rangos
FROM
    usuarios.estudios
INNER JOIN
    usuarios.pacientes ON usuarios.estudios.dni = usuarios.pacientes.dni
WHERE
    usuarios.estudios.dni = %s AND usuarios.estudios.fecha = %s

UNION ALL

SELECT
    'triglyceride' AS variable,
    usuarios.estudios.triglyceride AS valor_real,
    usuarios.pacientes.media_triglyceride AS valor_ideal,
    CONCAT(
        ROUND(CAST(usuarios.pacientes.media_triglyceride * 0.9 AS numeric), 2),
        ' - ',
        ROUND(CAST(usuarios.pacientes.media_triglyceride * 1.1 AS numeric), 2)
    ) AS rangos
FROM
    usuarios.estudios
INNER JOIN
    usuarios.pacientes ON usuarios.estudios.dni = usuarios.pacientes.dni
WHERE
    usuarios.estudios.dni = %s AND usuarios.estudios.fecha = %s

UNION ALL

SELECT
    'total_cholesterol' AS variable,
    usuarios.estudios.total_cholesterol AS valor_real,
    usuarios.pacientes.media_total_cholesterol AS valor_ideal,
    CONCAT(
        ROUND(CAST(usuarios.pacientes.media_total_cholesterol * 0.9 AS numeric), 2),
        ' - ',
        ROUND(CAST(usuarios.pacientes.media_total_cholesterol * 1.1 AS numeric), 2)
    ) AS rangos
FROM
    usuarios.estudios
INNER JOIN
    usuarios.pacientes ON usuarios.estudios.dni = usuarios.pacientes.dni
WHERE
    usuarios.estudios.dni = %s AND usuarios.estudios.fecha = %s

UNION ALL

SELECT
    'direct_hdl_cholesterol' AS variable,
    usuarios.estudios.direct_hdl_cholesterol AS valor_real,
    usuarios.pacientes.media_direct_hdl_cholesterol AS valor_ideal,
    CONCAT(
        ROUND(CAST(usuarios.pacientes.media_direct_hdl_cholesterol * 0.9 AS numeric), 2),
        ' - ',
        ROUND(CAST(usuarios.pacientes.media_direct_hdl_cholesterol * 1.1 AS numeric), 2)
    ) AS rangos
FROM
    usuarios.estudios
INNER JOIN
    usuarios.pacientes ON usuarios.estudios.dni = usuarios.pacientes.dni
WHERE
    usuarios.estudios.dni = %s AND usuarios.estudios.fecha = %s

UNION ALL

SELECT
    'ldl_cholesterol' AS variable,
    usuarios.estudios.ldl_cholesterol AS valor_real,
    usuarios.pacientes.media_ldl_cholesterol AS valor_ideal,
    CONCAT(
        ROUND(CAST(usuarios.pacientes.media_ldl_cholesterol * 0.9 AS numeric), 2),
        ' - ',
        ROUND(CAST(usuarios.pacientes.media_ldl_cholesterol * 1.1 AS numeric), 2)
    ) AS rangos
FROM
    usuarios.estudios
INNER JOIN
    usuarios.pacientes ON usuarios.estudios.dni = usuarios.pacientes.dni
WHERE
    usuarios.estudios.dni = %s AND usuarios.estudios.fecha = %s

UNION ALL

SELECT
    'uric_acid' AS variable,
    usuarios.estudios.uric_acid AS valor_real,
    usuarios.pacientes.media_uric_acid AS valor_ideal,
    CONCAT(
        ROUND(CAST(usuarios.pacientes.media_uric_acid * 0.9 AS numeric), 2),
        ' - ',
        ROUND(CAST(usuarios.pacientes.media_uric_acid * 1.1 AS numeric), 2)
    ) AS rangos
FROM
    usuarios.estudios
INNER JOIN
    usuarios.pacientes ON usuarios.estudios.dni = usuarios.pacientes.dni
WHERE
    usuarios.estudios.dni = %s AND usuarios.estudios.fecha = %s

UNION ALL

SELECT
    'blood_pressure_status' AS variable,
    usuarios.estudios.blood_pressure_status AS valor_real,
    usuarios.pacientes.media_blood_pressure_status AS valor_ideal,
    CONCAT(
        ROUND(CAST(usuarios.pacientes.media_blood_pressure_status * 0.9 AS numeric), 2),
        ' - ',
        ROUND(CAST(usuarios.pacientes.media_blood_pressure_status * 1.1 AS numeric), 2)
    ) AS rangos
FROM
    usuarios.estudios
INNER JOIN
    usuarios.pacientes ON usuarios.estudios.dni = usuarios.pacientes.dni
WHERE
    usuarios.estudios.dni = %s AND usuarios.estudios.fecha = %s

UNION ALL

SELECT
    'blood_pressure_time_seconds' AS variable,
    usuarios.estudios.blood_pressure_time_seconds AS valor_real,
    usuarios.pacientes.media_blood_pressure_time_seconds AS valor_ideal,
    CONCAT(
        ROUND(CAST(usuarios.pacientes.media_blood_pressure_time_seconds * 0.9 AS numeric), 2),
        ' - ',
        ROUND(CAST(usuarios.pacientes.media_blood_pressure_time_seconds * 1.1 AS numeric), 2)
    ) AS rangos
FROM
    usuarios.estudios
INNER JOIN
    usuarios.pacientes ON usuarios.estudios.dni = usuarios.pacientes.dni
WHERE
    usuarios.estudios.dni = %s AND usuarios.estudios.fecha = %s

        """

        # Ejecutar el query pasando los parámetros del dni y fecha
        df = pd.read_sql(query, conn, params=(dni, fecha, dni, fecha, dni, fecha, dni, fecha, dni, fecha, dni,fecha, dni, fecha, dni, fecha, dni, fecha, dni, fecha, dni,fecha))
        return df
    except Exception as e:
        print(f"Error al realizar la consulta: {e}")
        return pd.DataFrame()
    finally:
        conn.close()




def calcular_edad(fecha_nacimiento):
    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Calcular la edad restando el año de nacimiento del año actual
    edad = fecha_actual.year - fecha_nacimiento.year

    # Ajustar la edad si aún no se ha alcanzado el cumpleaños de este año
    if fecha_nacimiento.month > fecha_actual.month or (fecha_nacimiento.month == fecha_actual.month and fecha_nacimiento.day > fecha_actual.day):
        edad -= 1

    return edad


def perfil_paciente(fecha_nacimiento,altura, genero, peso, fumador, diabetes): 
    pacientes_df = pd.read_csv('questionnaire.csv')
    demographic_df = pd.read_csv('demographic.csv')
    labs_df = pd.read_csv("labs.csv")
    examination = pd.read_csv("examination.csv")

    edad = calcular_edad(fecha_nacimiento)

    join_key = 'SEQN'

# Lista para almacenar los dataframe

    list_df = (demographic_df, labs_df, examination)
    resultado = pacientes_df
    for df in list_df:
        resultado = pd.merge(resultado, df, on=join_key, how='inner')
    
    criterios = {
        'RIDAGEYR': (int(edad)-2, int(edad)+2),
        'RIAGENDR': genero,
        'SMQ040': int(fumador),
        'DIQ010': int(diabetes),
        'indice_masa': (int(peso)/int(altura) - 0.02, int(peso)/int(altura) + 0.02)
    }

    # Aplicar filtros basados en criterios

    for criterio, valor in criterios.items():
        if criterio == 'RIDAGEYR':
            resultado = resultado[((resultado[criterio] >= valor[0]) & resultado[criterio] <= valor[1])]
        elif criterio == 'indice_masa':
            resultado = resultado[((resultado['BMXWT']/resultado['BMXHT'] >= valor[0]) & resultado['BMXWT']/resultado['BMXHT'] <= valor[1])]
        else:
            resultado = resultado[resultado[criterio] == valor]
    

    print("Subgrupo filtrado:")

    media_red_blood_cc = resultado['LBXRBCSI'].mean() if 'LBXRBCSI' in resultado.columns else None
    media_hematocrit = resultado['LBXHCT'].mean() if 'LBXHCT' in resultado.columns else None
    media_insulin = resultado['LBXIN'].mean() if 'LBXIN' in resultado.columns else None
    media_two_hour_glucose = resultado['LBXGLT'].mean() if 'LBXGLT' in resultado.columns else None
    media_triglyceride = resultado['LBXTR'].mean() if 'LBXTR' in resultado.columns else None
    media_total_cholesterol = resultado['LBXTC'].mean() if 'LBXTC' in resultado.columns else None
    media_direct_hdl_cholesterol = resultado['LBDHDD'].mean() if 'LBDHDD' in resultado.columns else None
    media_ldl_cholesterol = resultado['LBDLDL'].mean() if 'LBDLDL' in resultado.columns else None
    media_uric_acid = resultado['LBXSUA'].mean() if 'LBXSUA' in resultado.columns else None
    media_blood_pressure_status = resultado['PEASCST1'].mean() if 'PEASCST1' in resultado.columns else None
    media_blood_pressure_time_seconds = resultado['PEASCTM1'].mean() if 'PEASCTM1' in resultado.columns else None

    return (
    media_red_blood_cc,
    media_hematocrit,
    media_insulin,
    media_two_hour_glucose,
    media_triglyceride,
    media_total_cholesterol,
    media_direct_hdl_cholesterol,
    media_ldl_cholesterol,
    media_uric_acid,
    media_blood_pressure_status,
    media_blood_pressure_time_seconds)


# Función para aplicar el estilo condicional
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
            # Convert the percentage difference into a light green shade
            green_intensity = int(100 * (1 - percentage_diff)) + 155  # light green
            color = f'background-color: rgba(144, 238, 144, {green_intensity / 255})'
            return [color if col == 'valor_real' else '' for col in row.index]
        else:
            # Calculate the percentage difference from the nearest bound (min_val or max_val)
            if val_real < min_val:
                percentage_diff = (min_val - val_real) / val_ideal
            else:
                percentage_diff = (val_real - max_val) / val_ideal
            
            # Cap the percentage_diff at 1 (100%) for the gradient calculation
            percentage_diff = min(percentage_diff, 1.0)
            
            # Convert the percentage difference into a light red shade
            red_intensity = int(100 * percentage_diff) + 155  # light red
            color = f'background-color: rgba(255, 182, 193, {red_intensity / 255})'
            return [color if col == 'valor_real' else '' for col in row.index]
    except Exception as e:
        return ['' for col in row.index]

def check_range(value_real, value_ideal):
                if pd.isna(value_ideal) or pd.isna(value_real):
                    return False
                try:
                    min_val = value_ideal * 0.9
                    max_val = value_ideal * 1.1
                    return min_val <= value_real <= max_val
                except:
                    return False