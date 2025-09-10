# pylint: skip-file

from pandasql import sqldf

from modelos import df_paises, df_sedes, df_secciones, df_redes_sociales, df_gdp_per_capita_2023

# Reporte 1, cantidad de sedes Argentinas por país, cantidad de secciones promedio por sede y PBI per cápita del país en el año 2023, consulta SQL
query_vista_por_pais = "SELECT a.pais, COUNT(DISTINCT b.sede_id) AS cantidad_sedes, CAST(COUNT(DISTINCT c.seccion_id) AS FLOAT) / COUNT(DISTINCT b.sede_id) AS promedio_secciones_por_sede, gdp_pc_2023_usd AS pbi_2023 FROM df_paises a LEFT JOIN df_sedes b ON a.country_code = b.country_code LEFT JOIN df_secciones c ON b.sede_id = c.sede_id LEFT JOIN df_gdp_per_capita_2023 d ON a.country_code = d.country_code GROUP BY a.country_code ORDER BY cantidad_sedes DESC, a.pais"
vista_por_pais = sqldf(query_vista_por_pais)
print(vista_por_pais)

# Reporte 2, por región geográfica, cantidad de países con al menos una sede argentina y el promedio de PBI 2023 de esos países, consulta SQL
query_vista_por_region = "SELECT p.region AS region_geografica, COUNT(DISTINCT s.country_code) AS paises_con_sedes, AVG(DISTINCT g.gdp_pc_2023_usd) AS promedio_pbi_2023 FROM df_paises p LEFT JOIN df_sedes s ON p.country_code = s.country_code JOIN df_gdp_per_capita_2023 g ON p.country_code = g.country_code GROUP BY p.region ORDER BY promedio_pbi_2023 DESC"
vista_por_region = sqldf(query_vista_por_region)
print(vista_por_region)

# Reporte 3, cantidad de tipos de red social diferentes que se utilizan como vía de comunicación las sedes de cada país, consulta SQL
query_vista_por_redes_sociales_por_pais = "SELECT a.pais AS Pais, COUNT(DISTINCT c.tipo_red) AS tipos_de_redes_sociales FROM df_paises a LEFT JOIN df_sedes b ON a.country_code = b.country_code LEFT JOIN df_redes_sociales c ON b.sede_id = c.sede_id GROUP BY a.country_code"
vista_por_redes_sociales_por_pais = sqldf(query_vista_por_redes_sociales_por_pais)
print(vista_por_redes_sociales_por_pais)

# Reporte 4, información de redes sociales con su país, nombre de sede, tipo de red y url correspondiente, consulta SQL
query_vista_por_redes_detalle = "SELECT c.pais, CONCAT(b.tipo_sede, ' - ',b.ciudad) as nombre_sede, a.tipo_red, a.url FROM df_redes_sociales a LEFT JOIN df_sedes b ON a.sede_id = b.sede_id LEFT JOIN df_paises c ON b.country_code = c.country_code GROUP BY a.red_id ORDER BY c.pais ASC, nombre_sede ASC, a.tipo_red ASC, a.url ASC"
vista_por_redes_detalle = sqldf(query_vista_por_redes_detalle)
print(vista_por_redes_detalle)
