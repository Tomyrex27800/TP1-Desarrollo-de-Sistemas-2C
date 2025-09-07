# pylint: skip-file
import re
import pandas as pd
import os


# Detectar nombres reales de columnas (simple)
def pick(df, opciones):
    for c in opciones:
        if c in df.columns:
            return c
    raise ValueError(f"Falta alguna de estas columnas: {opciones}")

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


#================================MODELO PAIS=======================================
# columnas de df_pbi_per_capita
col_code_gdp = pick(df_pbi_per_capita, ["country_code", "Country Code"])
col_pais_gdp = pick(df_pbi_per_capita, ["Country Name", "pais"])

# columnas de df_lista_sedes_datos
col_iso3_dat = pick(df_lista_sedes_datos, ["pais_iso_3", "country_code", "codigo_pais"])
col_region   = pick(df_lista_sedes_datos, ["region_geografica", "region"])

# merge GDP + sedes_datos
joined_paises = pd.merge(
    df_pbi_per_capita,
    df_lista_sedes_datos[[col_iso3_dat, col_region]],
    left_on=col_code_gdp,
    right_on=col_iso3_dat,
    how="inner"
)

# poblar df_paises
df_paises = pd.DataFrame(columns=columnas_paises)
for i in range(len(joined_paises)):
    fila = joined_paises.iloc[i]
    data = {
        "country_code": fila[col_code_gdp],
        "pais": fila[col_pais_gdp],
        "region": fila[col_region],
    }
    df_paises.loc[i] = data  # type: ignore

df_paises = df_paises.dropna(how='all')

print("df_paises:", df_paises.shape)
print(df_paises.head(5))

#================================MODELO SEDE=======================================
# columnas base en lista-sedes.csv
col_sede_id_base = pick(df_lista_sedes, ["digac","sede_id","id_sede","id"])
col_iso3_base    = pick(df_lista_sedes, ["pais_iso_3","country_code","codigo_pais"])
col_pais_base    = pick(df_lista_sedes, ["pais_castellano","pais"])
col_ciudad_base  = pick(df_lista_sedes, ["ciudad_castellano","ciudad"])
col_tipo_base    = pick(df_lista_sedes, ["sede_tipo","tipo_sede"])

# columnas extra en lista-sedes-datos.csv
col_sede_id_dat  = pick(df_lista_sedes_datos, ["digac","sede_id","id_sede","id"])
col_iso3_dat     = pick(df_lista_sedes_datos, ["pais_iso_3","country_code","codigo_pais"])
col_region       = pick(df_lista_sedes_datos, ["region_geografica","region"])
col_tel          = pick(df_lista_sedes_datos, ["telefono_principal","telefono"])
col_mail         = pick(df_lista_sedes_datos, ["correo_electronico","email"])
col_web          = pick(df_lista_sedes_datos, ["sitio_web","web"])

# join por (sede_id + iso3) con left para no perder sedes
joined_sedes = pd.merge(
    df_lista_sedes,
    df_lista_sedes_datos[[col_sede_id_dat, col_iso3_dat, col_region, col_tel, col_mail, col_web]],
    left_on=[col_sede_id_base, col_iso3_base],
    right_on=[col_sede_id_dat,  col_iso3_dat],
    how="left"
)

# poblar df_sedes (usa tus columnas exactas del modelo)
df_sedes = pd.DataFrame(columns=columnas_sedes)  # si ya existe, podés borrar esta línea
for i in range(len(joined_sedes)):
    fila = joined_sedes.iloc[i]
    data = {
        "sede_id":     fila[col_sede_id_base],
        "country_code":fila[col_iso3_base],
        "pais":        fila[col_pais_base],          # NO 'Country Name'
        "ciudad":      fila[col_ciudad_base],
        "tipo_sede":   fila[col_tipo_base],
        "telefono":    fila.get(col_tel,  pd.NA),    # usa nombres reales
        "email":       fila.get(col_mail, pd.NA),
        "sitio_web":   fila.get(col_web,  pd.NA),
        "region_geo":  fila.get(col_region, pd.NA),  # nombre del modelo
    }
    df_sedes.loc[i] = data  # type: ignore

df_sedes = df_sedes.dropna(how='all')


print("df_sedes:", df_sedes.shape)
print(df_sedes.head(5))

#================================MODELO SECCION=======================================
# columnas de df_lista_secciones

# detectar columnas (tolerante a variantes)
col_seccion_id = "seccion_id" if "seccion_id" in df_lista_secciones.columns else None
col_sede_id_sec = pick(df_lista_secciones, ["sede_id","digac","id_sede","id"])
col_tipo_sec    = pick(df_lista_secciones, ["tipo_seccion","seccion","tipo"])

