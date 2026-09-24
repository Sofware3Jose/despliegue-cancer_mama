# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import pickle


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="MediPredict | Cáncer de Mama",
    page_icon="🎗️",
    layout="wide"
)


# =========================================================
# DISEÑO
# =========================================================

st.markdown("""
<style>

    /* Fondo */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Ancho */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Título */
    .titulo-principal {
        background: linear-gradient(
            135deg,
            #f4017c,
            #c90066
        );
        padding: 35px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
    }

    .titulo-principal h1 {
        color: white;
        font-size: 40px;
        margin-bottom: 5px;
    }

    .titulo-principal p {
        color: white;
        font-size: 17px;
    }

    /* Tarjetas */
    .tarjeta {
        background-color: white;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #e5e9ef;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Resultado */
    .resultado {
        background-color: #fff0f8;
        border: 2px solid #f4017c;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-top: 25px;
        margin-bottom: 25px;
    }

    .resultado h2 {
        color: #718096;
        font-size: 16px;
    }

    .resultado h1 {
        color: #c90066;
        font-size: 32px;
    }

    /* Botón */
    .stButton > button {
        background-color: #f4017c;
        color: white;
        border-radius: 12px;
        height: 50px;
        font-size: 17px;
        font-weight: bold;
        border: none;
    }

    .stButton > button:hover {
        background-color: #c90066;
        color: white;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# CARGAMOS EL MODELO
# =========================================================

modelo = pickle.load(
    open("modelo_random_forest.pkl", "rb")
)

label_encoder = pickle.load(
    open("label_encoder.pkl", "rb")
)


# =========================================================
# CARGAMOS DATOS ZIP
# =========================================================

zip_data = pd.read_csv("zip_completo.csv")


columnas_numericas = [
    columna
    for columna in zip_data.columns
    if columna != "patient_zip3"
]


for columna in columnas_numericas:

    zip_data[columna] = pd.to_numeric(
        zip_data[columna],
        errors="coerce"
    )


zip_data["patient_zip3"] = pd.to_numeric(
    zip_data["patient_zip3"],
    errors="coerce"
)


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown(
    """
    <div class="titulo-principal">
    """,
    unsafe_allow_html=True
)

st.title("🎗️ MediPredict")

st.write(
    "Sistema de apoyo para la predicción del tipo de "
    "metástasis en pacientes con cáncer de mama."
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# INFORMACIÓN
# =========================================================

st.info(
    "💡 Ingrese los datos básicos del paciente. "
    "El sistema utilizará el código ZIP3 para obtener "
    "automáticamente las variables socioeconómicas "
    "asociadas a esa zona."
)


# =========================================================
# FORMULARIO
# =========================================================

col1, col2 = st.columns(2)


# =========================================================
# DATOS DEL PACIENTE
# =========================================================

with col1:

    st.subheader("👤 Información del paciente")

    st.write(
        "Ingrese los datos básicos necesarios."
    )

    zip3 = st.number_input(
        "📍 Código ZIP3",
        min_value=0,
        max_value=999,
        value=100,
        step=1,
        help="Ingrese los primeros tres dígitos del código postal."
    )


    Edad = st.number_input(
        "🎂 Edad del paciente",
        min_value=0,
        max_value=120,
        value=50,
        step=1
    )


    Payer = st.selectbox(
        "💳 Tipo de pagador",
        [
            "MEDICAID",
            "COMMERCIAL",
            "MEDICARE ADVANTAGE",
            "?"
        ]
    )


# =========================================================
# INFORMACIÓN CLÍNICA
# =========================================================

with col2:

    st.subheader("🔬 Información clínica")

    st.write(
        "Seleccione el código correspondiente."
    )


    Diagnostico = st.selectbox(
        "🧬 Código de diagnóstico de cáncer de mama",
        [
            "C50919",
            "C50411",
            "C50112",
            "C50212",
            "1749",
            "C50912",
            "C50512",
            "1744",
            "C50412",
            "C50812",
            "C50911",
            "C50312",
            "C50311",
            "C50111",
            "1741",
            "C5091",
            "C50811",
            "1748",
            "C50511",
            "1743",
            "C50211",
            "C50011",
            "C5051",
            "C50012",
            "C50419",
            "1742",
            "C50611",
            "C50612",
            "C50119",
            "C50819",
            "1746",
            "C5041",
            "C50619",
            "19881",
            "C5081",
            "1745",
            "C50219",
            "C50319",
            "C50019",
            "C50519",
            "C50929",
            "C50021",
            "C5021",
            "C5011",
            "C5031",
            "C509",
            "C50",
            "1759",
            "C5001",
            "C50421",
            "C50922",
            "C50921"
        ]
    )


# =========================================================
# VARIABLES SOCIOECONÓMICAS
# =========================================================

st.divider()

st.subheader("📍 Variables socioeconómicas")

st.write(
    "Estas variables no deben ser ingresadas manualmente. "
    "El sistema las obtiene automáticamente a partir del ZIP3."
)


# =========================================================
# BOTÓN
# =========================================================

st.divider()

if st.button(
    "🔮 REALIZAR PREDICCIÓN",
    use_container_width=True
):

    # =====================================================
    # BUSCAR ZIP
    # =====================================================

    datos_zip = zip_data[
        zip_data["patient_zip3"] == zip3
    ]


    if datos_zip.empty:

        st.error(
            f"❌ El ZIP3 {zip3} no se encuentra "
            "en la base de datos."
        )

        st.stop()


    datos_zip = datos_zip.iloc[0]


    # =====================================================
    # DATOS
    # =====================================================

    datos = [[
        Payer,
        Edad,
        Diagnostico,
        datos_zip["population"],
        datos_zip["density"],
        datos_zip["age_median"],
        datos_zip["age_60s"],
        datos_zip["age_70s"],
        datos_zip["married"],
        datos_zip["never_married"],
        datos_zip["family_size"],
        datos_zip["income_household_median"],
        datos_zip["income_household_10_to_15"],
        datos_zip["income_household_75_to_100"],
        datos_zip["income_household_100_to_150"],
        datos_zip["income_household_150_over"],
        datos_zip["income_household_six_figure"],
        datos_zip["income_individual_median"],
        datos_zip["home_ownership"],
        datos_zip["housing_units"],
        datos_zip["rent_median"],
        datos_zip["rent_burden"],
        datos_zip["education_less_highschool"],
        datos_zip["education_highschool"],
        datos_zip["education_bachelors"],
        datos_zip["education_college_or_above"],
        datos_zip["labor_force_participation"],
        datos_zip["unemployment_rate"],
        datos_zip["self_employed"],
        datos_zip["farmer"],
        datos_zip["race_white"],
        datos_zip["race_other"],
        datos_zip["race_multiple"],
        datos_zip["hispanic"],
        datos_zip["disabled"],
        datos_zip["poverty"],
        datos_zip["limited_english"],
        datos_zip["veteran"],
        datos_zip["Ozone"]
    ]]


    # =====================================================
    # COLUMNAS
    # =====================================================

    columnas = [
        "payer_type",
        "patient_age",
        "breast_cancer_diagnosis_code",
        "population",
        "density",
        "age_median",
        "age_60s",
        "age_70s",
        "married",
        "never_married",
        "family_size",
        "income_household_median",
        "income_household_10_to_15",
        "income_household_75_to_100",
        "income_household_100_to_150",
        "income_household_150_over",
        "income_household_six_figure",
        "income_individual_median",
        "home_ownership",
        "housing_units",
        "rent_median",
        "rent_burden",
        "education_less_highschool",
        "education_highschool",
        "education_bachelors",
        "education_college_or_above",
        "labor_force_participation",
        "unemployment_rate",
        "self_employed",
        "farmer",
        "race_white",
        "race_other",
        "race_multiple",
        "hispanic",
        "disabled",
        "poverty",
        "limited_english",
        "veteran",
        "Ozone"
    ]


    # =====================================================
    # DATAFRAME
    # =====================================================

    data = pd.DataFrame(
        datos,
        columns=columnas
    )


    # =====================================================
    # PREDICCIÓN
    # =====================================================

    Y_pred = modelo.predict(data)


    resultado = label_encoder.inverse_transform(
        Y_pred
    )


    # =====================================================
    # RESULTADO
    # =====================================================

    st.success(
        "✅ Predicción realizada correctamente"
    )

    st.markdown(
        """
        <div class="resultado">
        """,
        unsafe_allow_html=True
    )

    st.subheader(
        "🔬 Resultado de la predicción"
    )

    st.header(
        f"🎗️ {resultado[0]}"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # =====================================================
    # DATOS UTILIZADOS
    # =====================================================

    st.subheader("📋 Datos utilizados")


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "📍 ZIP3",
            zip3
        )


    with c2:

        st.metric(
            "🎂 Edad",
            Edad
        )


    with c3:

        st.metric(
            "💳 Pagador",
            Payer
        )


    with c4:

        st.metric(
            "🧬 Diagnóstico",
            Diagnostico
        )


    # =====================================================
    # INFORMACIÓN ZIP
    # =====================================================

    st.subheader(
        "📊 Información socioeconómica"
    )


    c1, c2 = st.columns(2)


    with c1:

        poblacion = datos_zip["population"]

        if pd.notna(poblacion):

            st.metric(
                "👥 Población",
                f"{poblacion:,.0f}"
            )

        else:

            st.metric(
                "👥 Población",
                "No disponible"
            )


    with c2:

        densidad = datos_zip["density"]

        if pd.notna(densidad):

            st.metric(
                "🏙️ Densidad",
                f"{densidad:,.2f}"
            )

        else:

            st.metric(
                "🏙️ Densidad",
                "No disponible"
            )


# =========================================================
# PIE DE PÁGINA
# =========================================================

st.divider()

st.caption(
    "🎗️ MediPredict | Sistema académico de predicción "
    "basado en Machine Learning · Random Forest"
)
