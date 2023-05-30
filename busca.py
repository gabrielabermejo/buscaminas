import tkinter as tk
from tkinter import messagebox
import random

# Dimensiones del tablero
NUM_FILAS = 8
NUM_COLUMNAS = 8
NUM_MINAS = 10

class Casilla:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.mina = False
        self.revelada = False
        self.marcada = False
        self.vecinos_mina = 0

class Buscaminas:
    def __init__(self, root):
        self.root = root
        self.tablero = []
        self.crear_tablero()
        self.crear_interfaz()

    def crear_tablero(self):
        # Inicializar el tablero vacío
        self.tablero = [[Casilla(fila, columna) for columna in range(NUM_COLUMNAS)] for fila in range(NUM_FILAS)]

        # Colocar las minas aleatoriamente
        minas_colocadas = 0
        while minas_colocadas < NUM_MINAS:
            fila = random.randint(0, NUM_FILAS - 1)
            columna = random.randint(0, NUM_COLUMNAS - 1)
            if not self.tablero[fila][columna].mina:
                self.tablero[fila][columna].mina = True
                minas_colocadas += 1

        # Calcular el número de minas vecinas para cada casilla
        for fila in range(NUM_FILAS):
            for columna in range(NUM_COLUMNAS):
                casilla = self.tablero[fila][columna]
                if not casilla.mina:
                    for vecino in self.obtener_vecinos(fila, columna):
                        if vecino.mina:
                            casilla.vecinos_mina += 1

    def crear_interfaz(self):
        self.root.title("Buscaminas")

        self.botones = []
        for fila in range(NUM_FILAS):
            fila_botones = []
            for columna in range(NUM_COLUMNAS):
                boton = tk.Button(self.root, width=2, relief=tk.RAISED)
                boton.grid(row=fila, column=columna)
                boton.bind('<Button-1>', lambda e, fila=fila, columna=columna: self.revelar_casilla(fila, columna))
                boton.bind('<Button-3>', lambda e, fila=fila, columna=columna: self.marcar_casilla(fila, columna))
                fila_botones.append(boton)
            self.botones.append(fila_botones)

    def revelar_casilla(self, fila, columna):
        casilla = self.tablero[fila][columna]

        if casilla.marcada or casilla.revelada:
            return

        casilla.revelada = True
        boton = self.botones[fila][columna]

        if casilla.mina:
            boton.config(relief=tk.SUNKEN, bg='red')
            self.mostrar_mensaje_derrota()
        else:
            boton.config(relief=tk.SUNKEN)
            if casilla.vecinos_mina == 0:
                for vecino in self.obtener_vecinos(fila, columna):
                    self.revelar_casilla(vecino.fila, vecino.columna)
            else:
                boton.config(text=str(casilla.vecinos_mina))

    def marcar_casilla(self, fila, columna):
        casilla = self.tablero[fila][columna]

        if casilla.revelada:
            return

        casilla.marcada = not casilla.marcada
        boton = self.botones[fila][columna]
        if casilla.marcada:
            boton.config(relief=tk.SUNKEN, bg='orange')
        else:
            boton.config(relief=tk.RAISED, bg='SystemButtonFace')

    def obtener_vecinos(self, fila, columna):
        vecinos = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                fila_vecino = fila + i
                columna_vecino = columna + j
                if (0 <= fila_vecino < NUM_FILAS) and (0 <= columna_vecino < NUM_COLUMNAS):
                    vecinos.append(self.tablero[fila_vecino][columna_vecino])
        return vecinos

    def mostrar_mensaje_derrota(self):
        messagebox.showinfo("Fin del juego", "¡Has perdido!")

# Crear la ventana principal
root = tk.Tk()

# Iniciar el juego
buscaminas = Buscaminas(root)

# Ejecutar el bucle principal de la interfaz
root.mainloop()
