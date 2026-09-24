import streamlit as st
import pandas as pd
import pickle

# ============================================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Predicción del Tipo de Metástasis",
    page_icon="🎗️",
    layout="centered"
)

st.title("🎗️ Predicción del Tipo de Metástasis")

st.write(
    "Ingrese los datos solicitados para realizar la predicción. "
    "Las variables socioeconómicas se obtienen automáticamente "
    "a partir del código ZIP3."
)


# ============================================================
# 2. CARGAR MODELO Y LABEL ENCODER
# ============================================================

@st.cache_resource
def cargar_componentes():

    with open("modelo_random_forest.pkl", "rb") as f:
        modelo = pickle.load(f)

    with open("label_encoder.pkl", "rb") as f:
        le = pickle.load(f)

    return modelo, le


modelo, le = cargar_componentes()


# ============================================================
# 3. CARGAR INFORMACIÓN DE LOS ZIP3
# ============================================================

@st.cache_data
def cargar_datos_zip():

    datos = pd.read_csv("zip_completo.csv")

    datos["patient_zip3"] = pd.to_numeric(
        datos["patient_zip3"],
        errors="coerce"
    ).astype("Int64")

    return datos


zip_data = cargar_datos_zip()


# ============================================================
# 4. VARIABLES UTILIZADAS POR EL MODELO
# ============================================================

variables_modelo = [
    'payer_type',
    'patient_age',
    'breast_cancer_diagnosis_code',
    'population',
    'density',
    'age_median',
    'age_60s',
    'age_70s',
    'married',
    'never_married',
    'family_size',
    'income_household_median',
    'income_household_10_to_15',
    'income_household_75_to_100',
    'income_household_100_to_150',
    'income_household_150_over',
    'income_household_six_figure',
    'income_individual_median',
    'home_ownership',
    'housing_units',
    'rent_median',
    'rent_burden',
    'education_less_highschool',
    'education_highschool',
    'education_bachelors',
    'education_college_or_above',
    'labor_force_participation',
    'unemployment_rate',
    'self_employed',
    'farmer',
    'race_white',
    'race_other',
    'race_multiple',
    'hispanic',
    'disabled',
    'poverty',
    'limited_english',
    'veteran',
    'Ozone'
]


# ============================================================
# 5. OPCIONES DE ENTRADA
# ============================================================

payer_options = [
    "MEDICAID",
    "COMMERCIAL",
    "MEDICARE ADVANTAGE",
    "?"
]


diagnostico_options = [
    'C50919',
    'C50411',
    'C50112',
    'C50212',
    '1749',
    'C50912',
    'C50512',
    '1744',
    'C50412',
    'C50812',
    'C50911',
    'C50312',
    'C50311',
    'C50111',
    '1741',
    'C5091',
    'C50811',
    '1748',
    'C50511',
    '1743',
    'C50211',
    'C50011',
    'C5051',
    'C50012',
    'C50419',
    '1742',
    'C50611',
    'C50612',
    'C50119',
    'C50819',
    '1746',
    'C5041',
    'C50619',
    '19881',
    'C5081',
    '1745',
    'C50219',
    'C50319',
    'C50019',
    'C50519',
    'C50929',
    'C50021',
    'C5021',
    'C5011',
    'C5031',
    'C509',
    'C50',
    '1759',
    'C5001',
    'C50421',
    'C50922',
    'C50921'
]


# ============================================================
# 6. DATOS DEL PACIENTE
# ============================================================

st.subheader("📋 Datos del paciente")


zip3 = st.number_input(
    "Código ZIP3",
    min_value=0,
    max_value=999,
    value=100,
    step=1,
    help="Ingrese los primeros tres dígitos del código postal."
)


edad = st.number_input(
    "Edad del paciente",
    min_value=0,
    max_value=120,
    value=50,
    step=1
)


payer_type = st.selectbox(
    "Tipo de pagador",
    payer_options
)


diagnostico = st.selectbox(
    "Código de diagnóstico de cáncer de mama",
    diagnostico_options
)


# ============================================================
# 7. PREDICCIÓN
# ============================================================

if st.button(
    "🔮 Realizar predicción",
    use_container_width=True
):

    # Buscar ZIP3
    registro_zip = zip_data[
        zip_data["patient_zip3"] == zip3
    ]

    if registro_zip.empty:

        st.error(
            f"El ZIP3 {zip3} no se encuentra en la base de datos."
        )

        st.stop()


    datos_zip = registro_zip.iloc[0]


    # Variables obtenidas automáticamente del ZIP
    variables_zip = [
        variable
        for variable in variables_modelo
        if variable not in [
            "payer_type",
            "patient_age",
            "breast_cancer_diagnosis_code"
        ]
    ]


    # Revisar valores faltantes
    datos_faltantes = [
        variable
        for variable in variables_zip
        if pd.isna(datos_zip[variable])
    ]


    if datos_faltantes:

        st.error(
            "El ZIP3 seleccionado contiene valores faltantes "
            "en algunas variables necesarias para la predicción."
        )

        st.write("Variables faltantes:")
        st.write(datos_faltantes)

        st.stop()


    # ========================================================
    # CREAR REGISTRO PARA EL MODELO
    # ========================================================

    datos_prediccion = {}


    for variable in variables_modelo:

        if variable == "payer_type":

            datos_prediccion[variable] = payer_type

        elif variable == "patient_age":

            datos_prediccion[variable] = edad

        elif variable == "breast_cancer_diagnosis_code":

            datos_prediccion[variable] = diagnostico

        else:

            datos_prediccion[variable] = datos_zip[variable]


    X_nuevo = pd.DataFrame(
        [datos_prediccion],
        columns=variables_modelo
    )


    # ========================================================
    # PREDICCIÓN
    # ========================================================

    prediccion = modelo.predict(X_nuevo)[0]


    # ========================================================
    # CONVERTIR PREDICCIÓN A NOMBRE DE CLASE
    # ========================================================

    try:

        resultado = le.inverse_transform([prediccion])[0]

    except Exception:

        try:
            resultado = le.inverse_transform(
                [int(prediccion)]
            )[0]

        except Exception:
            resultado = str(prediccion)


    # ========================================================
    # MOSTRAR RESULTADO
    # ========================================================

    st.success("Predicción realizada correctamente.")

    st.subheader("🔬 Resultado")

    st.info(
        f"**Tipo de metástasis predicho:** {resultado}"
    )


    # ========================================================
    # INFORMACIÓN DEL ZIP
    # ========================================================

    st.subheader("📍 Información del ZIP3")

    col1, col2 = st.columns(2)


    with col1:

        st.write(f"**ZIP3:** {zip3}")

        st.write(f"**Edad:** {edad}")


    with col2:

        st.write(
            f"**Población:** "
            f"{datos_zip['population']:,.0f}"
        )

        st.write(
            f"**Densidad:** "
            f"{datos_zip['density']:,.2f}"
        )


    # ========================================================
    # DATOS INGRESADOS
    # ========================================================

    st.subheader("📋 Datos ingresados")

    st.write(
        f"**Tipo de pagador:** {payer_type}"
    )

    st.write(
        f"**Código de diagnóstico:** {diagnostico}"
    )