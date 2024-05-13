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

# Game variables
GRAVITY = 0.25
BIRD_JUMP = -7.5
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150
PIPE_VELOCITY = -5
EDGE_OVERHANG = 8
ROTATION_SPEED = 5  # Speed of rotation
MAX_ROTATION = 25  # Maximum angle the bird can tilt upwards or downwards

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


class Bird(pygame.sprite.Sprite):
    """Class to represent the Bird character in the game."""
    
    def __init__(self):
        """Initialize the Bird."""
        super().__init__()
        # self.image = bird_image  # Commented out
        # self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.velocity = 0
        self.angle = 0
    
    def update(self):
        """Update the Bird's position and rotation."""
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        
        # Rotate the bird
        if self.velocity < 0:
            self.angle = max(self.angle - ROTATION_SPEED, -MAX_ROTATION)
        else:
            self.angle = min(self.angle + ROTATION_SPEED, MAX_ROTATION)
        
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # Prevent the bird from going off-screen
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0
    
    def jump(self):
        """Make the Bird jump."""
        self.velocity = BIRD_JUMP
        self.angle = -MAX_ROTATION


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
        # self.image = pygame.transform.flip(pipe_image, False, is_top)  # Commented out
        self.image = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))
        self.image.fill(GREEN)
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
    """Create a pair of pipes (top and bottom) and return them."""
    pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
    top_pipe = Pipe(SCREEN_WIDTH, pipe_height, True)
    bottom_pipe = Pipe(SCREEN_WIDTH, pipe_height + PIPE_GAP, False)
    return top_pipe, bottom_pipe


def main():
    """Main function to run the Flappy Bird game."""
    
    # Create sprite groups
    bird_group = pygame.sprite.Group()
    pipe_group = pygame.sprite.Group()
    
    # Create an instance of Bird and add it to the bird_group
    bird = Bird()
    bird_group.add(bird)
    
    # Initialize variables for game loop
    score = 0
    last_pipe = pygame.time.get_ticks()
    pipe_interval = 1500  # Milliseconds between pipe generation
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
        
        # Check for collisions
        if pygame.sprite.spritecollide(bird, pipe_group, False) or bird.rect.bottom >= SCREEN_HEIGHT:
            running = False
        
        # Update score
        for pipe in pipe_group:
            if pipe.rect.centerx == bird.rect.centerx and pipe.rect.bottom >= SCREEN_HEIGHT:
                score += 1
        
        # Draw everything
        screen.fill(WHITE)  # Background color instead of image
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
    
    pygame.quit()


if __name__ == "__main__":
    main()

