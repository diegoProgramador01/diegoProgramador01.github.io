import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import random
import shutil
import os
import ttkbootstrap as tb  # Usaremos ttkbootstrap para un diseño moderno
import subprocess
# Clase Pregunta
class Pregunta:
    def __init__(self, pregunta, respuesta_correcta, respuestas_incorrectas):
        self.pregunta = pregunta
        self.respuesta_correcta = respuesta_correcta
        self.respuestas_incorrectas = respuestas_incorrectas

    def obtener_opciones(self):
        opciones = self.respuestas_incorrectas + [self.respuesta_correcta]
        random.shuffle(opciones)
        return opciones

# Clase Trivia
class Trivia:
    def __init__(self):
        self.categorias = {
            'Deportes': [
                Pregunta("¿Cuál es el deporte más popular del mundo?", "Fútbol", ["Baloncesto", "Tenis", "Golf"]),
                Pregunta("¿Cuántos jugadores hay en un equipo de fútbol?", "11", ["7", "9", "12"]),
                Pregunta("¿Qué selección ha ganado más Copas Mundiales de Fútbol?", "Brasil", ["Argentina", "España", "Francia"]),
                Pregunta("¿Cuántos anillos hay en la bandera olímpica?", "5", ["7", "4", "6"]),
                Pregunta("¿Qué deporte se juega anualmente en París en el torneo de Roland Garros?", "Tenis", ["Badminton", "Cricket", "Padel"]),
            ],
            'Ciencia': [
                Pregunta("¿Cuál es el planeta más cercano al sol?", "Mercurio", ["Venus", "Tierra", "Marte"]),
                Pregunta("¿Qué partícula atómica tiene carga negativa?", "Electrón", ["Protón", "Neutrón", "Ion"]),
                Pregunta("¿Cuál es el animal más grande de la Tierra?", "Ballena Azul", ["Elefante", "Jirafa", "León"]),
                Pregunta("¿Cuántos lados tiene un heptadecágono?", "17", ["16", "11", "7"]),
                Pregunta("¿Qué gas liberan las plantas al hacer la fotosíntesis?", "Oxígeno", ["Nitrógeno", "Dióxido de carbono", "Hidrógeno"]),
            ],
            'Historia': [
                Pregunta("¿Quién fue el primer presidente de los Estados Unidos?", "George Washington", ["Abraham Lincoln", "Thomas Jefferson", "John Adams"]),
                Pregunta("¿En qué año se firmó la Declaración de Independencia de EE. UU.?", "1776", ["1783", "1791", "1801"]),
                Pregunta("¿Cuándo empezó la Primera Guerra Mundial?", "1914", ["1917", "1936", "1939"]),
                Pregunta("¿En qué año llegó Cristóbal Colón a América?", "1492", ["1592", "1692", "1092"]),
                Pregunta("Según la leyenda ¿quiénes fundaron a Roma?", "Rómulo y Remo", ["Julio César y Augusto", "Trajano y Adriano", "Nerón y Calígula"]),
            ],
            'Refranes': [
                Pregunta("A quien madruga, ---- le ayuda.", "Dios", ["La virgen", "Julen", "El sol"]),
                Pregunta("Más vale ---- que nunca.", "Tarde", ["Temprano", "Pronto", "Siempre"]),
                Pregunta("Camarón que se duerme, ---- se lo lleva.", "La corriente", ["El río", "El mar", "El viento"]),
                Pregunta("Dime con quién andas y te diré ----.", "Quién eres", ["Qué comes", "Qué haces", "A dónde vas"]),
                Pregunta("Cría cuervos y te sacarán ----.", "Los ojos", ["Las plumas", "El alma", "La voz"]),
            ],
            'Snake': [
                Pregunta("¿Mery estas lista para jugar al clásico juego Snake?", "Sí", ["No", "Tal vez", "Otro día"])
            ]
        }
        self.puntaje = 0
        self.imagen_actual = None

    def desbloquear_imagen(self, categoria):
        img_path = f"images/{categoria}.png"
        unlocked_path = f"unlocked/{categoria}.png"
        if not os.path.exists('unlocked'):
            os.makedirs('unlocked')
        shutil.copy(img_path, unlocked_path)
        self.imagen_actual = unlocked_path
        return unlocked_path

