import streamlit as st

# Import your custom modules
from tables import tables_id
from utils import filtrar
from data import load_data, extract_all_airtable
import soft
import tech
import tech_
import overview_
import pruebas_tecnicas
import pandas as pd

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

@st.cache_data
def cached_extract_all_data():
    return extract_all_airtable(tables_id = tables_id)

df_dicts = cached_extract_all_data()

# ---------------------------------------------------------------------------------------------
# Main App Layout
# ---------------------------------------------------------------------------------------------

st.title("Dashboard de Habilidades")

# Define options for the selectors
vertical_options = list(df["nueva_vertical"].unique()) + ["TODOS"]
rol_options = list(df["rol_que_le_corresponde"].unique()) + ["TODOS"]
sexo_options = ["M", "V"] + ["AMBOS"]
niveL_carrera_options = ["TODOS"]

dict_filtros = {"Vertical"       : [],
                "Rol"            : [],
                "Min Antiguedad" : 0,
                "Max Antiguedad" : 0,
                # "Nivel Carrera"  : niveL_carrera_options[-1],
                "Min Edad"       : 0,
                "Max Edad"       : 0,
                "Sexo"           : sexo_options[-1]}

with st.sidebar.form(key = "Filtros"):

    selected_vertical = st.multiselect(label  = "Vertical",
                                      options = vertical_options)
    
    selected_rol = st.multiselect(label   = "Rol",
                                  options = rol_options)
    
    selected_min_antiguedad = st.number_input(label     = "Min Antiguedad",
                                              min_value = 0,
                                              max_value = 50,
                                              value     = 0,
                                              step      = 1)
    
    selected_max_antiguedad = st.number_input(label     = "Max Antiguedad",
                                              min_value = 0,
                                              max_value = 50,
                                              value     = 0,
                                              step      = 1)
    
    # selected_nivel_carrera = st.selectbox(label   = "Nivel Carrera",
    #                                       options = niveL_carrera_options)
    
    selected_min_age = st.number_input(label     = "Min Edad",
                                       min_value = 0,
                                       max_value = 99,
                                       value     = 0,
                                       step      = 1)
    selected_max_age = st.number_input(label     = "Max Edad",
                                       min_value = 0,
                                       max_value = 99,
                                       value     = 0,
                                       step      = 1)
    
    selected_sex = st.selectbox(label   = "Sexo",
                                options = sexo_options,
                                index = len(sexo_options) - 1)

    submitted = st.form_submit_button(label = "Aplicar")
    if submitted:
        dict_filtros = {"Vertical"       : selected_vertical,
                        "Rol"            : selected_rol,
                        "Min Antiguedad" : selected_min_antiguedad,
                        "Max Antiguedad" : selected_max_antiguedad,
                        # "Nivel Carrera"  : selected_nivel_carrera,
                        "Min Edad"       : selected_min_age,
                        "Max Edad"       : selected_max_age,
                        "Sexo"           : selected_sex}
    
    
# --- Data Filtering ---
# Filter the data based on selections. This happens every time a widget is changed.
df_filtered = filtrar(df = df, dict_filtros = dict_filtros)

# --- Tabs ---
# Streamlit's st.tabs is a direct replacement for dcc.Tabs
tab1, tab2, tab3, tab4 = st.tabs(tabs = ["Soft Skills", "Tech Skills", "Overview", "Tech Test"],
                                 width = "stretch")


# --- Tab 1: Soft Skills Content ---
with tab1:
    st.header("Análisis de Soft Skills")

    # Check if the filtered DataFrame is empty
    if df_filtered.empty:
        st.warning("No hay datos para la selección actual.")
    else:

        filter_colors = st.multiselect(label = "Filtro", key = 123,
                                       options = ["Cumple con el nivel", "Sobrepasa el nivel", "Ligeramente por debajo del nivel", "Muy por debajo del nivel"],
                                       default = ["Cumple con el nivel", "Sobrepasa el nivel", "Ligeramente por debajo del nivel", "Muy por debajo del nivel"])
        
        map_color = {"Muy por debajo del nivel"         : "#CD5C5C",
                     "Ligeramente por debajo del nivel" : "#BDB76B",
                     "Sobrepasa el nivel"               : "#6495ED",
                     "Cumple con el nivel"              : "#8FBC8F"}
        
        filter_colors = [map_color[color] for color in filter_colors]

        # Get the figures from your 'soft' module
        fig1, fig2, fig3, fig4, fig5 = soft.get_soft_skills_scores_figs(df_filtered, filter_colors)

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
    
        fig6 = soft.sexta_grafica(df = df_filtered, filter_colors = filter_colors)
        st.plotly_chart(fig6, use_container_width=True)

        


