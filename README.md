# proyecto-pandas

# Investigación de funciones de Pandas

A continuación se documentan las funciones investigadas, con una breve descripción de su propósito, sintaxis, problema que resuelven y un ejemplo práctico extraído del proyecto.

---

## 1. `value_counts()`

**¿Qué hace?**  
Cuenta las frecuencias de cada valor único en una columna (Series).

**Sintaxis básica:**  
```python
serie.value_counts(normalize=False, sort=True, ascending=False, ...)
```

**Problema que resuelve:**  
Permite identificar rápidamente la distribución de categorías, por ejemplo, saber cuántos clientes hay por ciudad o qué producto se repite más.

**Uso en el proyecto:**  
```python
ciudad_counts = df_clientes["ciudad"].value_counts()
ciudad_mas_clientes = ciudad_counts.idxmax()
```

---

## 2. `nunique()`

**¿Qué hace?**  
Retorna el número de valores únicos en una columna o en todo el DataFrame.

**Sintaxis básica:**  
```python
df['columna'].nunique(dropna=True)
```

**Problema que resuelve:**  
Ayuda a conocer la cardinalidad de una variable (cuántos valores distintos tiene), útil para detectar columnas con pocas categorías o claves únicas.

**Uso en el proyecto:**  
```python
num_ciudades = df_clientes['ciudad'].nunique()
print(f"Hay {num_ciudades} ciudades diferentes.")
```

---

## 3. `drop_duplicates()`

**¿Qué hace?**  
Elimina filas duplicadas de un DataFrame, pudiendo basarse en todas o algunas columnas.

**Sintaxis básica:**  
```python
df.drop_duplicates(subset=None, keep='first', inplace=False)
```

**Problema que resuelve:**  
Limpia datos repetidos que pueden distorsionar análisis o generar errores en agregaciones.

**Uso en el proyecto:**  
```python
df_clientes.drop_duplicates(subset=["id_cliente"], keep="first", inplace=True)
```

---

## 4. `rename()`

**¿Qué hace?**  
Cambia los nombres de columnas o índices de un DataFrame.

**Sintaxis básica:**  
```python
df.rename(columns={'viejo': 'nuevo'}, inplace=False)
```

**Problema que resuelve:**  
Estandariza nombres de columnas para hacer el código más legible o para unificar criterios entre diferentes fuentes.

**Uso en el proyecto:**  
```python
df_clientes.rename(columns={"nombre": "cliente"}, inplace=True)
```

---

## 5. `astype()`

**¿Qué hace?**  
Convierte el tipo de dato de una o varias columnas (a int, float, str, datetime, etc.).

**Sintaxis básica:**  
```python
df['columna'] = df['columna'].astype('int64')
```

**Problema que resuelve:**  
Garantiza que los datos tengan el tipo correcto para operaciones matemáticas, filtros o fusiones. Evita errores por tipos incompatibles.

**Uso en el proyecto:**  
```python
df_ventas["cantidad"] = df_ventas["cantidad"].astype("int64")
df_ventas["precio_unitario"] = df_ventas["precio_unitario"].astype("float64")
```

---

## 6. `query()`

**¿Qué hace?**  
Filtra filas de un DataFrame usando una expresión booleana en forma de cadena (similar a SQL).

**Sintaxis básica:**  
```python
df.query('columna > 100 and otra == "valor"')
```

**Problema que resuelve:**  
Ofrece una sintaxis más limpia y legible para filtros complejos, especialmente útil cuando se trabaja con muchas condiciones.

**Uso en el proyecto (ejemplo hipotético):**  
```python
ventas_mayores = df_ventas.query('cantidad > 3 and precio_unitario > 100')
```

---

## 7. `merge()`

**¿Qué hace?**  
Combina dos DataFrames usando una o varias columnas como clave (similar a un JOIN de SQL).

**Sintaxis básica:**  
```python
pd.merge(df1, df2, on='columna_clave', how='inner')
```

**Problema que resuelve:**  
Permite enriquecer un DataFrame con información de otra tabla, relacionando datos de clientes, productos, etc.

**Uso en el proyecto:**  
```python
df_ventas_con_productos = pd.merge(df_ventas, df_productos[["id_producto", "producto", "precio"]],
                                   on="id_producto", how="left")
```

---

## 8. `concat()`

**¿Qué hace?**  
Concatena (apila) DataFrames o Series a lo largo de un eje (filas o columnas).

**Sintaxis básica:**  
```python
pd.concat([df1, df2], axis=0)   # apilar filas (por defecto)
pd.concat([df1, df2], axis=1)   # unir columnas
```

**Problema que resuelve:**  
Útil para combinar datos que tienen la misma estructura (por ejemplo, ventas de diferentes meses) o añadir nuevas columnas.

**Uso en el proyecto (ejemplo):**  
```python
# Combinar ventas de dos años
ventas_2024 = pd.read_csv('ventas2024.csv')
ventas_2025 = pd.read_csv('ventas2025.csv')
ventas_total = pd.concat([ventas_2024, ventas_2025], ignore_index=True)
```

---

## 9. `pivot_table()`

**¿Qué hace?**  
Crea una tabla dinámica (pivot) que agrupa y agrega datos, similar a una tabla de Excel.

**Sintaxis básica:**  
```python
pd.pivot_table(df, values='columna_valor', index='columna_fila',
               columns='columna_columna', aggfunc='mean')
```

**Problema que resuelve:**  
Resume grandes volúmenes de datos en una matriz, facilitando la visualización de relaciones entre categorías (ej. ventas por producto y mes).

**Uso en el proyecto (ejemplo):**  
```python
tabla_ventas = pd.pivot_table(df_ventas_con_productos,
                              values='ingreso',
                              index='producto',
                              columns='ciudad',
                              aggfunc='sum')
```

---

## 10. `groupby()`

**¿Qué hace?**  
Agrupa datos según una o más columnas y permite aplicar funciones de agregación (sum, mean, count, etc.) a cada grupo.

**Sintaxis básica:**  
```python
df.groupby('columna')['otra_columna'].sum()
```

**Problema que resuelve:**  
Es la base de los análisis segmentados: calcular totales, promedios o conteos por categoría (clientes, productos, regiones, etc.).

**Uso en el proyecto:**  
```python
agrupado_cliente = df_ventas_con_productos.groupby("id_cliente").agg(
    total_compras=("id_venta", "count"),
    total_gastado=("ingreso", "sum")
).reset_index()
```

---

**Conclusión:**  
Estas funciones son el núcleo del análisis con Pandas y permiten desde la limpieza básica hasta el procesamiento complejo de datos empresariales. Cada una resuelve un problema específico y, combinadas, ofrecen un flujo de trabajo completo y eficiente.
