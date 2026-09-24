# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import pickle


# =====================================================
# CARGAMOS EL MODELO
# =====================================================

modelo = pickle.load(
    open("modelo_random_forest.pkl", "rb")
)

label_encoder = pickle.load(
    open("label_encoder.pkl", "rb")
)


# =====================================================
# CARGAMOS LOS DATOS ZIP
# =====================================================

zip_data = pd.read_csv("zip_completo.csv")


# =====================================================
# INTERFAZ GRÁFICA
# =====================================================

st.title("🎗️ Predicción del Tipo de Metástasis")

st.write(
    "Ingrese los datos del paciente. "
    "Las variables socioeconómicas se obtienen "
    "automáticamente a partir del código ZIP3."
)


# Datos que ingresa el usuario

zip3 = st.number_input(
    "Código ZIP3",
    min_value=0,
    max_value=999,
    value=100,
    step=1
)

Edad = st.number_input(
    "Edad",
    min_value=0,
    max_value=120,
    value=50,
    step=1
)

Payer = st.selectbox(
    "Tipo de pagador",
    [
        "MEDICAID",
        "COMMERCIAL",
        "MEDICARE ADVANTAGE",
        "?"
    ]
)

Diagnostico = st.selectbox(
    "Código de diagnóstico de cáncer de mama",
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


# =====================================================
# BUSCAMOS LA INFORMACIÓN DEL ZIP
# =====================================================

if st.button("🔮 Realizar predicción"):

    datos_zip = zip_data[
        zip_data["patient_zip3"] == zip3
    ]


    if datos_zip.empty:

        st.error(
            "El ZIP3 ingresado no se encuentra en "
            "la base de datos."
        )

    else:

        # Tomamos la información del ZIP
        datos_zip = datos_zip.iloc[0]


        # =================================================
        # CREAMOS EL DATAFRAME
        # =================================================

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


        # =================================================
        # NOMBRES DE LAS VARIABLES
        # =================================================

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


        # =================================================
        # DATAFRAME FINAL
        # =================================================

        data = pd.DataFrame(
            datos,
            columns=columnas
        )


        # =================================================
        # PREDICCIÓN
        # =================================================

        Y_pred = modelo.predict(data)


        # =================================================
        # CONVERTIMOS LA PREDICCIÓN A SU NOMBRE
        # =================================================

        resultado = label_encoder.inverse_transform(
            Y_pred
        )


        # =================================================
        # MOSTRAMOS EL RESULTADO
        # =================================================

        st.success("Predicción realizada correctamente")

        st.subheader("🔬 Resultado")

        st.write(
            f"### Tipo de metástasis: {resultado[0]}"
        )


        # =================================================
        # MOSTRAMOS LOS DATOS
        # =================================================

        st.subheader("📋 Datos utilizados")

        st.write(f"**ZIP3:** {zip3}")
        st.write(f"**Edad:** {Edad}")
        st.write(f"**Tipo de pagador:** {Payer}")
        st.write(f"**Diagnóstico:** {Diagnostico}")

        st.write(
            f"**Población del ZIP3:** "
            f"{datos_zip['population']:,.0f}"
        )

        st.write(
            f"**Densidad:** "
            f"{datos_zip['density']:,.2f}"
        )
