# pylint: skip-file

import pandas as pd

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
