import tkinter as tk
from ttkbootstrap import Label
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3

# Consulta predeterminada
querty_datos_pricipales = "SELECT CLIENTES, FECHA, DIRECCION, TELEFONO, PROVEDOR, MAQUINA, IMPORTE, DETALLES, REPARACION FROM Datos_reparacion"

def limpiar_tabla(tabla):
    for item in tabla.get_children():
        tabla.delete(item)
def mostrar_datos(quety, parametros, tabla):
    conn = sqlite3.connect("BDreparaciones.db")
    cursor = conn.cursor()
    cursor.execute(quety, parametros)
    datos = cursor.fetchall()
    limpiar_tabla(tabla)
    for dato in datos:
        tabla.insert("", tk.END, values=dato)
    conn.close()

def buscar_cliente(termino_busqueda, tabla):
    if not termino_busqueda:  # Si el campo de búsqueda está vacío, no realizar la búsqueda.
        return
    conn = sqlite3.connect("BDreparaciones.db")
    cursor = conn.cursor()
    query = "SELECT CLIENTES, FECHA, DIRECCION, TELEFONO, PROVEDOR, MAQUINA, IMPORTE, DETALLES, REPARACION FROM Datos_reparacion WHERE CLIENTES LIKE ?"
    cursor.execute(query, ('%' + termino_busqueda + '%',))  # Realiza una búsqueda parcial
    resultados = cursor.fetchall()
    limpiar_tabla(tabla)
    for resultado in resultados:
        tabla.insert("", tk.END, values=resultado)
    conn.close()

def mostrar_buscar(frame_contenido):
    # Limpiar el área de contenido actual
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    # Crear el contenedor principal
    box = ttk.Frame(frame_contenido, padding=10)
    box.grid(row=0, column=0, sticky="nsew")
    frame_contenido.grid_rowconfigure(0, weight=1)
    frame_contenido.grid_columnconfigure(0, weight=1)

    # Etiqueta de título
    label = Label(box, text="Buscar Cliente", font=("Helvetica", 18))
    label.grid(row=0, column=0, sticky="n", pady=(0, 10))

    # Frame para los botones de búsqueda
    box_btn = ttk.Frame(box)
    box_btn.grid(row=1, column=0, pady=(0, 10))

    # Botones de búsqueda
    ttk.Button(box_btn, text="REFRESCAR", command=lambda: mostrar_datos(querty_datos_pricipales, (), tabla)).grid(row=0, column=0, padx=5, sticky="n")

    # Frame para la barra de búsqueda
    box_search = ttk.Frame(box, padding=10)
    box_search.grid(row=2, column=0, pady=(0, 10))

    # Barra de búsqueda y botón
    ttk.Label(box_search, text="Buscar Clientes:").grid(row=0, column=0, padx=(0, 5))
    search = ttk.Entry(box_search, width=30)
    search.grid(row=0, column=1, padx=(0, 5))
    btn_search = ttk.Button(box_search, text="Buscar", bootstyle="success", command=lambda: buscar_cliente(search.get(), tabla))
    btn_search.grid(row=0, column=2)

    # Frame para el Treeview
    box_treeview = ttk.Frame(box, padding=5)
    box_treeview.grid(row=3, column=0, sticky="nw")
    box.grid_rowconfigure(3, weight=1)
    box.grid_columnconfigure(0, weight=1)

    # Crear y configurar el Treeview con la columna "Fecha"
    columnas = ('Clientes', 'Fecha', 'Direccion', 'Telefono', 'Proveedor', 'Maquina', 'Importe',)
    tabla = ttk.Treeview(box_treeview, columns=columnas, show='headings', bootstyle="info")

    # Definir las columnas y los encabezados
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)  # Aumentar el ancho de las columnas


    tabla.grid(row=0, column=0)
    tabla.config(height=30)  # Aumenta la cantidad de filas visibles (cambia a 30 o más)
    box_treeview.grid_rowconfigure(0, weight=1)
    box_treeview.grid_columnconfigure(0, weight=1)

    # Frame para las acciones de reparación
    box_info = ttk.Frame(box_treeview, padding=5)
    box_info.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

    # Crear LabelFrame para Info Cliente
    box_datos = ttk.LabelFrame(box_info, text="Info Cliente", padding=10)
    box_datos.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    ttk.Label(box_datos, text="Cliente:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="nw")
    ttk.Label(box_datos, text="Direccion:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="nw")
    ttk.Label(box_datos, text="Provedor:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="nw")
    ttk.Label(box_datos, text="Telefo:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="nw")
    ttk.Label(box_datos, text="Fecha:", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky="nw")
    ttk.Label(box_datos, text="Presupuesto $:", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky="nw")

    label_cliente = ttk.Label(box_datos, text="", font=("Arial", 13, "bold"))
    label_cliente.grid(row=1, column=1, sticky="nw")
    label_direccion = ttk.Label(box_datos, text="", font=("Arial", 13, "bold"))
    label_direccion.grid(row=2, column=1, sticky="nw")
    label_proveedor = ttk.Label(box_datos, text="", font=("Arial", 13, "bold"))
    label_proveedor.grid(row=3, column=1, sticky="nw")
    label_telefono = ttk.Label(box_datos, text="", font=("Arial", 13, "bold"))
    label_telefono.grid(row=4, column=1, sticky="nw")
    label_fecha = ttk.Label(box_datos, text="", font=("Arial", 13, "bold"))
    label_fecha.grid(row=5, column=1, sticky="nw")
    label_email = ttk.Label(box_datos, text="", font=("Arial", 13, "bold"))
    label_email.grid(row=6, column=1, sticky="nw")

    # Crear LabelFrame para Mecanizado
    box_mecanizado = ttk.LabelFrame(box_info, text="Mecanizado", padding=10)
    box_mecanizado.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    ttk.Label(box_mecanizado, text="Esto se realizo a la maquina", font=("Arial", 10, "bold")).grid(row=0, column=0)
    info_mecanizado = ttk.Label(box_mecanizado, text="", wraplength=200, font=("Arial", 10, "bold"))
    info_mecanizado.grid(row=1, column=0)

    # Crear LabelFrame para Detalles
    box_detalles = ttk.LabelFrame(box_info, text="Detalles", padding=10)
    box_detalles.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

    ttk.Label(box_detalles, text="Detalles o estado de la maquina.", font=("Arial", 12, "bold")).grid(row=0, column=0)
    info_detalles = ttk.Label(box_detalles, text="", wraplength=170, font=("Arial", 13, "bold"))
    info_detalles.grid(row=1, column=0)

    # Función para actualizar la información del cliente
    def actualizar_info_cliente(event):
        selected_item = tabla.selection()
        if selected_item:
            item = tabla.item(selected_item)
            cliente_info = item['values']  # Esto obtiene los valores de la fila seleccionada
            label_cliente.config(text=cliente_info[0])  # Cliente
            label_direccion.config(text=cliente_info[2])  # Dirección
            label_proveedor.config(text=cliente_info[4])  # Proveedor
            label_telefono.config(text=cliente_info[3])  # Teléfono
            label_fecha.config(text=cliente_info[1])  # Fecha
            label_email.config(text=cliente_info[6])  # Email
            info_mecanizado.config(text=cliente_info[8])
            info_detalles.config(text=cliente_info[7])

    # Asociar la función de actualización con un evento de selección de fila
    tabla.bind("<ButtonRelease-1>", actualizar_info_cliente)
    mostrar_datos(querty_datos_pricipales, (), tabla)