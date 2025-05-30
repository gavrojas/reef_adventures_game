"""
utils.py - Funciones auxiliares y utilidades del juego

Este módulo contiene funciones de propósito general que pueden ser
utilizadas por diferentes partes del juego.
"""

import random
from entities import Enemy, Pearl, PowerUp
from config import *

def check_collision(rect1, rect2):
    """
    Verifica colisión entre dos rectángulos.
    
    Args:
        rect1, rect2: Rectángulos de pygame a verificar
        
    Returns:
        bool: True si hay colisión, False en caso contrario
    """
    return rect1.colliderect(rect2)

def create_enemies(level):
    """
    Crea una lista de enemigos según el nivel.
    Cantidad fija y balanceada, sin escalado excesivo.
    
    Args:
        level: Nivel actual del juego
        
    Returns:
        list: Lista de objetos Enemy
    """
    enemies = []
    enemy_types = ["jellyfish", "crab", "shark"]
    
    # Cantidad balanceada de enemigos (no excesiva)
    if level <= 3:
        num_enemies = 3  # Niveles iniciales: pocos enemigos
    elif level <= 10:
        num_enemies = 5  # Niveles medios: cantidad moderada
    elif level <= 20:
        num_enemies = 7  # Niveles altos: más enemigos
    else:
        num_enemies = 8  # Niveles expertos: máximo controlado
    
    # Determinar tipos de enemigos disponibles según el nivel
    if level <= 3:
        available_types = ["jellyfish"]  # Solo medusas al inicio
    elif level <= 8:
        available_types = ["jellyfish", "crab"]  # Agregar cangrejos
    else:
        available_types = enemy_types  # Todos los tipos disponibles
    
    # Crear enemigos
    for _ in range(num_enemies):
        # Posición aleatoria evitando los bordes
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = random.randint(100, SCREEN_HEIGHT - 100)
        
        # Seleccionar tipo según el nivel
        if level >= 15:
            # Niveles altos: más tiburones
            enemy_type = random.choices(
                available_types, 
                weights=[1, 2, 4],  # Más probabilidad de tiburones
                k=1
            )[0]
        elif level >= 8:
            # Niveles medios: balanceado
            enemy_type = random.choices(
                available_types,
                weights=[2, 3, 2] if len(available_types) == 3 else [3, 4],
                k=1
            )[0]
        else:
            # Niveles bajos: distribución normal
            enemy_type = random.choice(available_types)
        
        enemies.append(Enemy(x, y, enemy_type))
    
    return enemies

def create_pearls(count):
    """
    Crea una lista de perlas coleccionables.
    
    Args:
        count: Número de perlas a crear
        
    Returns:
        list: Lista de objetos Pearl
    """
    pearls = []
    attempts = 0
    max_attempts = count * 3  # Evitar bucle infinito
    
    while len(pearls) < count and attempts < max_attempts:
        # Posición aleatoria evitando los bordes
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        
        # Verificar que no esté muy cerca de otras perlas
        too_close = False
        for existing_pearl in pearls:
            distance = ((x - existing_pearl.x) ** 2 + (y - existing_pearl.y) ** 2) ** 0.5
            if distance < 40:  # Distancia mínima entre perlas
                too_close = True
                break
        
        if not too_close:
            pearls.append(Pearl(x, y))
        
        attempts += 1
    
    return pearls

def calculate_pearls_for_level(level):
    """
    Calcula cuántas perlas crear para un nivel específico.
    Cantidad fija y balanceada, la dificultad viene del valor de los puntos.
    
    Args:
        level: Nivel actual
        
    Returns:
        int: Número de perlas a crear
    """
    # Cantidad fija de perlas, no excesiva
    if level <= 5:
        return 8   # Niveles iniciales: pocas perlas
    elif level <= 15:
        return 12  # Niveles medios: cantidad moderada
    else:
        return 15  # Niveles altos: más perlas pero controlado

def is_milestone_level(level):
    """
    Verifica si un nivel es un hito especial.
    
    Args:
        level: Nivel a verificar
        
    Returns:
        bool: True si es un nivel de hito
    """
    return level in MILESTONE_LEVELS

