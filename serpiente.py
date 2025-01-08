import turtle
import time
import random
from tkinter import Tk, Button, filedialog
import os
posponer = 0.1

# Marcador
score = 0
high_score = 0

# Configuracion de la ventana
wn = turtle.Screen()
wn.title("Snake Game 1.5.2")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# Cabeza serpiente
cabeza = turtle.Turtle()
cabeza.speed(0)
cabeza.shape("square")
cabeza.color("dark green")
cabeza.penup()
cabeza.goto(0, 0)
cabeza.direction = "stop"

# Comida
comida = turtle.Turtle()
comida.speed(0)
comida.shape("circle")
comida.color("red")
comida.penup()
comida.goto(0, 100)

# Segmentos
segmentos = []

# Texto
texto = turtle.Turtle()
texto.speed(0)
texto.color("white")
texto.penup()
texto.hideturtle()
texto.goto(0, 260)
texto.write("Score: 0     High Score: 0", align="center", font=("Courier", 24, "normal"))

# Funciones
def arriba():
    if cabeza.direction != "down":
        cabeza.direction = "up"

def abajo():
    if cabeza.direction != "up":
        cabeza.direction = "down"

def izquierda():
    if cabeza.direction != "right":
        cabeza.direction = "left"

def derecha():
    if cabeza.direction != "left":
        cabeza.direction = "right"

def mov():
    if cabeza.direction == "up":
        y = cabeza.ycor()
        cabeza.sety(y + 20)

    if cabeza.direction == "down":
        y = cabeza.ycor()
        cabeza.sety(y - 20)

    if cabeza.direction == "left":
        x = cabeza.xcor()
        cabeza.setx(x - 20)

    if cabeza.direction == "right":
        x = cabeza.xcor()
        cabeza.setx(x + 20)

# Mostrar Imagen de Victoria
def mostrar_imagen_victoria():
    """Muestra una imagen de victoria y oculta elementos del juego."""
    # Ocultar elementos del juego
    cabeza.hideturtle()
    comida.hideturtle()
    for segmento in segmentos:
        segmento.hideturtle()
    
    # Detener el bucle principal
    global running
    running = False
    wn.bgpic("images/mistery.png")  # Mostrar imagen de fondo
    wn.setup(width=512, height=512)  # Cambiar tamaño de la ventana
    wn.update()

# Descargar Imagen
def descargar_imagen():
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    ruta_destino = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png")],
                                                initialfile="sorpresa_5")
    if ruta_destino:
        origen = os.path.join("images", "Survival.png")
        if os.path.exists(origen):
            import shutil
            shutil.copy(origen, ruta_destino)
            print("Imagen descargada en:", ruta_destino)
        else:
            print("Error: El archivo 'Survival.png' no existe en el directorio 'images'.")
    root.destroy()

# Teclado
wn.listen()
wn.onkeypress(arriba, "Up")
wn.onkeypress(abajo, "Down")
wn.onkeypress(izquierda, "Left")
wn.onkeypress(derecha, "Right")

# Bucle principal del juego
while True:
    wn.update()

    # Colisiones bordes
    if cabeza.xcor() > 280 or cabeza.xcor() < -280 or cabeza.ycor() > 280 or cabeza.ycor() < -280:
        time.sleep(1)
        cabeza.goto(0, 0)
        cabeza.direction = "stop"

        for segmento in segmentos:
            segmento.goto(1000, 1000)

        segmentos.clear()
        score = 0
        texto.clear()
        posponer = 0.1
        texto.write("Score: {}     High Score: {}".format(score, high_score),
                    align="center", font=("Courier", 24, "normal"))

    # Colisiones comida
    if cabeza.distance(comida) < 20:
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        comida.goto(x, y)

        nuevo_segmento = turtle.Turtle()
        nuevo_segmento.speed(0)
        nuevo_segmento.shape("square")
        nuevo_segmento.color("light green")
        nuevo_segmento.penup()
        segmentos.append(nuevo_segmento)
        nuevo_segmento = turtle.Turtle()
        nuevo_segmento.speed(0)
        nuevo_segmento.shape("square")
        nuevo_segmento.color("green")
        nuevo_segmento.penup()
        segmentos.append(nuevo_segmento)
        nuevo_segmento = turtle.Turtle()
        nuevo_segmento.speed(0)
        nuevo_segmento.shape("square")
        nuevo_segmento.color("green")
        nuevo_segmento.penup()
        segmentos.append(nuevo_segmento)

        score += 1

        if score > high_score:
            high_score = score

        texto.clear()
        texto.write("Score: {}    High Score: {}".format(score, high_score),
                    align="center", font=("Courier", 24, "normal"))
        
        # Acelerar la serpiente
        if score == 3:
            posponer = 0.05
        elif score == 6:
            posponer = 0.03
        elif score == 6:
            posponer = 0.025

    # Verificar si se ha ganado la partida
    if score == 10:
        texto.clear()
        texto.goto(0, 0)
        texto.write("🎉 ¡Felicidades, has ganado! 🎉", align="center", font=("Courier", 24, "normal"))
        mostrar_imagen_victoria()
        
        # Crear ventana para el botón de descarga
        root = Tk()
        root.title("¡Victoria!")
        Button(root, text="Descargar Imagen", command=descargar_imagen).pack(pady=20)
        Button(root, text="Salir", command=lambda: (root.quit(), wn.bye())).pack(pady=10)
        root.mainloop()
        break

    # Mover el cuerpo de la serpiente
    totalSeg = len(segmentos)
    for index in range(totalSeg - 1, 0, -1):
        x = segmentos[index - 1].xcor()
        y = segmentos[index - 1].ycor()
        segmentos[index].goto(x, y)

    if totalSeg > 0:
        x = cabeza.xcor()
        y = cabeza.ycor()
        segmentos[0].goto(x, y)

    mov()

    # Colisiones con el cuerpo
    for segmento in segmentos:
        if segmento.distance(cabeza) < 20:
            time.sleep(1)
            cabeza.goto(0, 0)
            cabeza.direction = "stop"

            for segmento in segmentos:
                segmento.goto(1000, 1000)

            segmentos.clear()
            score = 0
            texto.clear()
            posponer = 0.1
            texto.write("Score: {}    High Score: {}".format(score, high_score),
                        align="center", font=("Courier", 24, "normal"))

    time.sleep(posponer)

    