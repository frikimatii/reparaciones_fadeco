from ttkbootstrap import Label

def mostrar_panel(frame_contenido):
    # Limpiar el área de contenido actual
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    # Crear el contenido de la sección "Eliminar"
    label = Label(frame_contenido, text="Sección: Panel", font=("Helvetica", 16))
    label.pack(pady=20)
