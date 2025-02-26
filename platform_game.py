"""
Platform Games
-------------
A simple 2D platform game built with Pygame Zero.

Features:
- Player movement and jumping mechanics
- Enemy AI with patrolling behavior
- Lives system with heart display
- Score system
- Win condition: Reach 100% progress
- Menu system with music and sound controls

Author: Nurbeniz Yağlı
Version: 1.0.0
"""

import math
import random
import pgzrun

# Game Constants
TITLE = "Platform Games"
WIDTH = 740
HEIGHT = 460

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game States
MENU = 0
PLAYING = 1
WIN = 2
GAME_OVER = 3

# Physics Constants
GRAVITY = 0.5
JUMP_SPEED = -10
MOVE_SPEED = 5
PLATFORM_TOP = HEIGHT - 120
GROUND_HEIGHT = HEIGHT - 95

# Visual Settings
PLAYER_SCALE = 3.5
ENEMY_SCALE = 3.0
HEART_SCALE = 2.0
HEART_SPACING = 40
ANIMATION_SPEED = 8
WIN_SCORE = 1000

# Button Settings
BUTTON_SCALE = 2.0
CLOSE_BUTTON_SCALE = 0.15

# Enemy Respawn Time (frames)
ENEMY_RESPAWN_TIME = 180

class Character:
    """Base class for game characters with common properties and methods."""
    def __init__(self, image, x, y, scale):
        self.actor = Actor(image, anchor=('center', 'bottom'))
        self.actor.x = x
        self.actor.y = y
        self.actor.scale = scale
        self.direction = 1
        self.frame = 0
        self.alive = True
        self.velocity_y = 0

    def update_animation(self):
        """Update character animation frame."""
        self.frame = (self.frame + 1) % (2 * ANIMATION_SPEED)

    def apply_gravity(self):
        """Apply gravity to the character."""
        self.velocity_y += GRAVITY
        self.actor.y += self.velocity_y
        
        if self.actor.y > PLATFORM_TOP:
            self.actor.y = PLATFORM_TOP
            self.velocity_y = 0

class Player(Character):
    """Player character class with specific player mechanics."""
    def __init__(self, x, y):
        super().__init__('character', x, y, PLAYER_SCALE)
        self.score = 0
        self.progress = 0
        self.lives = 3
        self.invulnerable = 0

    def move(self, dx):
        """Handle player movement."""
        self.actor.x += dx * MOVE_SPEED
        self.direction = 1 if dx > 0 else -1 if dx < 0 else self.direction
        
        # Screen bounds
        if self.actor.x < 0:
            self.actor.x = 0
        elif self.actor.x > WIDTH:
            self.actor.x = WIDTH

    def jump(self):
        """Handle player jumping."""
        if self.actor.y == PLATFORM_TOP:
            self.velocity_y = JUMP_SPEED
            if sound_on:
                sounds.jump.play()

    def update(self):
        """Update player state."""
        # Movement
        if keyboard.left:
            self.move(-1)
        if keyboard.right:
            self.move(1)
        if keyboard.space:
            self.jump()

        # Physics and animation
        self.apply_gravity()
        self.update_animation()
        
        # Invulnerability frames
        if self.invulnerable > 0:
            self.invulnerable -= 1

    def check_enemy_collision(self, enemy):
        """Check collision with enemy and handle the interaction."""
        if not enemy.alive or self.invulnerable > 0:
            return

        # Calculate collision bounds
        player_bottom = self.actor.y
        enemy_top = enemy.actor.y - 30  # Adjust collision height
        
        # Check if player is above the enemy
        if (abs(self.actor.x - enemy.actor.x) < 30 and 
            self.velocity_y > 0 and 
            player_bottom < enemy_top + 20):
            
            # Successful jump on enemy
            self.score += 50  # Puan kazanma
            self.progress += 10  # Her düşman için %10 ilerleme
            enemy.defeat()
            self.velocity_y = JUMP_SPEED * 0.7  # Bounce off enemy
            if sound_on:
                sounds.jump.play()
        else:
            # Side collision - player takes damage
            if abs(self.actor.x - enemy.actor.x) < 30 and abs(self.actor.y - enemy.actor.y) < 30:
                self.take_damage()
                if self.lives <= 0:  # Eğer canlar bittiyse hemen game over
                    global game_state
                    game_state = GAME_OVER

    def take_damage(self):
        """Handle player taking damage."""
        global game_state  # global değişkeni kullanacağımızı belirtiyoruz
        
        if self.invulnerable == 0:
            self.lives -= 1
            self.invulnerable = 60
            if sound_on:
                sounds.hurt.play()
            
            # Can sıfırlanınca game over
            if self.lives <= 0:
                self.alive = False
                game_state = GAME_OVER
                if sound_on:
                    sounds.hurt.play()

