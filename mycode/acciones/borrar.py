import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3

query_datos_mecanizado = "SELECT MECANIZADO, PRECIO FROM Precio_Mecanizado"

def limpiar_tabla(tabla):
    """Limpia los datos actuales de la tabla (Treeview)."""
    for item in tabla.get_children():
        tabla.delete(item)

def mostrar_datos(tabla, query):
    """Carga datos desde la base de datos en la tabla proporcionada."""
    conn = sqlite3.connect("BDreparaciones.db")
    cursor = conn.cursor()
    cursor.execute(query)
    datos = cursor.fetchall()
    conn.close()
    
    limpiar_tabla(tabla)
    for dato in datos:
        tabla.insert("", tk.END, values=dato)

def agregar_mecanizado(entry_mecanizado, entry_precio, tabla):
    """Inserta un nuevo mecanizado en la base de datos y actualiza la tabla."""
    mecanizado = entry_mecanizado.get()
    precio = entry_precio.get()

    if mecanizado and precio:
        try:
            conn = sqlite3.connect("BDreparaciones.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Precio_Mecanizado (MECANIZADO, PRECIO) VALUES (?, ?)", (mecanizado, precio))
            conn.commit()
            conn.close()

            # Actualizar la tabla con los nuevos datos
            mostrar_datos(tabla, query_datos_mecanizado)

            # Limpiar los campos de entrada
            entry_mecanizado.delete(0, tk.END)
            entry_precio.delete(0, tk.END)
        except Exception as e:
            print("Error al insertar datos:", e)
    else:
        print("Por favor, completa ambos campos antes de agregar.")

def borrar_mecanizado(tabla, pieza):
    """Elimina un mecanizado seleccionado de la base de datos."""
    seleccionado = tabla.focus()
    if seleccionado:
        valores = tabla.item(seleccionado, 'values')
        mecanizado = valores[0]

        pieza.config(text=mecanizado)
        
        try:
            conn = sqlite3.connect("BDreparaciones.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Precio_Mecanizado WHERE MECANIZADO = ?", (mecanizado, ))
            conn.commit()
            conn.close()
            
            mostrar_datos(tabla, query_datos_mecanizado)
        except Exception as e:
            print("Error al borrar el Dato:", e)
    else:
        print("Por Favor Selecciona un Dato de la tabla")

def mostrar_pieza_seleccionada(tabla, pieza_label, entry_mecanizado_act, entry_precio_act):
    """Muestra la pieza seleccionada en el Label y carga datos para modificar."""
    seleccionado = tabla.focus()
    if seleccionado:
        valores = tabla.item(seleccionado, "values")
        if valores:
            pieza_label.config(text=f"Seleccionado: {valores[0]}")
            entry_mecanizado_act.delete(0, tk.END)
            entry_precio_act.delete(0, tk.END)
            entry_mecanizado_act.insert(0, valores[0])  # Mecanizado
            entry_precio_act.insert(0, valores[1])  # Precio
        else:
            pieza_label.config(text="Seleccionado: Ninguno")
            entry_mecanizado_act.delete(0, tk.END)
            entry_precio_act.delete(0, tk.END)
    else:
        pieza_label.config(text="Seleccionado: Ninguno")
        entry_mecanizado_act.delete(0, tk.END)
        entry_precio_act.delete(0, tk.END)

def actualizar_mecanizado(tabla, entry_mecanizado_act, entry_precio_act):
    """Actualiza el mecanizado seleccionado en la base de datos."""
    seleccionado = tabla.focus()
    if seleccionado:
        valores = tabla.item(seleccionado, "values")
        mecanizado_anterior = valores[0]  # Mecanizado original (clave primaria)

        mecanizado_nuevo = entry_mecanizado_act.get()
        precio_nuevo = entry_precio_act.get()

        if mecanizado_nuevo and precio_nuevo:
            try:
                conn = sqlite3.connect("BDreparaciones.db")
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE Precio_Mecanizado SET MECANIZADO = ?, PRECIO = ? WHERE MECANIZADO = ?",
                    (mecanizado_nuevo, precio_nuevo, mecanizado_anterior)
                )
                conn.commit()
                conn.close()

                # Actualizar la tabla
                mostrar_datos(tabla, query_datos_mecanizado)

                # Limpiar los campos
                entry_mecanizado_act.delete(0, tk.END)
                entry_precio_act.delete(0, tk.END)
            except Exception as e:
                print("Error al actualizar el dato:", e)
        else:
            print("Por favor, completa ambos campos antes de actualizar.")
    else:
        print("Por favor, selecciona un dato de la tabla para modificar.")

