"""
graphics.py - Funciones de dibujo y renderizado

Este módulo contiene todas las funciones relacionadas con el dibujo,
siguiendo el principio de Responsabilidad Única (SRP).
"""

import pygame
import random
from config import *

def draw_fish(surface, x, y, size, color, direction=1):
    """
    Dibuja un pez personalizado.
    
    Args:
        surface: Superficie donde dibujar
        x, y: Posición del pez
        size: Tamaño del pez
        color: Color del pez
        direction: Dirección (1 = derecha, -1 = izquierda)
    """
    # Cuerpo del pez (elipse)
    body_rect = pygame.Rect(x - size//2, y - size//3, size, size//1.5)
    pygame.draw.ellipse(surface, color, body_rect)
    
    # Cola del pez
    tail_points = [
        (x - size//2 * direction, y),
        (x - size * direction, y - size//3),
        (x - size * direction, y + size//3)
    ]
    pygame.draw.polygon(surface, color, tail_points)
    
    # Ojo del pez
    eye_x = x + size//4 * direction
    eye_y = y - size//6
    pygame.draw.circle(surface, WHITE, (eye_x, eye_y), size//6)
    pygame.draw.circle(surface, BLACK, (eye_x + 2 * direction, eye_y), size//10)

def draw_jellyfish(surface, x, y, size, color):
    """
    Dibuja una medusa con tentáculos.
    
    Args:
        surface: Superficie donde dibujar
        x, y: Posición de la medusa
        size: Tamaño de la medusa
        color: Color de la medusa
    """
    # Cuerpo de la medusa (semicírculo)
    pygame.draw.circle(surface, color, (x, y), size//2)
    pygame.draw.rect(surface, color, (x - size//2, y, size, size//4))
    
    # Tentáculos animados
    for i in range(3):
        start_x = x - size//4 + i * size//4
        end_x = start_x + random.randint(-3, 3)
        end_y = y + size//2 + random.randint(8, 15)
        pygame.draw.line(surface, color, (start_x, y + size//4), (end_x, end_y), 2)

def draw_background(surface):
    """
    Dibuja el fondo oceánico con degradado.
    
    Args:
        surface: Superficie donde dibujar el fondo
    """
    # Degradado de azul desde arriba (claro) hacia abajo (oscuro)
    for y in range(SCREEN_HEIGHT):
        intensity = int(255 * (y / SCREEN_HEIGHT))
        color = (0, max(0, 100 - intensity//3), min(255, 150 + intensity//2))
        pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))

def draw_heart(surface, x, y, size=12):
    """
    Dibuja un corazón para representar vidas.
    
    Args:
        surface: Superficie donde dibujar
        x, y: Posición del corazón
        size: Tamaño del corazón
    """
    # Dos círculos para la parte superior del corazón
    pygame.draw.circle(surface, RED, (x, y), size)
    pygame.draw.circle(surface, RED, (x + 8, y), size)
    
    # Triángulo para la parte inferior del corazón
    pygame.draw.polygon(surface, RED, [
        (x - size, y + 5),
        (x + 4, y + size + 8),
        (x + size + 8, y + 5)
    ])

def draw_pearl(surface, x, y, size=15):
    """
    Dibuja una perla coleccionable.
    
    Args:
        surface: Superficie donde dibujar
        x, y: Posición de la perla
        size: Tamaño de la perla
    """
    # Perla principal
    pygame.draw.circle(surface, CORAL, (int(x), int(y)), size)
    # Brillo de la perla
    pygame.draw.circle(surface, WHITE, (int(x - 3), int(y - 3)), size//3)

def draw_powerup(surface, powerup):
    """
    Dibuja un power-up.
    
    Args:
        surface: Superficie donde dibujar
        powerup: Objeto PowerUp a dibujar
    """
    # Power-up principal
    pygame.draw.circle(surface, powerup.color, 
                      (int(powerup.x), int(powerup.y)), powerup.size)
    
    # Símbolo según el tipo
    if powerup.type == "speed":
        # Líneas de velocidad
        for i in range(3):
            start_x = powerup.x - powerup.size//2 + i * 5
            pygame.draw.line(surface, WHITE, 
                           (start_x, powerup.y - 5), 
                           (start_x + 8, powerup.y - 5), 2)
    elif powerup.type == "shield":
        # Círculo interior para el escudo
        pygame.draw.circle(surface, WHITE, 
                         (int(powerup.x), int(powerup.y)), powerup.size//2, 2)

def draw_bullet(surface, bullet):
    """
    Dibuja un proyectil del jugador.
    
    Args:
        surface: Superficie donde dibujar
        bullet: Diccionario con información del proyectil
    """
    pygame.draw.circle(surface, LIGHT_BLUE, 
                      (int(bullet['x']), int(bullet['y'])), BULLET_SIZE)
    # Núcleo más brillante
    pygame.draw.circle(surface, WHITE, 
                      (int(bullet['x']), int(bullet['y'])), BULLET_SIZE//2)

def draw_hud(surface, font, player):
    """
    Dibuja la interfaz de usuario (HUD).
    
    Args:
        surface: Superficie donde dibujar
        font: Fuente para el texto
        player: Objeto jugador con la información a mostrar
    """
    # Dibujar vidas
    for i in range(player.health):
        heart_x = 20 + i * 35
        draw_heart(surface, heart_x, 30)
    
    # Puntuación
    score_text = font.render(f"Puntuación: {player.score}", True, WHITE)
    surface.blit(score_text, (20, 60))
    
    # Power-ups activos
    y_offset = 90
    if player.speed_boost > 0:
        speed_text = font.render(f"Velocidad: {player.speed_boost//60 + 1}s", True, YELLOW)
        surface.blit(speed_text, (20, y_offset))
        y_offset += 25
    
    if player.shield_active > 0:
        shield_text = font.render(f"Escudo: {player.shield_active//60 + 1}s", True, LIGHT_BLUE)
        surface.blit(shield_text, (20, y_offset))
        y_offset += 25
    
    # Mostrar estado de invulnerabilidad
    if player.invulnerability_timer > 0:
        invul_text = font.render(f"Invulnerable: {player.invulnerability_timer//60 + 1}s", True, RED)
        surface.blit(invul_text, (20, y_offset))

def draw_enemy(surface, enemy):
    """
    Dibuja un enemigo según su tipo.
    
    Args:
        surface: Superficie donde dibujar
        enemy: Objeto Enemy a dibujar
    """
    if enemy.type == "jellyfish":
        draw_jellyfish(surface, int(enemy.x), int(enemy.y), 
                      enemy.size, enemy.color)
    elif enemy.type == "crab":
        # Dibujar cangrejo como elipse con pinzas
        pygame.draw.ellipse(surface, enemy.color,
                          (enemy.x - enemy.size//2, enemy.y - enemy.size//3,
                           enemy.size, enemy.size//1.5))
        # Pinzas del cangrejo
        pincer_size = enemy.size // 4
        pygame.draw.circle(surface, enemy.color,
                         (int(enemy.x - enemy.size//3), int(enemy.y)), pincer_size)
        pygame.draw.circle(surface, enemy.color,
                         (int(enemy.x + enemy.size//3), int(enemy.y)), pincer_size)
    elif enemy.type == "shark":
        draw_fish(surface, int(enemy.x), int(enemy.y), 
                 enemy.size, enemy.color)

def draw_level_info(surface, font, level, score, target_score):
    """
    Dibuja información del nivel actual.
    
    Args:
        surface: Superficie donde dibujar
        font: Fuente para el texto
        level: Nivel actual
        score: Puntuación actual
        target_score: Puntuación objetivo
    """
    # Color especial para niveles altos
    if level >= 30:
        level_color = CORAL  # Dorado para maestros
    elif level >= 20:
        level_color = PURPLE  # Púrpura para expertos
    elif level >= 10:
        level_color = YELLOW  # Amarillo para avanzados
    else:
        level_color = WHITE  # Blanco para principiantes
    
    level_text = font.render(f"Nivel: {level}", True, level_color)
    surface.blit(level_text, (SCREEN_WIDTH - 120, 20))
    
    progress_text = font.render(f"Progreso: {score}/{target_score}", True, WHITE)
    surface.blit(progress_text, (SCREEN_WIDTH - 200, 45))
    
    # Mostrar indicador de zona según el nivel
    if level >= 30:
        zone_text = font.render("ZONA MAESTRO", True, CORAL)
        surface.blit(zone_text, (SCREEN_WIDTH - 150, 70))
    elif level >= 20:
        zone_text = font.render("ZONA EXPERTA", True, PURPLE)
        surface.blit(zone_text, (SCREEN_WIDTH - 150, 70))
    elif level >= 10:
        zone_text = font.render("ZONA AVANZADA", True, YELLOW)
        surface.blit(zone_text, (SCREEN_WIDTH - 150, 70))