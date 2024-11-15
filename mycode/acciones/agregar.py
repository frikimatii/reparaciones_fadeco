import tkinter as tk
from ttkbootstrap import Label, DateEntry
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3

def actualizar_lista_reparaciones():
    """Función para obtener la lista de reparaciones de la base de datos en tiempo real."""
    lista = []
    conn = sqlite3.connect("BDreparaciones.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MECANIZADO FROM reparaciones")
    datos = cursor.fetchall()
    lista = [dato[0] for dato in datos]
    conn.close()
    return lista

# Función principal para mostrar la pantalla de clientes
def mostrar_clientes(frame_contenido):
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    main_frame = ttk.Frame(frame_contenido, padding=10)
    main_frame.pack(fill="both", expand=True)

    label = Label(main_frame, text="Clientes", font=("Helvetica", 16))
    label.pack(pady=20)

    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=10)

    add_button = ttk.Button(button_frame, text="Agregar", command=lambda: cambiar_pantalla('agregar', content_frame))
    modify_button = ttk.Button(button_frame, text="Modificar", command=lambda: cambiar_pantalla('modificar', content_frame))
    delete_button = ttk.Button(button_frame, text="Eliminar", command=lambda: cambiar_pantalla('eliminar', content_frame))

    add_button.grid(row=0, column=0, padx=10)
    modify_button.grid(row=0, column=1, padx=10)
    delete_button.grid(row=0, column=2, padx=10)

    content_frame = ttk.Frame(main_frame)
    content_frame.pack(fill="both", expand=True, pady=20)

    cambiar_pantalla('agregar', content_frame)

def cambiar_pantalla(accion, frame):
    for widget in frame.winfo_children():
        widget.destroy()
    
    if accion == 'agregar':
        mostrar_agregar(frame)
    elif accion == 'modificar':
        mostrar_modificar(frame)
    elif accion == 'eliminar':
        mostrar_eliminar(frame)

def mostrar_agregar(frame):
    lista_reparaciones = actualizar_lista_reparaciones()

    # Primera columna: Campos básicos del cliente
    frame_cliente = ttk.LabelFrame(frame, text="Información del Cliente", padding=10, bootstyle="primary")
    frame_cliente.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Campos de entrada para el cliente
    label_cliente = ttk.Label(frame_cliente, text="Cliente", font=("Helvetica", 12))
    label_cliente.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_cliente = ttk.Entry(frame_cliente, width=30)
    entry_cliente.grid(row=0, column=1, padx=5, pady=5)

    label_direccion = ttk.Label(frame_cliente, text="Dirección", font=("Helvetica", 12))
    label_direccion.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_direccion = ttk.Entry(frame_cliente, width=30)
    entry_direccion.grid(row=1, column=1, padx=5, pady=5)

    label_fecha = ttk.Label(frame_cliente, text="Fecha", font=("Helvetica", 12))
    label_fecha.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    dataentry = DateEntry(frame_cliente, width=30)
    dataentry.grid(row=2, column=1, padx=5, pady=5)

    label_maquina = ttk.Label(frame_cliente, text="Máquina", font=("Helvetica", 12))
    label_maquina.grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_maquina = ttk.Entry(frame_cliente, width=30)
    entry_maquina.grid(row=3, column=1, padx=5, pady=5)

    label_telefono = ttk.Label(frame_cliente, text="Teléfono", font=("Helvetica", 12))
    label_telefono.grid(row=4, column=0, padx=5, pady=5, sticky="e")
    entry_telefono = ttk.Entry(frame_cliente, width=30)
    entry_telefono.grid(row=4, column=1, padx=5, pady=5)

    # Segunda columna: Proveedor, Reparaciones y Presupuesto
    frame_proveedor = ttk.LabelFrame(frame, text="Detalles Adicionales", padding=10, bootstyle="primary")
    frame_proveedor.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    label_provedor = ttk.Label(frame_proveedor, text="Proveedor", font=("Helvetica", 12))
    label_provedor.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_provedor = ttk.Entry(frame_proveedor, width=30)
    entry_provedor.grid(row=0, column=1, padx=5, pady=5)

    label_reparaciones = ttk.Label(frame_proveedor, text="Reparaciones", font=("Helvetica", 12))
    label_reparaciones.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

    listbox_reparaciones = tk.Listbox(frame_proveedor, selectmode=tk.MULTIPLE, height=5, width=30)
    listbox_reparaciones.grid(row=1, column=1, padx=5, pady=5)

    # Agregar las opciones al Listbox desde la lista actualizada
    for reparacion in lista_reparaciones:
        listbox_reparaciones.insert(tk.END, reparacion)

    label_presupuesto = ttk.Label(frame_proveedor, text="Presupuesto", font=("Helvetica", 12))
    label_presupuesto.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_presupuesto = ttk.Entry(frame_proveedor, width=30)
    entry_presupuesto.grid(row=2, column=1, padx=5, pady=5)

    # Tercera columna: Botón de guardar
    frame_guardar = ttk.LabelFrame(frame, text="Guardar Información", padding=10, bootstyle="primary")
    frame_guardar.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    btn_guardar = tk.Button(frame_guardar, text="Guardar", command=lambda: guardar_cliente(
    entry_cliente.get(), entry_direccion.get(), entry_maquina.get(), 
    entry_telefono.get(), entry_provedor.get(), listbox_reparaciones))

    btn_guardar.grid(row=0, column=0, padx=10, pady=10)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

def guardar_cliente(cliente, direccion, maquina, telefono, provedor, listbox_reparaciones):
    """Función para guardar el cliente y las reparaciones seleccionadas."""
    reparaciones_seleccionadas = [listbox_reparaciones.get(i) for i in listbox_reparaciones.curselection()]
    
    # Obtener la fecha seleccionada correctamente
      # Cambiar de get() a get_date()
    
    # Aquí puedes agregar el código para guardar los datos en la base de datos, incluyendo las reparaciones seleccionadas
    print("Cliente:", cliente)
    print("Dirección:", direccion)  # Mostrar la fecha correctamente
    print("Máquina:", maquina)
    print("Teléfono:", telefono)
    print("Proveedor:", provedor)
    print("Reparaciones Seleccionadas:", reparaciones_seleccionadas)


# Función para mostrar la pantalla de Modificar Cliente
def mostrar_modificar(frame):
    label_modificar = ttk.Label(frame, text="Modificar Cliente", font=("Helvetica", 14))
    label_modificar.pack(pady=10)
    ttk.Entry(frame, width=30).pack(pady=5)
    ttk.Button(frame, text="Modificar").pack(pady=10)

# Función para mostrar la pantalla de Eliminar Cliente
def mostrar_eliminar(frame):
    label_eliminar = ttk.Label(frame, text="Eliminar Cliente", font=("Helvetica", 14))
    label_eliminar.pack(pady=10)
    ttk.Entry(frame, width=30).pack(pady=5)
    ttk.Button(frame, text="Eliminar").pack(pady=10)

