import pygame

# Game variables
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_VELOCITY = -5
EDGE_OVERHANG = 8
SCREEN_HEIGHT = 600

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
        self.image.fill((0, 255, 0))
        # Create the edge of the pipe
        self.edge_image = pygame.Surface((PIPE_WIDTH + EDGE_OVERHANG, 20))
        self.edge_image.fill((0, 200, 0))
        if is_top:
            self.rect = self.image.get_rect(midbottom=(x, y))
            self.edge_rect = self.edge_image.get_rect(midbottom=(x, y))
        else:
            self.rect = self.image.get_rect(midtop=(x, y))
            self.edge_rect = self.edge_image.get_rect(midtop=(x, y))
        self.passed = False  # Add this line

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

