import string

import numpy as np
import pandas as pd

import plotly.graph_objects as go

from utils import get_color
import streamlit as st

def extract_comp_data(comp: str) -> tuple[str, int]:
    """Extrae información de las competencias blandas. Retorna la competencia en cuestion y el nivel en formato tupla."""
    parts = comp.split("-")
    comp_str = "".join([char for char in parts[0] if char.isalpha() or char.isspace() or char in string.punctuation]).strip()
    lvl = parts[1].strip()
    lvl_map = {
        "Participa y colabora" : 1,
        "Desarrolla y aplica" : 2,
        "Gestiona técnica o funcionalmente" : 3,
        "Gestiona y diseña técnica y funcionalmente" : 4,
        "Lidera" : 5
    }
    return comp_str, lvl_map[lvl]

def get_required_levels(row: pd.Series, required_skills_col: str):
    """Callback que extrae los niveles de la competencias necesarias, proporcionado el nombre de la columna que las guarda."""
    required_skills = [extract_comp_data(comp) for comp in row[required_skills_col]]
    return {skill: level for skill, level in required_skills}

def score_dataframe(df: pd.DataFrame, actual_skills_col="competencias_tecnicas", required_skills_col="competencias_tecnicas_necesarias"):
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

def get_tech_skills_scores_figs(df, filter_colors):
    """Toma un dataframe filtrado y hace un plot de las competencias tecnicas de cada candidato."""
    df_dropped = df.dropna(subset=["competencias_tecnicas", "competencias_tecnicas_necesarias"])
    average_levels, std_levels, required_levels = score_dataframe(df_dropped)

    average_levels = {k: average_levels[k] if k in average_levels.keys() else 0 for k in required_levels.keys()}
    std_levels = {k: std_levels[k] if k in std_levels.keys() else 0 for k in required_levels.keys()}
        
    colors = [get_color(average_levels[skill], required_levels[skill])
            for skill in required_levels]

    std_levels = [v for v, c in zip(std_levels.values(), colors) if c in filter_colors]

    average_levels = {k : v for (k, v), c in zip(average_levels.items(), colors) if c in filter_colors}

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(average_levels.keys()),
        y=list(average_levels.values()),
        # This is the key part for adding error bars
        error_y=dict(
            type='data',
            array=list(std_levels),
            visible=True,
            color='gray',  # Optional: style the error bars
            thickness=1.5
        ),
        # Use marker_color to pass your custom color list
        marker_color=colors
    ))
    
    # Update layout properties
    fig.update_layout(
        title_text=f"Competencias Técnicas (n={df_dropped.shape[0]})",
        yaxis_title='Nivel Promedio: Muy bajo (0) - Muy alto (4)',
        yaxis_range=[0, 6],
        showlegend=False # Hide legend as colors are informational
    )
        
    return fig