import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, Menu
from tkinter.filedialog import askopenfile, asksaveasfilename
from lectura_escritura.lector import Lector
from analizador import Analizador

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(0, 0)
        self.title("Proyecto #2 - LFP")
        self.iconbitmap("img/cheems.ico")
        self.archivo = None
        self.archivo_activo = None
        self.fila = 1
        self.columna = 1
        self.label_ruta = tk.Label(self, text="")
        self.campo_texto = tk.Text(self)
        self.crear_menu()
        self.crear_componentes()

    # Configurar el editor y etiqueta de ruta de archivo
    def crear_componentes(self):
        tk.Label(self, text="").grid(row=1, column=1, columnspan=3)
        tk.Label(self, text="\t").grid(row=2, column=1)
        tk.Label(self, text="- Ruta del archivo activo -").grid(row=2, column=2)
        tk.Label(self, text="\t").grid(row=2, column=3)
        self.label_ruta.grid(row=3, column=2)
        tk.Label(self, text="").grid(row=4, column=1, columnspan=3)
        self.campo_texto.grid(row=5, column=2)
        tk.Label(self, text="").grid(row=6, column=1, columnspan=3)
        tk.Label(self, text=f"Ln {self.fila}, Col{self.columna}").grid(row=7, column=1, columnspan=3)
        tk.Label(self, text="").grid(row=8, column=1, columnspan=3)

    def crear_menu(self):
        # Crear el menú principal
        menu_principal = Menu(self)
        # Crear submenús
        submenu_archivo = Menu(menu_principal, tearoff=False)
        submenu_analisis = Menu(menu_principal, tearoff=0)
        submenu_tokens = Menu(menu_principal, tearoff=0)
        submenu_errores = Menu(menu_principal, tearoff=0)
        # Agregar opciones y separadores en el submenú "Archivo"
        submenu_archivo.add_command(label="Nuevo", command=self.nuevo)
        submenu_archivo.add_separator()
        submenu_archivo.add_command(label="Abrir", command=self.abrir)
        submenu_archivo.add_separator()
        submenu_archivo.add_command(label="Guardar", command=self.guardar)
        submenu_archivo.add_separator()
        submenu_archivo.add_command(label="Guardar Como", command=self.guardar_como)
        submenu_archivo.add_separator()
        submenu_archivo.add_command(label="Salir", command=self.salir)
        # Agregar opción al submenú "Análisis"
        submenu_analisis.add_command(label="Generar sentencias MongoDB", command=self.generar_sentencias)
        # Agregar opción al submenú "Tokens"
        submenu_tokens.add_command(label="Ver tokens", command=self.ver_tokens)
        # Agregar opción al submenú "Errores"
        submenu_errores.add_command(label="Ver errores", command=self.ver_errores)
        # Agregar los submenús al menú principal
        menu_principal.add_cascade(menu=submenu_archivo, label="Archivo")
        menu_principal.add_cascade(menu=submenu_analisis, label="Análisis")
        menu_principal.add_cascade(menu=submenu_tokens, label="Tokens")
        menu_principal.add_cascade(menu=submenu_errores, label="Errores")
        # Mostrar el menú en la ventana principal
        self.config(menu=menu_principal)

    def nuevo(self):
        # Verificar si hay un archivo abierto o activo
        if self.archivo_activo != None:
            respuesta = messagebox.askyesno("", "¿Desea guardar los cambios?")
            if respuesta:
                self.guardar_como()
                self.borrar()
            else:
                self.borrar()
        else:
            self.borrar()

    def borrar(self):
        # Eliminar el texto anterior
        self.campo_texto.delete(1.0, tk.END)
        self.label_ruta["text"] = ""
        self.archivo_activo = None

    def abrir(self):
        try:
            # askopenfile (explorador para abrir archivo)
            self.archivo_activo = askopenfile(mode="r")
            # Verificar si se seleccionó un archivo a abrir
            if self.archivo_activo != None:
                with open(self.archivo_activo.name, "r") as self.archivo:
                    texto = self.archivo.read()
                    # Eliminar el texto anterior
                    self.campo_texto.delete(1.0, tk.END)
                    # Insertar el contenido del archivo
                    self.campo_texto.insert(1.0, texto)
                    self.label_ruta["text"] = f"{self.archivo.name}"
        except:
            messagebox.showerror("ERROR", "No pudo abrirse el archivo indicado")
            self.archivo_activo = None

    def guardar(self):
        # Verificar si hay un archivo abierto o activo
        if self.archivo_activo != None:
            with open(self.archivo_activo.name, "w") as self.archivo:
                # Leer el contenido del cuadro de texto
                texto = self.campo_texto.get(1.0, tk.END)
                # Escribir contenido del cuadro de texto en el mismo archivo
                self.archivo.write(texto)
        else:
            self.guardar_como()

    def guardar_como(self):
        # Configuración respecto a la extensión del archivo
        self.archivo = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        # Verificar si se va a guardar un archivo
        if self.archivo:
            with open(self.archivo, "w") as self.archivo:
                # Leer el contenido del cuadro de texto
                texto = self.campo_texto.get(1.0, tk.END)
                # Escribir contenido del cuadro de texto en el nuevo archivo
                self.archivo.write(texto)
                self.label_ruta["text"] = f"{self.archivo.name}"
                self.archivo_activo = self.archivo

    def salir(self):
        self.quit()
        self.destroy()
        sys.exit()

    def generar_sentencias(self):
        # Verifica si hay algún archivo abierto con anterioridad
        if not self.archivo:
            messagebox.showerror("ERROR", "No se ha abierto ningún archivo para analizar")
            return
        archivo_leer = Lector(self.archivo_activo.name)
        archivo_leido = archivo_leer.leer_archivo()
        analizador = Analizador(archivo_leido)
        analizador.compilar()
        messagebox.showinfo("INFORMACIÓN", "Análisis realizado")
        try:
            with open("resultados\TRADUCCION_202010003.txt", "r") as self.archivo:
                # Eliminar el texto anterior
                self.campo_texto.delete(1.0, tk.END)
                # Leer el contenido del archivo y guardarlo en la variable texto
                texto = self.archivo.read()
                # Insertar el contenido del archivo
                self.campo_texto.insert(1.0, texto)
                self.label_ruta["text"] = ""
                self.archivo = None
                self.archivo_activo = None
        except:
            messagebox.showerror("ERROR", "No pudo abrirse el archivo de errores")
            self.archivo_activo = False

    def ver_tokens(self):
        try:
            ruta = "resultados\TOKENS_202010003.html"
            leer = open(ruta, "r")
            leer.close()
            subprocess.Popen([ruta], shell=True)
        except:
            messagebox.showerror("ERROR", "No existe un archivo de tokens")

    def ver_errores(self):
        try:
            ruta = "resultados\ERRORES_202010003.html"
            leer = open(ruta, "r")
            leer.close()
            subprocess.Popen([ruta], shell=True)
        except:
            messagebox.showerror("ERROR", "No existe un archivo de errores")