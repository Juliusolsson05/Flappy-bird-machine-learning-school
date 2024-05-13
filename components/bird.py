import pygame
import numpy as np
from components.neural_network import NeuralNetwork

# Game variables
GRAVITY = 0.25
BIRD_JUMP = -7.5
SCREEN_HEIGHT = 600


class Bird(pygame.sprite.Sprite):
    """Class to represent the Bird character in the game."""

    def __init__(self, nn=None):
        """Initialize the Bird."""
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.image.fill((255, 0, 0))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.hitbox = pygame.Surface((30, 30), pygame.SRCALPHA)  # Invisible hitbox
        self.hitbox_rect = self.hitbox.get_rect(center=self.rect.center)
        self.velocity = 0
        self.angle = 0
        self.score = 0
        self.alive = True
        self.nn = nn or NeuralNetwork(4, 8, 1)

    def update(self):
        """Update the Bird's position and angle."""
        if not self.alive:
            return

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

    def think(self, pipes):
        """Make the Bird decide whether to jump."""
        if not pipes:
            return

        # Find the nearest pipe
        nearest_pipe = None
        for pipe in pipes:
            if pipe.rect.right > self.rect.left:
                nearest_pipe = pipe
                break

        if not nearest_pipe:
            return

        # Prepare inputs for the neural network
        inputs = [
            self.rect.y / SCREEN_HEIGHT,
            nearest_pipe.rect.top / SCREEN_HEIGHT,
            nearest_pipe.rect.bottom / SCREEN_HEIGHT,
            nearest_pipe.rect.left / SCREEN_WIDTH,
        ]

        output = self.nn.forward(inputs)[0]
        if output > 0.5:
            self.jump()

    def draw(self, screen):
        """Draw the Bird."""
        screen.blit(self.image, self.rect.topleft)
        # Uncomment the following line to see the hitbox
        # pygame.draw.rect(screen, (0, 0, 255), self.hitbox_rect, 2)

