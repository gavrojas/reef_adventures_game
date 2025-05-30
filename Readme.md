# Aventuras en el Arrecife Perdido

Un juego educativo desarrollado en Python con PyGame que demuestra conceptos fundamentales de programación aplicando principios SOLID.

## 📋 Descripción

Controla a un pequeño pez que debe navegar por el océano, coleccionando perlas y derrotando enemigos para avanzar a través de niveles cada vez más desafiantes. El juego presenta un **sistema de progresión exponencial** donde cada nivel requiere significativamente más puntos que el anterior.

## 🎮 Características Principales

### Sistema de Puntuación Dinámico
- **Las perlas aumentan su valor cada nivel**: Nivel 1 = 27pts, Nivel 5 = 35pts, Nivel 10 = 45pts
- **Los enemigos dan más puntos por nivel**: Nivel 1 = 80pts, Nivel 5 = 100pts, Nivel 10 = 125pts
- **Progresión exponencial de niveles**: Nivel 1 = 50pts, Nivel 3 = 280pts, Nivel 10 = 3200pts

### Enemigos
- 🎐 **Medusas**: Movimiento ondulatorio lento
- 🦀 **Cangrejos**: Patrullan lateralmente
- 🦈 **Tiburones**: Persiguen activamente al jugador

### Power-ups
- ⚡ **Velocidad** (Amarillo): Aumenta velocidad temporalmente
- 🛡️ **Escudo** (Azul): Protección temporal contra daños

### Sistema de Progresión
- **Dos formas de avanzar de nivel**: Alcanzar el puntaje objetivo O derrotar todos los enemigos
- **Niveles infinitos**: El juego continúa indefinidamente con dificultad creciente
- **Zonas especiales**: Avanzada (Nivel 10+), Experta (Nivel 20+), Maestro (Nivel 30+)

## 🚀 Instalación y Ejecución

### Requisitos
- Python 3.7+
- PyGame 2.0+

### Instalación
```
pip install pygame
python main.py
```

## 🎮 Controles

### Menú Principal
- **↑↓** o **W/S**: Navegar opciones
- **ENTER** o **ESPACIO**: Seleccionar

### Durante el Juego
- **WASD** o **Flechas**: Mover el pez
- **ESPACIO**: Disparar burbujas

## 📁 Estructura del Proyecto
```
aventuras_arrecife/
├── main.py              # Punto de entrada principal
├── game.py              # Lógica principal del juego y estados
├── entities.py          # Clases Player, Enemy, Pearl, PowerUp
├── graphics.py          # Funciones de dibujo y renderizado
├── utils.py             # Utilidades y generación de contenido
└── config.py            # Configuración y constantes
```

## 🎯 Características Técnicas

### Principios SOLID Aplicados
- **Single Responsibility**: Cada clase tiene una responsabilidad específica
- **Open/Closed**: Fácil extensión sin modificar código existente
- **Separation of Concerns**: Lógica, gráficos y utilidades separadas

### Conceptos de Programación
- Programación Orientada a Objetos
- Manejo de estados del juego
- Sistemas de colisión
- Animación y rendering
- Gestión de eventos

## 🛠️ Personalización

### Modificar Dificultad
Editar valores en `config.py`:
```
PEARL_POINTS = 25        # Puntos base por perla
ENEMY_POINTS = 75        # Puntos base por enemigo
PLAYER_SPEED = 5         # Velocidad del jugador
```

## Agregar Nuevos Enemigos

Crear comportamiento en entities.py
Añadir visualización en graphics.py
Incluir en generación en utils.py

## 🎓 Uso Educativo
Este proyecto fue desarrollado como un trabajo práctico de un tutor de Python:

Arquitectura de software modular
Principios de diseño SOLID
Programación de videojuegos básica
Buenas prácticas de Python

## 📄 Licencia
Proyecto educativo de código abierto. Libre para usar, modificar y distribuir en contextos de aprendizaje.