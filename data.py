import requests

import numpy as np
import pandas as pd

from utils import replace_ids_with_names

import streamlit as st

# DATA -------------------------------------------------------------------------
def extract_airtable(app: str, tbl: str, token: str) -> pd.DataFrame:
    url = f"https://api.airtable.com/v0/{app}/{tbl}"

    response = requests.get(url, headers={"Authorization" : f"Bearer {token}"})
    data = response.json()
    records = data["records"]

    while "offset" in data.keys():
        r = requests.get(url, headers={"Authorization" : f"Bearer {token}"}, params={"offset" : data["offset"]})
        data = r.json()
        records.extend(data["records"])

    return pd.json_normalize(records)

def load_data() -> pd.DataFrame:

    AIRTABLE_API_KEY = st.secrets.get("AIRTABLE_API_KEY")

    app_id = "appACxf1z2b7fsR44"
    table_id = "tblNBHV9KDGDQNs8y"
    df = extract_airtable(app_id, table_id, AIRTABLE_API_KEY)

    # -------------------------------------

    table_id = "tblk2itGEWE7ePo73"
    df_roles = extract_airtable(app_id, table_id, AIRTABLE_API_KEY)

    # -------------------------------------

    table_id = "tblXhF1lZUBKiNixP"
    df_tecnologias = extract_airtable(app_id, table_id, AIRTABLE_API_KEY)

    # -------------------------------------

    table_id = "tblLUDGmhm7otZhGp"
    df_comp_tecnicas = extract_airtable(app_id, table_id, AIRTABLE_API_KEY)

    # -------------------------------------

    table_id = "tblvuUUjjnUvdS1z1"
    df_comp_blandas = extract_airtable(app_id, table_id, AIRTABLE_API_KEY)

    # -------------------------------------

    # table_id = "tblGy8pLPexkcpJcq"
    # df_prubas_tec = extract_airtable(app_id, table_id, AIRTABLE_API_KEY)

    # -------------------------------------

    table_id = "tblDZzmvFmWfMbmx5"
    df_vert = extract_airtable(app_id, table_id, AIRTABLE_API_KEY)

    # CLEANING -------------------------------------------------------------------------
    print(f"\n\n\n\nDATAFRAME\n\n\n\n")
    for col in df.columns:
        print(col, end=" | ")
    print(f"\n\n\n\n")

    df = df[[
        "id", "fields.Nombre", "fields.Status", "fields.Email",
        "fields.Nivel de carrera",
        "fields.Rol que le corresponde",
        "fields.Puesto actual", "fields.Nueva vertical", "fields.Veredicto", "fields.Equipo",
        "fields.Resultado de la prueba (from Pruebas técnicas)",
        "fields.TEC necesarias (from Rol que le corresponde)", "fields.Tecnologías actuales Selección IT",
        "fields.CompT necesarias (from Rol que le corresponde)", "fields.Competencias técnicas Selección IT",
        "fields.Competencia blanda (from Rol que le corresponde)", "fields.Competencias blandas Selección IT",
        "fields.Puntaje Negocio (from Pruebas técnicas)",
        "fields.Edad", 
        "fields.Antigüedad",
        "fields.Sexo",
        "fields.Bloques",
        "fields.Área",
        "fields.Nivel de carrera MAPFRE (from Rol que le corresponde)"
        ]]
    
    df.columns = df.columns.str.lower().str.replace("fields.", "")

    rename = {
        "nivel de carrera" : "rol",
        "resultado de la prueba (from pruebas técnicas)" : "prueba_tecnica",
        "tec necesarias (from rol que le corresponde)" : "tecnologias_necesarias",
        "tecnologías actuales selección it" : "tecnologias",
        "compt necesarias (from rol que le corresponde)" : "competencias_tecnicas_necesarias",
        "competencias técnicas selección it" : "competencias_tecnicas",
        "competencia blanda (from rol que le corresponde)" : "competencias_blandas_necesarias",
        "competencias blandas selección it" : "competencias_blandas",
        "puntaje negocio (from pruebas técnicas)" : "prueba_negocio",
        "sexo" : "sexo",
        "edad" : "edad",
        "antigüedad" : "antiguedad",
        "bloques" : "bloque",
        "área" : "area",
        "nivel de carrera mapfre (from rol que le corresponde)" : "nivel"
    }
    
    df = df.rename(columns=rename)
    df.columns = df.columns.str.replace(" ", "_")
    # -------------------------------------

    df.loc[: ,["rol", "rol_que_le_corresponde", "nueva_vertical", "prueba_tecnica", "prueba_negocio"]] = df[["rol", "rol_que_le_corresponde", "nueva_vertical", "prueba_tecnica", "prueba_negocio"]].map(lambda x: x[0] if isinstance(x, list) else np.nan)
    df = df[df["status"] == "Evaluación completada"]

    # -------------------------------------

    df = pd.merge(left=df, right=df_roles[["id", "fields.Nivel de carrera MAPFRE"]], left_on="rol", right_on="id", how="left", suffixes=["", "_ext"]).drop(["id_ext", "rol"], axis=1)
    df = df.rename(columns={"fields.Nivel de carrera MAPFRE" : "rol"})

    df = pd.merge(left=df, right=df_roles[["id", "fields.Nivel de carrera MAPFRE"]], left_on="rol_que_le_corresponde", right_on="id", how="left", suffixes=["", "_ext"]).drop(["id_ext", "rol_que_le_corresponde"], axis=1)
    df = df.rename(columns={"fields.Nivel de carrera MAPFRE" : "rol_que_le_corresponde"})

    df = pd.merge(left=df, right=df_vert[["id", "fields.Vertical"]], left_on="nueva_vertical", right_on="id", how="left", suffixes=["", "_ext"]).drop(["id_ext", "nueva_vertical"], axis=1)
    df = df.rename(columns={"fields.Vertical" : "nueva_vertical"})

    # -------------------------------------

    df = replace_ids_with_names(df, df_tecnologias, "id", "fields.Nombre", "tecnologias")
    df = replace_ids_with_names(df, df_tecnologias, "id", "fields.Nombre", "tecnologias_necesarias")

    df = replace_ids_with_names(df, df_comp_tecnicas, "id", "fields.Nombre", "competencias_tecnicas_necesarias")
    df = replace_ids_with_names(df, df_comp_tecnicas, "id", "fields.Nombre", "competencias_tecnicas")

    df = replace_ids_with_names(df, df_comp_blandas, "id", "fields.Nombre", "competencias_blandas_necesarias")
    df = replace_ids_with_names(df, df_comp_blandas, "id", "fields.Nombre", "competencias_blandas")

    return df

# -------------------------------------

def extract_all_airtable(tables_id: dict) -> dict:

    AIRTABLE_API_KEY = st.secrets.get("AIRTABLE_API_KEY")

    app_id = "appACxf1z2b7fsR44"

    df_dicts = dict()
    for k, v in tables_id.items():
        
        df_bucle = extract_airtable(app = app_id, tbl = v, token = AIRTABLE_API_KEY).drop(["createdTime"], axis = 1)

        df_bucle.columns = [col.replace("fields.", "") for col in df_bucle.columns]

        df_dicts[k] = df_bucle
        
    return df_dicts