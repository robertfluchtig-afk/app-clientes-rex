import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Diseño imperial
st.set_page_config(page_title="Tesorería Real", page_icon="👑", layout="centered")

st.title("👑 Consulta de Estado Financiero")
st.markdown("---")
st.write("Ingrese su código identificador para consultar su estado en la base de datos.")

# Conexión a la base de datos
conn = st.connection("gsheets", type=GSheetsConnection)

# Ingreso del código
codigo_vasallo = st.text_input("Código de Cliente:", type="password")

if st.button("Consultar Estado"):
    if codigo_vasallo:
        try:
            # Leemos la pestaña exacta "Hoja 1"
            df = conn.read(ttl="0") 
            df = df.dropna(subset=['Codigo'])
            
            # Buscamos al cliente
            vasallo = df[df['Codigo'].astype(str) == codigo_vasallo]
            
            if not vasallo.empty:
                st.success("Identidad confirmada.")
                datos = vasallo.iloc[0]
                
                # Leemos las columnas EXACTAS de su imagen 11.png
                col1, col2 = st.columns(2)
                col1.metric("Puntos Acumulados", f"{datos['Puntos']}")
                col2.metric("Crédito Disponible", f"${datos['Credito_Disponible_CLP']}")
                
                st.warning(f"Deuda Pendiente: ${datos['Deuda_Pendiente_CLP']}")
                st.info(f"Fecha de Deuda: {datos['Fecha_Deuda']}")
                
                # Verificamos si tiene restricción
                if str(datos['Restringido']).strip().lower() in ["sí", "si"]:
                    st.error("⚠️ ESTADO: CRÉDITO RESTRINGIDO. Comuníquese con la administración.")
            else:
                st.error("Código incorrecto. Intruso detectado.")
        except Exception as e:
            # Si algo falla, este mensaje nos dirá EXACTAMENTE la línea del error
            st.error(f"Fallo crítico detectado. Detalle técnico: {e}")
    else:
        st.warning("Debe ingresar un código para proceder.")
