# pylint: skip-file

import pandas as pd
from pandasql import sqldf

from modelos import df_paises, df_sedes, df_secciones, df_redes_sociales, df_gdp_per_capita_2023

query_test = "SELECT COUNT(sede_id) FROM df_sedes WHERE country_code = 'USA'"
query_vista_por_pais = "SELECT a.pais, COUNT(b.sede_id) AS cantidad_sedes, AVG(c.seccion_id) AS promedio_secciones_por_sede, gdp_pc_2023_usd AS pbi_2023 FROM df_paises a LEFT JOIN df_sedes b ON a.country_code = b.country_code LEFT JOIN df_secciones c ON b.sede_id = c.sede_id LEFT JOIN df_gdp_per_capita_2023 d ON a.country_code = d.country_code GROUP BY a.country_code"
vista_por_pais = sqldf(query_vista_por_pais)
print(vista_por_pais)
