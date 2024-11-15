import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from mycode.main import crear_menu

from mycode.acciones.buscar import mostrar_buscar
from mycode.acciones.agregar import mostrar_clientes
from mycode.acciones.borrar import mostrar_panel

# Crear la ventana principal
root = ttk.Window(themename="darkly")
root.title("Fadeco Stock")
root.geometry("1130x520")  

# Crear el marco de contenido (donde se mostrarán las secciones)
frame_contenido = ttk.Frame(root, padding=10)
frame_contenido.grid(row=0, column=1, sticky="nsew")

# Configuración de expansión de columnas y filas
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Crear el menú lateral, pasando las funciones para cada sección
ventana_vertical = crear_menu(root, frame_contenido,mostrar_buscar, mostrar_clientes, mostrar_panel)
ventana_vertical.grid(row=0, column=0, sticky="nsew")

# Ejecutar la aplicación
root.mainloop()

