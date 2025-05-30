"""
entities.py - Entidades del juego (Player, Enemy, Pearl, PowerUp)

Este módulo contiene todas las clases que representan objetos del juego,
siguiendo el principio de Responsabilidad Única (SRP).
"""

import pygame
import random
import math
from config import *

class Player:
    """
    Clase que representa al jugador (pez protagonista).
    
    Responsabilidades:
    - Manejar movimiento del jugador
    - Gestionar disparos y proyectiles
    - Controlar power-ups activos
    - Detectar colisiones
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.health = 3
        self.score = 0
        self.bullets = []
        self.shoot_cooldown = 0
        self.direction = 1  # 1 = derecha, -1 = izquierda
        
        # Power-ups
        self.speed_boost = 0
        self.shield_active = 0
        
        # Sistema de invulnerabilidad
        self.invulnerability_timer = 0
        
    def update(self, keys):
        """Actualiza la posición y estado del jugador"""
        # Movimiento con speed boost si está activo
        speed = self.speed * 1.5 if self.speed_boost > 0 else self.speed
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= speed
            self.direction = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += speed
            self.direction = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += speed
            
        # Mantener dentro de los límites de pantalla
        self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
        self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))
        
        # Disparar
        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            self._shoot()
            
        # Actualizar cooldowns y efectos
        self._update_timers()
        self._update_bullets()
    
    def _shoot(self):
        """Método privado para crear un proyectil"""
        self.bullets.append({
            'x': self.x + self.size * self.direction,
            'y': self.y,
            'dx': BULLET_SPEED * self.direction
        })
        self.shoot_cooldown = 15
    
    def _update_timers(self):
        """Método privado para actualizar temporizadores"""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.speed_boost > 0:
            self.speed_boost -= 1
        if self.shield_active > 0:
            self.shield_active -= 1
        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= 1
    
    def _update_bullets(self):
        """Método privado para actualizar proyectiles"""
        for bullet in self.bullets[:]:
            bullet['x'] += bullet['dx']
            if bullet['x'] < 0 or bullet['x'] > SCREEN_WIDTH:
                self.bullets.remove(bullet)
    
    def get_rect(self):
        """Retorna el rectángulo de colisión del jugador"""
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, 
                          self.size, self.size)
    
    def take_damage(self):
        """El jugador recibe daño"""
        if self.shield_active <= 0:
            self.health -= 1
            # Período de invulnerabilidad después de recibir daño
            self.invulnerability_timer = 120  # 2 segundos a 60 FPS
            return True
        return False
    
    def can_take_damage(self):
        """Verifica si el jugador puede recibir daño"""
        return self.invulnerability_timer <= 0 and self.shield_active <= 0
    
    def is_invulnerable(self):
        """Verifica si el jugador está en período de invulnerabilidad"""
        return self.invulnerability_timer > 0 or self.shield_active > 0
    
    def apply_powerup(self, power_type):
        """Aplica un power-up al jugador"""
        if power_type == "speed":
            self.speed_boost = 300  # 5 segundos
        elif power_type == "shield":
            self.shield_active = 300  # 5 segundos

class Enemy:
    """
    Clase que representa a los enemigos.
    
    Responsabilidades:
    - Implementar comportamientos específicos por tipo
    - Manejar movimiento y animación
    - Proporcionar información de colisión
    """
    
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.size = ENEMY_SIZE
        self.type = enemy_type
        self.speed = ENEMY_SPEED
        self.direction = random.choice([-1, 1])
        self.animation_timer = 0
        
        # Configuración específica por tipo
        self._configure_by_type()
    
    def _configure_by_type(self):
        """Método privado para configurar propiedades según el tipo"""
        if self.type == "jellyfish":
            self.color = PURPLE
            self.speed = 1
        elif self.type == "crab":
            self.color = RED
            self.speed = 2
        elif self.type == "shark":
            self.color = (70, 70, 70)
            self.speed = 3
            self.size = 35
    
    def update(self, player_x, player_y):
        """Actualiza el comportamiento del enemigo según su tipo"""
        self.animation_timer += 1
        
        if self.type == "jellyfish":
            self._update_jellyfish()
        elif self.type == "crab":
            self._update_crab()
        elif self.type == "shark":
            self._update_shark(player_x, player_y)
        
        # Mantener en pantalla
        self._keep_in_bounds()
    
    def _update_jellyfish(self):
        """Comportamiento específico de medusa"""
        # Movimiento ondulatorio
        self.y += math.sin(self.animation_timer * 0.05) * 0.5
        self.x += self.direction * 0.5
    
    def _update_crab(self):
        """Comportamiento específico de cangrejo"""
        # Movimiento lateral
        self.x += self.direction * self.speed
        if self.animation_timer % 120 == 0:
            self.direction *= -1
    
    def _update_shark(self, player_x, player_y):
        """Comportamiento específico de tiburón"""
        # Perseguir al jugador
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
    
    def _keep_in_bounds(self):
        """Método privado para mantener enemigo en pantalla"""
        self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
        self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))
    
    def get_rect(self):
        """Retorna el rectángulo de colisión del enemigo"""
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, 
                          self.size, self.size)
    
    def get_points_value(self, level):
        """Calcula los puntos que da el enemigo según el nivel actual"""
        base_points = ENEMY_POINTS
        return base_points + (level * 5)  # +5 puntos por nivel

class Pearl:
    """
    Clase que representa las perlas coleccionables.
    
    Responsabilidades:
    - Manejar animación de flotación
    - Proporcionar información de colisión
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 15
        self.animation_timer = 0
        # El valor base se calculará dinámicamente según el nivel
        self.base_value = PEARL_POINTS
    
    def update(self):
        """Actualiza la animación de la perla"""
        self.animation_timer += 1
        self.y += math.sin(self.animation_timer * 0.1) * 0.3
    
    def get_rect(self):
        """Retorna el rectángulo de colisión de la perla"""
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, 
                          self.size, self.size)
    
    def get_value(self, level):
        """Calcula el valor de la perla según el nivel actual"""
        return self.base_value + (level * 2)  # +2 puntos por nivel

class PowerUp:
    """
    Clase que representa los power-ups.
    
    Responsabilidades:
    - Manejar animación de power-up
    - Definir tipo y efectos
    - Proporcionar información de colisión
    """
    
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.size = 20
        self.type = power_type  # "speed" o "shield"
        self.animation_timer = 0
        self.color = YELLOW if power_type == "speed" else LIGHT_BLUE
    
    def update(self):
        """Actualiza la animación del power-up"""
        self.animation_timer += 1
        self.y += math.sin(self.animation_timer * 0.15) * 0.5
    
    def get_rect(self):
        """Retorna el rectángulo de colisión del power-up"""
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, 
                          self.size, self.size)