# Clase GUI
class TriviaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Trivia - CumpleTrivia")
        self.trivia = Trivia()
        self.categoria_actual = None
        self.indice_pregunta = 0
        self.preguntas = []
        self.iniciar_juego()

    def limpiar_pantalla(self):
        """Destruye todos los widgets en la ventana principal."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def iniciar_juego(self):
        self.limpiar_pantalla()
        frame_inicio = tb.Frame(self.root, padding=20)
        frame_inicio.pack(pady=50)

        tb.Label(frame_inicio, text="¡Bienvenido al juego de Trivia!", font=("Arial", 24), bootstyle="primary").pack(pady=20)
        tb.Button(frame_inicio, text="Iniciar Juego", command=self.seleccionar_categoria, bootstyle="success").pack(pady=10)

    def seleccionar_categoria(self):
        self.limpiar_pantalla()
        frame_categoria = tb.Frame(self.root, padding=20)
        frame_categoria.pack(pady=50)

        tb.Label(frame_categoria, text="Selecciona una categoría:", font=("Arial", 18), bootstyle="info").pack(pady=10)
        for categoria in self.trivia.categorias.keys():
            tb.Button(frame_categoria, text=categoria, command=lambda c=categoria: self.iniciar_categoria(c), bootstyle="secondary").pack(pady=5)

    def iniciar_categoria(self, categoria):
        self.categoria_actual = categoria
        if categoria == "Snake":
            self.iniciar_snake()
        else:
            self.preguntas = self.trivia.categorias[categoria]
            self.indice_pregunta = 0
            self.mostrar_pregunta()

    def mostrar_pregunta(self):
        self.limpiar_pantalla()
        pregunta = self.preguntas[self.indice_pregunta]

        frame_pregunta = tb.Frame(self.root, padding=20)
        frame_pregunta.pack(pady=50)

        tb.Label(frame_pregunta, text=pregunta.pregunta, font=("Arial", 16), bootstyle="warning").pack(pady=10)
        opciones = pregunta.obtener_opciones()
        for opcion in opciones:
            tb.Button(frame_pregunta, text=opcion, command=lambda o=opcion: self.verificar_respuesta(o), bootstyle="outline").pack(pady=5)

    def verificar_respuesta(self, respuesta):
        """Verifica si la respuesta es correcta."""
        pregunta = self.preguntas[self.indice_pregunta]
        self.limpiar_pantalla()
        
        frame_respuesta = tb.Frame(self.root, padding=20)
        frame_respuesta.pack(pady=50)

        tb.Label(frame_respuesta, text=pregunta.pregunta, font=("Arial", 16), bootstyle="warning").pack(pady=10)
        
        if respuesta == pregunta.respuesta_correcta:
            self.trivia.puntaje += 1
            self.label_resultado = tb.Label(frame_respuesta, text="✅ ¡Respuesta correcta! Avanzando...", 
                                            font=("Arial", 14), bootstyle="success")
            self.label_resultado.pack(pady=10)
            self.root.after(1000, self.siguiente_pregunta)
        else:
            self.label_resultado = tb.Label(frame_respuesta, text=f"❌ Incorrecto. La respuesta era: {pregunta.respuesta_correcta}.",
                                            font=("Arial", 14), bootstyle="danger")
            self.label_resultado.pack(pady=10)
            tb.Button(frame_respuesta, text="Intentar con un ejercicio matemático", 
                      command=self.mostrar_ejercicio_matematico, bootstyle="info").pack(pady=10)

    def mostrar_ejercicio_matematico(self):
        """Muestra un ejercicio matemático simple si fallas una pregunta."""
        self.limpiar_pantalla()
        self.generar_nuevo_ejercicio()
        
        frame_matematico = tb.Frame(self.root, padding=20)
        frame_matematico.pack(pady=50)

        self.label_matematico = tb.Label(frame_matematico, text=self.ejercicio_actual, font=("Arial", 16), bootstyle="info")
        self.label_matematico.pack(pady=10)
        
        self.entry_matematico = tb.Entry(frame_matematico)
        self.entry_matematico.pack(pady=5)
        
        self.label_resultado = tb.Label(frame_matematico, text="", font=("Arial", 14), bootstyle="warning")  # Etiqueta dinámica
        self.label_resultado.pack(pady=10)
        
        self.boton_comprobar = tb.Button(frame_matematico, text="Comprobar", command=self.verificar_ejercicio_matematico, bootstyle="success")
        self.boton_comprobar.pack(pady=10)

    def verificar_ejercicio_matematico(self):
        """Verifica si el ejercicio matemático es correcto."""
        respuesta_usuario = self.entry_matematico.get()
        try:
            if int(respuesta_usuario) == self.respuesta_correcta_matematica:
                self.label_resultado.config(text="✔️ Correcto!", bootstyle="success")
                self.root.after(1000, self.siguiente_pregunta)
            else:
                self.label_resultado.config(text=f"❌ Incorrecto. La respuesta correcta era {self.respuesta_correcta_matematica}.", bootstyle="danger")
                self.root.after(1000, self.mostrar_ejercicio_matematico)
        except ValueError:
            self.label_resultado.config(text="❌ Por favor, introduce un número válido.", bootstyle="danger")
        
        # Deshabilitar el botón "Comprobar" después de presionarlo
        
        self.boton_comprobar.config(state="disabled")
        self.root.after(2000, self.boton_comprobar.config, {"state": "normal"})
        

    def generar_nuevo_ejercicio(self):
        """Genera un nuevo ejercicio matemático."""
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operador = random.choice(['+', '-', '*'])
        self.respuesta_correcta_matematica = eval(f"{num1} {operador} {num2}")
        self.ejercicio_actual = f"Resuelve: {num1} {operador} {num2}"
    

    def siguiente_pregunta(self):
        self.indice_pregunta += 1
        if self.indice_pregunta < len(self.preguntas):
            self.mostrar_pregunta()
        else:
            self.mostrar_imagen_categoria()

    def mostrar_imagen_categoria(self):
        """Muestra una imagen común al ganar una categoría."""
        self.limpiar_pantalla()
        
        # Mostrar siempre la imagen mistery.png
        img_path = "images/mistery.png"
        self.img_categoria_descarga = self.trivia.desbloquear_imagen(self.categoria_actual)  # Imagen específica para descargar
        
        frame_imagen = tb.Frame(self.root, padding=20)
        frame_imagen.pack(pady=50)

        # Cargar y mostrar mistery.png
        img = Image.open(img_path)
        img = img.resize((512, 512))
        self.img_tk = ImageTk.PhotoImage(img)

        tb.Label(frame_imagen, image=self.img_tk).pack()
        tb.Button(frame_imagen, text="Descargar Imagen de la Categoría", 
                  command=lambda: self.descargar_imagen(self.img_categoria_descarga), bootstyle="info").pack(pady=5)
        tb.Button(frame_imagen, text="Continuar", command=self.seleccionar_categoria, bootstyle="primary").pack(pady=5)


    def descargar_imagen(self, img_path):
        """Permite descargar la imagen específica de la categoría con un nombre personalizado."""
        # Diccionario con nombres personalizados
        nombres_personalizados = {
            'Deportes': 'sorpresa_1',
            'Ciencia': 'sorpresa_2',
            'Historia': 'sorpresa_3',
            'Refranes': 'sorpresa_4'
        }
        
         # Obtener el nombre personalizado según la categoría actual
        nombre_predeterminado = nombres_personalizados.get(self.categoria_actual, 'sorpresa.png')
        
        # Mostrar cuadro de diálogo con el nombre predeterminado
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            initialfile=nombre_predeterminado  # Nombre personalizado
        )
        
        if file_path:
            shutil.copy(img_path, file_path)
            self.limpiar_pantalla()
            frame_descarga = tb.Frame(self.root, padding=20)
            frame_descarga.pack(pady=50)
            tb.Label(frame_descarga, text="✅ ¡Imagen descargada correctamente!", 
                    font=("Arial", 16), bootstyle="success").pack(pady=10)
            tb.Button(frame_descarga, text="Continuar", command=self.seleccionar_categoria, bootstyle="primary").pack(pady=5)
    

    def iniciar_snake(self):
        """Ejecuta el juego Snake desde un archivo externo."""
        try:
            # Asegúrate de cambiar "snake_game.py" al nombre correcto de tu archivo
            subprocess.run(["python", "serpiente.py"], check=True)
        except FileNotFoundError:
            self.limpiar_pantalla()
            frame_error = tb.Frame(self.root, padding=20)
            frame_error.pack(pady=50)
            tb.Label(frame_error, text="❌ Archivo 'snake_game.py' no encontrado.", font=("Arial", 16), bootstyle="danger").pack(pady=10)
            tb.Button(frame_error, text="Volver", command=self.seleccionar_categoria, bootstyle="primary").pack(pady=5)
        except subprocess.CalledProcessError:
            self.limpiar_pantalla()
            frame_error = tb.Frame(self.root, padding=20)
            frame_error.pack(pady=50)
            tb.Label(frame_error, text="❌ Error al ejecutar 'snake_game.py'.", font=("Arial", 16), bootstyle="danger").pack(pady=10)
            tb.Button(frame_error, text="Volver", command=self.seleccionar_categoria, bootstyle="primary").pack(pady=5)


# Inicializar App
if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = TriviaGUI(root)
    root.mainloop()
