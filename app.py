# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import pickle


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Predicción de Metástasis",
    page_icon="🎗️",
    layout="centered"
)

st.title("🎗️ Predicción del Tipo de Metástasis")

st.write(
    "Ingrese los datos del paciente. "
    "Las variables socioeconómicas se obtienen automáticamente "
    "a partir del código ZIP3."
)


# =========================================================
# CARGAR MODELO Y LABEL ENCODER
# =========================================================

modelo = pickle.load(
    open("modelo_random_forest.pkl", "rb")
)

label_encoder = pickle.load(
    open("label_encoder.pkl", "rb")
)


# =========================================================
# CARGAR DATOS ZIP
# =========================================================

zip_data = pd.read_csv("zip_completo.csv")


# Asegurar que ZIP3 tenga formato numérico
zip_data["patient_zip3"] = pd.to_numeric(
    zip_data["patient_zip3"],
    errors="coerce"
)


# =========================================================
# VARIABLES DEL MODELO
# =========================================================

variables_modelo = [
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


# =========================================================
# OPCIONES
# =========================================================

payer_options = [
    "MEDICAID",
    "COMMERCIAL",
    "MEDICARE ADVANTAGE",
    "?"
]


diagnostico_options = [
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


# =========================================================
# INTERFAZ
# =========================================================

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


# =========================================================
# PREDICCIÓN
# =========================================================

if st.button(
    "🔮 Realizar predicción",
    use_container_width=True
):

    # -----------------------------------------------------
    # Buscar ZIP3
    # -----------------------------------------------------

    registro_zip = zip_data[
        zip_data["patient_zip3"] == zip3
    ]


    if registro_zip.empty:

        st.error(
            f"El ZIP3 {zip3} no se encuentra en la base de datos."
        )

        st.stop()


    # Tomamos el primer registro correspondiente al ZIP3
    datos_zip = registro_zip.iloc[0]


    # -----------------------------------------------------
    # Crear registro para el modelo
    # -----------------------------------------------------

    datos = {}


    for variable in variables_modelo:

        if variable == "payer_type":

            datos[variable] = payer_type

        elif variable == "patient_age":

            datos[variable] = edad

        elif variable == "breast_cancer_diagnosis_code":

            datos[variable] = diagnostico

        else:

            datos[variable] = datos_zip[variable]


    # -----------------------------------------------------
    # DataFrame final
    # -----------------------------------------------------

    data = pd.DataFrame(
        [datos],
        columns=variables_modelo
    )


    # -----------------------------------------------------
    # Predicción
    # -----------------------------------------------------

    try:

        prediccion = modelo.predict(data)

        resultado = label_encoder.inverse_transform(
            prediccion.astype(int)
        )[0]


        # -------------------------------------------------
        # Mostrar resultado
        # -------------------------------------------------

        st.success(
            "Predicción realizada correctamente."
        )

        st.subheader("🔬 Resultado")

        st.info(
            f"**Tipo de metástasis predicho:** {resultado}"
        )


        # -------------------------------------------------
        # Información del paciente
        # -------------------------------------------------

        st.subheader("📋 Datos utilizados")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**ZIP3:** {zip3}"
            )

            st.write(
                f"**Edad:** {edad}"
            )

            st.write(
                f"**Pagador:** {payer_type}"
            )


        with col2:

            st.write(
                f"**Diagnóstico:** {diagnostico}"
            )

            st.write(
                f"**Población:** "
                f"{datos_zip['population']:,.0f}"
            )

            st.write(
                f"**Densidad:** "
                f"{datos_zip['density']:,.2f}"
            )


    except Exception as e:

        st.error(
            "Ocurrió un error al realizar la predicción."
        )

        st.exception(e)
