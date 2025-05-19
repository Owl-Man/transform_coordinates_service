import streamlit as st
import pandas as pd
import requests
import io
import base64

st.set_page_config(
    page_title="Преобразование координат",
    page_icon="📍",
    layout="wide"
)

BACKEND_URL = "http://localhost:8000"

st.title("Преобразование координат")
st.markdown("""
Это приложение позволяет преобразовывать координаты из различных систем координат в ГСК-2011.
Загрузите Excel файл с координатами (колонки: Name, X, Y, Z) и выберите исходную систему координат.
""")

try:
    response = requests.get(f"{BACKEND_URL}/coordinate-systems")
    coordinate_systems = response.json()["systems"]
except:
    st.error("Не удалось получить список систем координат. Убедитесь, что бэкенд запущен.")
    coordinate_systems = []

source_system = st.selectbox(
    "Выберите исходную систему координат:",
    coordinate_systems,
    index=0 if coordinate_systems else None
)

uploaded_file = st.file_uploader("Загрузите Excel файл с координатами", type=['xlsx'])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        
        required_columns = ['Name', 'X', 'Y', 'Z']
        if not all(col in df.columns for col in required_columns):
            st.error(f"Файл должен содержать колонки: {', '.join(required_columns)}")
        else:
            st.subheader("Исходные данные")
            st.dataframe(df)
            
            if st.button("Преобразовать координаты"):
                try:
                    files = {'file': ('data.xlsx', uploaded_file.getvalue())}
                    data = {'source_system': source_system}
                    response = requests.post(f"{BACKEND_URL}/transform", files=files, data=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        report = result['report']
                        
                        st.download_button(
                            label="Скачать отчет",
                            data=report,
                            file_name="transformation_report.md",
                            mime="text/markdown"
                        )
                        
                        st.markdown(report)
                    else:
                        st.error(f"Ошибка: {response.json()['detail']}")
                except Exception as e:
                    st.error(f"Ошибка при преобразовании: {str(e)}")
    except Exception as e:
        st.error(f"Ошибка при чтении файла: {str(e)}")

st.markdown("---")
st.markdown("Сервис на FAST API для преобразования координат. UgurlievAgamir") 