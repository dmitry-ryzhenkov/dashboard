import streamlit as st

# Import your custom modules
from tables import tables_id
from utils import filtrar
from data import load_data, extract_all_airtable
import soft
import tech
import tech_
import overview_

# ---------------------------------------------------------------------------------------------
# Page Configuration and Data Loading
# ---------------------------------------------------------------------------------------------

# Use Streamlit's page config to set a title and layout
st.set_page_config(layout="wide", page_title="Dashboard de Habilidades")

# Use st.cache_data for performance: the data will be loaded once and cached.
@st.cache_data
def cached_load_data():
    return load_data()

df = cached_load_data()

# ---------------------------------------------------------------------------------------------
# Main App Layout
# ---------------------------------------------------------------------------------------------

st.title("Dashboard de Habilidades")

# Define options for the selectors
vertical_options = list(df["nueva_vertical"].unique()) + ["TODOS"]
rol_options = list(df["rol"].unique()) + ["TODOS"]


selected_vertical = st.sidebar.selectbox(
    label="Seleccionar Vertical",
    options=vertical_options,
)

selected_rol = st.sidebar.selectbox(
    label="Seleccionar Rol",
    options=rol_options
)

# --- Data Filtering ---
# Filter the data based on selections. This happens every time a widget is changed.
df_filtered = filtrar(df, selected_vertical, selected_rol)

# --- Tabs ---
# Streamlit's st.tabs is a direct replacement for dcc.Tabs
tab1, tab2, tab3 = st.tabs(["Soft Skills", "Tech Skills", "Overview"], width="stretch")


# --- Tab 1: Soft Skills Content ---
with tab1:
    st.header("Análisis de Soft Skills")

    # Check if the filtered DataFrame is empty
    if df_filtered.empty:
        st.warning("No hay datos para la selección actual.")
    else:
        # Get the figures from your 'soft' module
        fig1, fig2, fig3, fig4, fig5 = soft.get_soft_skills_scores_figs(df_filtered)

        # Create a 2x2 grid layout using st.columns
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            st.plotly_chart(fig1, use_container_width=True)
        with row1_col2:
            st.plotly_chart(fig2, use_container_width=True)

        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            st.plotly_chart(fig3, use_container_width=True)
        with row2_col2:
            st.plotly_chart(fig4, use_container_width=True)

        st.plotly_chart(fig5, use_container_width=True)

        


# --- Tab 2: Tech Skills Content ---
with tab2:
    st.header("Análisis de Habilidades Técnicas")
    
    # Check if the filtered DataFrame is empty
    if df_filtered.empty:
        st.warning("No hay datos para la selección actual.")
    else:
        # Get the figures from your 'tech' and 'tech_' modules
        tech_fig_1 = tech.get_tech_skills_scores_figs(df_filtered)
        tech_fig_2 = tech_.get_tech_scores_figs(df_filtered)

        # Display the charts one after another
        st.plotly_chart(tech_fig_1, use_container_width=True)
        st.plotly_chart(tech_fig_2, use_container_width=True)

# --- Tab 3: Overwiev Content ---
with tab3:
    st.header("Análisis General")
    
    # Check if the filtered DataFrame is empty
    if df_filtered.empty:
        st.warning("No hay datos para la selección actual.")
    else:
        df_dicts = extract_all_airtable(tables_id = tables_id)
        # Get the figures from your 'tech' and 'tech_' modules
        overview_fig_1 = overview_.primera_grafica(df_dicts = df_dicts)
        overview_fig_2 = overview_.segunda_grafica(df_dicts = df_dicts)
        overview_fig_3 = overview_.grafica_veredicto_vertical(df_dicts = df_dicts)

        # Display the charts one after another
        st.plotly_chart(overview_fig_1, use_container_width=True)
        st.plotly_chart(overview_fig_2, use_container_width=True)
        st.plotly_chart(overview_fig_3, use_container_width=True)



