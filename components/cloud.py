import pygame
import random

# Game variables
SCREEN_WIDTH = 800
CLOUD_SPEED = -1  # Speed at which clouds move to the left
WHITE = (255, 255, 255)


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

