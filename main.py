import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from data.adding_data import add_data
from data.getting_data import get_data
from login.login import login_user

# Inicializando o serviço do banco de dados Firebase:
try:
    firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred)

database = firestore.client()


def app():
    user_id = (
        login_user()
    )  # Supondo que login_user retorna o identificador do usuário logado

    if user_id:
        st.title("Formulário de Deem's")

        # Obtendo os dados do usuário logado
        user_data = get_data(user_id)

        code = st.text_input("Código", value=user_data.get("code", ""))
        quantity = st.text_input("Quantidade", value=user_data.get("quantity", ""))
        rc = st.text_input("Relação de Carga", value=user_data.get("rc", ""))
        type = st.selectbox("Tipo da Deem", options=["Maior", "Menor"], value=user_data.get("type", ""))

        if st.button("Enviar"):
            if (
                code and quantity and rc and type
            ):  # Verificando se todos os campos foram preenchidos
                add_data(user_id, code, quantity, description, rc, type)
                st.success("Divergência inserida com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos.")

        df = get_data()  # Se você deseja mostrar todos os dados
        st.dataframe(df)


if __name__ == "__main__":
    app()
