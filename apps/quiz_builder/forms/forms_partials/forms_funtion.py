import pandas as pd
#from apps.formularios.models import Solicitud_Cliente, Solicitud_Cliente_Productos, Solicitud_Cliente_Archivos

area_value = ['SERVICIOS','PROYECTOS']

def create_solicitud(user, nombre_proveedor, rut_proveedor, area_value, centro_costo, nombre_solicitante, nombre_autoriza, table_producto, table_file):
    records1, solicitud_cliente = create_solicitud_cliente(user, nombre_proveedor, rut_proveedor, area_value, centro_costo, nombre_solicitante, nombre_autoriza)
    records2 = create_solicitud_cliente_productos(solicitud_cliente, table_producto)
    table_file = create_solicitud_cliente_archivos(solicitud_cliente, table_file)
    return records1, records2, table_file


def create_solicitud_cliente(user, nombre_proveedor, rut_proveedor, area_value, centro_costo, nombre_solicitante, nombre_autoriza):
    user_id = user.id
    username = user.username
    df_solicitud_cliente = pd.DataFrame({
        "User_Id": [user_id],
        "User_Name": [username],
        "Formulario": ["Cotización Realizada"],
        "Nombre Proveedor": [nombre_proveedor],
        "Rut_Proveedor": [rut_proveedor],
        "Empresa": ["DTS"],
        "Area": [area_value],
        "Centro Costo": [centro_costo],
        "Nombre Solicitante": [nombre_solicitante],
        "Nombre de Quién Autoriza": [nombre_autoriza],
    })
    solicitud_cliente = Solicitud_Cliente.objects.create(
        User_Id=user_id,
        User_Name=username,
        Formulario="Cotización Realizada",
        Nombre_Proveedor=nombre_proveedor,
        Rut_Proveedor=rut_proveedor,
        Empresa="DTS",
        Area=area_value,
        Centro_Costo=centro_costo,
        Nombre_Solicitante=nombre_solicitante,
        Nombre_Autoriza=nombre_autoriza,
    )
    return df_solicitud_cliente.to_dict('records'), solicitud_cliente

def create_solicitud_cliente_productos(solicitud_cliente, table_producto):
    if table_producto is None:
        table_producto = []
    else:
        for producto in table_producto:
            Solicitud_Cliente_Productos.objects.create(
                ID_OC=solicitud_cliente,
                Nombre_Producto=producto['Nombre Producto'],
                Cantidad=producto['Cantidad'],
                Descripcion_Producto=producto['Descripción Producto'],
            )
    df_solicitud_cliente_productos = pd.DataFrame(table_producto)
    return df_solicitud_cliente_productos.to_dict('records')

def create_solicitud_cliente_archivos(solicitud_cliente, table_file):
    for archivo in table_file:
        Solicitud_Cliente_Archivos.objects.create(
            ID_OC=solicitud_cliente,
            File_Number=archivo['File Number'],
            File_Name=archivo['File Name'],
            File_Type=archivo['File Type'],
        )
    return table_file