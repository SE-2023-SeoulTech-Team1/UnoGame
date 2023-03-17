import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Set the window dimensions
WINDOW_SIZE = (800, 600)

# Set up the screen
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Drop Down Menu")

# Set up fonts
menu_font = pygame.font.SysFont(None, 50)
option_font = pygame.font.SysFont(None, 30)

# Set up menu options
menu_options = ["Play", "Options", "Exit"]

# Set up the menu rect
menu_rect = pygame.Rect(50, 50, 200, 50)

# Set up the options rect
options_rect = pygame.Rect(menu_rect.x, menu_rect.y + menu_rect.height, menu_rect.width, 0)

# Set up the current option index
current_option = None

# Set up the game loop
done = False

while not done:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if menu_rect.collidepoint(mouse_pos):
                # Toggle the options
                if options_rect.height == 0:
                    options_rect.height = len(menu_options) * 30
                else:
                    options_rect.height = 0
                # Determine which option was selected
                option_index = (mouse_pos[1] - options_rect.y) // 30
                if option_index < len(menu_options):
                    current_option = menu_options[option_index]

    # Clear the screen
    screen.fill(WHITE)

    # Draw the menu
    pygame.draw.rect(screen, BLACK, menu_rect, 2)
    menu_text = menu_font.render("Menu", True, BLACK)
