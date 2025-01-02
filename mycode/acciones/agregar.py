import tkinter as tk
from ttkbootstrap import Label, DateEntry
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
from datetime import datetime
import threading
import time
from tkinter import ttk, messagebox

from mycode.funciones.funcion_buscar import datos, mostrar_datos
querty_datos_pricipales_ = "SELECT CLIENTES, FECHA, DIRECCION, TELEFONO, PROVEDOR, MAQUINA, IMPORTE, DETALLES, REPARACION FROM Datos_reparacion"


# Función para obtener reparaciones de la base de datos
def actualizar_lista_reparaciones():
    lista = []
    try:
        conn = sqlite3.connect("BDreparaciones.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MECANIZADO FROM Precio_Mecanizado")
        datos = cursor.fetchall()
        lista = [dato[0] for dato in datos]
    except sqlite3.Error as e:
        print("Error al obtener reparaciones:", e)
    finally:
        conn.close()
    return lista

# Pantalla principal para gestionar clientes
def mostrar_clientes(frame_contenido):
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    main_frame = ttk.Frame(frame_contenido, padding=10)
    main_frame.pack(fill="both", expand=True)

    ttk.Label(main_frame, text="Clientes", font=("Helvetica", 16)).pack(pady=3)

    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=3)

    ttk.Button(button_frame, text="Agregar", command=lambda: cambiar_pantalla('agregar', content_frame), bootstyle="success").grid(row=0, column=0, padx=10)
    ttk.Button(button_frame, text="Modificar", command=lambda: cambiar_pantalla('modificar', content_frame), bootstyle="warningn").grid(row=0, column=1, padx=10)
    ttk.Button(button_frame, text="Eliminar", command=lambda: cambiar_pantalla('eliminar', content_frame), bootstyle="danger").grid(row=0, column=2, padx=10)

    content_frame = ttk.Frame(main_frame)
    content_frame.pack(fill="both", expand=True, pady=10)

    cambiar_pantalla('agregar', content_frame)

# Cambiar entre pantallas
def cambiar_pantalla(accion, frame):
    for widget in frame.winfo_children():
        widget.destroy()
    if accion == 'agregar':
        mostrar_agregar(frame)
    elif accion == 'modificar':
        mostrar_modificar(frame)
    elif accion == 'eliminar':
        mostrar_borrar(frame)
# Pantalla para agregar clientes




