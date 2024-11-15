from ttkbootstrap import Frame, Button

def crear_menu(root, frame_contenido, mostrar_detalles, mostrar_clientes, mostrar_panel):
    # Crear el marco para el menú lateral
    ventana_vertical = Frame(root, padding=40, bootstyle="info")
    
    # Botones del menú que llaman a las funciones correspondientes
    Button(ventana_vertical, text="Buscar", command=lambda: mostrar_detalles(frame_contenido), padding=20).grid(row=0, column=0, pady=10, sticky="nsew")
    Button(ventana_vertical, text="Clietes", command=lambda: mostrar_clientes(frame_contenido), padding=20).grid(row=1, column=0, pady=10, sticky="nsew")
    Button(ventana_vertical, text="Panel De Control", command=lambda: mostrar_panel(frame_contenido), padding=20).grid(row=2, column=0, pady=10, sticky="nsew")

    return ventana_vertical
