import sqlite3
import tkinter as tk


def limpiar_tabla(tabla):
    for item in tabla.get_children():
        tabla.delete(item)

def datos():
    print("HOla")
    
def mostrar_datos(quety, tabla):
    conn = sqlite3.connect("BDreparaciones.db")
    cursor = conn.cursor()
    cursor.execute(quety)
    datos = cursor.fetchall()
    limpiar_tabla(tabla)
    for dato in datos:
        tabla.insert("", tk.END, values=dato)