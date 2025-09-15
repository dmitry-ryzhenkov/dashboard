import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

def primera_grafica(df_filtered, df_dicts):

    df = df_dicts["Trabajadores"][["id", "Nombre", "Certificaciones", "Certificaciones (from Rol que le corresponde)", "Certificaciones faltantes para el rol (INFORME)", "Nueva vertical"]]
    
    for col in df.columns:
    
        df[col] = df[col].apply(lambda x : list(set(x)) if type(x) == list else x)
    
    df["Certificaciones Totales"] = df["Certificaciones"].apply(lambda x : len(x) if type(x) == list else 0)
    
    df["Certificaciones Totales por Rol"] = df["Certificaciones (from Rol que le corresponde)"].apply(lambda x : len(x) if type(x) == list else 0)
    
    df["Certificaciones Faltantes"] = df["Certificaciones faltantes para el rol (INFORME)"].apply(lambda x : len(x) if type(x) == list else 0)
    
    df["Porcentaje Certificaciones Faltantes"] = np.round(df["Certificaciones Faltantes"] / df["Certificaciones Totales por Rol"] * 100, 2)
    
    df = pd.merge(left = df.explode("Nueva vertical"), right = df_dicts["Verticales"][["id", "Vertical"]], left_on = "Nueva vertical", right_on = "id", how = "left")

    df = pd.merge(left = df_filtered, right = df, left_on = "id", right_on = "id_x", how = "left")
    
    df_resultado = df.groupby(by = ["Vertical"], as_index = False).agg({"Porcentaje Certificaciones Faltantes" : "mean"})
    
    df_resultado["Porcentaje Certificaciones Faltantes"] = df_resultado["Porcentaje Certificaciones Faltantes"].clip(lower = 0, upper = 100)
    df_resultado["Porcentaje Certificaciones Realizadas"] = 100 - df_resultado["Porcentaje Certificaciones Faltantes"].clip(lower = 0, upper = 100)
    
    df_resultado[["Porcentaje Certificaciones Faltantes", "Porcentaje Certificaciones Realizadas"]] = df_resultado[["Porcentaje Certificaciones Faltantes", "Porcentaje Certificaciones Realizadas"]].round(decimals = 2)
    
    df_resultado = df_resultado.sort_values("Porcentaje Certificaciones Faltantes")
    
    fig = px.bar(data_frame = df_resultado,
                 x          = "Vertical",
                 y          = "Porcentaje Certificaciones Realizadas",
                 range_y    = [0, 100],
                 text_auto  = True,
                 title      = "Procentaje de Certificaciones Realizadas por Vertical")
    
    fig.update_layout(xaxis = dict(title = dict(text = "Vertical")),
                      yaxis = dict(title = dict(text = "% Certificaciones Realizadas")))
    
    return fig

def segunda_grafica(df_filtered, df_dicts):
    df = pd.merge(left = df_dicts["Trabajadores"].explode("Nivel"),
              right = df_dicts["Roles"][["id", "Nivel de carrera MAPFRE"]],
              left_on = "Nivel",
              right_on = "id")
    
    df = pd.merge(left = df_filtered, right = df, left_on = "id", right_on = "id_x", how = "left")

    df = df[["Certificaciones", "Certificaciones (from Rol que le corresponde)", "Certificaciones faltantes para el rol (INFORME)", "Nivel de carrera MAPFRE"]]

    puestos_orden = ["TÉCNICO AVANZADO",
                    "TÉCNICO SENIOR",
                    "ESPECIALISTA",
                    "EXPERTO",
                    "CONSULTOR",
                    "RESPONSABLE",
                    "JEFE",
                    "SUBDIRECTOR",
                    "DIRECTOR"]

    df["Nivel de carrera MAPFRE"] = pd.Categorical(df["Nivel de carrera MAPFRE"], categories = puestos_orden, ordered = True)
    df = df.sort_values("Nivel de carrera MAPFRE")

    df = df.reset_index(drop = True)

    df["Certificaciones Totales"] = df["Certificaciones"].apply(lambda x : len(x) if type(x) == list else 0)

    df["Certificaciones Totales por Rol"] = df["Certificaciones (from Rol que le corresponde)"].apply(lambda x : len(x) if type(x) == list else 0)

    df["Certificaciones Faltantes"] = df["Certificaciones faltantes para el rol (INFORME)"].apply(lambda x : len(x) if type(x) == list else 0)

    df["Porcentaje Certificaciones Faltantes"] = np.round(df["Certificaciones Faltantes"] / df["Certificaciones Totales por Rol"] * 100, 2)

    df_resultado = df.groupby(by = ["Nivel de carrera MAPFRE"], as_index = False).agg({"Porcentaje Certificaciones Faltantes" : "mean"})

    df_resultado["Porcentaje Certificaciones Faltantes"] = df_resultado["Porcentaje Certificaciones Faltantes"].clip(lower = 0, upper = 100)
    df_resultado["Porcentaje Certificaciones Realizadas"] = 100 - df_resultado["Porcentaje Certificaciones Faltantes"].clip(lower = 0, upper = 100)

    df_resultado[["Porcentaje Certificaciones Faltantes", "Porcentaje Certificaciones Realizadas"]] = df_resultado[["Porcentaje Certificaciones Faltantes", "Porcentaje Certificaciones Realizadas"]].round(decimals = 2)

    fig = px.bar(data_frame = df_resultado,
             x          = "Nivel de carrera MAPFRE",
             y          = "Porcentaje Certificaciones Realizadas",
             range_y    = [0, 100],
             text_auto  = True,
             title      = "Procentaje de Certificaciones Realizadas por Nivel")

    fig.update_layout(xaxis = {"title" : {"text" : "Nivel"}},
                    yaxis = {"title" : {"text" : "% Certificaciones Realizadas"}})

    return fig

