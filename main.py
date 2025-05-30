#!/usr/bin/env python3
"""
Aventuras en el Arrecife Perdido - Versión Universal
Punto de entrada principal del juego que funciona en desktop y web.
"""

import asyncio
import sys
from game import Game

def main():
    """
    Función principal que detecta el entorno y ejecuta el juego apropiadamente.
    """
    try:
        game = Game()
        
        # Detectar si estamos en un entorno web (Pygame Web/Emscripten)
        try:
            # Intentar detectar entorno web
            import platform
            if hasattr(platform, 'machine') and 'wasm' in platform.machine().lower():
                # Estamos en web, usar versión asíncrona
                asyncio.run(game.run())
            else:
                # Estamos en desktop, usar versión síncrona
                game.run_sync()
        except:
            # Fallback: usar versión síncrona para desktop
            game.run_sync()
            
    except KeyboardInterrupt:
        print("\nJuego interrumpido por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")
        print("Por favor, verifica que PyGame esté instalado correctamente.")

if __name__ == "__main__":
    main()