# --- Tab 2: Tech Skills Content ---
with tab2:
    st.header("Análisis de Habilidades Técnicas")

    map_color = {"#CD5C5C" : "Muy por debajo del nivel",
                 "#BDB76B" : "Ligeramente por debajo del nivel",
                 "#6495ED" : "Sobrepasa el nivel",
                 "#8FBC8F" : "Cumple con el nivel"}


    filter_colors = st.multiselect(label = "Filtro",
                                   options = ["Cumple con el nivel", "Sobrepasa el nivel", "Ligeramente por debajo del nivel", "Muy por debajo del nivel"],
                                   default = ["Cumple con el nivel", "Sobrepasa el nivel", "Ligeramente por debajo del nivel", "Muy por debajo del nivel"])
    
    map_color = {"Muy por debajo del nivel" : "#CD5C5C",
                 "Ligeramente por debajo del nivel" : "#BDB76B",
                 "Sobrepasa el nivel" : "#6495ED",
                 "Cumple con el nivel" : "#8FBC8F"}
    
    filter_colors = [map_color[color] for color in filter_colors]


    
    # Check if the filtered DataFrame is empty
    if df_filtered.empty:
        st.warning("No hay datos para la selección actual.")
    else:
        # Get the figures from your 'tech' and 'tech_' modules
        tech_fig_1 = tech.get_tech_skills_scores_figs(df_filtered, filter_colors)
        tech_fig_2 = tech_.get_tech_scores_figs(df_filtered, filter_colors)
        tech_fig_3 = tech.quinta_grafica(df_filtered = df_filtered, df_dicts = df_dicts)

        # Display the charts one after another
        st.plotly_chart(tech_fig_1, use_container_width=True)
        st.plotly_chart(tech_fig_2, use_container_width=True)
        st.plotly_chart(tech_fig_3, use_container_width=True)

# --- Tab 3: Overwiev Content ---
with tab3:
    st.header("Análisis General")
    
    # Check if the filtered DataFrame is empty
    if df_filtered.empty:
        st.warning("No hay datos para la selección actual.")
    else:
        # Get the figures from your 'tech' and 'tech_' modules
        overview_fig_1 = overview_.primera_grafica(df_filtered = df_filtered, df_dicts = df_dicts)
        overview_fig_2 = overview_.segunda_grafica(df_filtered = df_filtered, df_dicts = df_dicts)
        overview_fig_3 = overview_.grafica_veredicto_vertical(df_filtered = df_filtered, df_dicts = df_dicts)
        overview_fig_4 = overview_.grafica_veredicto_rol(df_filtered = df_filtered, df_dicts = df_dicts)
        overview_fig_5 = overview_.quinta_grafica(df_filtered = df_filtered, df_dicts = df_dicts)

        # Display the charts one after another
        st.plotly_chart(overview_fig_1, use_container_width=True)
        st.plotly_chart(overview_fig_2, use_container_width=True)
        st.plotly_chart(overview_fig_3, use_container_width=True)
        st.plotly_chart(overview_fig_4, use_container_width=True)
        st.plotly_chart(overview_fig_5, use_container_width=True)

# --- Tab 4: Tech test Content ---
with tab4:
    st.header("Pruebas Técnicas")
    # Check if the filtered DataFrame is empty
    if df_filtered.empty:
        st.warning("No hay datos para la selección actual.")
    else:
        
        prueba_tecnica_fig_1 = pruebas_tecnicas.primera_grafica(df_filtered = df_filtered, df_dicts = df_dicts)
        prueba_tecnica_fig_2 = pruebas_tecnicas.segunda_grafica(df_filtered = df_filtered, df_dicts = df_dicts)
        # Get the figures from your 'tech' and 'tech_' modules
        # overview_fig_1 = overview_.primera_grafica(df_dicts = df_dicts)
        # overview_fig_2 = overview_.segunda_grafica(df_dicts = df_dicts)
        # overview_fig_3 = overview_.grafica_veredicto_vertical(df_dicts = df_dicts)
        # overview_fig_4 = overview_.grafica_veredicto_rol(df_dicts = df_dicts)

        # # Display the charts one after another
        st.plotly_chart(prueba_tecnica_fig_1, use_container_width=True)
        st.plotly_chart(prueba_tecnica_fig_2, use_container_width=True)
        # st.plotly_chart(overview_fig_3, use_container_width=True)
        # st.plotly_chart(overview_fig_4, use_container_width=True)
