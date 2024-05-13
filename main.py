import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 200, 0)
BLUE = (135, 206, 235)  # Sky blue color

# Game variables
GRAVITY = 0.25
BIRD_JUMP = -7.5
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150
PIPE_VELOCITY = -5
EDGE_OVERHANG = 8
PIPE_OFFSET = 100  # Distance from the right edge of the screen to generate pipes
CLOUD_SPEED = -1  # Speed at which clouds move to the left

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Load images (commented out)
# bird_image = pygame.image.load('bird.png').convert_alpha()
# background_image = pygame.image.load('background.png').convert()
# pipe_image = pygame.image.load('pipe.png').convert_alpha()

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Font for score display
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

class Cloud:
    """Class to represent a cloud in the sky."""
    
    def __init__(self):
        """Initialize the Cloud."""
        self.x = random.randint(0, SCREEN_WIDTH * 2)  # Scattered across twice the screen width
        self.y = random.randint(50, 200)
        self.speed = CLOUD_SPEED
        self.size = random.randint(20, 40)  # Random size for variety
    
    def update(self):
        """Update the Cloud's position."""
        self.x += self.speed
        if self.x < -self.size * 2:
            self.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH * 2)
            self.y = random.randint(50, 200)
    
    def draw(self, screen):
        """Draw the Cloud."""
        # Cloud is made of multiple circles with varying sizes and positions
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size)
        pygame.draw.circle(screen, WHITE, (self.x + int(self.size * 0.6), self.y + int(self.size * 0.2)), int(self.size * 0.8))
        pygame.draw.circle(screen, WHITE, (self.x - int(self.size * 0.6), self.y + int(self.size * 0.2)), int(self.size * 0.8))
        pygame.draw.circle(screen, WHITE, (self.x + int(self.size * 0.4), self.y + int(self.size * 0.5)), int(self.size * 0.6))
        pygame.draw.circle(screen, WHITE, (self.x - int(self.size * 0.4), self.y + int(self.size * 0.5)), int(self.size * 0.6))
        pygame.draw.circle(screen, WHITE, (self.x, self.y + int(self.size * 0.6)), int(self.size * 0.7))


class Bird(pygame.sprite.Sprite):
    """Class to represent the Bird character in the game."""
    
    def __init__(self):
        """Initialize the Bird."""
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.image.fill(RED)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.hitbox = pygame.Surface((30, 30), pygame.SRCALPHA)  # Invisible hitbox
        self.hitbox_rect = self.hitbox.get_rect(center=self.rect.center)
        self.velocity = 0
        self.angle = 0
    
    def update(self):
        """Update the Bird's position and angle."""
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        
        # Prevent the bird from going off-screen
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0
        
        # Rotate the bird
        self.angle = min(max(self.velocity * -5, -90), 90)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # Update hitbox position
        self.hitbox_rect.center = self.rect.center
    
    def jump(self):
        """Make the Bird jump."""
        self.velocity = BIRD_JUMP
    
    def draw(self, screen):
        """Draw the Bird."""
        screen.blit(self.image, self.rect.topleft)
        # Uncomment the following line to see the hitbox
        # pygame.draw.rect(screen, (0, 0, 255), self.hitbox_rect, 2)


class Pipe(pygame.sprite.Sprite):
    """Class to represent a Pipe in the game."""
    
    def __init__(self, x, y, is_top):
        """
        Initialize the Pipe.
        
        Args:
            x (int): The x-coordinate of the pipe.
            y (int): The y-coordinate of the pipe.
            is_top (bool): Whether the pipe is the top pipe.
        """
        super().__init__()
        # Create the pipe surface
        self.image = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))
        self.image.fill(GREEN)
        # Create the edge of the pipe
        self.edge_image = pygame.Surface((PIPE_WIDTH + EDGE_OVERHANG, 20))
        self.edge_image.fill(DARK_GREEN)
        if is_top:
            self.rect = self.image.get_rect(midbottom=(x, y))
            self.edge_rect = self.edge_image.get_rect(midbottom=(x, y))
        else:
            self.rect = self.image.get_rect(midtop=(x, y))
            self.edge_rect = self.edge_image.get_rect(midtop=(x, y))
    
    def update(self):
        """Update the Pipe's position."""
        self.rect.x += PIPE_VELOCITY
        self.edge_rect.x += PIPE_VELOCITY
        if self.rect.right < 0:
            self.kill()
    
    def draw(self, screen):
        """Draw the Pipe and its edge."""
        screen.blit(self.image, self.rect)
        screen.blit(self.edge_image, self.edge_rect)


