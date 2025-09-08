# pylint: skip-file

from modelos import df_paises, df_sedes, df_secciones, df_redes_sociales, df_gdp_per_capita_2023

print("df_paises:", df_paises.shape)
print(df_paises.head(5))

print("df_sedes:", df_sedes.shape)
print(df_sedes.head(5))

print("df_secciones:", df_secciones.shape)
print(df_secciones.head(5))

print("df_redes_sociales:", df_redes_sociales.shape)
print(df_redes_sociales.head(10))

print("df_gdp_per_capita_2023:", df_gdp_per_capita_2023.shape)
print(df_gdp_per_capita_2023.head(10))
