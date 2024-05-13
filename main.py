import pygame
import random
import neat
import os
import pickle
from components.bird import Bird
from components.pipe import Pipe
from components.cloud import Cloud

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)  # Sky blue color

# Game variables
PIPE_OFFSET = 100  # Distance from the right edge of the screen to generate pipes
PIPE_GAP = 150  # Gap between the top and bottom pipes

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Font for score display
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)


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


def eval_genomes(genomes, config):
    """Evaluate the genomes and run the simulation for each generation."""
    nets = []
    birds = []
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird())
        genome.fitness = 0

    bird_group = pygame.sprite.Group()
    pipe_group = pygame.sprite.Group()
    bird_group.add(*birds)

    last_pipe = pygame.time.get_ticks()
    pipe_interval = 1500  # Milliseconds between pipe generation

    clouds = [Cloud() for _ in range(10)]

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

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

        for i, bird in enumerate(birds):
            if bird.alive:
                nearest_pipe = None
                for pipe in pipe_group:
                    if pipe.rect.right > bird.rect.left:
                        nearest_pipe = pipe
                        break

                if nearest_pipe is not None:
                    output = nets[i].activate((
                        bird.rect.y / SCREEN_HEIGHT,
                        nearest_pipe.rect.top / SCREEN_HEIGHT,
                        nearest_pipe.rect.bottom / SCREEN_HEIGHT,
                        nearest_pipe.rect.left / SCREEN_WIDTH
                    ))

                    if output[0] > 0.5:
                        bird.jump()

                genomes[i][1].fitness += 0.1

        # Check for collisions
        for bird in birds:
            if bird.alive and (pygame.sprite.spritecollide(bird, pipe_group, False, pygame.sprite.collide_mask) or bird.rect.bottom >= SCREEN_HEIGHT):
                bird.alive = False

        if all(not bird.alive for bird in birds):
            running = False

        # Draw everything
        screen.fill(BLUE)  # Background color for sky
        for cloud in clouds:
            cloud.draw(screen)
        bird_group.draw(screen)
        for pipe in pipe_group:
            pipe.draw(screen)

        # Update display
        pygame.display.flip()

        # Control frame rate
        clock.tick(FPS)


def run(config_file):
    """Run the NEAT algorithm to train a neural network to play Flappy Bird."""
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # Save the winner.
    with open('winner.pkl', 'wb') as f:
        pickle.dump(winner, f)


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

        draw_text(screen, "Flappy Bird", large_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text(screen, "Press P to play", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5)
        draw_text(screen, "Press S to simulate", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text(screen, f"High Score: {high_score}", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
        pygame.display.flip()
        
        waiting = True
        mode = None
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
        return mode
   

   # Show the start menu
    mode = show_menu()

    while True:
        if mode == 'play':
            score = game_loop()
        elif mode == 'simulate':
            config_path = os.path.join(os.path.dirname(__file__), 'config-feedforward.txt')
            run(config_path)
        
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
                    bird_group.empty()
                    pipe_group.empty()
                    clouds = [Cloud() for _ in range(10)]

if __name__ == "__main__":
    main()

