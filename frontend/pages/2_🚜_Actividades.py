import streamlit as st
import pandas as pd
import api_client
from datetime import date

st.set_page_config(page_title="Registro de Actividades", page_icon="🚜")

st.title("🚜 Registro de Actividades")
st.markdown("Añade actividades operativas a cada cultivo y haz seguimiento de costos y fechas.")

crops = api_client.get_crops()

if not crops:
    st.warning("Primero debes registrar un cultivo para poder asignarle actividades.")
    st.stop()

# Seleccionar cultivo principal
crop_options = [(c["id"], c["name"]) for c in crops]
selected_crop = st.selectbox("Selecciona el Cultivo a trabajar:", crop_options, format_func=lambda x: x[1])
crop_id = selected_crop[0]

# Trazar una división para el formulario
st.divider()

col_form, col_list = st.columns([1, 1.5])

with col_form:
    st.subheader("Añadir Actividad")
    with st.form("form_create_activity"):
        activity_type = st.selectbox("Tipo de Tarea", ["Riego", "Poda", "Fumigación", "Abono", "Cosecha", "Otro"])
        activity_date = st.date_input("Fecha de Actividad")
        cost = st.number_input("Costo Estimado ($)", min_value=0.0, step=10.0)
        desc = st.text_area("Observaciones", placeholder="Opcional...")
        
        submitted = st.form_submit_button("Guardar Tarea")
        if submitted:
            data = {
                "activity_type": activity_type,
                "date": str(activity_date),
                "cost": cost,
                "description": desc
            }
            if api_client.create_activity(crop_id, data):
                st.success("Tarea asignada correctamente al cultivo.")
                st.rerun()
            else:
                st.error("Error registrando.")

with col_list:
    st.subheader(f"Historial de Actividades: {selected_crop[1]}")
    activities = api_client.get_activities(crop_id)
    
    if not activities:
        st.info("Sin registro de tareas para este cultivo específico.")
    else:
        df_act = pd.DataFrame(activities)
        df_show = df_act.drop(columns=["id", "crop_id"], errors="ignore")
        st.dataframe(df_show, use_container_width=True)
