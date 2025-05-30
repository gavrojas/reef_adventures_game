#!/usr/bin/env python3
"""
Aventuras en el Arrecife Perdido - Versión Simplificada
Punto de entrada principal del juego.

Este archivo solo se encarga de inicializar y ejecutar el juego,
siguiendo el principio de Responsabilidad Única (SRP).
"""

from game import Game

def main():
    """
    Función principal que ejecuta el juego.
    
    Esta función es el punto de entrada único del programa,
    manteniendo la separación de responsabilidades.
    """
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nJuego interrumpido por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")
        print("Por favor, verifica que PyGame esté instalado correctamente.")

if __name__ == "__main__":
    main()