# paso8.py
# pylint: skip-file

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from modelos import df_paises, df_sedes, df_gdp_per_capita_2023

# =======================
# 1. Cantidad de sedes por región geográfica
# =======================
sedes_region = df_sedes.groupby("region_geo").size().reset_index(name="cantidad_sedes")
sedes_region = sedes_region.sort_values("cantidad_sedes", ascending=False)

plt.figure(figsize=(10,6))
sns.barplot(x="region_geo", y="cantidad_sedes", data=sedes_region, palette="viridis")
plt.xticks(rotation=45)
plt.title("Cantidad de sedes por región geográfica")
plt.tight_layout()
plt.show()

# =======================
# 2. Boxplot PBI per cápita 2023 por región (solo países con sede)
# =======================
pbi_region = df_sedes.merge(df_gdp_per_capita_2023, on="country_code").merge(df_paises, on="country_code")

plt.figure(figsize=(10,6))
orden_regiones = pbi_region.groupby("region")["gdp_pc_2023_usd"].median().sort_values().index
sns.boxplot(x="region", y="gdp_pc_2023_usd", data=pbi_region, order=orden_regiones, palette="Set2")
plt.xticks(rotation=45)
plt.title("Distribución del PBI per cápita 2023 por región (solo países con sede)")
plt.tight_layout()
plt.show()

# =======================
# 3. Relación PBI per cápita vs cantidad de sedes
# =======================
sedes_pbi = df_sedes.groupby("country_code").size().reset_index(name="cantidad_sedes")
sedes_pbi = sedes_pbi.merge(df_gdp_per_capita_2023, on="country_code").merge(df_paises, on="country_code")

plt.figure(figsize=(8,6))
sns.scatterplot(x="gdp_pc_2023_usd", y="cantidad_sedes", hue="region", data=sedes_pbi, alpha=0.7)
plt.title("Relación entre PBI per cápita 2023 y cantidad de sedes argentinas")
plt.xlabel("PBI per cápita 2023 (USD)")
plt.ylabel("Cantidad de sedes")
plt.tight_layout()
plt.show()
