import streamlit as st
import pandas as pd
import plotly.express as px
import api_client

st.set_page_config(
    page_title="AgroTech Dashboard",
    page_icon="🌱",
    layout="wide",
)

st.title("🌱 AgroTech Dashboard Principal")
st.markdown("Bienvenido al **MVP** de gestión agrícola para decisiones inteligentes. Utiliza el menú izquierdo para navegar entre cultivos y actividades.")

st.divider()

if not api_client.check_health():
    st.error("⚠️ Error: No se pudo conectar al Backend. Por favor verifica que el servidor FastAPI esté corriendo.")
    st.stop()

# ----- OBTENER DATOS KPI -----
stats = api_client.get_dashboard_stats()

if not stats:
    st.info("Aún no hay datos para procesar. Comienza registrando un nuevo cultivo.")
    st.stop()

# --- CARDS DE KPIs ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Cultivos", value=stats.get("total_crops", 0))

with col2:
    st.metric(label="Cultivos Activos", value=stats.get("active_crops", 0))

with col3:
    st.metric(label="Área Total (Hectáreas)", value=f"{stats.get('total_area', 0)} ha")

with col4:
    st.metric(label="Costo Total", value=f"${stats.get('total_cost', 0):.2f}")

st.markdown("<br>", unsafe_allow_html=True)

# --- GRÁFICOS INTERACTIVOS (PLOTLY EXCELENTES ESTÉTICAMENTE) ---
col_plot1, col_plot2 = st.columns(2)

with col_plot1:
    st.subheader("Costos por Actividad")
    cost_by_activity = stats.get("cost_by_activity", [])
    if cost_by_activity:
        df_act = pd.DataFrame(cost_by_activity)
        fig1 = px.pie(df_act, names='type', values='cost', hole=0.4, 
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Sin registros de costos de actividad.")

with col_plot2:
    st.subheader("Costo Total por Cultivo")
    cost_by_crop = stats.get("cost_by_crop", [])
    if cost_by_crop:
        df_crop = pd.DataFrame(cost_by_crop)
        # Barchart premium y pastel
        fig2 = px.bar(df_crop, x='crop', y='cost', text_auto='.2s', 
                      color='crop', color_discrete_sequence=px.colors.qualitative.Pastel)
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sin costos asignados a cultivos todavía.")

st.caption("🚀 AgroTech MVP - Panel Analítico para la toma de decisiones informadas.")
