import tkinter as tk
from ttkbootstrap import Label
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime  # Para manejar fechas
from fpdf import FPDF
import os
import sqlite3
from datetime import timedelta

def maquina_final(frame_contenido):
    # Eliminar widgets previos
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    # Crear el marco principal
    box = ttk.Frame(frame_contenido, padding=10)
    box.grid(row=0, column=0, sticky="nsew")
    
    frame_contenido.grid_rowconfigure(0, weight=1)
    frame_contenido.grid_columnconfigure(0, weight=1)
    
    # Etiqueta principal
    label = Label(box, text="Máquinas Terminadas", font=("Helvetica", 18))
    label.grid(row=0, column=0, sticky="n", pady=(0, 10))
    
    # Frame para la tabla
    box_treeview = ttk.Frame(box)
    box_treeview.grid(row=1, column=0)
    
    columnas_visibles = ('ID', 'Cliente', 'Maquina', 'Importe', 'Detalles', 'Reparaciones', 'FechaEmision')
    
    # Crear Treeview
    tabla = ttk.Treeview(box_treeview, columns=columnas_visibles, show='headings', bootstyle='primary')
    
    for col in columnas_visibles:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)
    
    tabla.grid(row=0, column=0, pady=10)
    tabla.config(height=10)
    
    # Función para cargar datos en la tabla
    def cargar_datos():
        tabla.delete(*tabla.get_children())  # Limpiar la tabla
        conn = sqlite3.connect("BDreparaciones.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Cliente, Maquina, Importe, Detalles, Reparaciones, FechaEmision FROM maquinas_terminadas")
        datos = cursor.fetchall()
        
        for dato in datos:
            tabla.insert("", tk.END, values=dato)
        
        conn.close()
    
    # Cargar los datos al iniciar
    cargar_datos()
    
    # Frame para mostrar los datos seleccionados
    frame_datos = ttk.Frame(box)
    frame_datos.grid(row=2, column=0, pady=10)
    
    dato = ttk.LabelFrame(frame_datos, text="Detalles de la Máquina Terminada", padding=10)
    dato.grid(row=0, column=0, padx=10)
    
    # Etiquetas para mostrar los datos seleccionados
    ttk.Label(dato, text="ID:", font=("Arial", 12, "bold")).grid(row=0, column=0,sticky="w")
    ids = ttk.Label(dato, text="")  # Inicialmente vacío
    ids.grid(row=0, column=1,sticky="w")
    
    ttk.Label(dato, text="Cliente:", font=("Arial", 12, "bold")).grid(row=1, column=0,sticky="w")
    clientes = ttk.Label(dato, text="")  # Inicialmente vacío
    clientes.grid(row=1, column=1,sticky="w")
    
    ttk.Label(dato, text="Máquina:", font=("Arial", 12, "bold")).grid(row=2, column=0,sticky="w")
    maquina = ttk.Label(dato, text="")  # Inicialmente vacío
    maquina.grid(row=2, column=1,sticky="w")
    
    ttk.Label(dato, text="Importe:", font=("Arial", 12, "bold")).grid(row=3, column=0,sticky="w")
    importe = ttk.Label(dato, text="")  # Inicialmente vacío
    importe.grid(row=3, column=1,sticky="w")
    
    ttk.Label(dato, text="Detalles:", font=("Arial", 12, "bold")).grid(row=4, column=0,sticky="w")
    detalles = ttk.Label(dato, text="")  # Inicialmente vacío
    detalles.grid(row=4, column=1,sticky="w")
    
    ttk.Label(dato, text="Reparaciones:", font=("Arial", 12, "bold")).grid(row=5, column=0,sticky="w")
    reparaciones = ttk.Label(dato, text="")  # Inicialmente vacío
    reparaciones.grid(row=5, column=1,sticky="w")
    
    ttk.Label(dato, text="Fecha de Emisión:", font=("Arial", 12, "bold")).grid(row=6, column=0,sticky="w")
    fecha_emision = ttk.Label(dato, text="")  # Inicialmente vacío
    fecha_emision.grid(row=6, column=1,sticky="w")
    
    # Función para manejar la selección en la tabla
    def mostrar_datos(event):
        seleccion = tabla.selection()
        if seleccion:
            valores = tabla.item(seleccion, "values")
            ids.config(text=valores[0])
            clientes.config(text=valores[1])
            maquina.config(text=valores[2])
            importe.config(text=valores[3])
            detalles.config(text=valores[4])
            reparaciones.config(text=valores[5])
            fecha_emision.config(text=valores[6])
    
    # Vincular el evento de selección a la función mostrar_datos
    tabla.bind("<<TreeviewSelect>>", mostrar_datos)
    
    # Función para crear factura final
    # Función para crear factura
    def crear_factura():
        try:
            # Asegurarnos de que se haya seleccionado una fila
            seleccion = tabla.selection()
            if not seleccion:
                print("Error: No se ha seleccionado ninguna máquina.")
                return

            # Obtener los valores de la fila seleccionada
            valores = tabla.item(seleccion, "values")
            id_factura = valores[0]
            cliente = valores[1]
            maquina = valores[2]
            importe = valores[3]
            detalles = valores[4]
            reparaciones = valores[5]
            fecha_emision = valores[6]

            # Validar que los campos no estén vacíos
            if not (cliente and maquina and importe and detalles and reparaciones and fecha_emision and id_factura):
                print("Error: Faltan datos para generar la factura.")
                return

            # Fecha de la factura
            fecha_factura = datetime.strptime(fecha_emision, "%d/%m/%Y")
            fecha_factura_str = fecha_factura.strftime('%d/%m/%Y')

            # Calcular la fecha límite (60 días después de la fecha de la factura)
            fecha_limite = fecha_factura + timedelta(days=30)
            fecha_limite_str = fecha_limite.strftime('%d/%m/%Y')

            # Crear carpeta para guardar PDFs si no existe
            carpeta_pdf = "FacturasFinales"
            if not os.path.exists(carpeta_pdf):
                os.makedirs(carpeta_pdf)

            # Conectar a la base de datos para almacenar los datos de la factura
            conn = sqlite3.connect("BDreparaciones.db")
            cursor = conn.cursor()

            # Insertar la nueva factura en la base de datos
            cursor.execute(
                "INSERT INTO datos_facturas (ID, Cliente, Maquina, Fecha_factura, Importe, Detalles, Reparaciones) VALUES   (?, ?, ?, ?, ?, ?, ?)",
                (id_factura, cliente, maquina, fecha_factura_str, importe, detalles, reparaciones)
            )
            conn.commit()
            conn.close()

            # Definir el nombre del archivo PDF
            pdf_file = os.path.join(
                carpeta_pdf,
                f"Factura_{id_factura}_{cliente.replace(' ', '_')}_{maquina.replace(' ', '_')}.pdf"
            )

            # Generar el PDF
            pdf = FPDF()
            pdf.add_page()

            # Cabecera de la factura
            pdf.set_xy(10, 10)
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 5, 'Eduardo', ln=True)
            pdf.cell(0, 5, "Reparaciones de Cortadoras", ln=True)
            pdf.cell(0, 5, "1 de Agosto de 1806 3687, B1650 Billinghurst", ln=True)
            pdf.cell(0, 5, "Telefono: 011 5113-2717", ln=True)
            pdf.cell(0, 5, f"Fecha Emisión: {fecha_factura_str}", ln=True)

            pdf.ln(7)

            # Título de la factura
            pdf.set_font("Arial", size=18)
            pdf.cell(0, 10, "Factura Final", ln=True, align='C')

            # Detalles de la factura
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, f"Numero Factura: {id_factura}", ln=True, align="C")
            pdf.cell(0, 5, "=" * 45, ln=True, align='C')
            pdf.cell(0, 10, "Datos Del Cliente", ln=True, align='L')
            pdf.cell(0, 10, f"Cliente: {cliente}", ln=True, align='L')
            pdf.cell(0, 10, f"Maquina: {maquina}", ln=True, align='L')
            pdf.multi_cell(0, 5, f"Reparación: {reparaciones}", align='L')
            pdf.cell(0, 10, f"Importe: {importe} $", ln=True, align='L')
            pdf.multi_cell(0, 5, f"Detalles De la Maquina: {detalles}", align='L')
            pdf.cell(0, 5, "=" * 45, ln=True, align='C')
            pdf.ln(5)

            # Mensaje de advertencia
            pdf.cell(0, 8, f"Factura generada en fecha {fecha_factura_str}", ln=True, align='C')
            pdf.cell(0, 5, f"Garantia: {fecha_limite_str}", ln=True, align="C")
            pdf.cell(0, 5, "Gracias por elegirnos", ln=True, align="C")

            # Guardar el archivo PDF
            pdf.output(pdf_file)
            print(f"Factura creada: {pdf_file}")
            os.startfile(pdf_file)
        except Exception as e:
            print(f"Error al generar la factura: {e}")

    
    # Botón para crear factura
    factura_button = ttk.Button(box, text="Crear Factura", bootstyle="success", command=crear_factura)
    factura_button.grid(row=3, column=0, pady=20)