def create_pipe():
    """Create a pair of pipes (top and bottom) and return them.
    
    Returns:
        tuple: A tuple containing the top and bottom pipes.
    """
    pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
    top_pipe = Pipe(SCREEN_WIDTH + PIPE_OFFSET, pipe_height, True)
    bottom_pipe = Pipe(SCREEN_WIDTH + PIPE_OFFSET, pipe_height + PIPE_GAP, False)
    return top_pipe, bottom_pipe


def draw_text(screen, text, font, color, x, y):
    """Draw text on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def main():
    """Main function to run the Flappy Bird game."""
    
    # Load high score
    try:
        with open('highscore.txt', 'r') as file:
            high_score = int(file.read())
    except:
        high_score = 0
    
    def save_high_score(score):
        """Save the high score to a file."""
        with open('highscore.txt', 'w') as file:
            file.write(str(score))
    
    # Create sprite groups
    bird_group = pygame.sprite.Group()
    pipe_group = pygame.sprite.Group()
    
    # Create an instance of Bird and add it to the bird_group
    bird = Bird()
    bird_group.add(bird)
    
    # Create clouds
    clouds = [Cloud() for _ in range(10)]
    
    def game_loop():
        """Run the main game loop."""
        nonlocal high_score
        score = 0
        last_pipe = pygame.time.get_ticks()
        pipe_interval = 1500  # Milliseconds between pipe generation
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.jump()
            
            # Add new pipes at regular intervals
            if pygame.time.get_ticks() - last_pipe > pipe_interval:
                last_pipe = pygame.time.get_ticks()
                top_pipe, bottom_pipe = create_pipe()
                pipe_group.add(top_pipe)
                pipe_group.add(bottom_pipe)
            
            # Update game state
            bird_group.update()
            pipe_group.update()
            for cloud in clouds:
                cloud.update()
            
            # Check for collisions
            if pygame.sprite.spritecollide(bird, pipe_group, False, pygame.sprite.collide_mask) or bird.rect.bottom >= SCREEN_HEIGHT:
                running = False
            
            # Update score
            for pipe in pipe_group:
                if pipe.rect.centerx == bird.rect.centerx and pipe.rect.bottom >= SCREEN_HEIGHT:
                    score += 1
            
            # Draw everything
            screen.fill(BLUE)  # Background color for sky
            for cloud in clouds:
                cloud.draw(screen)
            bird_group.draw(screen)
            for pipe in pipe_group:
                pipe.draw(screen)
            
            # Display the score
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))
            
            # Update display
            pygame.display.flip()
            
            # Control frame rate
            clock.tick(FPS)
        
        # Update high score
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        
        return score
    
    def show_menu():
        """Show the start or play-again menu."""
        screen.fill(BLUE)
        for cloud in clouds:
            cloud.draw(screen)
        bird_group.draw(screen)
        for pipe in pipe_group:
            pipe.draw(screen)

        # Create a semi-transparent black overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)  # Transparency level (0-255)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        draw_text(screen, "Flappy Bird", large_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text(screen, "Press SPACE to start", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text(screen, f"High Score: {high_score}", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
    
    # Show the start menu
    show_menu()
    
    while True:
        score = game_loop()
        screen.fill(BLUE)
        for cloud in clouds:
            cloud.draw(screen)
        bird_group.draw(screen)
        for pipe in pipe_group:
            pipe.draw(screen)

        # Create a semi-transparent black overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)  # Transparency level (0-255)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        draw_text(screen, "Game Over", large_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text(screen, f"Score: {score}", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text(screen, f"High Score: {high_score}", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
        draw_text(screen, "Press SPACE to play again", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.2)
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
                    # Reset game state
                    bird = Bird()
                    bird_group.empty()
                    bird_group.add(bird)
                    pipe_group.empty()
                    clouds = [Cloud() for _ in range(10)]
    
if __name__ == "__main__":
    main()

