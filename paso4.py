# pylint: skip-file

import pandas as pd
import os



# fuentes de datos

archivo_lista_secciones = './lista-secciones.csv'
fname_lista_secciones = os.path.join(archivo_lista_secciones)
df_lista_secciones = pd.read_csv(fname_lista_secciones)

archivo_lista_sedes_datos = './lista-sedes-datos.csv'
fname_lista_sedes_datos = os.path.join(archivo_lista_sedes_datos)
df_lista_sedes_datos = pd.read_csv(fname_lista_sedes_datos)

archivo_lista_sedes = './lista-sedes.csv'
fname_lista_sedes = os.path.join(archivo_lista_sedes)
df_lista_sedes = pd.read_csv(fname_lista_sedes)

archivo_pbi_per_capita = './pbi-per-capita-pais.csv'
fname_pbi_per_capita = os.path.join(archivo_pbi_per_capita)
df_pbi_per_capita = pd.read_csv(fname_pbi_per_capita)



# dataframes vacios

columnas_paises = ['country_code', 'pais', 'region']
columnas_sedes = ['sede_id', 'country_code', 'pais', 'ciudad', 'tipo_sede', 'telefono', 'email', 'sitio_web', 'region_geo']
columnas_secciones = ['seccion_id', 'sede_id', 'tipo_seccion']
columnas_redes_sociales = ['red_id', 'sede_id', 'tipo_red', 'url']
columnas_gdp_per_capita_2023 = ['country_code', 'gdp_pc_2023_usd']

df_paises = pd.DataFrame(columns=columnas_paises)
df_sedes = pd.DataFrame(columns=columnas_sedes)
df_secciones = pd.DataFrame(columns=columnas_secciones)
df_redes_sociales = pd.DataFrame(columns=columnas_redes_sociales)
df_gdp_per_capita_2023 = pd.DataFrame(columns=columnas_gdp_per_capita_2023)



joined_paises = pd.merge(df_pbi_per_capita, df_lista_sedes_datos, left_on="country_code", right_on="pais_iso_3", how="inner")
for i in range(len(joined_paises)):
    data = {
        "country_code": joined_paises.iloc[i]['country_code'],
        "pais": joined_paises.iloc[i]['Country Name'],
        "region": joined_paises.iloc[i]['region_geografica']
    }
    df_paises.loc[i] = data # type: ignore
df_paises = df_paises.dropna(how='all')

joined_sedes = pd.merge(df_pbi_per_capita, df_lista_sedes_datos, left_on="country_code", right_on="pais_iso_3", how="inner")
for i in range(len(joined_sedes)):
    data = {
        "country_code": joined_sedes.iloc[i]['country_code'],
        "pais": joined_sedes.iloc[i]['Country Name'],
        "region": joined_sedes.iloc[i]['region_geografica']
    }
    df_sedes.loc[i] = data # type: ignore
df_sedes = df_paises.dropna(how='all')


print(df_paises.head)
#print(df_sedes.head)
