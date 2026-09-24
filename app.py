# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import pickle


# =========================================================
# CONFIGURACIÓN DE LA PÁGINA
# =========================================================

st.set_page_config(
    page_title="MediPredict | Cáncer de Mama",
    page_icon="🎗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# ESTILOS PERSONALIZADOS
# =========================================================

st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Ocultar menú y footer de Streamlit */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Contenedor principal */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Encabezado */
    .hero {
        background: linear-gradient(
            135deg,
            #f4017c 0%,
            #c90066 100%
        );

        padding: 35px 40px;
        border-radius: 24px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(244, 1, 124, 0.18);
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 8px;
        font-weight: 700;
    }

    .hero p {
        font-size: 17px;
        margin: 0;
        opacity: 0.95;
    }

    /* Tarjetas */
    .card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #e8edf3;
        box-shadow: 0 5px 18px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    .card-title {
        font-size: 21px;
        font-weight: 700;
        color: #263238;
        margin-bottom: 5px;
    }

    .card-description {
        color: #718096;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* Botón */
    .stButton > button {
        width: 100%;
        border-radius: 14px;
        height: 52px;
        background: linear-gradient(
            135deg,
            #f4017c,
            #d9006f
        );
        color: white;
        border: none;
        font-size: 17px;
        font-weight: 700;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background: linear-gradient(
            135deg,
            #d9006f,
            #b8005d
        );
        transform: translateY(-1px);
    }

    /* Resultado */
    .result-card {
        background: linear-gradient(
            135deg,
            #fff0f8,
            #ffffff
        );

        border: 2px solid #f4017c;
        padding: 30px;
        border-radius: 22px;
        text-align: center;
        margin-top: 25px;
        margin-bottom: 25px;
    }

    .result-label {
        color: #718096;
        font-size: 15px;
        margin-bottom: 8px;
    }

    .result-value {
        color: #c90066;
        font-size: 32px;
        font-weight: 800;
    }

    /* Información */
    .info-box {
        background-color: #eef7ff;
        border-left: 5px solid #3498db;
        padding: 17px 20px;
        border-radius: 12px;
        color: #34495e;
        margin-bottom: 25px;
    }

    /* Métricas */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 17px;
        border: 1px solid #e8edf3;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    }

    .metric-title {
        font-size: 13px;
        color: #718096;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 23px;
        font-weight: 700;
        color: #263238;
    }

    /* Separadores */
    .section-space {
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #8a94a6;
        font-size: 13px;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #e5e9ef;
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
# CARGAMOS LOS DATOS ZIP
# =========================================================

zip_data = pd.read_csv("zip_completo.csv")


# Convertimos las variables numéricas

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

st.markdown("""
<div class="hero">

    <h1>🎗️ MediPredict</h1>

    <p>
        Sistema de apoyo para la predicción del tipo de
        metástasis en pacientes con cáncer de mama.
    </p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# INFORMACIÓN
# =========================================================

st.markdown("""
<div class="info-box">

<strong>¿Cómo funciona?</strong><br>

Ingrese los datos básicos del paciente. El sistema utiliza
el código ZIP3 para recuperar automáticamente las variables
socioeconómicas asociadas a esa zona y posteriormente realiza
la predicción mediante un modelo de Random Forest.

</div>
""", unsafe_allow_html=True)


# =========================================================
# FORMULARIO
# =========================================================

col_izquierda, col_derecha = st.columns(
    [1, 1],
    gap="large"
)


# =========================================================
# DATOS DEL PACIENTE
# =========================================================

with col_izquierda:

    st.markdown("""
    <div class="card">

        <div class="card-title">
            👤 Información del paciente
        </div>

        <div class="card-description">
            Ingrese los datos básicos necesarios para realizar
            la predicción.
        </div>

    </div>
    """, unsafe_allow_html=True)


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

with col_derecha:

    st.markdown("""
    <div class="card">

        <div class="card-title">
            🔬 Información clínica
        </div>

        <div class="card-description">
            Seleccione el código correspondiente al diagnóstico
            de cáncer de mama.
        </div>

    </div>
    """, unsafe_allow_html=True)


    Diagnostico = st.selectbox(
        "🧬 Código de diagnóstico",
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
# INFORMACIÓN AUTOMÁTICA DEL ZIP
# =========================================================

st.markdown(
    '<div class="section-space"></div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="card">

    <div class="card-title">
        📍 Variables socioeconómicas
    </div>

    <div class="card-description">
        No es necesario ingresar estas variables manualmente.
        El sistema las obtiene automáticamente utilizando el
        código ZIP3 seleccionado.
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# BOTÓN DE PREDICCIÓN
# =========================================================

st.markdown(
    '<div class="section-space"></div>',
    unsafe_allow_html=True
)

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


    # Primer registro

    datos_zip = datos_zip.iloc[0]


    # =====================================================
    # CREAR DATOS
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


    # =====================================================
    # CONVERTIR RESULTADO
    # =====================================================

    resultado = label_encoder.inverse_transform(
        Y_pred
    )


    # =====================================================
    # RESULTADO
    # =====================================================

    st.markdown(f"""
    <div class="result-card">

        <div class="result-label">
            RESULTADO DE LA PREDICCIÓN
        </div>

        <div class="result-value">
            🎗️ {resultado[0]}
        </div>

    </div>
    """, unsafe_allow_html=True)


    # =====================================================
    # DATOS DEL PACIENTE
    # =====================================================

    st.subheader("📋 Datos utilizados")


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.markdown(f"""
        <div class="metric-card">

            <div class="metric-title">
                ZIP3
            </div>

            <div class="metric-value">
                {zip3}
            </div>

        </div>
        """, unsafe_allow_html=True)


    with c2:

        st.markdown(f"""
        <div class="metric-card">

            <div class="metric-title">
                Edad
            </div>

            <div class="metric-value">
                {Edad}
            </div>

        </div>
        """, unsafe_allow_html=True)


    with c3:

        st.markdown(f"""
        <div class="metric-card">

            <div class="metric-title">
                Pagador
            </div>

            <div class="metric-value">
                {Payer}
            </div>

        </div>
        """, unsafe_allow_html=True)


    with c4:

        st.markdown(f"""
        <div class="metric-card">

            <div class="metric-title">
                Diagnóstico
            </div>

            <div class="metric-value">
                {Diagnostico}
            </div>

        </div>
        """, unsafe_allow_html=True)


    # =====================================================
    # INFORMACIÓN DEL ZIP
    # =====================================================

    st.subheader("📊 Información socioeconómica del ZIP3")


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


    # =====================================================
    # MENSAJE FINAL
    # =====================================================

    st.success(
        "✅ La predicción fue realizada correctamente "
        "utilizando el modelo Random Forest."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

    🎗️ <strong>MediPredict</strong><br>
    Sistema académico de predicción basado en Machine Learning.<br>
    Random Forest · Datos clínicos · Variables socioeconómicas

</div>
""", unsafe_allow_html=True)
