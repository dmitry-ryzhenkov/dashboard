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

def filtrar(df: pd.DataFrame, vertical: str, rol: str) -> pd.DataFrame:
    """Devuelve únicamente a las personas con la vertical y rol seleccionados"""
    if vertical == "TODOS" and rol == "TODOS":
        return df

    if rol == "TODOS":
        return df[df["nueva_vertical"] == vertical]
    
    if vertical == "TODOS":
        return df[df["rol"] == rol]
    
    return df[(df["rol"] == rol) & (df["nueva_vertical"] == vertical)]

def get_color(actual_level, required_level):
    """Función auxiliar que determina el color de la barra de un barplot."""
    difference = actual_level - required_level

    if difference < -0.8:
        return "#CD5C5C"
    if difference < 0:
        return "#BDB76B"
    if difference <= 0.8:
        return "#8FBC8F"
    else: return "#6495ED"
