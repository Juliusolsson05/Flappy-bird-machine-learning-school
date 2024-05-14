import pygame
import random
import neat
import os
import pickle
from typing import List, Tuple
from components.bird import Bird
from components.pipe import Pipe
from components.cloud import Cloud

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600

# Colors
WHITE: Tuple[int, int, int] = (255, 255, 255)
BLACK: Tuple[int, int, int] = (0, 0, 0)
BLUE: Tuple[int, int, int] = (135, 206, 235)  # Sky blue color

# Game variables
PIPE_OFFSET: int = 100  # Distance from the right edge of the screen to generate pipes
PIPE_GAP: int = 150  # Gap between the top and bottom pipes

# Set up display
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Clock for controlling frame rate
clock: pygame.time.Clock = pygame.time.Clock()
FPS: int = 60

# Font for score display
font: pygame.font.Font = pygame.font.Font(None, 36)
large_font: pygame.font.Font = pygame.font.Font(None, 72)


def create_pipe() -> Tuple[Pipe, Pipe]:
    """
    Create a pair of pipes (top and bottom) and return them.

    Returns:
        Tuple[Pipe, Pipe]: A tuple containing the top and bottom pipes.
    """
    pipe_height: int = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
    top_pipe: Pipe = Pipe(SCREEN_WIDTH + PIPE_OFFSET, pipe_height, True)
    bottom_pipe: Pipe = Pipe(SCREEN_WIDTH + PIPE_OFFSET, pipe_height + PIPE_GAP, False)
    return top_pipe, bottom_pipe


def draw_text(screen: pygame.Surface, text: str, font: pygame.font.Font, color: Tuple[int, int, int], x: int, y: int) -> None:
    """
    Draw text on the screen.

    Args:
        screen (pygame.Surface): The Pygame screen surface to draw on.
        text (str): The text to draw.
        font (pygame.font.Font): The font to use for the text.
        color (Tuple[int, int, int]): The color of the text.
        x (int): The x-coordinate of the text's center.
        y (int): The y-coordinate of the text's center.
    """
    text_surface: pygame.Surface = font.render(text, True, color)
    text_rect: pygame.Rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


best_score_ever: int = 0


def eval_genomes(genomes: List[Tuple[int, neat.DefaultGenome]], config: neat.Config) -> None:
    """
    Evaluate genomes using the NEAT algorithm.

    This function evaluates a list of genomes by simulating a Flappy Bird game. Each bird is controlled
    by a neural network that is evolved using the NEAT algorithm.

    Args:
        genomes (List[Tuple[int, neat.DefaultGenome]]): A list of tuples, where each tuple contains a genome ID and a genome.
        config (neat.Config): The NEAT configuration.

    Explanation:
        - For each genome, create a neural network and a bird.
        - Simulate the game, updating bird positions and checking for collisions.
        - Use the neural network to decide whether each bird should jump.
        - Assign fitness scores based on survival time and the number of pipes passed.
    """
    global best_score_ever

    nets: List[neat.nn.FeedForwardNetwork] = []
    birds: List[Bird] = []
    ge: List[neat.DefaultGenome] = []

    # Initialize neural networks, birds, and genome fitness
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        bird = Bird()
        bird.jump()  # Initial jump to start the game
        genome.fitness = 0  # Initial fitness
        birds.append(bird)
        ge.append(genome)

    bird_group: pygame.sprite.Group = pygame.sprite.Group(*birds)
    pipe_group: pygame.sprite.Group = pygame.sprite.Group()

    pipe_distance: int = 200  # Distance in pixels between pipes
    last_pipe_x: int = SCREEN_WIDTH + PIPE_OFFSET  # Initial position for the first pipe

    clouds: List[Cloud] = [Cloud() for _ in range(10)]

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Generate new pipes based on distance
        if len(pipe_group) == 0 or (pipe_group.sprites()[-1].rect.x < SCREEN_WIDTH - pipe_distance):
            top_pipe, bottom_pipe = create_pipe()
            pipe_group.add(top_pipe)
            pipe_group.add(bottom_pipe)

        bird_group.update()
        pipe_group.update()
        for cloud in clouds:
            cloud.update()

        for i, bird in enumerate(birds):
            if bird.alive:
                nearest_pipe: Pipe = None
                for pipe in pipe_group:
                    if pipe.rect.right > bird.rect.left:
                        nearest_pipe = pipe
                        break

                if nearest_pipe is not None:
                    inputs: Tuple[float, float, float, float] = (
                        bird.rect.y / SCREEN_HEIGHT,
                        nearest_pipe.rect.top / SCREEN_HEIGHT,
                        nearest_pipe.rect.bottom / SCREEN_HEIGHT,
                        nearest_pipe.rect.left / SCREEN_WIDTH
                    )
                    output: List[float] = nets[i].activate(inputs)
                    if output[0] > 0.5:
                        bird.jump()

                    ge[i].fitness += 0.1  # Reward for staying alive

                    if bird.rect.right > nearest_pipe.rect.left and not nearest_pipe.passed:
                        nearest_pipe.passed = True
                        ge[i].fitness += 5  # Reward for passing a pipe
                        bird.score += 1  # Increment bird's score for passing a pipe

            # Check if bird hits the ground, pipe, or ceiling
            if bird.alive and (
                    pygame.sprite.spritecollide(bird, pipe_group, False, pygame.sprite.collide_mask)
                    or bird.rect.bottom >= SCREEN_HEIGHT
                    or bird.rect.top <= 0  # Check for collision with the ceiling
            ):
                ge[i].fitness -= 1  # Penalize for hitting ground, pipe, or ceiling
                bird.alive = False
                bird_group.remove(bird)  # Remove dead bird from the sprite group

        if all(not bird.alive for bird in birds):
            running = False

        # Draw the game screen
        screen.fill(BLUE)
        for cloud in clouds:
            cloud.draw(screen)
        bird_group.draw(screen)
        for pipe in pipe_group:
            pipe.draw(screen)

        # Display leading bird's score and number of birds left
        leading_bird: Bird = max(birds, key=lambda b: b.score, default=None)
        leading_score: int = leading_bird.score if leading_bird else 0
        birds_left: int = sum(1 for b in birds if b.alive)

        best_score_ever = max(best_score_ever, leading_score)

        draw_text(screen, f"Score: {leading_score}", font, BLACK, 80, 10)
        draw_text(screen, f"Birds Left: {birds_left}", font, BLACK, 80, 50)
        draw_text(screen, f"Best Score: {best_score_ever}", font, BLACK, 80, 90)

        # Update the display and control the frame rate
        pygame.display.flip()
        pygame.time.delay(10)
        clock.tick(FPS)


