import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


def primera_grafica(df_filtered, df_dicts):

    df_prueba_tecnica = pd.merge(left = df_filtered, right = df_dicts["Pruebas técnicas"].explode("Trabajador/a"), left_on = "id", right_on = "Trabajador/a")
    df_prueba_tecnica = df_prueba_tecnica.explode("Nueva vertical Rollup (from Trabajador/a)")
    df_prueba_tecnica["Puntaje final IA"] = df_prueba_tecnica["Puntaje final IA"].replace("N/A", np.nan).astype("float")
    df_prueba_tecnica = df_prueba_tecnica.groupby(by       = ["Nueva vertical Rollup (from Trabajador/a)", "Resultado de la prueba", "¿Se ha usado IA?", "¿Ha copiado?"],
                                                  as_index = False).agg({"Puntaje técnico"                   : ["count", "std"],
                                                                         "Puntaje Negocio"                   : ["count", "std"],
                                                                         "Prueba conocimientos generales IA" : ["count", "std"],
                                                                         "Puntaje final IA"                  : ["count", "std"]})

    df_prueba_tecnica.columns = [x[0] if x[1] == "" else "_".join(x) for x in df_prueba_tecnica.columns]

    fig = px.bar(data_frame = df_prueba_tecnica[df_prueba_tecnica["Resultado de la prueba"] != "Problemas prueba"],
             x          = "Resultado de la prueba",
             y          = "Puntaje técnico_count",
             color      = "¿Ha copiado?")

    return fig

def segunda_grafica(df_filtered, df_dicts):

    df_prueba_tecnica = pd.merge(left = df_filtered, right = df_dicts["Pruebas técnicas"].explode("Trabajador/a"), left_on = "id", right_on = "Trabajador/a")
    df_prueba_tecnica = df_prueba_tecnica.explode("Nueva vertical Rollup (from Trabajador/a)")
    df_prueba_tecnica["Puntaje final IA"] = df_prueba_tecnica["Puntaje final IA"].replace("N/A", np.nan).astype("float")
    df_prueba_tecnica = df_prueba_tecnica.groupby(by       = ["Nueva vertical Rollup (from Trabajador/a)", "Resultado de la prueba", "¿Se ha usado IA?", "¿Ha copiado?"],
                                                  as_index = False).agg({"Puntaje técnico"                   : ["count", "std"],
                                                                         "Puntaje Negocio"                   : ["count", "std"],
                                                                         "Prueba conocimientos generales IA" : ["count", "std"],
                                                                         "Puntaje final IA"                  : ["count", "std"]})

    df_prueba_tecnica.columns = [x[0] if x[1] == "" else "_".join(x) for x in df_prueba_tecnica.columns]

    fig = px.bar(data_frame = df_prueba_tecnica[df_prueba_tecnica["Resultado de la prueba"] != "Problemas prueba"],
             x          = "Resultado de la prueba",
             y          = "Puntaje técnico_count",
             color      = "¿Se ha usado IA?")

    return fig