def get_milestone_message(level):
    """
    Obtiene el mensaje especial para un nivel de hito.
    
    Args:
        level: Nivel de hito
        
    Returns:
        str: Mensaje especial
    """
    messages = {
        10: "¡Felicitaciones! ¡Has alcanzado el nivel 10!",
        20: "¡Increíble! ¡Nivel 20 conquistado!",
        30: "¡MAESTRO DEL ARRECIFE! ¡Nivel 30 completado!",
        40: "¡LEYENDA MARINA! ¡Nivel 40 alcanzado!",
        50: "¡EMPERADOR DEL OCÉANO! ¡Nivel 50 dominado!"
    }
    return messages.get(level, f"¡Nivel {level} completado!")

def spawn_powerup():
    """
    Genera un power-up aleatorio con baja probabilidad.
    
    Returns:
        PowerUp or None: Objeto PowerUp si se genera, None en caso contrario
    """
    # Probabilidad muy baja de generar power-up
    if random.randint(1, 300) == 1:
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        power_type = random.choice(["speed", "shield"])
        return PowerUp(x, y, power_type)
    
    return None

def get_level_target_score(level):
    """
    Calcula la puntuación objetivo para un nivel específico.
    
    Nueva progresión exponencial agresiva:
    - Nivel 1: 50 puntos
    - Nivel 2: 120 puntos (+70)
    - Nivel 3: 280 puntos (+160)
    - Nivel 4: 450 puntos (+170)
    - Nivel 5: 700 puntos (+250)
    - Nivel 6: 1000 puntos (+300)
    - Nivel 7: 1400 puntos (+400)
    - Nivel 8: 1900 puntos (+500)
    - Nivel 9: 2500 puntos (+600)
    - Nivel 10: 3200 puntos (+700)
    
    Args:
        level: Nivel del juego (1, 2, 3, ...)
        
    Returns:
        int: Puntuación necesaria para pasar al siguiente nivel
    """
    # Tabla predefinida para los primeros niveles con progresión agresiva
    level_scores = {
        1: 50,
        2: 120,
        3: 280,
        4: 450,
        5: 700,
        6: 1000,
        7: 1400,
        8: 1900,
        9: 2500,
        10: 3200,
        11: 4000,
        12: 4900,
        13: 5900,
        14: 7000,
        15: 8200,
        16: 9500,
        17: 11000,
        18: 12600,
        19: 14400,
        20: 16300,
        21: 18400,
        22: 20700,
        23: 23200,
        24: 25900,
        25: 28800,
        26: 31900,
        27: 35200,
        28: 38700,
        29: 42400,
        30: 46300
    }
    
    # Si el nivel está en la tabla, usar el valor predefinido
    if level in level_scores:
        return level_scores[level]
    
    # Para niveles superiores a 30, usar fórmula exponencial
    base_score = level_scores[30]  # 46300
    extra_levels = level - 30
    # Aumentar 5000 puntos por cada nivel adicional después del 30
    return base_score + (extra_levels * 5000)

def clamp(value, min_value, max_value):
    """
    Limita un valor entre un mínimo y máximo.
    
    Args:
        value: Valor a limitar
        min_value: Valor mínimo
        max_value: Valor máximo
        
    Returns:
        int/float: Valor limitado entre min_value y max_value
    """
    return max(min_value, min(max_value, value))

def is_position_safe(x, y, entities, min_distance=50):
    """
    Verifica si una posición está lo suficientemente lejos de otras entidades.
    
    Args:
        x, y: Posición a verificar
        entities: Lista de entidades existentes
        min_distance: Distancia mínima requerida
        
    Returns:
        bool: True si la posición es segura, False en caso contrario
    """
    for entity in entities:
        distance = ((x - entity.x) ** 2 + (y - entity.y) ** 2) ** 0.5
        if distance < min_distance:
            return False
    return True

def get_random_safe_position(entities, min_distance=50, max_attempts=10):
    """
    Obtiene una posición aleatoria que esté lejos de otras entidades.
    
    Args:
        entities: Lista de entidades existentes
        min_distance: Distancia mínima requerida
        max_attempts: Número máximo de intentos
        
    Returns:
        tuple: (x, y) posición segura, o posición aleatoria si no se encuentra
    """
    for _ in range(max_attempts):
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        
        if is_position_safe(x, y, entities, min_distance):
            return x, y
    
    # Si no se encuentra posición segura, devolver una aleatoria
    return random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)