# si no existe seccion_id, lo creamos incremental
if col_seccion_id is None:
    df_lista_secciones = df_lista_secciones.copy()
    df_lista_secciones["seccion_id"] = range(1, len(df_lista_secciones) + 1)
    col_seccion_id = "seccion_id"

# poblar df_secciones según tu modelo
df_secciones = pd.DataFrame(columns=columnas_secciones)  # ['seccion_id','sede_id','tipo_seccion']
for i in range(len(df_lista_secciones)):
    fila = df_lista_secciones.iloc[i]
    data = {
        "seccion_id":  fila[col_seccion_id],
        "sede_id":     fila[col_sede_id_sec],
        "tipo_seccion": (str(fila[col_tipo_sec]).strip() 
                        if pd.notna(fila[col_tipo_sec]) else pd.NA),
    }
    df_secciones.loc[i] = data  # type: ignore

# limpieza mínima
df_secciones["tipo_seccion"] = df_secciones["tipo_seccion"].astype("string")
df_secciones["sede_id"] = df_secciones["sede_id"].astype("string").str.strip()

df_secciones = df_secciones.dropna(how="all")

print("df_secciones:", df_secciones.shape)
print(df_secciones.head(5))

#================================MODELO REDES SOCIALES=======================================

# detectar columna con redes en lista-sedes-datos
col_sede_id_dat = pick(df_lista_sedes_datos, ["digac","sede_id","id_sede","id"])
col_redes = None
for c in ["redes_sociales","redes","RRSS","social","social_media"]:
    if c in df_lista_sedes_datos.columns:
        col_redes = c
        break

# si no existe columna de redes → tabla vacía
if col_redes is None:
    df_redes_sociales = pd.DataFrame(columns=columnas_redes_sociales)
    print("df_redes_sociales: (0, 4) — no se encontró columna de redes")
else:
    df_redes_sociales = pd.DataFrame(columns=columnas_redes_sociales)

    TIPOS = ("facebook","instagram","twitter","x","youtube","linkedin")

    def extraer(texto: str):
        if not isinstance(texto, str):
            return []
        pares = []
        # patrón 'tipo: http...'
        for m in re.finditer(r"(facebook|instagram|twitter|x|youtube|linkedin)\s*[:\-]\s*(https?://\S+)", texto, flags=re.I):
            t = m.group(1).lower().replace("x","twitter")
            u = m.group(2)
            pares.append((t,u))
        # urls sueltas → inferir tipo por dominio
        for m in re.finditer(r"(https?://\S+)", texto, flags=re.I):
            u = m.group(1)
            t = ("instagram" if "instagram" in u.lower() else
                "twitter"   if ("twitter" in u.lower() or "x.com" in u.lower()) else
                "facebook"  if "facebook" in u.lower() else
                "youtube"   if "youtu" in u.lower() else
                "linkedin"  if "linkedin" in u.lower() else
                None)
            if t: pares.append((t,u))
        return pares

    rid = 1
    for _, fila in df_lista_sedes_datos.iterrows():
        sede = str(fila[col_sede_id_dat])
        for tipo, url in extraer(fila.get(col_redes, "")):
            df_redes_sociales.loc[len(df_redes_sociales)] = {
                "red_id": rid,
                "sede_id": sede,
                "tipo_red": tipo,
                "url": url
            }
            rid += 1

    print("df_redes_sociales:", df_redes_sociales.shape)
    print(df_redes_sociales.head(10))

#================================MODELO GDP PER CAPITA 2023=======================================

# columnas del CSV de PBI
col_code_gdp = pick(df_pbi_per_capita, ["country_code", "Country Code"])
col_value_gdp = pick(df_pbi_per_capita, ["2023", "gdp_pc_2023_usd"])

# poblar df_gdp_per_capita_2023
df_gdp_per_capita_2023 = pd.DataFrame(columns=columnas_gdp_per_capita_2023)  # ['country_code','gdp_pc_2023_usd']

for i in range(len(df_pbi_per_capita)):
    fila = df_pbi_per_capita.iloc[i]
    data = {
        "country_code": fila[col_code_gdp],
        "gdp_pc_2023_usd": fila[col_value_gdp]
    }
    df_gdp_per_capita_2023.loc[i] = data  # type: ignore

# limpiar filas vacías
df_gdp_per_capita_2023 = df_gdp_per_capita_2023.dropna(how='all')

print("df_gdp_per_capita_2023:", df_gdp_per_capita_2023.shape)
print(df_gdp_per_capita_2023.head(10))