# Vertical y Veredicto
def grafica_veredicto_vertical(df_filtered, df_dicts):

    df_func = pd.merge(left = df_filtered, right = df_dicts["Trabajadores"].explode("Nueva vertical"), left_on = "id", right_on = "id", how = "left")

    df_vertical_veredicto = pd.merge(left = df_func.groupby(by = ["Nueva vertical", "Veredicto"], as_index = False).agg({"id" : "count"}),
                                    right = df_dicts["Verticales"][["id", "Vertical"]],
                                    left_on = "Nueva vertical",
                                    right_on = "id")[["Vertical", "Veredicto", "id_x"]]
    
    df_vertical_veredicto.columns = ["Vertical", "Veredicto", "count"]
    
    veredicto_orden = ["Cumple con el nivel y vertical asignado",
                    "Cumple la vertical, pero no con el nivel asignado",
                    "Excede el nivel de la vertical prevista",
                    "Cumple con el nivel, pero no con la vertical asignada",
                    "No cumple con nivel, ni vertical previsto"]
    
    df_vertical_veredicto["Veredicto"] = pd.Categorical(df_vertical_veredicto["Veredicto"], categories = veredicto_orden, ordered = True)
    df_vertical_veredicto = df_vertical_veredicto.sort_values("Veredicto")
    
    fig = px.bar(data_frame = df_vertical_veredicto, x = "Veredicto", y = "count", color = "Vertical")

    return fig

# Rol y Veredicto
def grafica_veredicto_rol(df_filtered, df_dicts):

    df_func = pd.merge(left = df_filtered, right = df_dicts["Trabajadores"].explode("Nuevo puesto"), left_on = "id", right_on = "id", how = "left")
    
    df_rol_veredicto = pd.merge(left = df_func.groupby(by = ["Nuevo puesto", "Veredicto"], as_index = False).agg({"id" : "count"}),
                                right = df_dicts["Roles"][["Nivel de carrera MAPFRE", "Puesto"]],
                                left_on = "Nuevo puesto",
                                right_on = "Puesto")[["Nivel de carrera MAPFRE", "Veredicto", "id"]]

    df_rol_veredicto.columns = ["Rol", "Veredicto", "count"]

    veredicto_orden = ["Cumple con el nivel y vertical asignado",
                    "Cumple la vertical, pero no con el nivel asignado",
                    "Excede el nivel de la vertical prevista",
                    "Cumple con el nivel, pero no con la vertical asignada",
                    "No cumple con nivel, ni vertical previsto"]

    df_rol_veredicto["Veredicto"] = pd.Categorical(df_rol_veredicto["Veredicto"], categories = veredicto_orden, ordered = True)
    df_rol_veredicto = df_rol_veredicto.sort_values("Veredicto")

    return px.bar(data_frame = df_rol_veredicto, x = "Veredicto", y = "count", color = "Rol")