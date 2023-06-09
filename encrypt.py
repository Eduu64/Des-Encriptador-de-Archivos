from cryptography.fernet import Fernet
from tkinter import ttk
import tkinter as tk
import os
from tkinter import filedialog as fd

# Definir ruta de descargas
descargas_dir = os.path.expanduser('~/Downloads')

def clave():
   # Define el nombre del archivo de clave y agrega la extensión ".key"
    nombrearch = fd.asksaveasfilename(initialdir=descargas_dir, title="Guardar como", filetypes=(("key files", "*.key"), ("todos los archivos", "*")))
    
    if not nombrearch:  # Si el usuario cancela la selección, sale de la función
        return

    nombre, extension = os.path.splitext(nombrearch)
    if not extension:  # Si el usuario no especifica la extensión, se agrega la extensión ".key" por defecto
        nombrearch = f"{nombre}.key"
    else:
        nombrearch = f"{nombre}{extension}"

    # Genera la clave y escribe en el archivo de clave
    key_gen = Fernet.generate_key()
    with open(nombrearch, "wb") as archivo_key:
        archivo_key.write(key_gen)

def cargarCLAVE():
    # Permite al usuario seleccionar un archivo de clave y carga la clave
    archivo_key=fd.askopenfilename(initialdir = descargas_dir,title = "Seleccione la key",filetypes = (("key files","*.key"),("todos los archivos","*")))
    key = open(archivo_key,"rb").read()
    return key

def encriptarARCHIVO():
    # Permite al usuario seleccionar un archivo y lo encripta usando la clave proporcionada
    key = cargarCLAVE()
    nom_archivo=fd.askopenfilename(initialdir = descargas_dir,title = "Seleccione archivo",filetypes = (("txt files","*.txt"),("todos los archivos","*.*")))
    f = Fernet(key)
    with open(nom_archivo,"rb") as archivo:
        data = archivo.read()
        data_encriptada = f.encrypt(data)

    nombre, ext = os.path.splitext(nom_archivo)
    nombre_enc = nombre + "_encrypted"
    nombre_final = nombre_enc + ext
    
    if os.path.exists(nombre_final):
        i = 1
        while os.path.exists(f"{nombre_enc}({i}){ext}"):
            i += 1
        nombre_final = f"{nombre_enc}({i}){ext}"

    with open(nombre_final,"wb") as archivo:
        archivo.write(data_encriptada)

def des_encriptarARCHIVO():
    # Permite al usuario seleccionar un archivo encriptado y lo desencripta usando la clave proporcionada
    key = cargarCLAVE()
    nom_archivo=fd.askopenfilename(initialdir = descargas_dir,title = "Seleccione archivo",filetypes = (("txt files","*.txt"),("todos los archivos","*.*")))
    f = Fernet(key)
    with open(nom_archivo,"rb") as archivo:
        data = archivo.read()
        data_desencriptada = f.decrypt(data)

    nombre, ext = os.path.splitext(nom_archivo)
    nombre_enc = nombre + "_decrypted"
    nombre_final = nombre_enc + ext
    
    if os.path.exists(nombre_final):
        i = 1
        while os.path.exists(f"{nombre_enc}({i}){ext}"):
            i += 1
        nombre_final = f"{nombre_enc}({i}){ext}"

    with open(nombre_final,"wb") as archivo:
        archivo.write(data_desencriptada)

    

window = tk.Tk()
window.title("Encriptador")
window.geometry("300x150")

btngenerar = tk.Button(text="Generar clave", command=clave)
btncodificar = tk.Button(text="Seleccione Archivo a codificar", command=encriptarARCHIVO)
btndecodificar = tk.Button(text="Seleccione Archivo a decodificar", command=des_encriptarARCHIVO)
btngenerar.pack(pady=5)
btncodificar.pack(pady=5)
btndecodificar.pack(pady=5)

window.mainloop()