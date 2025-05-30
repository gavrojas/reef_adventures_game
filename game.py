"""
game.py - Lógica principal del juego

Este módulo contiene la clase Game que maneja toda la lógica del juego,
siguiendo los principios SOLID y separación de responsabilidades.
Incluye soporte para despliegue web con Pygame Web.
"""

import pygame
import sys
import asyncio
from entities import Player
from graphics import *
from utils import *
from config import *

class Game:
    """
    Clase principal que maneja todo el juego.
    
    Responsabilidades:
    - Coordinar todas las partes del juego
    - Manejar estados del juego (menú, jugando, game over)
    - Procesar eventos de entrada
    - Actualizar lógica del juego
    - Coordinar el renderizado
    - Soporte para ejecución web y desktop
    """
    
    def __init__(self):
        """Inicializa el juego y sus componentes"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Aventuras en el Arrecife Perdido")
        self.clock = pygame.time.Clock()
        
        # Fuentes
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)
        
        # Estado del juego
        self.state = MENU
        self.selected_option = 0
        self.menu_options = ["JUGAR", "INSTRUCCIONES", "SALIR"]
        
        # Inicializar objetos del juego
        self._initialize_game_objects()
        
    def _initialize_game_objects(self):
        """Método privado para inicializar objetos del juego"""
        self.player = None
        self.enemies = []
        self.pearls = []
        self.powerups = []
        self.level = 1

    def reset_game(self):
        """Reinicia el juego a su estado inicial"""
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.level = 1
        self.enemies = create_enemies(self.level)
        # Crear perlas apropiadas para el nivel 1
        pearls_needed = calculate_pearls_for_level(self.level)
        self.pearls = create_pearls(pearls_needed)
        self.powerups = []

    async def run(self):
        """Bucle principal del juego - versión asíncrona para web"""
        running = True
        
        while running:
            running = self._handle_events()
            self._update()
            self._render()
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
            # Permitir que el navegador procese otros eventos
            await asyncio.sleep(0)
        
        self._cleanup()
    
    def run_sync(self):
        """Bucle principal del juego - versión síncrona para desktop"""
        running = True
        
        while running:
            running = self._handle_events()
            self._update()
            self._render()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        self._cleanup()

    def _handle_events(self):
        """Maneja todos los eventos del juego"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if not self._handle_keydown_event(event):
                    return False
        
        return True

    def _handle_keydown_event(self, event):
        """Maneja eventos de teclas presionadas"""
        if self.state == MENU:
            return self._handle_menu_input(event)
        elif self.state == INSTRUCTIONS:
            return self._handle_instructions_input(event)
        elif self.state == GAME_OVER:
            return self._handle_game_over_input(event)
        
        return True

    def _handle_menu_input(self, event):
        """Maneja entrada en el menú principal"""
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.selected_option = (self.selected_option - 1) % len(self.menu_options)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.selected_option = (self.selected_option + 1) % len(self.menu_options)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.selected_option == 0:  # JUGAR
                self.state = PLAYING
                self.reset_game()
            elif self.selected_option == 1:  # INSTRUCCIONES
                self.state = INSTRUCTIONS
            elif self.selected_option == 2:  # SALIR
                return False
        return True

    def _handle_instructions_input(self, event):
        """Maneja entrada en pantalla de instrucciones"""
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
            self.state = MENU
        return True

    def _handle_game_over_input(self, event):
        """Maneja entrada en pantalla de game over"""
        if event.key == pygame.K_SPACE:
            self.state = MENU
        elif event.key == pygame.K_ESCAPE:
            return False
        return True

    def _update(self):
        """Actualiza la lógica del juego según el estado actual"""
        if self.state == PLAYING:
            self._update_game_logic()

    def _update_game_logic(self):
        """Actualiza toda la lógica cuando el juego está activo"""
        keys = pygame.key.get_pressed()
        
        # Actualizar jugador
        self.player.update(keys)
        
        # Actualizar entidades
        self._update_entities()
        
        # Verificar colisiones
        self._check_collisions()
        
        # Generar nuevos power-ups
        self._spawn_new_powerups()
        
        # Verificar condiciones de nivel
        self._check_level_progression()

    def _update_entities(self):
        """Actualiza todas las entidades del juego"""
        # Actualizar enemigos
        for enemy in self.enemies:
            enemy.update(self.player.x, self.player.y)
        
        # Actualizar perlas
        for pearl in self.pearls:
            pearl.update()
        
        # Actualizar power-ups
        for powerup in self.powerups:
            powerup.update()

    def _check_collisions(self):
        """Verifica todas las colisiones del juego"""
        self._check_bullet_enemy_collisions()
        self._check_player_enemy_collisions()
        self._check_player_pearl_collisions()
        self._check_player_powerup_collisions()

    def _check_bullet_enemy_collisions(self):
        """Verifica colisiones entre balas y enemigos"""
        for bullet in self.player.bullets[:]:
            bullet_rect = pygame.Rect(bullet['x'] - BULLET_SIZE//2, 
                                    bullet['y'] - BULLET_SIZE//2, 
                                    BULLET_SIZE, BULLET_SIZE)
            
            for enemy in self.enemies[:]:
                if check_collision(bullet_rect, enemy.get_rect()):
                    # Calcular puntos según el nivel actual
                    points = enemy.get_points_value(self.level)
                    self.player.score += points
                    self.enemies.remove(enemy)
                    self.player.bullets.remove(bullet)
                    break

    def _check_player_enemy_collisions(self):
        """Verifica colisiones entre jugador y enemigos"""
        for enemy in self.enemies:
            if check_collision(self.player.get_rect(), enemy.get_rect()):
                # Solo causar daño si el jugador puede recibirlo
                if self.player.can_take_damage():
                    if self.player.take_damage():
                        # El jugador recibió daño
                        if self.player.health <= 0:
                            self.state = GAME_OVER
                        # Romper el bucle para evitar múltiples daños por frame
                        break

    def _check_player_pearl_collisions(self):
        """Verifica colisiones entre jugador y perlas"""
        for pearl in self.pearls[:]:
            if check_collision(self.player.get_rect(), pearl.get_rect()):
                # Calcular puntos según el nivel actual
                points = pearl.get_value(self.level)
                self.player.score += points
                self.pearls.remove(pearl)

    def _check_player_powerup_collisions(self):
        """Verifica colisiones entre jugador y power-ups"""
        for powerup in self.powerups[:]:
            if check_collision(self.player.get_rect(), powerup.get_rect()):
                self.player.apply_powerup(powerup.type)
                self.powerups.remove(powerup)

    def _spawn_new_powerups(self):
        """Genera nuevos power-ups ocasionalmente"""
        new_powerup = spawn_powerup()
        if new_powerup:
            self.powerups.append(new_powerup)

    def _check_level_progression(self):
        """Verifica si el jugador debe avanzar de nivel"""
        target_score = get_level_target_score(self.level)
        
        # Dos formas de pasar de nivel (para todos los niveles):
        # 1. Alcanzar el puntaje objetivo
        # 2. Derrotar todos los enemigos
        score_reached = self.player.score >= target_score
        all_enemies_defeated = len(self.enemies) == 0
        
        if score_reached or all_enemies_defeated:
            self._advance_level()
    
    def _advance_level(self):
        """Avanza al siguiente nivel"""
        self.level += 1
        
        # Verificar si es un nivel de hito
        if is_milestone_level(self.level - 1):  # Nivel anterior completado
            milestone_msg = get_milestone_message(self.level - 1)
        
        # Crear nuevos enemigos y perlas con cantidades balanceadas
        self.enemies = create_enemies(self.level)
        pearls_needed = calculate_pearls_for_level(self.level)
        new_pearls = create_pearls(pearls_needed)
        self.pearls.extend(new_pearls)
    
    def _complete_game(self):
        """Nunca se llama - el juego es infinito"""
        pass  # El juego ahora es infinito

    def _render(self):
        """Renderiza la pantalla según el estado actual"""
        if self.state == MENU:
            self._render_menu()
        elif self.state == INSTRUCTIONS:
            self._render_instructions()
        elif self.state == PLAYING:
            self._render_game()
        elif self.state == GAME_OVER:
            self._render_game_over()

    def _render_menu(self):
        """Renderiza el menú principal"""
        draw_background(self.screen)
        
        # Título del juego
        title = self.title_font.render("AVENTURAS EN EL", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(title, title_rect)
        
        subtitle = self.title_font.render("ARRECIFE PERDIDO", True, CORAL)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 250))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Opciones del menú
        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.selected_option else WHITE
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 350 + i * 50))
            self.screen.blit(text, text_rect)
        
        # Indicador de selección
        self._draw_menu_selector()
        
        # Instrucciones de control
        controls = self.font.render("Usa ARRIBA/ABAJO y ENTER para navegar", True, LIGHT_BLUE)
        controls_rect = controls.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        self.screen.blit(controls, controls_rect)

    def _draw_menu_selector(self):
        """Dibuja el selector del menú"""
        selector_y = 340 + self.selected_option * 50
        pygame.draw.rect(self.screen, YELLOW, 
                        (SCREEN_WIDTH//2 - 100, selector_y, 200, 30), 2)

    def _render_instructions(self):
        """Renderiza la pantalla de instrucciones"""
        draw_background(self.screen)
        
        # Fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Título
        title = self.title_font.render("INSTRUCCIONES", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        # Contenido de instrucciones
        self._draw_instructions_content()

    def _draw_instructions_content(self):
        """Dibuja el contenido de las instrucciones"""
        instructions = [
            "OBJETIVO:",
            "  * Colecciona perlas y derrota enemigos",
            "  * Los puntos AUMENTAN cada nivel",
            "",
            "CONTROLES:",
            "  * WASD o flechas: moverse",
            "  * ESPACIO: disparar burbujas",
            "",
            "SISTEMA DE PUNTOS DINAMICO:",
            "  * Nivel 1: Perlas=27pts, Enemigos=80pts",
            "  * Nivel 5: Perlas=35pts, Enemigos=100pts",
            "  * Nivel 10: Perlas=45pts, Enemigos=125pts",
            "",
            "PROGRESION EXPONENCIAL:",
            "  * Nivel 1: 50 puntos",
            "  * Nivel 3: 280 puntos",
            "  * Nivel 10: 3200 puntos",
            "",
            "¡Cada nivel es MAS DIFICIL!",
            "",
            "Presiona ESPACIO para volver"
        ]
        
        y_offset = 120
        for line in instructions:
            color = self._get_instruction_line_color(line)
            
            if line.strip():
                text = self.font.render(line, True, color)
                self.screen.blit(text, (SCREEN_WIDTH//2 - 200, y_offset))
            
            y_offset += 25

    def _get_instruction_line_color(self, line):
        """Determina el color para una línea de instrucciones"""
        if line.endswith(":"):
            return CORAL
        elif line.startswith("  *"):
            return WHITE
        else:
            return LIGHT_BLUE

    def _render_game(self):
        """Renderiza el juego en acción"""
        draw_background(self.screen)
        
        # Dibujar todas las entidades
        self._draw_game_entities()
        
        # Dibujar HUD
        draw_hud(self.screen, self.font, self.player)
        
        # Dibujar información del nivel
        target_score = get_level_target_score(self.level)
        draw_level_info(self.screen, self.font, self.level, 
                       self.player.score, target_score)
        
        # Dibujar mensaje de progreso en la parte inferior
        self._draw_progress_message(target_score)

    def _draw_game_entities(self):
        """Dibuja todas las entidades del juego"""
        # Dibujar perlas
        for pearl in self.pearls:
            draw_pearl(self.screen, pearl.x, pearl.y, pearl.size)
        
        # Dibujar power-ups
        for powerup in self.powerups:
            draw_powerup(self.screen, powerup)
        
        # Dibujar enemigos
        for enemy in self.enemies:
            draw_enemy(self.screen, enemy)
        
        # Dibujar jugador con efecto de invulnerabilidad
        player_color = LIGHT_BLUE if self.player.shield_active > 0 else ORANGE
        
        # Efecto de parpadeo durante invulnerabilidad
        if self.player.invulnerability_timer > 0:
            # Parpadear cada 5 frames
            if (self.player.invulnerability_timer // 5) % 2 == 0:
                draw_fish(self.screen, int(self.player.x), int(self.player.y), 
                         self.player.size, player_color, self.player.direction)
        else:
            draw_fish(self.screen, int(self.player.x), int(self.player.y), 
                     self.player.size, player_color, self.player.direction)
        
        # Dibujar balas
        for bullet in self.player.bullets:
            draw_bullet(self.screen, bullet)

    def _render_game_over(self):
        """Renderiza la pantalla de game over"""
        draw_background(self.screen)
        
        # Fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Título
        title = self.title_font.render("JUEGO TERMINADO", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(title, title_rect)
        
        # Estadísticas
        self._draw_game_over_stats()
        
        # Mensaje motivacional
        self._draw_motivational_message()
        
        # Instrucciones
        continue_text = self.font.render("ESPACIO: Volver al menú  |  ESC: Salir", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, 500))
        self.screen.blit(continue_text, continue_rect)

    def _draw_game_over_stats(self):
        """Dibuja las estadísticas del game over"""
        score_text = self.font.render(f"Puntuación Final: {self.player.score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(score_text, score_rect)
        
        level_text = self.font.render(f"Nivel Alcanzado: {self.level}", True, YELLOW)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, 330))
        self.screen.blit(level_text, level_rect)

    def _draw_motivational_message(self):
        """Dibuja un mensaje motivacional basado en el desempeño"""
        if self.player.score < 100:
            message = "¡Sigue practicando!"
        elif self.player.score < 200:
            message = "¡Buen trabajo!"
        else:
            message = "¡Excelente puntuación!"
        
        message_text = self.font.render(message, True, CORAL)
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH//2, 400))
        self.screen.blit(message_text, message_rect)

    def _draw_progress_message(self, target_score):
        """Dibuja mensaje de progreso en la parte inferior de la pantalla"""
        enemies_count = len(self.enemies)
        points_needed = target_score - self.player.score
        
        # Determinar el mensaje según la situación
        if points_needed <= 0:
            message = f"¡Puntaje alcanzado! ({self.player.score}/{target_score}) - Avanzando de nivel..."
            color = GREEN
        elif enemies_count == 0:
            message = "¡Todos los enemigos derrotados! Avanzando de nivel..."
            color = GREEN
        else:
            # Mostrar ambas opciones claramente
            if enemies_count == 1:
                message = f"Faltan {points_needed} puntos ({self.player.score}/{target_score}) O derrota al último enemigo"
            else:
                message = f"Faltan {points_needed} puntos ({self.player.score}/{target_score}) O derrota los {enemies_count} enemigos"
            color = YELLOW
        
        # Agregar información especial para niveles altos
        if self.level >= 20:
            if "Faltan" in message:
                message += " - ¡ZONA EXPERTA!"
        elif self.level >= 10:
            if "Faltan" in message:
                message += " - ¡Zona Avanzada!"
        
        # Agregar información especial para niveles con saltos grandes
        if self.level <= 10:
            target_next = get_level_target_score(self.level + 1) if self.level < 30 else None
            if target_next and "Faltan" in message:
                increment = target_next - target_score
                message += f" | Próximo nivel: +{increment}"
        
        # Crear superficie con fondo semi-transparente
        text_surface = self.font.render(message, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        
        # Fondo para mejor legibilidad
        bg_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 5, 
                             text_rect.width + 20, text_rect.height + 10)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
        bg_surface.set_alpha(150)
        bg_surface.fill(BLACK)
        
        self.screen.blit(bg_surface, bg_rect)
        self.screen.blit(text_surface, text_rect)

    def _cleanup(self):
        """Limpia recursos y cierra el juego"""
        pygame.quit()
        sys.exit()