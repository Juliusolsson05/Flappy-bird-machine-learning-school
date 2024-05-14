import pygame
import random

# Game variables
GRAVITY = 0.25
BIRD_JUMP = -7.5
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

class Bird(pygame.sprite.Sprite):
    """Class to represent the Bird character in the game."""

    def __init__(self):
        """Initialize the Bird."""
        super().__init__()
        
        # Generate a random dark color for the bird
        self.color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.hitbox = pygame.Surface((30, 30), pygame.SRCALPHA)  # Invisible hitbox
        self.hitbox_rect = self.hitbox.get_rect(center=self.rect.center)
        self.velocity = 0
        self.angle = 0
        self.score = 0
        self.alive = True

    def update(self):
        """Update the Bird's position and angle."""
        if not self.alive:
            return

        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Prevent the bird from going off-screen
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

        # Rotate the bird
        self.angle = min(max(self.velocity * -5, -90), 90)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Update hitbox position
        self.hitbox_rect.center = self.rect.center

        # Update score
        if self.alive:
            self.score += 1

    def jump(self):
        """Make the Bird jump."""
        if self.rect.top > 0:  # Only jump if the bird is not at the ceiling
            self.velocity = BIRD_JUMP

    def draw(self, screen):
        """Draw the Bird."""
        screen.blit(self.image, self.rect.topleft)
        # Uncomment the following line to see the hitbox
        # pygame.draw.rect(screen, (0, 0, 255), self.hitbox_rect, 2)

