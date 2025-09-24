import string

import numpy as np
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from utils import get_color

def extract_comp_data(comp: str) -> tuple[str, int]:
    """Extrae información de las competencias blandas. Retorna la competencia en cuestion y el nivel en formato tupla."""
    parts = comp.split("-")
    comp_str = ""
    for part in parts[:-1]:
        comp_str += "".join([char for char in part if char.isalpha() or char.isspace() or char in string.punctuation]).strip()
    lvl = parts[-1].strip()
    lvl_map = {
        "Avanzado" : 3,
        "Medio" : 2,
        "Básico" : 1
    }
    return comp_str, lvl_map[lvl]

def get_required_levels(row: pd.Series, required_skills_col: str):
    """Callback que extrae los niveles de la competencias necesarias, proporcionado el nombre de la columna que las guarda."""
    required_skills = [extract_comp_data(comp) for comp in row[required_skills_col]]
    return {skill: level for skill, level in required_skills}

def score_dataframe(df: pd.DataFrame, actual_skills_col="tecnologias", required_skills_col="tecnologias_necesarias"):
    """Calcula el promedio de las competencias blandas y los compara con el nivel necesario."""

    # Calculate the required skill levels for each row
    df['required_levels'] = df.apply(lambda row: get_required_levels(row, required_skills_col), axis=1)

    # Extract all soft skills and their levels
    all_skills = []
    for _, row in df.iterrows():
        for comp in row[actual_skills_col]:
            skill, level = extract_comp_data(comp)
            all_skills.append((skill, level))

    # Calculate the average level for each soft skill
    skill_levels = {}
    for skill, level in all_skills:
        if skill in skill_levels:
            skill_levels[skill].append(level)
        else:
            skill_levels[skill] = [level]

    average_levels = {skill: np.mean(levels) for skill, levels in skill_levels.items()}
    std_dev_levels = {skill: np.std(levels) for skill, levels in skill_levels.items()}

    # Find the "average" required level
    required_levels = {}
    for _, row in df.iterrows():
        for skill, level in row['required_levels'].items():
            if skill in required_levels:
                required_levels[skill].append(level)
            else:
                required_levels[skill] = [level]

    most_common_required = {skill: max(set(levels), key=levels.count) for skill, levels in required_levels.items()}

    return average_levels, std_dev_levels, most_common_required

def get_tech_scores_figs(df, filter_colors):
    """Toma un dataframe filtrado y hace un plot de las competencias tecnicas de cada candidato."""
    df_dropped = df.dropna(subset=["competencias_tecnicas", "competencias_tecnicas_necesarias"])
    average_levels, std_levels, required_levels = score_dataframe(df_dropped)

    average_levels = {k: average_levels[k] if k in average_levels.keys() else 0 for k in required_levels.keys()}
    std_levels = {k: std_levels[k] if k in std_levels.keys() else 0 for k in required_levels.keys()}
        
    colors = [get_color(average_levels[skill], required_levels[skill])
            for skill in required_levels]
    # colors = [c for c in colors if c in filter_colors]
    
    std_levels = [v for v in std_levels.values()]

    average_levels = {k : v for k, v in average_levels.items()}

    map_color = {"#FF0000" : "Muy por debajo del nivel",
                 "#FFFF00" : "Ligeramente por debajo del nivel",
                 "#013220" : "Sobrepasa el nivel",
                 "#90EE90" : "Cumple con el nivel"}
    df_grafica = pd.DataFrame()
    df_grafica["skill"] = average_levels.keys()
    df_grafica["avg"] = np.round(list(average_levels.values()), 2)
    df_grafica["std"] = std_levels
    df_grafica["color"] = colors
    df_grafica["inv_color"] = df_grafica["color"].apply(lambda x : map_color[x])

    df_grafica = df_grafica[df_grafica["color"].isin(filter_colors)]

    fig = px.bar(
        df_grafica,
        x="skill",
        y="avg",
        color="inv_color",
        error_y="std",
        text="avg",
        color_discrete_map = {"Muy por debajo del nivel"         : "#FF0000",
                     "Ligeramente por debajo del nivel" : "#FFFF00",
                     "Sobrepasa el nivel"               : "#013220",
                     "Cumple con el nivel"              : "#90EE90"}
    
)
    fig.update_traces(textposition="inside", insidetextanchor = "start")
   
    # Update layout properties
    fig.update_layout(
        title_text=f"Tecnologías (n={df_dropped.shape[0]})",
        yaxis_title='Nivel Promedio: Muy bajo (0) - Muy alto (4)',
        yaxis_range=[0, 4],
        legend_title_text = "",
        showlegend=True # Hide legend as colors are informational
    )
        
    return fig
