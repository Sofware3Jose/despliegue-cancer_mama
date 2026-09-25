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
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# ESTILOS (DISEÑO MODERNO)
# =========================================================

st.markdown("""
<style>

    /* ---------- Fuente e importaciones ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ---------- Variables de color ---------- */
    :root {
        --primary: #ec0d7c;
        --primary-dark: #b3005f;
        --primary-light: #ff4fa0;
        --bg: #f6f7fb;
        --card-bg: #ffffff;
        --border: #eceef3;
        --text-dark: #1a1d29;
        --text-muted: #6b7280;
    }

    /* ---------- Fondo general ---------- */
    .stApp {
        background: radial-gradient(circle at top left, #fdf2f8 0%, #f6f7fb 35%);
    }

    /* ---------- Ancho del contenedor ---------- */
    .block-container {
        max-width: 1180px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* ---------- Ocultar elementos por defecto de Streamlit ---------- */
    #MainMenu, footer, header {visibility: hidden;}

    /* ---------- Header / Hero ---------- */
    .hero {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        padding: 42px 44px;
        border-radius: 24px;
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 12px 30px -8px rgba(236, 13, 124, 0.45);
        position: relative;
        overflow: hidden;
    }

    .hero::after {
        content: "";
        position: absolute;
        top: -60px;
        right: -60px;
        width: 220px;
        height: 220px;
        background: rgba(255,255,255,0.08);
        border-radius: 50%;
    }

    .hero .eyebrow {
        display: inline-block;
        background: rgba(255,255,255,0.18);
        padding: 5px 14px;
        border-radius: 999px;
        font-size: 12.5px;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 14px;
    }

    .hero h1 {
        font-size: 36px;
        font-weight: 800;
        margin: 0 0 8px 0;
        line-height: 1.15;
    }

    .hero p {
        font-size: 16px;
        opacity: 0.92;
        margin: 0;
        max-width: 640px;
    }

    /* ---------- Tarjetas de sección ---------- */
    .card {
        background-color: var(--card-bg);
        padding: 26px 28px;
        border-radius: 18px;
        border: 1px solid var(--border);
        box-shadow: 0 2px 10px rgba(17, 24, 39, 0.04);
        margin-bottom: 22px;
    }

    .card-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 17px;
        font-weight: 700;
        color: var(--text-dark);
        margin-bottom: 4px;
    }

    .card-subtitle {
        font-size: 13.5px;
        color: var(--text-muted);
        margin-bottom: 18px;
    }

    /* ---------- Banner informativo ---------- */
    .info-banner {
        background: #fdf2f8;
        border: 1px solid #fbcfe8;
        border-left: 4px solid var(--primary);
        border-radius: 14px;
        padding: 16px 20px;
        font-size: 14.5px;
        color: #831843;
        margin-bottom: 24px;
    }

    /* ---------- Resultado ---------- */
    .resultado-box {
        background: linear-gradient(135deg, #fff0f8 0%, #fdf2f8 100%);
        border: 1.5px solid var(--primary-light);
        border-radius: 22px;
        padding: 36px;
        text-align: center;
        margin-top: 8px;
        margin-bottom: 26px;
        box-shadow: 0 10px 28px -10px rgba(236, 13, 124, 0.35);
    }

    .resultado-box .label {
        color: var(--text-muted);
        font-size: 13.5px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 10px;
    }

    .resultado-box .valor {
        color: var(--primary-dark);
        font-size: 30px;
        font-weight: 800;
    }

    /* ---------- Métricas dentro de tarjetas ---------- */
    div[data-testid="stMetric"] {
        background-color: #fafafc;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 14px 16px;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 13px !important;
        color: var(--text-muted) !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 20px !important;
        color: var(--text-dark) !important;
        font-weight: 700 !important;
    }

    /* ---------- Inputs ---------- */
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border-color: var(--border) !important;
    }

    /* ---------- Botón principal ---------- */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        border-radius: 14px;
        height: 52px;
        font-size: 16.5px;
        font-weight: 700;
        border: none;
        box-shadow: 0 8px 18px -6px rgba(236, 13, 124, 0.55);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 22px -6px rgba(236, 13, 124, 0.65);
        color: white;
    }

    .stButton > button:active {
        transform: translateY(0px);
    }

    /* ---------- Divisores ---------- */
    hr {
        margin: 1.8rem 0 !important;
        border-color: var(--border) !important;
    }

    /* ---------- Pie de página ---------- */
    .footer-note {
        text-align: center;
        color: var(--text-muted);
        font-size: 13px;
        margin-top: 10px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# CARGAMOS EL MODELO
# =========================================================

modelo = pickle.load(open("modelo_random_forest.pkl", "rb"))
label_encoder = pickle.load(open("label_encoder.pkl", "rb"))


# =========================================================
# CARGAMOS DATOS ZIP
# =========================================================

zip_data = pd.read_csv("zip_completo.csv")

columnas_numericas = [c for c in zip_data.columns if c != "patient_zip3"]

for columna in columnas_numericas:
    zip_data[columna] = pd.to_numeric(zip_data[columna], errors="coerce")

zip_data["patient_zip3"] = pd.to_numeric(zip_data["patient_zip3"], errors="coerce")

zips_disponibles = sorted(
    zip_data["patient_zip3"].dropna().astype(int).unique()
)


# =========================================================
# ENCABEZADO (HERO)
# =========================================================

st.markdown("""
<div class="hero">
    <span class="eyebrow">🎗️ Sistema de apoyo clínico</span>
    <h1>MediPredict</h1>
    <p>Predicción asistida por Machine Learning del tipo de metástasis
    en pacientes con cáncer de mama, combinando datos clínicos y
    variables sociodemográficas por zona geográfica.</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# INFORMACIÓN
# =========================================================

st.markdown("""
<div class="info-banner">
    💡 Ingrese los datos básicos del paciente. El sistema utilizará el
    código <strong>ZIP3</strong> para obtener automáticamente las
    variables sociodemográficas asociadas a esa zona.
</div>
""", unsafe_allow_html=True)


# =========================================================
# FORMULARIO
# =========================================================

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">👤 Información del paciente</div>
        <div class="card-subtitle">Ingrese los datos básicos necesarios.</div>
    """, unsafe_allow_html=True)

    zip3 = st.selectbox("📍 Código ZIP3", zips_disponibles)
    Edad = st.selectbox("🎂 Edad del paciente", list(range(0, 92)), index=50)
    Payer = st.selectbox(
        "💳 Tipo de pagador",
        ["MEDICAID", "COMMERCIAL", "MEDICARE ADVANTAGE", "?"]
    )

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">🔬 Información clínica</div>
        <div class="card-subtitle">Seleccione el código correspondiente.</div>
    """, unsafe_allow_html=True)

    Diagnostico = st.selectbox(
        "🧬 Código de diagnóstico de cáncer de mama",
        [
            "C50919", "C50411", "C50112", "C50212", "1749", "C50912",
            "C50512", "1744", "C50412", "C50812", "C50911", "C50312",
            "C50311", "C50111", "1741", "C5091", "C50811", "1748",
            "C50511", "1743", "C50211", "C50011", "C5051", "C50012",
            "C50419", "1742", "C50611", "C50612", "C50119", "C50819",
            "1746", "C5041", "C50619", "19881", "C5081", "1745",
            "C50219", "C50319", "C50019", "C50519", "C50929", "C50021",
            "C5021", "C5011", "C5031", "C509", "C50", "1759", "C5001",
            "C50421", "C50922", "C50921"
        ]
    )

    st.markdown("""
        <p style="font-size:13px; color:#6b7280; margin-top:8px;">
        📍 Las variables sociodemográficas se obtienen automáticamente
        a partir del ZIP3 seleccionado.
        </p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# BOTÓN DE PREDICCIÓN
# =========================================================

st.write("")
predecir = st.button("🔮 REALIZAR PREDICCIÓN", use_container_width=True)

if predecir:

    datos_zip = zip_data[zip_data["patient_zip3"] == zip3]

    if datos_zip.empty:
        st.error(f"❌ El ZIP3 {zip3} no se encuentra en la base de datos.")
        st.stop()

    datos_zip = datos_zip.iloc[0]

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

    columnas = [
        "payer_type", "patient_age", "breast_cancer_diagnosis_code",
        "population", "density", "age_median", "age_60s", "age_70s",
        "married", "never_married", "family_size",
        "income_household_median", "income_household_10_to_15",
        "income_household_75_to_100", "income_household_100_to_150",
        "income_household_150_over", "income_household_six_figure",
        "income_individual_median", "home_ownership", "housing_units",
        "rent_median", "rent_burden", "education_less_highschool",
        "education_highschool", "education_bachelors",
        "education_college_or_above", "labor_force_participation",
        "unemployment_rate", "self_employed", "farmer", "race_white",
        "race_other", "race_multiple", "hispanic", "disabled", "poverty",
        "limited_english", "veteran", "Ozone"
    ]

    data = pd.DataFrame(datos, columns=columnas)

    Y_pred = modelo.predict(data)
    resultado = label_encoder.inverse_transform(Y_pred)

    st.success("✅ Predicción realizada correctamente")

    st.markdown(f"""
    <div class="resultado-box">
        <div class="label">Resultado de la predicción</div>
        <div class="valor">🎗️ {resultado[0]}</div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- Datos utilizados ----------------
    st.markdown('<div class="card"><div class="card-title">📋 Datos utilizados</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📍 ZIP3", zip3)
    with c2:
        st.metric("🎂 Edad", Edad)
    with c3:
        st.metric("💳 Pagador", Payer)
    with c4:
        st.metric("🧬 Diagnóstico", Diagnostico)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Info sociodemográfica ----------------
    st.markdown('<div class="card"><div class="card-title">📊 Información sociodemográfica del ZIP3</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        poblacion = datos_zip["population"]
        st.metric("👥 Población", f"{poblacion:,.0f}" if pd.notna(poblacion) else "No disponible")

    with c2:
        densidad = datos_zip["density"]
        st.metric("🏙️ Densidad", f"{densidad:,.2f}" if pd.notna(densidad) else "No disponible")

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# PIE DE PÁGINA
# =========================================================

st.divider()
st.markdown(
    '<p class="footer-note">🎗️ MediPredict · Sistema académico de predicción '
    'basado en Machine Learning · Random Forest</p>',
    unsafe_allow_html=True
)
