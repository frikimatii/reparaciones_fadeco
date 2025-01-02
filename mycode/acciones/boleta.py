import os
import tkinter as tk
from ttkbootstrap import Label
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
import random
from fpdf import FPDF
from ttkbootstrap import ttk
from datetime import datetime, timedelta

def buscar_datos(tabla, criterio):
    for item in tabla.get_children():
        tabla.delete(item)

    try:
        # Conexión a la base de datos
        conn = sqlite3.connect("BDreparaciones.db")
        cursor = conn.cursor()

        # Consulta con búsqueda por nombre o máquina
        cursor.execute(""" 
            SELECT CLIENTES, PROVEDOR, MAQUINA, DETALLES, IMPORTE, REPARACION
            FROM Datos_reparacion 
            WHERE CLIENTES LIKE ? OR MAQUINA LIKE ? 
        """, (f"%{criterio}%", f"%{criterio}%"))

        # Inserta los resultados en el Treeview
        for row in cursor.fetchall():
            tabla.insert("", 0, values=row)

    except sqlite3.Error as e:
        print("Error al buscar datos:", e)
    finally:
        conn.close()


def mostrar_boleta(frame_contenido):
    # Limpiar el contenido anterior
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    # Crear el contenedor principal
    box = ttk.Frame(frame_contenido, padding=10)
    box.grid(row=0, column=0, sticky="nsew")
    frame_contenido.grid_rowconfigure(0, weight=1)
    frame_contenido.grid_columnconfigure(0, weight=1)

    # Etiqueta de título
    label = Label(box, text="Comprobante de retiro", font=("Helvetica", 18))
    label.grid(row=0, column=0, sticky="n", pady=(0, 10))

    # Contenedor para tabla y búsqueda
    box_tabla = ttk.Frame(box)
    box_tabla.grid(row=1, column=0, sticky="nsew")

    # Entrada de búsqueda
    box_busqueda = ttk.Frame(box_tabla, padding=5)
    box_busqueda.grid(row=0, column=0, sticky="n", pady=(0, 10))

    ttk.Label(box_busqueda, text="Buscar:", font=("Helvetica", 12)).grid(row=0, column=0, sticky="w")
    entry_busqueda = ttk.Entry(box_busqueda, width=30)
    entry_busqueda.grid(row=0, column=1, padx=5, sticky="n")

    # Botón de búsqueda
    btn_buscar = ttk.Button(
        box_busqueda, text="Buscar", bootstyle="success",
        command=lambda: buscar_datos(tabla, entry_busqueda.get())
    )
    btn_buscar.grid(row=0, column=2, padx=5)

    # Contenedor para el Treeview
    box_treeview = ttk.Frame(box_tabla, padding=5)
    box_treeview.grid(row=1, column=0, sticky="nsew")

    columnas_ = ("Cliente","Provedor", "Máquina", "Detalles", "Importe", "Reparacion")
    tabla = ttk.Treeview(box_treeview, columns=columnas_, show="headings", bootstyle="primary")

    for col in columnas_:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)

    tabla.grid(row=0, column=0, pady=10, sticky="nsew")
    tabla.config(height=20)

    # Carga inicial de datos (sin filtrar)
    buscar_datos(tabla, "")

    # Contenedor para los detalles con un Frame contenedor alrededor del Labelframe
    frame_detalles = ttk.Frame(box)  # Este es el Frame contenedor
    frame_detalles.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)

    # Labelframe para los detalles
    detalles_frame = ttk.Labelframe(frame_detalles, text="Detalles del Cliente", bootstyle="info", padding=10)
    detalles_frame.grid(row=0, column=0, sticky="nsew")

    # Etiquetas dentro del Labelframe
    label_nombre = ttk.Label(detalles_frame, text="Cliente: ", font=("Helvetica", 12))
    label_nombre.grid(row=0, column=0, sticky="w", pady=5)

    label_provedor = ttk.Label(detalles_frame, text="Provedor: ", font=("Helvetica", 12))
    label_provedor.grid(row=1, column=0, sticky="w", pady=5)
    
    label_maquina = ttk.Label(detalles_frame, text="Máquina: ", font=("Helvetica", 12))
    label_maquina.grid(row=2, column=0, sticky="w", pady=5)

    label_importe = ttk.Label(detalles_frame, text="Importe: ", font=("Helvetica", 12))
    label_importe.grid(row=3, column=0, sticky="w", pady=5)

    label_detalles = ttk.Label(detalles_frame, text="Detalles: ", font=("Helvetica", 12), wraplength=200)
    label_detalles.grid(row=4, column=0, sticky="w", pady=5)

    label_reparacion = ttk.Label(detalles_frame, text="Reparacion: ", font=("Helvetica", 12), wraplength=200)
    label_reparacion.grid(row=5, column=0, sticky="w", pady=5)

    btn_imprimir = ttk.Button(detalles_frame, text="Generar Comprobante", command=lambda: imprimir_comprobante())
    btn_imprimir.grid(row=6, column=0, sticky="w", pady=5)

    # Función para actualizar los detalles al seleccionar un elemento
    def actualizar_detalles(event):
        # Obtener la selección
        item = tabla.selection()
        if item:
            valores = tabla.item(item, "values")
            label_nombre.config(text=f"Nombre: {valores[0]}", font=("Arial", 12, "bold"))
            label_provedor.config(text=f"Provedor: {valores[1]}", font=("Arial", 12, "bold"))
            label_maquina.config(text=f"Máquina: {valores[2]}", font=("Arial", 12, "bold"))
            label_reparacion.config(text=f"Reparacion: {valores[5]}", font=("Arial", 12, "bold"))
            label_importe.config(text=f"Importe $: {valores[4]}", font=("Arial", 12, "bold"))
            label_detalles.config(text=f"Detalles: {valores[3]}", font=("Arial", 12, "bold"))

    # Asignar el evento de selección al Treeview
    tabla.bind("<<TreeviewSelect>>", actualizar_detalles)




    def imprimir_comprobante():
        try:
            # Obtener texto de las etiquetas
            cliente = label_nombre.cget("text").split(":")[1].strip()
            provedor = label_provedor.cget("text").split(":")[1].strip()
            maquina = label_maquina.cget("text").split(":")[1].strip()
            importe = label_importe.cget("text").split(":")[1].strip()
            detalles = label_detalles.cget("text").split(":")[1].strip()
            reparacion = label_reparacion.cget("text").split(":")[1].strip()

            # Validar datos
            if not (cliente and maquina and importe and detalles and reparacion and provedor):
                print("Error: Faltan datos para generar el comprobante.")
                return

            fecha_factura = datetime.now()
            fecha_factura_str = fecha_factura.strftime('%d/%m/%Y')

            # Calcular la fecha límite (60 días después de la fecha de la factura)
            fecha_limite = fecha_factura + timedelta(days=60)
            fecha_limite_str = fecha_limite.strftime('%d/%m/%Y')

            # Generar ID de factura aleatorio
            id_factura = 'F' + str(random.randrange(1000000, 999999999))

            # Crear carpeta para guardar PDFs
            carpeta_pdf = "ComprobantesRetiro"
            if not os.path.exists(carpeta_pdf):
                os.makedirs(carpeta_pdf)

            # Conectar a la base de datos
            conn = sqlite3.connect("BDreparaciones.db")
            cursor = conn.cursor()

            # Insertar datos en la base de datos
            cursor.execute(
            "INSERT INTO datos_facturas (ID, Cliente , Provedor, Maquina,Fecha_factura, Importe, Detalles, Reparaciones) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (id_factura, cliente, provedor, maquina, fecha_factura_str, importe, detalles, reparacion)
            )
            conn.commit()
            conn.close()

            # Definir el nombre del archivo
            pdf_file = os.path.join(
                carpeta_pdf,
                f"Factura_{id_factura}_{cliente.replace(' ', '_')}_{maquina.replace(' ', '_')}.pdf"
            )

            # Generar PDF
            pdf = FPDF()
            pdf.add_page()

            # Cabecera
            pdf.set_xy(10, 10)
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 5, 'Eduardo', ln=True)
            pdf.cell(0, 5, "Reparaciones de Cortadoras", ln=True)
            pdf.cell(0, 5, "1 de Agosto de 1806 3687, B1650 Billinghurst", ln=True)
            pdf.cell(0, 5, "Telefono: 011 5113-2717", ln=True)
            pdf.cell(0, 5, f"Fecha Emicion: {fecha_factura_str}", ln=True)

            pdf.ln(7)

            # Título
            pdf.set_font("Arial", size=18)
            pdf.cell(0, 10, "Comprobante de Retiro", ln=True, align='C')

            # Información de la factura
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, f"Numero Factura: {id_factura}", ln=True, align="C")
            pdf.cell(0, 5, "=" * 45, ln=True, align='C')
            pdf.set_font('Arial', 'U', 12)  # 'U' is for underline
            pdf.cell(0, 10, "Datos Del Cliente", ln=True, align='L')
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, f"Cliente: {cliente}", ln=True, align='L')
            pdf.cell(0, 10, f"Maquina: {maquina}", ln=True, align='L')
            pdf.multi_cell(0, 5, f"Reparacion: {reparacion}", align='L')
            pdf.cell(0, 10, f"Provedor: {provedor}", ln=True, align='L')
            pdf.cell(0, 10, f"Importe  {importe} $", ln=True, align='L')
            pdf.multi_cell(0, 5, f"Detalles De la Maquina: {detalles}", align='L')
            pdf.cell(0, 5, "=" * 45, ln=True, align='C')
            pdf.ln(5)

            # Mensaje de advertencia
            pdf.cell(0, 8, f"=====Si no retira la máquina en 60 días, no hay reclamo para retirarla.=====", ln=True, align='C')
            pdf.cell(0, 5, f"=====Fecha límite: {fecha_limite_str}=====", ln=True, align='C')
            pdf.ln(15)
            
            
            pdf.cell(0, 8, f"................................................................................................................................................................", ln=True, align='C')
            
            pdf.set_font("Arial", size=18)
            pdf.cell(0, 10, "Comprobante de reparacion", ln=True, align='C')
            pdf.ln(5)
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, f"Numero Factura: {id_factura}", ln=True, align="C")
            pdf.set_font('Arial', 'U', 12)  # 'U' is for underline
            pdf.cell(0, 10, "Datos Del Cliente", ln=True, align='C')
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, f"Cliente: {cliente}", ln=True, align='C')
            pdf.cell(0, 10, f"Maquina: {maquina}", ln=True, align='C')
            pdf.multi_cell(0, 5, f"Reparacion: {reparacion}", align='C')
            pdf.cell(0, 10, f"Provedor: {provedor}", ln=True, align='C')

            # Guardar el PDF
            pdf.output(pdf_file)

            # Mostrar mensaje de éxito
            print(f"Comprobante generado: {pdf_file}")

            # Intentar abrir el archivo PDF
            if os.name == 'posix':  # Linux or MacOS
                os.system(f"xdg-open {pdf_file}")
            elif os.name == 'nt':  # Windows
                os.startfile(pdf_file)

        except Exception as e:
            print(f"Error al generar el comprobante: {e}")