def run(config_file: str) -> None:
    """
    Run the NEAT algorithm to train a neural network to play Flappy Bird.

    Args:
        config_file (str): Path to the NEAT configuration file.
    """
    config: neat.Config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    # Create the population, which is the top-level object for a NEAT run.
    p: neat.Population = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats: neat.StatisticsReporter = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations.
    winner: neat.DefaultGenome = p.run(eval_genomes, 50)

    # Save the winner.
    with open('winner.pkl', 'wb') as f:
        pickle.dump(winner, f)


def main() -> None:
    """
    Main function to run the Flappy Bird game.

    This function loads the high score, initializes the game state, shows the menu, and handles the game loop.
    """
    
    # Load high score
    try:
        with open('highscore.txt', 'r') as file:
            high_score: int = int(file.read())
    except:
        high_score = 0
    
    def save_high_score(score: int) -> None:
        """
        Save the high score to a file.

        Args:
            score (int): The high score to save.
        """
        with open('highscore.txt', 'w') as file:
            file.write(str(score))
    
    def reset_game_state() -> None:
        """
        Reset the game state for a new game.
        """
        nonlocal bird_group, pipe_group, clouds, bird
        bird_group.empty()
        pipe_group.empty()
        clouds = [Cloud() for _ in range(10)]
        bird = Bird()
        bird_group.add(bird)
    
    # Create sprite groups
    bird_group: pygame.sprite.Group = pygame.sprite.Group()
    pipe_group: pygame.sprite.Group = pygame.sprite.Group()
    
    # Create an instance of Bird and add it to the bird_group
    bird: Bird = Bird()
    bird_group.add(bird)
    
    # Create clouds
    clouds: List[Cloud] = [Cloud() for _ in range(10)]
    
    def game_loop() -> int:
        """
        Run the main game loop.

        Returns:
            int: The final score of the game.
        """
        nonlocal high_score
        score: int = 0
        last_pipe: int = pygame.time.get_ticks()
        pipe_interval: int = 1500  # Milliseconds between pipe generation
        running: bool = True
        
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
            score_text: pygame.Surface = font.render(f"Score: {score}", True, BLACK)
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


    
    def show_menu() -> str:
        """
        Show the start or play-again menu.

        Returns:
            str: The selected game mode ('play' or 'simulate').
        """
        screen.fill(BLUE)
        for cloud in clouds:
            cloud.draw(screen)
        bird_group.draw(screen)
        for pipe in pipe_group:
            pipe.draw(screen)

        # Create a semi-transparent black overlay
        overlay: pygame.Surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)  # Transparency level (0-255)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        draw_text(screen, "Flappy Bird", large_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text(screen, "Press P to play", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5)
        draw_text(screen, "Press S to simulate", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text(screen, f"High Score: {high_score}", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
        pygame.display.flip()
        
        waiting: bool = True
        mode: str = None
        while waiting:
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        mode = 'play'
                        waiting = False
                    if event.key == pygame.K_s:
                        mode = 'simulate'
                        waiting = False
        return mode

    # Show the start menu
    mode: str = show_menu()

    while True:
        if mode == 'play':
            score: int = game_loop()
            reset_game_state()  # Reset game state for play again
        elif mode == 'simulate':
            config_path: str = os.path.join(os.path.dirname(__file__), 'config-feedforward.txt')
            run(config_path)
            reset_game_state()  # Reset game state after simulation

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

        if mode == 'play':
            draw_text(screen, "Game Over", large_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            draw_text(screen, f"Score: {score}", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            draw_text(screen, f"High Score: {high_score}", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
        draw_text(screen, "Press P to play again", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.2)
        draw_text(screen, "Press S to simulate", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.1)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        mode = 'play'
                        waiting = False
                    if event.key == pygame.K_s:
                        mode = 'simulate'
                        waiting = False
                    # Reset game state
                    reset_game_state()

if __name__ == "__main__":
    main()

