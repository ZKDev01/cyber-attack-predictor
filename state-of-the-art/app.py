import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Ciberataques",
    page_icon="🔒",
    layout="wide"
)

# Título principal
st.title("📊 Análisis de Estado del Arte en Ciberataques")

# Cargar los datos


@st.cache_data
def load_data():
  return pd.read_csv('cyber-attack.csv')


df = load_data()

# Sidebar con filtros
st.sidebar.header("Filtros")
selected_tags = st.sidebar.multiselect(
    "Filtrar por etiquetas",
    options=sorted(
        set([tag.strip() for tags in df['etiquetas del archivo'].str.split(',') for tag in tags])),
    default=[]
)

# Filtrar datos basado en las etiquetas seleccionadas
if selected_tags:
  filtered_df = df[df['etiquetas del archivo'].apply(
      lambda x: all(tag in x for tag in selected_tags))]
else:
  filtered_df = df

# Contenido principal
st.header("Vista General de Publicaciones")

# Métricas clave
col1, col2, col3 = st.columns(3)
with col1:
  st.metric("Total de Publicaciones", len(filtered_df))
with col2:
  total_datasets = filtered_df['insight-dataset'].str.split(',').explode().nunique()
  st.metric("Datasets Únicos", total_datasets)
with col3:
  total_models = filtered_df['insight-models'].str.split(',').explode().nunique()
  st.metric("Modelos Únicos", total_models)

# Análisis de datasets
st.subheader("Datasets más utilizados")
datasets = filtered_df['insight-dataset'].str.split(',').explode().value_counts()
fig_datasets = px.bar(
    datasets,
    title="Frecuencia de uso de Datasets",
    labels={'index': 'Dataset', 'value': 'Frecuencia'}
)
st.plotly_chart(fig_datasets)

# Análisis de modelos
st.subheader("Modelos más utilizados")
models = filtered_df['insight-models'].str.split(
    ',').explode().str.strip().value_counts()
fig_models = px.bar(
    models,
    title="Frecuencia de uso de Modelos",
    labels={'index': 'Modelo', 'value': 'Frecuencia'}
)
st.plotly_chart(fig_models)

# Tabla detallada
st.subheader("Detalles de las Publicaciones")
st.dataframe(
    filtered_df[['nombre', 'publication', 'insights', 'insight-metrics', 'url']],
    hide_index=True
)
