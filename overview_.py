import numpy as np
import pandas as pd
import plotly.express as px

def primera_grafica(df_dicts):
    
    df = df_dicts["Trabajadores"][["Nombre", "Certificaciones", "Certificaciones (from Rol que le corresponde)", "Certificaciones faltantes para el rol (INFORME)", "Nueva vertical"]]
    
    for col in df.columns:
    
        df[col] = df[col].apply(lambda x : list(set(x)) if type(x) == list else x)
    
    df["Certificaciones Totales"] = df["Certificaciones"].apply(lambda x : len(x) if type(x) == list else 0)
    
    df["Certificaciones Totales por Rol"] = df["Certificaciones (from Rol que le corresponde)"].apply(lambda x : len(x) if type(x) == list else 0)
    
    df["Certificaciones Faltantes"] = df["Certificaciones faltantes para el rol (INFORME)"].apply(lambda x : len(x) if type(x) == list else 0)
    
    df["Porcentaje Certificaciones Faltantes"] = np.round(df["Certificaciones Faltantes"] / df["Certificaciones Totales por Rol"] * 100, 2)
    
    df = pd.merge(left = df.explode("Nueva vertical"), right = df_dicts["Verticales"][["id", "Vertical"]], left_on = "Nueva vertical", right_on = "id", how = "left")
    
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
                 title      = "Procentaje de Certificaciones Finalizadas por Vertical")
    
    fig.update_layout(xaxis = dict(title = dict(text = "Vertical")),
                      yaxis = dict(title = dict(text = "% Certificaciones Finalizadas")))
    
    return fig

def segunda_grafica(df_dicts):
    df = pd.merge(left = df_dicts["Trabajadores"].explode("Nivel").drop("id", axis = 1),
              right = df_dicts["Roles"][["id", "Nivel de carrera MAPFRE"]],
              left_on = "Nivel",
              right_on = "id")

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
             title      = "Procentaje de Certificaciones Finalizadas por Nivel")

    fig.update_layout(xaxis = {"title" : {"text" : "Nivel"}},
                    yaxis = {"title" : {"text" : "% Certificaciones Finalizadas"}})

    return fig