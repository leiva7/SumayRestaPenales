import random
from tkinter import *
import pyglet
import time



class Cuentas():
    """Clase que representa la cuenta con sus números, reultado y conjuntos de falsos resultados"""
    def __init__(self):
        cuenta = self.hacerCuenta()
        self.numeros = cuenta[0]
        self.resultado = cuenta[1]
        self.resultadosFalsos = self.genererResultadosFalsos(self.resultado)
        self.respuestas = list(self.resultadosFalsos)
        self.respuestas.append(self.resultado)
        self.respuestas = self.mezclar_lista(self.respuestas)
    
    def hacerCuenta(self, terminos=4):
        """Retorna una lista con: una lista del conjunto de números que componen la cuenta, y el resultado de la cuenta (que será 
    numeros[0]-numeros[1]+numeros[2]-numeros[3]"""
        numeros = []
        for n in range(int(terminos/2)):
            numeros.append( random.randint(0, 999) )

        i=0
        while len(numeros) < terminos:
            numeros.insert(i+1,random.randint(0,numeros[i]))
            i +=2
            
        resultado = numeros[0]-numeros[1]+numeros[2]-numeros[3]
        return [numeros, resultado]
        
    def genererResultadosFalsos(self,resultado):
        """Retorna una lista con 5 falos resultados en un márgen +10 -10 del resultado real"""
        falsos = []
        i=0
        while len(falsos) < 5:
            azar = random.randint(resultado-10, resultado+10)
            if (azar not in falsos) and (azar is not resultado):
                falsos.append(azar)
        return falsos
        
    def mezclar_lista(self, lista_original):
        """Mezcla una lista"""
        # Crear una copia, ya que no deberíamos modificar la original
        # https://parzibyte.me/blog/2020/05/31/python-clonar-lista-eliminar-referencia/
        lista = lista_original[:]
        # Ciclo for desde 0 hasta la longitud de la lista -1
        longitud_lista = len(lista)
        for i in range(longitud_lista):
            # Obtener un índice aleatorio
            # https://parzibyte.me/blog/2019/04/04/generar-numero-aleatorio-rango-python/
            indice_aleatorio = random.randint(0, longitud_lista - 1)
            # Intercambiar
            temporal = lista[i]
            lista[i] = lista[indice_aleatorio]
            lista[indice_aleatorio] = temporal
        # Regresarla
        return lista

class Pelota():
    """Representa las pelotas que tienen un valor y las características que componen los botones de pelota"""
    def __init__(self, valor, correcto):
        self.valor = valor
        self.archivo = PhotoImage(file="D:\Fran\Programando\PenalesSumayResta\pelota.PNG")
        self.boton = Button(root, text=str(valor),image=self.archivo, compound="top", command=lambda:clickeando(self.valor, correcto), borderwidth=0)
        self.boton.config(bg="white") 
        #Sobre el por qué de lambda:    https://stackoverflow.com/questions/8269096/why-is-button-parameter-command-executed-when-declared


def creacion ():
    global cuenta
    global pelotas
    global label
    global lbl
    #CREANDO CUENTAS Y FALSOS RESULTADOS
    cuenta = Cuentas()
    cOpciones = 6

    #CREANDO PELOTAS CON OPCIONES
    pelotas = []
    for i in range(cOpciones):
        pelotas.append(Pelota(cuenta.respuestas[i], cuenta.resultado))
        pelotas[-1].boton.place(x=(100*(i+1)), y=280)
    
    #MOSTRANDO LA CUENTA
    label = Label(root, text=str(cuenta.numeros[0])+"-"+str(cuenta.numeros[1])+"+"+str(cuenta.numeros[2])+"-"+str(cuenta.numeros[3]))
    label.pack(anchor=NW)
    label.config(#fg="blue",    # Foreground
                 bg="white",   # Background
                 font=("Verdana",30)) 
    label.place(x=200, y=400)
    
    #MOSTRANDO INSTRUCCION O RESULADO
    lbl = Label(root, text="Patea la respuesta correcta")
    lbl.pack(anchor=NW)
    lbl.config(fg="green",    # Foreground
                 bg="white",   # Background
                 font=("Verdana",20)) 
    lbl.place(x=200, y=350)


#CREANDO CANVAS
root = Tk()
root.title("Penales sumas y restas")
root.geometry("750x500")
root.resizable(False, False)
w = 750
h = 500
my_canvas = Canvas(root, width=w, heigh=h, bg="white" )
my_canvas.pack(pady=20)


#CREANDO IMAGEN DE FONDO
fondo =PhotoImage(file="basico.jpg")
my_image_fondo = my_canvas.create_image(375,0, anchor=N, image=fondo)

#Llamando al creador
creacion()




#RESPONDIENDO A LOS BOTONES
def clickeando(valorPelota, correcto):
        global lbl
        if (valorPelota == correcto):
            animation = pyglet.image.load_animation("gol.gif")
            animSprite = pyglet.sprite.Sprite(animation)
            w = animSprite.width
            h = animSprite.height
            window = pyglet.window.Window(width=w, height=h)
            r,g,b,alpha = 0.5,0.5,0.8,0.5
            pyglet.gl.glClearColor(r,g,b,alpha)
            @window.event
            def on_draw():
                window.clear()
                animSprite.draw()             
            def close(event):
                window.close()
            pyglet.clock.schedule_once(close, 2.5)
            pyglet.app.run()
            lbl.after(1, lbl.destroy())
            creacion()
            
        else:
            animation = pyglet.image.load_animation("caida.gif")
            animSprite = pyglet.sprite.Sprite(animation)
            w = animSprite.width
            h = animSprite.height
            window = pyglet.window.Window(width=w, height=h)
            r,g,b,alpha = 0.5,0.5,0.8,0.5
            pyglet.gl.glClearColor(r,g,b,alpha)
            @window.event
            def on_draw():
                window.clear()
                animSprite.draw()           
            def close(event):
                window.close()
            pyglet.clock.schedule_once(close, 2.5)
            pyglet.app.run()
            lbl.after(1, lbl.destroy())
            lbl = Label(root, text="¡Oh no!, intenta de nuevo")
            lbl.pack(anchor=NW)
            lbl.config(fg="red",    # Foreground
                         bg="white",   # Background
                         font=("Verdana",20)) 
            lbl.place(x=200, y=350)

while True:
    root.mainloop()



# tutorial moving
# https://www.youtube.com/watch?v=Z4zePg2M5H8&ab_channel=Codemy.com