def mostrar_agregar(frame):
    lista_reparaciones = actualizar_lista_reparaciones()

    # Frame de datos del cliente
    frame_cliente = ttk.LabelFrame(frame, text="Información del Cliente", padding=10, bootstyle="light")
    frame_cliente.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    campos = ["Cliente", "Dirección", "Email", "Máquina", "Teléfono", "Proveedor"]
    entradas = {}
    for i, campo in enumerate(campos):
        ttk.Label(frame_cliente, text=campo, font=("Helvetica", 12)).grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entradas[campo] = ttk.Entry(frame_cliente, width=30)
        entradas[campo].grid(row=i, column=1, padx=5, pady=5)

    # Frame de detalles adicionales
    frame_proveedor = ttk.LabelFrame(frame, text="Detalles Adicionales", padding=10, bootstyle="light")
    frame_proveedor.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    ttk.Label(frame_proveedor, text="Reparaciones", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    listbox_reparaciones = tk.Listbox(frame_proveedor, selectmode=tk.MULTIPLE, height=8, width=30)
    listbox_reparaciones.grid(row=0, column=1, padx=5, pady=5)

    for reparacion in lista_reparaciones:
        listbox_reparaciones.insert(tk.END, reparacion)

    ttk.Label(frame_proveedor, text="Presupuesto $", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="nw")
    resultado_presupuesto = ttk.Label(frame_proveedor, text="0", font=("Helvetica", 12, "bold"))
    resultado_presupuesto.grid(row=1, column=1, padx=5, pady=5, sticky="nw")

    ttk.Label(frame_proveedor, text="Detalles o Estado de La Maquina", font=("Helvetica", 12), wraplength=100).grid(row=2, column=0, padx=5, pady=5, sticky="nw")
    entry_detalles = tk.Text(frame_proveedor, width=30, height=5)
    entry_detalles.grid(row=2, column=1, padx=5, pady=5)

    listbox_reparaciones.bind("<<ListboxSelect>>", lambda event: actualizar_presupuesto(listbox_reparaciones, resultado_presupuesto))

    # Frame de guardar
    frame_guardar = ttk.LabelFrame(frame, text="Guardar Información", padding=10, bootstyle="light")
    frame_guardar.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    el_cliente = ttk.Label(frame_guardar, text="",foreground="green")
    el_cliente.grid(row=0, column=0)
    
    progress = ttk.Progressbar(frame_guardar, orient="horizontal", mode="determinate", length=150, bootstyle="success")
    progress.grid(row=1, column=0, pady=5)

    btn_guardar = ttk.Button(frame_guardar, text="Guardar", command=lambda: iniciar_guardado(
        entradas["Cliente"].get(), entradas["Dirección"].get(),entradas["Email"].get(), entradas["Máquina"].get(), entradas["Teléfono"].get(), entradas["Proveedor"].get(),  listbox_reparaciones, resultado_presupuesto, entry_detalles, el_cliente, progress), bootstyle="success")
    btn_guardar.grid(row=2, column=0, pady=10)

# Actualizar presupuesto basado en reparaciones seleccionadas
def actualizar_presupuesto(listbox_reparaciones, resultado_presupuesto):
    reparaciones_seleccionadas = [listbox_reparaciones.get(i) for i in listbox_reparaciones.curselection()]
    if not reparaciones_seleccionadas:
        resultado_presupuesto.config(text="0")
        return

    try:
        conn = sqlite3.connect("BDreparaciones.db")
        cursor = conn.cursor()
        total = sum(
            cursor.execute("SELECT PRECIO FROM Precio_Mecanizado WHERE MECANIZADO = ?", (rep,)).fetchone()[0]
            for rep in reparaciones_seleccionadas
        )
        resultado_presupuesto.config(text=str(total))
    except sqlite3.Error as e:
        print("Error:", e)
        resultado_presupuesto.config(text="Error")
    finally:
        conn.close()

# Guardar cliente con progreso
def iniciar_guardado(cliente, direccion,email, maquina, telefono,  proveedor, listbox_reparaciones, resultado_presupuesto, detalles, el_cliente, progress):
    progress["value"] = 0
    threading.Thread(target=guardar_cliente, args=(
        cliente, direccion,  email,maquina, telefono, proveedor, listbox_reparaciones, 
        resultado_presupuesto, detalles, el_cliente, progress)).start()

def guardar_cliente(cliente, direccion, email, maquina,  telefono, proveedor, listbox_reparaciones, resultado_presupuesto, detalles, el_cliente, progress):
    reparaciones_seleccionadas = [listbox_reparaciones.get(i) for i in listbox_reparaciones.curselection()]
    if not reparaciones_seleccionadas:
        el_cliente.config(text="Seleccione al menos una reparación.")
        return

    presupuesto = resultado_presupuesto.cget("text")
    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    try:
        conn = sqlite3.connect("BDreparaciones.db")
        cursor = conn.cursor()
        for i in range(1, 101):
            progress["value"] = i
            time.sleep(0.02)
        cursor.execute("""
            INSERT INTO Datos_reparacion (CLIENTES, DIRECCION,EMAIL, FECHA, MAQUINA,  TELEFONO, PROVEDOR, REPARACION, IMPORTE, DETALLES)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
            (cliente, direccion,email, fecha_actual, maquina, telefono, proveedor,  ", ".join(reparaciones_seleccionadas), presupuesto, detalles.get("1.0", tk.END)))
        conn.commit()
        el_cliente.config(text="Cliente guardado exitosamente.")
    except sqlite3.Error as e:
        el_cliente.config(text="Error al guardar cliente.")
        print("Error:", e)
    finally:
        conn.close()
        progress["value"] = 100
        el_cliente.after(2000, lambda: el_cliente.config(text=""))
        progress["value"] = 0



def mostrar_modificar(frame):
    # Crear marco principal
    caja = ttk.Frame(frame)
    caja.grid(row=0, column=0, columnspan=3, padx=3, pady=3, sticky="nsew")

    # Información de Clientes
    cajainfo = ttk.Frame(caja)
    cajainfo.grid(row=0, column=0, sticky="nsew")

    info = ttk.Labelframe(cajainfo, text="Información de Clientes", padding=10, bootstyle="light")
    info.grid(row=0, column=0, padx=7, pady=3, sticky="nsew")

    ttk.Label(info, text="Cliente:").grid(row=0, column=0, padx=5, pady=5)
    entry_cliente = ttk.Entry(info)
    entry_cliente.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(info, text="Dirección:").grid(row=1, column=0, padx=5, pady=5)
    entry_direccion = ttk.Entry(info)
    entry_direccion.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(info, text="Máquina:").grid(row=2, column=0, padx=5, pady=5)
    entry_maquina = ttk.Entry(info)
    entry_maquina.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(info, text="Teléfono:").grid(row=3, column=0, padx=5, pady=5)
    entry_telefono = ttk.Entry(info)
    entry_telefono.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(info, text="Fecha:").grid(row=4, column=0, padx=5, pady=5)
    entry_fecha = ttk.Entry(info)
    entry_fecha.grid(row=4, column=1, padx=5, pady=5)

    # Detalles
    cajadetalles = ttk.Frame(caja)
    cajadetalles.grid(row=0, column=1)

    detalles = ttk.Labelframe(cajadetalles, text="Detalles", padding=10, bootstyle="light")
    detalles.grid(row=0, column=0, padx=7, pady=3, sticky="nsew")

    ttk.Label(detalles, text="Detalles:").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
    caja_texto = tk.Text(detalles, height=3, width=30)
    caja_texto.grid(row=1, column=1, padx=5, pady=5, sticky="nw")

    ttk.Label(detalles, text="Proveedor:").grid(row=2, column=0, padx=5, pady=5, sticky="nw")
    entry_proveedor = ttk.Entry(detalles)
    entry_proveedor.grid(row=2, column=1, padx=5, pady=5, sticky="nw")

    ttk.Label(detalles, text="Reparación:").grid(row=3, column=0, sticky="nw")
    reparacion = tk.Listbox(detalles, height=3, width=30)
    reparacion.grid(row=3, column=1, sticky="nw", padx=5, pady=5)

    ttk.Label(detalles, text="Importe").grid(row=4, column=0, sticky="nw")
    importe = ttk.Entry(detalles)
    importe.grid(row=4, column=1, padx=5, pady=5, sticky="nw")

    # Botones y barra de progreso
    acciones_btn = ttk.Frame(caja)
    acciones_btn.grid(row=0, column=2)

    btn_frame = ttk.Labelframe(acciones_btn, text="Actualizar Datos", padding=10, bootstyle="light")
    btn_frame.grid(row=0, column=0, padx=3, pady=7, sticky="nsew")

    el_cliente = ttk.Label(btn_frame, text="", foreground="yellow")
    el_cliente.grid(row=0, column=0, padx=5, pady=5)

    progress = ttk.Progressbar(btn_frame, orient="horizontal", mode="determinate", length=150, bootstyle="warning")
    progress.grid(row=1, column=0, pady=5, padx=5)

    actualizar_btn = ttk.Button(btn_frame, text="Actualizar")
    actualizar_btn.grid(row=2, column=0, padx=5, pady=5)

    # Treeview para mostrar los datos
    box_treeview = ttk.Frame(frame, padding=5)
    box_treeview.grid(row=1, column=0)

    columnas_visibles = ('Clientes', 'Fecha', 'Direccion', 'Telefono', 'Proveedor', 'Maquina', 'Importe')
    tabla = ttk.Treeview(box_treeview, columns=columnas_visibles, show='headings', bootstyle="primary")

    for col in columnas_visibles:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)

    tabla.grid(row=0, column=0, pady=10)
    tabla.config(height=7)

    # Función para cargar datos desde la base de datos
    def cargar_datos():
        tabla.delete(*tabla.get_children())  # Limpiar tabla
        conexion = sqlite3.connect("BDreparaciones.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT CLIENTES, FECHA, DIRECCION, TELEFONO, PROVEDOR, MAQUINA, REPARACION, IMPORTE, DETALLES FROM Datos_reparacion")
        for fila in cursor.fetchall():
            valores_visibles = fila[:6] + (fila[7],)  # Mostrar CLIENTES a IMPORTE
            tabla.insert('', tk.END, values=valores_visibles + fila[6:])  # REPARACION y DETALLES como valores ocultos
        conexion.close()

    # Actualizar campos al seleccionar un elemento
    def actualizar_campos(event):
        selected_item = tabla.selection()
        if selected_item:
            values = tabla.item(selected_item)['values']
            entry_cliente.delete(0, tk.END)
            entry_cliente.insert(0, values[0])
            entry_fecha.delete(0, tk.END)
            entry_fecha.insert(0, values[1])
            entry_direccion.delete(0, tk.END)
            entry_direccion.insert(0, values[2])
            entry_telefono.delete(0, tk.END)
            entry_telefono.insert(0, values[3])
            entry_proveedor.delete(0, tk.END)
            entry_proveedor.insert(0, values[4])
            entry_maquina.delete(0, tk.END)
            entry_maquina.insert(0, values[5])
            importe.delete(0, tk.END)
            importe.insert(0, values[6])
            caja_texto.delete("1.0", tk.END)
            caja_texto.insert("1.0", values[9])

            # Limpiar Listbox y seleccionar los valores correspondientes
            reparacion.delete(0, tk.END)
            for item in values[7].split(", "):  # Dividir los datos en una lista
                reparacion.insert(tk.END, item)

    def guardar_modificaciones():
        selected_item = tabla.selection()
        if selected_item:
            cliente = entry_cliente.get()
            direccion = entry_direccion.get()
            maquina = entry_maquina.get()
            telefono = entry_telefono.get()
            fecha = entry_fecha.get()
            proveedor = entry_proveedor.get()
            detalles = caja_texto.get("1.0", tk.END).strip()
            importe_valor = importe.get()
            reparaciones = ", ".join(reparacion.get(0, tk.END))
            values = tabla.item(selected_item)['values']
           
            # Configuración inicial de la barra de progreso
            progress['value'] = 0

            for step in range(1, 101):
                progress['value'] = step
                progress.update_idletasks()
                time.sleep(0.02)

            # Conexión a la base de datos para realizar la actualización
            conexion = sqlite3.connect("BDreparaciones.db")
            cursor = conexion.cursor()
            cursor.execute(""" 
               UPDATE Datos_reparacion
               SET CLIENTES = ?, FECHA = ?, DIRECCION = ?, TELEFONO = ?, PROVEDOR = ?, MAQUINA = ?, REPARACION = ?, IMPORTE = ?, DETALLES = ?
               WHERE CLIENTES = ? AND FECHA = ? AND DIRECCION = ?
           """, (cliente, fecha, direccion, telefono, proveedor, maquina, reparaciones, importe_valor, detalles,
                  values[0], values[1], values[2]))
            conexion.commit()
            conexion.close()

            cargar_datos()
            el_cliente.config(text="¡Datos Actualizados!")

    actualizar_btn.config(command=guardar_modificaciones)

    # Cargar datos iniciales
    cargar_datos()

    tabla.bind("<ButtonRelease-1>", actualizar_campos)



def mostrar_borrar(frame):
    # Crear contenedor principal
    box = ttk.Frame(frame)
    box.grid(row=0, column=0)

    tree = ttk.Frame(box)
    tree.grid(row=0, column=0)

    box_treeview = ttk.Frame(tree, padding=5)
    box_treeview.grid(row=1, column=0)

    # Columnas visibles
    columnas = ('Clientes', 'Fecha', 'Direccion', 'Telefono', 'Proveedor', 'Maquina', 'Importe')
    tabla = ttk.Treeview(box_treeview, columns=columnas, show='headings', bootstyle="info")

    # Configurar columnas
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)

    tabla.grid(row=0, column=0)
    tabla.config(height=14)

    # Mostrar datos en el Treeview
    datos_tabla(tabla)

    # Contenedor inferior para información y botón
    box_elimiar = ttk.Frame(box)
    box_elimiar.grid(row=1, column=0, columnspan=2)

    # Sección para mostrar datos seleccionados
    datoinfo = ttk.Labelframe(box_elimiar, text="Datos Info", padding=20)
    datoinfo.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

    ttk.Label(datoinfo, text="Cliente").grid(row=1, column=0)
    lbl_cliente = ttk.Label(datoinfo, text="", font=("Arial", 12, "bold"))
    lbl_cliente.grid(row=2, column=0, padx=5, pady=5)
    ttk.Label(datoinfo, text="Maquinas").grid(row=3, column=0)
    lbl_maquina = ttk.Label(datoinfo, text="", font=("Arial", 12, "bold"))
    lbl_maquina.grid(row=4, column=0, padx=5, pady=5)

    # Sección para el botón y la barra de progreso
    frame_bnt = ttk.Labelframe(box_elimiar, text="Acciones", padding=20)
    frame_bnt.grid(row=0, column=1, padx=5, pady=5)

    lbl_notificacion = ttk.Label(frame_bnt, text="")
    lbl_notificacion.grid(row=0, column=0, padx=5, pady=5)
    # Barra de progreso
    barra_progreso = ttk.Progressbar(frame_bnt, orient="horizontal", mode="determinate", length=150, bootstyle="danger")
    barra_progreso.grid(row=2, column=0, padx=5, pady=5)

    btn_eliminar = ttk.Button(
        frame_bnt,
        text="Eliminar",
        padding=10,
        command=lambda: elimina_seleccionar(tabla, lbl_cliente, lbl_maquina, barra_progreso,    lbl_notificacion),
        bootstyle="danger"
    )
    btn_eliminar.grid(row=3, column=0, padx=5, pady=5)


    # Vincular evento de selección en el Treeview
    tabla.bind("<<TreeviewSelect>>", lambda e: mostrar_seleccion(tabla, lbl_cliente, lbl_maquina))


def datos_tabla(tabla):
    conn = sqlite3.connect("BDreparaciones.db")
    cursor = conn.cursor()

    try:
        consulta = "SELECT CLIENTES, FECHA, DIRECCION, TELEFONO, PROVEDOR, MAQUINA, IMPORTE FROM Datos_reparacion"
        cursor.execute(consulta)

        for fila in cursor.fetchall():
            tabla.insert("", "end", values=fila)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")
    finally:
        conn.close()


def mostrar_seleccion(tabla, lbl_cliente, lbl_maquina):
    """Muestra los datos del registro seleccionado en las etiquetas."""
    seleccionado = tabla.selection()

    if not seleccionado:
        return

    item = tabla.item(seleccionado)
    valores = item['values']

    # Actualizar etiquetas con Cliente y Máquina
    lbl_cliente.config(text=f"{valores[0]}")
    lbl_maquina.config(text=f"{valores[5]}")
    
    
def elimina_seleccionar(tabla, lbl_cliente, lbl_maquina, barra_progreso, lbl_notificacion):

    seleccionado = tabla.selection()

    if not seleccionado:
        lbl_notificacion.config(text="Error: Por favor, selecciona un elemento para eliminar.", foreground="red")
        return

    # Obtener datos del elemento seleccionado
    item = tabla.item(seleccionado)
    id_item = item['values'][0]  # Asumiendo que 'CLIENTES' es único

    # Pausa breve antes de iniciar la barra de progreso
    time.sleep(0.5)

    # Configurar barra de progreso
    barra_progreso['value'] = 0  # Reiniciar barra
    barra_progreso.grid()  # Mostrar barra de progreso
    barra_progreso.update()

    conn = sqlite3.connect("BDreparaciones.db")
    cursor = conn.cursor()

    try:
        # Simular progreso continuo (avance más fluido)
        for step in range(1, 101):  # Rango de 1 a 100 para simular progreso continuo
            barra_progreso['value'] = step
            barra_progreso.update()
            time.sleep(0.02)  # Ajusta el tiempo para controlar la velocidad del progreso

        # Eliminar de la base de datos
        cursor.execute("DELETE FROM Datos_reparacion WHERE CLIENTES = ?", (id_item,))
        conn.commit()

        # Eliminar del Treeview
        tabla.delete(seleccionado)

        # Limpiar etiquetas
        lbl_cliente.config(text="")
        lbl_maquina.config(text="")

        # Mensaje de éxito
        lbl_notificacion.config(text="Registro eliminado correctamente.", foreground="red")

    except Exception as e:
        conn.rollback()
    finally:
        # Ocultar barra de progreso después de completarse
        time.sleep(0.5)
        barra_progreso['value'] = 0
        lbl_notificacion.after(2000, lambda: lbl_notificacion.config(text=""))
        conn.close()