class Enemy(Character):
    """Enemy character class with AI behavior."""
    def __init__(self, enemy_type, x, y, zone):
        image = 'snake' if enemy_type == "snake" else 'mushroom_1'
        super().__init__(image, x, y, ENEMY_SCALE)
        self.type = enemy_type
        self.zone = zone
        self.respawn_timer = 0

    def update(self):
        """Update enemy state and AI behavior."""
        if not self.alive:
            self.respawn_timer += 1
            if self.respawn_timer >= ENEMY_RESPAWN_TIME:
                self.respawn()
        else:
            # Move within zone
            self.actor.x += MOVE_SPEED * self.direction
            
            # Check zone boundaries
            zone_left = WIDTH * self.zone[0]
            zone_right = WIDTH * self.zone[1]
            
            if self.actor.x <= zone_left or self.actor.x >= zone_right:
                self.direction *= -1
            
            self.update_animation()

    def defeat(self):
        """Handle enemy defeat."""
        self.alive = False
        self.respawn_timer = 0

    def respawn(self):
        """Handle enemy respawn."""
        self.alive = True
        self.respawn_timer = 0
        self.actor.x = WIDTH * (self.zone[0] + self.zone[1]) / 2

# Game objects and states
player = None
enemies = []
game_state = MENU
music_on = True
sound_on = True
close_button = None
background_music = None

