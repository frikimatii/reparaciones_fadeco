import tkinter as tk
from ttkbootstrap import Label
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from mycode.funciones.funcion_buscar import datos, mostrar_datos

querty_datos_pricipales = "SELECT CLIENTES, FECHA, DIRECCION, TELEFONO, PROVEDOR, MAQUNA FROM Datos_reparacion "

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
    
    ttk.Button(box_btn, text="Nombre").grid(row=0, column=0, padx=5)
    ttk.Button(box_btn, text="Proveedor", command= lambda: mostrar_datos(querty_datos_pricipales, tabla) ).grid(row=0, column=1, padx=5)
    ttk.Button(box_btn, text="Maquina").grid(row=0, column=2, padx=5)
    
    # Frame para la barra de búsqueda
    box_search = ttk.Frame(box, padding=10)
    box_search.grid(row=2, column=0, pady=(0, 10))
    
    ttk.Label(box_search, text="Buscar Clientes:").grid(row=0, column=0, padx=(0, 5))
    search = ttk.Entry(box_search, width=30)
    search.grid(row=0, column=1, padx=(0, 5))
    btn_search = ttk.Button(box_search, text="Buscar", command= lambda: datos())
    btn_search.grid(row=0, column=2)

    # Frame para el Treeview
    box_treeview = ttk.Frame(box, padding=10)
    box_treeview.grid(row=3, column=0, sticky="nsew")
    box.grid_rowconfigure(3, weight=1)
    box.grid_columnconfigure(0, weight=1)
    
    # Crear y configurar el Treeview con la columna "Fecha"
    columnas = ('Clientes', 'Fecha', 'Direccion', 'Telefono', 'Proveedor', 'Maquina', 'Reparacion')
    tabla = ttk.Treeview(box_treeview, columns=columnas, show='headings', bootstyle="info")
    
    # Definir las columnas y los encabezados
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)
    
    tabla.grid(row=0, column=0, sticky="nsew")
    box_treeview.grid_rowconfigure(0, weight=1)
    box_treeview.grid_columnconfigure(0, weight=1)
    
    
    # Scrollbar para el Treeview
    scrollbar = ttk.Scrollbar(box_treeview, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")
