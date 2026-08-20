import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

def cargar_datos():
    clientes = pd.read_csv(DATA_DIR / "clientes.csv")
    productos = pd.read_excel(DATA_DIR / "productos.xlsx")
    ventas = pd.read_csv(DATA_DIR / "ventas.csv")
    if clientes.empty or productos.empty or ventas.empty:
        raise ValueError("Uno o más archivos están vacíos.")
    return clientes, productos, ventas

def explorar_datos(nombre, df):
    print(f"\\n--- {nombre} ---")
    print("Registros:", len(df))
    print("Columnas:", df.shape[1])
    print("Nombres:", list(df.columns))
    print("Tipos:\\n", df.dtypes)
    print("Primeros 5:\\n", df.head())
    print("Últimos 5:\\n", df.tail())
    print("Nulos:\\n", df.isnull().sum())

def analizar_ventas(ventas):
    return {"Total de ventas": ventas.total_venta.sum(),"Promedio": ventas.total_venta.mean(),"Máxima": ventas.total_venta.max(),"Mínima": ventas.total_venta.min(),"Transacciones": ventas.venta_id.nunique()}

def analizar_clientes(clientes, ventas):
    compras=ventas.groupby("cliente_id").size().reset_index(name="numero_compras")
    gasto=ventas.groupby("cliente_id",as_index=False)["total_venta"].sum()
    resumen=clientes.merge(compras,on="cliente_id",how="left").merge(gasto,on="cliente_id",how="left").fillna(0)
    mayor_compras=resumen.loc[resumen.numero_compras.idxmax()]
    mayor_gasto=resumen.loc[resumen.total_venta.idxmax()]
    metricas={"Cliente con más compras":mayor_compras.nombre,"Cliente que más gastó":mayor_gasto.nombre,"Ciudad con más clientes":clientes.ciudad.value_counts().idxmax(),"Promedio de compra por cliente":resumen.total_venta.mean()}
    return metricas,resumen

def analizar_productos(productos, ventas):
    cantidades=ventas.groupby("producto_id",as_index=False)["cantidad"].sum()
    ingresos=ventas.groupby("producto_id",as_index=False)["total_venta"].sum()
    resumen=productos.merge(cantidades,on="producto_id",how="left").merge(ingresos,on="producto_id",how="left").fillna(0)
    metricas={"Producto más vendido":resumen.loc[resumen.cantidad.idxmax(),"producto"],"Producto menos vendido":resumen.loc[resumen.cantidad.idxmin(),"producto"],"Producto con mayor ingreso":resumen.loc[resumen.total_venta.idxmax(),"producto"],"Producto con menor ingreso":resumen.loc[resumen.total_venta.idxmin(),"producto"]}
    return metricas,resumen

def funciones_investigadas(clientes, productos, ventas):
    # drop_duplicates, rename, astype, query, merge, pivot_table, groupby y value_counts
    clientes=clientes.drop_duplicates().rename(columns={"nombre":"nombre_cliente"})
    clientes["cliente_id"]=clientes["cliente_id"].astype(int)
    ventas_mayores=ventas.query("total_venta > total_venta.mean()")
    detalle=ventas.merge(clientes,on="cliente_id",how="left").merge(productos,on="producto_id",how="left")
    pivote=pd.pivot_table(detalle,values="total_venta",index="ciudad",columns="categoria",aggfunc="sum",fill_value=0)
    return ventas_mayores, detalle, pivote

def generar_reporte(ventas, clientes, productos, mv, mc, mp):
    REPORTS_DIR.mkdir(exist_ok=True)
    resumen=pd.DataFrame({"Indicador":list(mv)+list(mc)+list(mp),"Valor":list(mv.values())+list(mc.values())+list(mp.values())})
    with pd.ExcelWriter(REPORTS_DIR/"reporte_final.xlsx",engine="openpyxl") as writer:
        resumen.to_excel(writer,sheet_name="Resumen",index=False)
        ventas.to_excel(writer,sheet_name="Ventas",index=False)
        clientes.to_excel(writer,sheet_name="Clientes",index=False)
        productos.to_excel(writer,sheet_name="Productos",index=False)

def main():
    clientes,productos,ventas=cargar_datos()
    for nombre,df in [("Clientes",clientes),("Productos",productos),("Ventas",ventas)]:
        explorar_datos(nombre,df)
    mv=analizar_ventas(ventas)
    mc,rc=analizar_clientes(clientes,ventas)
    mp,rp=analizar_productos(productos,ventas)
    funciones_investigadas(clientes,productos,ventas)
    generar_reporte(ventas,rc,rp,mv,mc,mp)
    print("Reporte generado:", REPORTS_DIR/"reporte_final.xlsx")

if __name__=="__main__":
    main()
