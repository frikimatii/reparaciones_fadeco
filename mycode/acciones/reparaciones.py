import tkinter as tk
from ttkbootstrap import Label
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
from datetime import datetime  # Para manejar fechas


def reparacion_view(frame_contenido):
    # Eliminar widgets previos
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    # Crear el marco principal
    box = ttk.Frame(frame_contenido, padding=5)
    box.grid(row=0, column=0, sticky="nsew")
    
    frame_contenido.grid_rowconfigure(0, weight=1)
    frame_contenido.grid_columnconfigure(0, weight=1)
    
    # Etiqueta principal
    label = Label(box, text="Reparaciones", font=("Helvetica", 18))
    label.grid(row=0, column=0, sticky="n", pady=(0, 10))
    
    # Frame para el buscador
    frame_buscar = ttk.LabelFrame(box, text="Buscar por ID", padding=(10, 5))
    frame_buscar.grid(row=1, column=0, pady=(5, 10))
    
    # Entry para buscar ID
    id_buscar = ttk.Entry(frame_buscar, width=20)
    id_buscar.grid(row=0, column=0, padx=(0, 5))
    
    # Función para buscar ID (modificada para búsqueda parcial)
    def buscar_id():
        id_value = id_buscar.get()
        if id_value:
            conn = sqlite3.connect("BDreparaciones.db")
            cursor = conn.cursor()
            # Usamos LIKE con % para buscar coincidencias parciales
            cursor.execute("SELECT ID, Cliente, Maquina, Fecha_factura, Importe, Detalles, Reparaciones FROM datos_facturas WHERE ID LIKE ?", ('%' + id_value + '%',))
            datos = cursor.fetchall()
            
            # Limpiar la tabla antes de cargar nuevos datos
            tabla.delete(*tabla.get_children())
            
            for dato in datos:
                tabla.insert("", tk.END, values=dato)
            
            conn.close()
    
    # Botón de búsqueda
    boton_buscar = ttk.Button(frame_buscar, text="Buscar", bootstyle="primary", command=buscar_id)
    boton_buscar.grid(row=0, column=1)

    # Frame para la tabla
    box_treeview = ttk.Frame(box)
    box_treeview.grid(row=2, column=0)
    
    columnas_visibles = ('ID', 'Cliente', 'Maquina', 'Fecha', 'Importe', 'Detalles', 'Reparaciones')
    
    # Crear Treeview
    tabla = ttk.Treeview(box_treeview, columns=columnas_visibles, show='headings', bootstyle='primary')
    
    for col in columnas_visibles:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)
    
    tabla.grid(row=0, column=0, pady=10)
    tabla.config(height=10)
    
    # Función para cargar datos en la tabla
    def cargar_datos():
        tabla.delete(*tabla.get_children())
        conn = sqlite3.connect("BDreparaciones.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Cliente, Maquina, Fecha_factura, Importe, Detalles, Reparaciones FROM datos_facturas")
        datos = cursor.fetchall()
        
        for dato in datos:
            tabla.insert("", tk.END, values=dato)
        conn.close()
    
    cargar_datos()
    
    # Frame para mostrar los datos
    frame_datos = ttk.Frame(box)
    frame_datos.grid(row=3, column=0)
    
    dato = ttk.LabelFrame(frame_datos, text="Datos", padding=10)
    dato.grid(row=0, column=0, padx=10, sticky="w")
    
    # Etiquetas para los datos seleccionados
    ttk.Label(dato, text="ID:", font=("Arial", 12, "bold")).grid(row=0, column=0,sticky="w")
    ids = ttk.Label(dato, text="")
    ids.grid(row=0, column=1,sticky="w")
    
    ttk.Label(dato, text="Cliente:", font=("Arial", 12, "bold")).grid(row=1, column=0,sticky="w")
    clientes = ttk.Label(dato, text="")
    clientes.grid(row=1, column=1,sticky="w")
    
    ttk.Label(dato, text="Máquina:", font=("Arial", 12, "bold")).grid(row=2, column=0,sticky="w")
    maquina = ttk.Label(dato, text="")
    maquina.grid(row=2, column=1,sticky="w")
    
    ttk.Label(dato, text="Fecha:", font=("Arial", 12, "bold")).grid(row=3, column=0,sticky="w")
    fecha = ttk.Label(dato, text="")
    fecha.grid(row=3, column=1,sticky="w")
    
    ttk.Label(dato, text="Importe:", font=("Arial", 12, "bold")).grid(row=4, column=0,sticky="w")
    importe = ttk.Label(dato, text="")
    importe.grid(row=4, column=1,sticky="w")
    
    ttk.Label(dato, text="Detalles:", font=("Arial", 12, "bold")).grid(row=5, column=0,sticky="w")
    detalles = ttk.Label(dato, text="")
    detalles.grid(row=5, column=1,sticky="w")
    
    ttk.Label(dato, text="Reparaciones:", font=("Arial", 12, "bold")).grid(row=6, column=0,sticky="w")
    reparaciones = ttk.Label(dato, text="")
    reparaciones.grid(row=6, column=1,sticky="w")
    
    # Función para manejar la selección en la tabla
    def mostrar_datos(event):
        seleccion = tabla.selection()
        if seleccion:
            valores = tabla.item(seleccion, "values")
            ids.config(text=valores[0])
            clientes.config(text=valores[1])
            maquina.config(text=valores[2])
            fecha.config(text=valores[3])
            importe.config(text=valores[4])
            detalles.config(text=valores[5])
            reparaciones.config(text=valores[6])
    
    # Vincular el evento de selección a la función mostrar_datos
    tabla.bind("<<TreeviewSelect>>", mostrar_datos)
    
    # Función para guardar en la tabla `maquinas_terminadas`
    def guardar_reparacion():
        if ids.cget("text") != "":
            # Usar la fecha existente (la que aparece en el Label 'fecha')
            fecha_existente = fecha.cget("text")
            
            conn = sqlite3.connect("BDreparaciones.db")
            cursor = conn.cursor()
            cursor.execute(""" 
                INSERT INTO maquinas_terminadas (ID, Cliente, Maquina, Importe, Detalles, Reparaciones, FechaEmision) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""", (
                ids.cget("text"),           # ID
                clientes.cget("text"),      # Cliente
                maquina.cget("text"),       # Máquina
                importe.cget("text"),       # Importe
                detalles.cget("text"),      # Detalles
                reparaciones.cget("text"),  # Reparaciones
                fecha_existente             # Fecha ya existente
            ))
            
            # Eliminar el registro de la tabla original
            cursor.execute("DELETE FROM datos_facturas WHERE ID = ?", (ids.cget("text"),))
            conn.commit()
            conn.close()
            
            # Mostrar mensaje de éxito
            print(f"Datos guardados con la fecha existente {fecha_existente}.")
            
            # Eliminar de la tabla actual
            for item in tabla.selection():
                tabla.delete(item)

    
    # Botón "Reparado"
    boton_reparado = ttk.Button(frame_datos, text="Maquina Reparada", bootstyle="success", command=guardar_reparacion, padding=10)
    boton_reparado.grid(row=0, column=1, pady=10, padx=10)
