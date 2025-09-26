import pandas as pd

def replace_ids_with_names(df1, df2, id_col, name_col, list_col):
    df1 = df1.copy()
    id_to_name = pd.Series(df2[name_col].values, index=df2[id_col]).to_dict()

    def replace_ids_in_list(id_list):
        if isinstance(id_list, list):
            return [name for id in id_list if (name := id_to_name.get(id)) is not None]
        else:
            return id_list

    df1[list_col] = df1[list_col].apply(replace_ids_in_list)

    return df1

def filtrar(df: pd.DataFrame, dict_filtros) -> pd.DataFrame:

    """Devuelve únicamente a las personas con la vertical y rol seleccionados"""

    if dict_filtros["Vertical"] != []:
        df = df[df["nueva_vertical"].isin(dict_filtros["Vertical"])]
    
    if dict_filtros["Rol"] != []:
        df = df[df["rol_que_le_corresponde"].isin(dict_filtros["Rol"])]

    if dict_filtros["Sexo"] != "AMBOS":
        df = df[df["sexo"] == dict_filtros["Sexo"]]

    # if dict_filtros["Nivel Carrera"] != "TODOS":
    #     df = df[df["Nivel Carrera"] == dict_filtros["Nivel Carrera"]]

    if (dict_filtros["Min Edad"] != 0) | (dict_filtros["Max Edad"] != 0):
        df = df[df["edad"].between(dict_filtros["Min Edad"], dict_filtros["Max Edad"])]
    
    if (dict_filtros["Min Antiguedad"] != 0) | (dict_filtros["Max Antiguedad"] != 0):
        df = df[df["antigüedad"].between(dict_filtros["Min Antiguedad"], dict_filtros["Max Antiguedad"])]

    return df

def get_color(actual_level, required_level):
    """Función auxiliar que determina el color de la barra de un barplot."""
    difference = actual_level - required_level

    if difference < -0.8:
        return "#FF0000"
    if difference < 0:
        return "#FFFF00"
    if difference <= 0.8:
        return "#90EE90"
    else: return "#013220"
