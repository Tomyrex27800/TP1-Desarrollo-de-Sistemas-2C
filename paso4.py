# pylint: skip-file

import pandas as pd
import os



# fuentes de datos

archivo_lista_secciones = 'lista-secciones.csv'
fname_lista_secciones = os.path.join(archivo_lista_secciones)
df_lista_secciones = pd.read_csv(fname_lista_secciones)

archivo_lista_sedes_datos = 'lista-sedes-datos.csv'
fname_lista_sedes_datos = os.path.join(archivo_lista_sedes_datos)
df_lista_sedes_datos = pd.read_csv(fname_lista_sedes_datos)

archivo_lista_sedes = 'lista-sedes.csv'
fname_lista_sedes = os.path.join(archivo_lista_sedes)
df_lista_sedes = pd.read_csv(fname_lista_sedes)

archivo_pbi_per_capita = 'API_NY.GDP.PCAP.CD_DS2_en_csv_v2_122367.csv'
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



print(df_paises)
print(df_sedes)
print(df_secciones)
print(df_redes_sociales)
print(df_gdp_per_capita_2023)
