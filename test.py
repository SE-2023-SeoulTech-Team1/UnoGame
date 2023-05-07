import pygame

# Initialize Pygame
pygame.init()

# Set the window size
size = (400, 400)
screen = pygame.display.set_mode(size)

# Load the image
image = pygame.image.load("./assets/cards/red1.png")

# Set the initial position of the image
x = 0
y = 0

# Set the target position of the image
target_x = 200
target_y = 200

# Set the speed of the animation
speed = 1

# Start the loop
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Calculate the distance between the current position and the target position
    distance_x = target_x - x
    distance_y = target_y - y

    # Calculate the direction of the movement
    direction_x = 1 if distance_x > 0 else -1
    direction_y = 1 if distance_y > 0 else -1

    # Calculate the amount to move in each direction
    move_x = speed * direction_x
    move_y = speed * direction_y

    # Update the position of the image
    x += move_x
    y += move_y

    # Draw the image on the screen
    screen.blit(image, (x, y))

    # Update the screen
    pygame.display.flip()

    # Check if the target position has been reached
    if x == target_x and y == target_y:
        done = True

# Wait for the user to close the window
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

# Quit Pygame
pygame.quit()
