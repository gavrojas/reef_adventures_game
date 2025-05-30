"""
config.py - Configuración y constantes del juego

Este módulo contiene todas las configuraciones globales del juego,
siguiendo el principio de separación de configuración del código.
"""

import pygame

# ===== CONFIGURACIÓN DE PANTALLA =====
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# ===== PALETA DE COLORES =====
# Colores del océano
BLUE = (0, 100, 200)
LIGHT_BLUE = (100, 150, 255)
DARK_BLUE = (0, 50, 150)

# Colores básicos
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Colores temáticos del juego
ORANGE = (255, 165, 0)      # Color del jugador
PURPLE = (128, 0, 128)      # Color de medusas
CORAL = (255, 127, 80)      # Color de perlas
PINK = (255, 192, 203)      # Color decorativo

# ===== CONFIGURACIÓN DEL JUGADOR =====
PLAYER_SIZE = 30
PLAYER_SPEED = 5
PLAYER_MAX_HEALTH = 3

# ===== CONFIGURACIÓN DE ENEMIGOS =====
ENEMY_SIZE = 25
ENEMY_SPEED = 2

# ===== CONFIGURACIÓN DE PROYECTILES =====
BULLET_SIZE = 8
BULLET_SPEED = 8

# ===== CONFIGURACIÓN DE COLECCIONABLES =====
PEARL_SIZE = 15
POWERUP_SIZE = 20
POWERUP_DURATION = 300  # frames (5 segundos a 60 FPS)

# ===== SISTEMA DE PUNTUACIÓN =====
PEARL_POINTS = 25  # Aumentado de 10 a 25
ENEMY_POINTS = 75  # Aumentado de 20 a 75

# Puntos base para calcular progresión de niveles
BASE_POINTS_PER_LEVEL = 150  # Aumentado de 40 a 150
POINTS_INCREMENT_PER_LEVEL = 50  # Aumentado de 10 a 50

# Número de niveles principales (con mensaje especial cada 10 niveles)
MILESTONE_LEVELS = [10, 20, 30, 40, 50]  # Niveles especiales

# Número máximo de niveles antes de modo infinito
MAX_PLANNED_LEVELS = 30

# ===== ESTADOS DEL JUEGO =====
MENU = 0
PLAYING = 1
GAME_OVER = 2
INSTRUCTIONS = 3

# ===== CONFIGURACIÓN DE DIFICULTAD =====
# Probabilidad de spawn de power-ups (1 en X frames)
POWERUP_SPAWN_CHANCE = 300

# Número máximo de enemigos por nivel
MAX_ENEMIES_PER_LEVEL = 6

# ===== CONFIGURACIÓN DE ANIMACIÓN =====
# Velocidades de animación (valores más altos = más lento)
JELLYFISH_ANIMATION_SPEED = 0.05
PEARL_ANIMATION_SPEED = 0.1
POWERUP_ANIMATION_SPEED = 0.15

# ===== MENSAJES DE JUEGO =====
GAME_TITLE = "AVENTURAS EN EL ARRECIFE PERDIDO"
MENU_OPTIONS = ["JUGAR", "INSTRUCCIONES", "SALIR"]

# Mensajes motivacionales según puntuación
PERFORMANCE_MESSAGES = {
    0: "¡Sigue practicando!",
    100: "¡Buen trabajo!",
    200: "¡Excelente puntuación!"
}