import streamlit as st
import pandas as pd
import api_client
from datetime import date

st.set_page_config(page_title="Gestión de Cultivos", page_icon="🌾")

st.title("🌾 Gestión de Cultivos")
st.markdown("Registra y monitorea el estado fundamental de la producción en tus campos.")

col_form, col_list = st.columns([1, 2])

with col_form:
    st.subheader("Nuevo Cultivo")
    with st.form("form_create_crop"):
        name = st.text_input("Nombre del Cultivo (ej: Maíz)", placeholder="Tomate")
        area = st.number_input("Área en Hectáreas", min_value=0.1, step=0.1, value=1.0)
        planting_date = st.date_input("Fecha de Siembra", value=date.today())
        status = st.selectbox("Estado", ["Activo", "Cosechado"])
        
        submitted = st.form_submit_button("Guardar Cultivo")
        if submitted:
            if not name:
                st.error("El nombre es requerido.")
            else:
                data = {
                    "name": name,
                    "area": area,
                    "planting_date": str(planting_date),
                    "status": status
                }
                success = api_client.create_crop(data)
                if success:
                    st.success(f"Cultivo '{name}' registrado con éxito!")
                    st.rerun()
                else:
                    st.error("Error conectando con el servidor.")

with col_list:
    st.subheader("Tus Cultivos")
    crops = api_client.get_crops()
    
    if not crops:
        st.info("No hay cultivos registrados todavía.")
    else:
        # Convertir a dataframe para display más rico visualmente
        df = pd.DataFrame(crops)
        # Ocultar campos innecesarios
        df_display = df.drop(columns=["activities", "id"], errors="ignore")
        # Mostrar como Tabla interactiva
        st.dataframe(df_display, use_container_width=True)
        
        # Eliminar Cultivo con Extender
        with st.expander("Eliminar un cultivo"):
            crop_to_delete = st.selectbox("Selecciona cultivo para borrar", [""] + [(c["id"], c["name"]) for c in crops])
            if st.button("Eliminar (Irreversible)"):
                if crop_to_delete and crop_to_delete != "":
                    if api_client.delete_crop(crop_to_delete[0]):
                        st.success("Eliminado exitosamente.")
                        st.rerun()
                    else:
                        st.error("Error eliminando.")