def init():
    """Initialize game objects and variables."""
    global player, enemies, game_state, close_button, background_music
    
    # Start background music
    if music_on and not background_music:
        music.play('the_valley')
        music.set_volume(0.5)
    
    # Create player
    player = Player(WIDTH // 4, PLATFORM_TOP)
    
    # Create enemies with their own zones
    enemies = []
    zones = [(0.3, 0.5), (0.5, 0.7), (0.7, 0.9)]
    for i in range(3):
        enemy = Enemy("snake" if i % 2 == 0 else "mushroom", 
                     WIDTH * (zones[i][0] + zones[i][1]) / 2,
                     PLATFORM_TOP,
                     zones[i])
        enemies.append(enemy)
    
    # Create close button
    close_button = Actor('close', topright=(WIDTH-10, 10))
    close_button.scale = CLOSE_BUTTON_SCALE

def draw_menu_button(text, y, selected=False):
    """Draw a menu button with text."""
    button_width = 200
    button_height = 40
    button_x = WIDTH // 2 - button_width // 2
    button_color = (90, 90, 180) if selected else (70, 70, 150)
    
    # Draw button background
    screen.draw.filled_rect(Rect((button_x, y), (button_width, button_height)), button_color)
    screen.draw.rect(Rect((button_x, y), (button_width, button_height)), (255, 255, 255))
    
    # Draw button text
    screen.draw.text(text, center=(WIDTH//2, y + button_height//2), 
                    color=WHITE, fontsize=24)
    
    return Rect((button_x, y), (button_width, button_height))

def on_mouse_down(pos):
    """Handle mouse click events."""
    global game_state, music_on, sound_on, background_music
    
    if game_state == MENU:
        # Start Game button
        if Rect((WIDTH//2 - 100, HEIGHT//2 - 50), (200, 40)).collidepoint(pos):
            game_state = PLAYING
            init()
        # Music button
        elif Rect((WIDTH//2 - 100, HEIGHT//2 + 10), (200, 40)).collidepoint(pos):
            music_on = not music_on
            if music_on:
                music.play('the_valley')
                music.set_volume(0.5)
            else:
                music.stop()
        # Sound button
        elif Rect((WIDTH//2 - 100, HEIGHT//2 + 70), (200, 40)).collidepoint(pos):
            sound_on = not sound_on
        # Exit button
        elif Rect((WIDTH//2 - 100, HEIGHT//2 + 130), (200, 40)).collidepoint(pos):
            exit()
    elif game_state == PLAYING:
        # Close button
        if close_button.collidepoint(pos):
            game_state = MENU
    elif game_state == WIN:
        # Close button for win screen
        if close_button.collidepoint(pos):
            game_state = MENU

def update():
    """Update game state each frame."""
    global game_state, player
    
    if game_state == PLAYING and player.alive:
        # Update player
        player.update()
        
        # Update enemies and check collisions
        for enemy in enemies:
            enemy.update()
            player.check_enemy_collision(enemy)
        
        # Check win condition
        if player.progress >= 100:
            game_state = WIN

    elif (game_state == WIN or game_state == GAME_OVER) and keyboard.space:
        game_state = PLAYING
        init()

def draw():
    """Draw game elements each frame."""
    screen.clear()
    
    if game_state == MENU:
        screen.blit('background', (0, 0))
        screen.draw.text("Platform Games", center=(WIDTH//2, HEIGHT//2 - 150), 
                        color=WHITE, fontsize=64, shadow=(2, 2))
        
        draw_menu_button("Start Game", HEIGHT//2 - 50)
        draw_menu_button(f"Music: {'On' if music_on else 'Off'}", HEIGHT//2 + 10)
        draw_menu_button(f"Sound: {'On' if sound_on else 'Off'}", HEIGHT//2 + 70)
        draw_menu_button("Exit", HEIGHT//2 + 130)
        
    elif game_state == PLAYING:
        screen.blit('background', (0, 0))
        
        if player.invulnerable == 0 or player.invulnerable % 10 < 5:
            walk_frame = player.frame // ANIMATION_SPEED
            if player.direction > 0:
                player.actor.image = 'character' if walk_frame % 2 == 0 else 'character_2'
            else:
                player.actor.image = 'character_left' if walk_frame % 2 == 0 else 'character_left2'
            player.actor.draw()
        
        for enemy in enemies:
            if not enemy.alive:
                continue
                
            if enemy.type == "snake":
                enemy.actor.image = 'snake' if enemy.direction > 0 else 'snake_2'
            else:
                mushroom_frame = (enemy.frame // ANIMATION_SPEED) % 2
                enemy.actor.image = 'mushroom_1' if mushroom_frame == 0 else 'mushroom_2'
            enemy.actor.draw()
        
        for i in range(player.lives):
            heart = Actor('heart', anchor=('center', 'center'))
            heart.x = WIDTH - (30 + (HEART_SPACING * i))
            heart.y = 70
            heart.scale = HEART_SCALE
            heart.draw()
        
        screen.draw.text(f"Score: {player.score}", (10, 10), 
                       color=WHITE, fontsize=32)
        
        screen.draw.text(f"Progress: {player.progress}%", (10, 50), 
                       color=WHITE, fontsize=24)
        
        close_button.draw()
    
    elif game_state == WIN:
        screen.blit('background', (0, 0))
        screen.draw.text("TEBRİKLER!", center=(WIDTH//2, HEIGHT//2 - 60), 
                        color=(255, 215, 0), fontsize=64, shadow=(4, 4))  # Altın rengi
        screen.draw.text(f"Toplam Puan: {player.score}", center=(WIDTH//2, HEIGHT//2), 
                        color=WHITE, fontsize=32, shadow=(2, 2))
        screen.draw.text("Menüye dönmek için çarpıya tıklayın", center=(WIDTH//2, HEIGHT//2 + 40), 
                        color=WHITE, fontsize=24)
        
        close_button.draw()
        
    elif game_state == GAME_OVER:
        screen.blit('background', (0, 0))
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), color=WHITE, fontsize=64)
        screen.draw.text("Press SPACE to try again", center=(WIDTH//2, HEIGHT//2 + 50), color=WHITE, fontsize=32)

init()
pgzrun.go()