def mostrar_panel(frame_contenido):
    # Limpiar el área de contenido actual
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    box = ttk.Frame(frame_contenido, padding=10)
    box.grid(row=0, column=0, sticky="nsew")
    frame_contenido.grid_rowconfigure(0, weight=1)
    frame_contenido.grid_columnconfigure(0, weight=1)

    # Etiqueta de título
    label = ttk.Label(box, text="Panel De Control", font=("Helvetica", 18))
    label.grid(row=0, column=0, sticky="n")

    # Frame para la tabla y botones
    box_tabla = ttk.Frame(box)
    box_tabla.grid(row=1, column=0, pady=(0, 10), sticky="nsew")
    
    # Frame para la tabla con scrollbar
    box_treeview = ttk.Frame(box_tabla, padding=5)
    box_treeview.grid(row=0, column=0, sticky="nsew")

    columnas_visibles = ("Mecanizado", "Importe")
    tabla = ttk.Treeview(box_treeview, columns=columnas_visibles, show='headings', bootstyle="primary")

    for col in columnas_visibles:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)

    tabla.grid(row=0, column=0, pady=10, sticky="nsew")
    tabla.config(height=20)

    # Cargar datos en la tabla
    mostrar_datos(tabla, query_datos_mecanizado)
    tabla.bind("<ButtonRelease-1>", lambda event: mostrar_pieza_seleccionada(tabla, pieza_label, entry_mecanizado_act, entry_precio_act))

    

    frame_dato = ttk.Frame(box)
    frame_dato.grid(row=1, column=1, sticky="n")
    
    # Frame para agregar datos
    
    
    frame_agregar = ttk.Labelframe(frame_dato, text="Agregar Mecanizado", padding=5)
    frame_agregar.grid(row=0, column=0, sticky="nsew")

    # Campos de entrada
    
    ttk.Label(frame_agregar, text="Mecanizado").grid(row=0, column=1)
    ttk.Label(frame_agregar, text="Precio").grid(row=0, column=2)
    
    entry_mecanizado = ttk.Entry(frame_agregar, bootstyle="light")
    entry_mecanizado.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    entry_precio = ttk.Entry(frame_agregar, bootstyle="light")
    entry_precio.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
    
    ttk.Button(frame_agregar, text="Agregar", bootstyle="success", padding=5, command=lambda: agregar_mecanizado(entry_mecanizado, entry_precio, tabla)).grid(row=2, column=0, columnspan=3, pady=10, sticky="s")

    # Frame para editar
    frame_editar = ttk.Labelframe(frame_dato, text="Editar Mecanizado", padding=5)
    frame_editar.grid(row=1, column=0, sticky="nsew")

    # Campos de edición
    entry_mecanizado_act = ttk.Entry(frame_editar, bootstyle="light")
    entry_mecanizado_act.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    entry_precio_act = ttk.Entry(frame_editar, bootstyle="light")
    entry_precio_act.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

    ttk.Button(frame_editar, text="Actualizar", bootstyle="warningn", padding=5, command=lambda: actualizar_mecanizado(tabla, entry_mecanizado_act, entry_precio_act)).grid(row=1, column=0, columnspan=3, pady=10, sticky="s") 


    frame_borrar = ttk.Labelframe(frame_dato, text="Borrar Mecanizado", padding=7)
    frame_borrar.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

    ttk.Label(frame_borrar, text="Selecciones un dato de la tabla para borrar", font=("Arial", 9, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    # Label para mostrar la pieza seleccionada
    pieza_label = ttk.Label(frame_borrar, text="Seleccionado: Ninguno", bootstyle="light")
    pieza_label.grid(row=2, column=0, columnspan=2, pady=5, sticky="nsew")

    # Botón para eliminar el mecanizado seleccionado
    ttk.Button(
        frame_borrar, 
        text="Eliminar", 
        padding=5, 
        bootstyle="danger",
        command=lambda: borrar_mecanizado(tabla, pieza_label)
    ).grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")