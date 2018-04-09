import pygame
from random import randint

# --- Globals ---
# Colors
BLACK = (135,206,250)
WHITE = (255, 255, 255)
RED = (100,149,237)
PURPLE = (100,149,237)

score = 0
clock_speed = 5


# Set the width and height of each snake segment
segment_width = 15
segment_height = 15

# Margin between each segment
segment_margin = 3




screen_width = 40
screen_height = 25

screen_width_px = (segment_width+segment_margin)*screen_width + segment_margin
screen_height_px = (segment_height+segment_margin)*screen_height + segment_margin



# Set initial speed
x_change = segment_width + segment_margin
y_change = 0


active_pellet = None
last_key = pygame.K_RIGHT


def grid_to_px(x,y):
    if x is not 0:
        x = (segment_width+segment_margin)*x + segment_margin
    else:
        x = segment_margin
    if y is not 0:
        y = (segment_height+segment_margin)*y + segment_margin
    else:
        y = segment_margin

    return x,y


def random_block():
    x = randint(0, screen_width_px)
    x = x-x%(segment_width+segment_margin)+segment_margin
    y = randint(0, screen_height_px)
    y = y - y%(segment_height+segment_margin)+segment_margin
    return x,y

def gen_pellet():
    x,y = random_block()

    a = []
    for s in snake_segments:
        a.append((s.rect.x,s.rect.y))
    #
    # while (x,y) in a:
    #     x,y = random_block()
    pellet = Segment(x,y)
    pellet_sprite = Segment(x, y, PURPLE)
    allspriteslist.add(pellet_sprite)

    return pellet,pellet_sprite

def del_pellet(pellet):

    allspriteslist.remove(pellet)



def in_bounds(segment):
    if segment.rect.x < 0 or segment.rect.x > screen_width_px-1 or segment.rect.y < 0 or segment.rect.y > screen_height_px-1:
        return False
    return True


class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """

    # -- Methods
    # Constructor function
    def __init__(self, x, y, color = WHITE):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([screen_width_px, screen_height_px])

# Set the title of the window
pygame.display.set_caption('CMPSC 360 Snake Game')

allspriteslist = pygame.sprite.Group()

# Create an initial snake
snake_segments = []
for i in range(8):
    x = screen_width//2 - i
    y = screen_height//2
    x,y = grid_to_px(x,y)

    segment = Segment(x, y)
    snake_segments.append(segment)
    allspriteslist.add(segment)

pellet,active_pellet = gen_pellet()
hasPellet = True
pop = True


clock = pygame.time.Clock()
done = False

while not done:
    a = []
    for snake_segment in snake_segments:
        a.append((snake_segment.rect.x,snake_segment.rect.y))

    b = (pellet.rect.x,pellet.rect.y)




    if b in a:
        clock.tick(40/clock_speed)
        clock_speed += .5
        score += 10
        pop = False
        del_pellet(active_pellet)
        pellet,active_pellet = gen_pellet()



    if list(set(a)).__len__() is not a.__len__() or not in_bounds(snake_segments[0]):


        snake_segments = snake_segments[::-1]
        while snake_segments.__len__() > 0:

            seg = snake_segments.pop()
            allspriteslist.remove(seg)
            seg.image.fill(RED)
            clock.tick(5)
            screen.fill(BLACK)
            allspriteslist.add(seg)
            allspriteslist.draw(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break


        break



    if len(a) is screen_height*screen_width:
        print("You Win!!")
        break


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and last_key is not pygame.K_RIGHT:
                x_change = (segment_width + segment_margin) * -1
                y_change = 0
                last_key = pygame.K_LEFT

            if event.key == pygame.K_RIGHT and last_key is not pygame.K_LEFT:
                x_change = (segment_width + segment_margin)
                y_change = 0
                last_key = pygame.K_RIGHT

            if event.key == pygame.K_UP and last_key is not pygame.K_DOWN:
                x_change = 0
                y_change = (segment_height + segment_margin) * -1
                last_key = pygame.K_UP

            if event.key == pygame.K_DOWN and last_key is not pygame.K_UP:
                x_change = 0
                y_change = (segment_height + segment_margin)
                last_key = pygame.K_DOWN

    if pop:
        # Get rid of last segment of the snake
        # .pop() command removes last item in list
        old_segment = snake_segments.pop()
        allspriteslist.remove(old_segment)
    else:
        pop = True

    # Figure out where new segment will be
    x = snake_segments[0].rect.x + x_change
    y = snake_segments[0].rect.y + y_change
    segment = Segment(x, y)

    # Insert new segment into the list
    snake_segments.insert(0, segment)
    allspriteslist.add(segment)

    # -- Draw everything
    # Clear screen
    screen.fill(BLACK)

    allspriteslist.draw(screen)

    message = str(score)
    font = pygame.font.SysFont('bnmachine', int(2*segment_height))
    text = font.render(message, 1, RED)
    s = snake_segments[0].rect

    if last_key is pygame.K_RIGHT:
        screen.blit(text, (s.x-segment_width,s.y+segment_height))
    if last_key is pygame.K_LEFT:
        screen.blit(text, (s.x-segment_width,s.y+segment_height))
    if last_key is pygame.K_UP:
        screen.blit(text, (s.x+int(segment_width)+segment_margin,s.y+segment_height))
    if last_key is pygame.K_DOWN:
        screen.blit(text, (s.x-segment_width,s.y+segment_height))



    # Flip screen
    pygame.display.flip()



    # Pause
    clock.tick(clock_speed)

pygame.quit()