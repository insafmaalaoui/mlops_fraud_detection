import streamlit as st
import requests
st.markdown("""
    <style>
    label { font-weight: bold; }
    </style>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="💳",
    layout="centered"
)

# TITRE
st.markdown(
    """
    <h1 style='text-align:center; color:#FF4B4B;'>💳 Fraud Detection App</h1>
    <p style='text-align:center; color:#BBB;'>Analysez une transaction et détectez si elle est frauduleuse !</p>
    """,
    unsafe_allow_html=True
)

# FORMULAIRE
st.subheader("📝 Entrer les features de la transaction")

cols = st.columns(2)
inputs = {}

feature_list = [
    "Time","V1","V2","V3","V4","V5","V6","V7","V8","V9","V10",
    "V11","V12","V13","V14","V15","V16","V17","V18","V19","V20",
    "V21","V22","V23","V24","V25","V26","V27","V28","Amount"
]

for i, f in enumerate(feature_list):
    with cols[i % 2]:
        inputs[f] = st.number_input(f"{f} :", value=0.0, step=0.01)

# BOUTON
if st.button("🔍 Prédire"):
    with st.spinner("Analyse en cours..."):
        response = requests.post("http://localhost:8000/predict", json=inputs)

        if response.status_code == 200:
            result = response.json()

            if result["fraud"] == 1:
                st.error("🚨 **FRAUDE DÉTECTÉE !** La transaction semble dangereuse.")
            else:
                st.success("✅ **Aucune fraude détectée.** La transaction paraît normale.")
        else:
            st.error("❌ Erreur : impossible de contacter l’API.")
