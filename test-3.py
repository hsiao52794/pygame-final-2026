# Collect Blocks
# Author: Alex Hsiao
# Date: Jan 15, 2026

import random
import pygame

# COLOURS - (R, G, B)
# CONSTANTS ALL HAVE CAPS FOR THEIR NAMES
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
GREY  = (128, 128, 128)
BROWN = (153,  76,   0)

# CONSTANTS
WIDTH = 1920
centerx = int(WIDTH / 2)
HEIGHT = 1080
centery = int(HEIGHT / 2)
SIZE = (WIDTH, HEIGHT)
map_size = 2000

# Creating the Screen
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Collect Blocks")
pygame.mouse.set_visible(True)

# Create a sprite group
all_sprites_group = pygame.sprite.Group()
block_sprites_group = pygame.sprite.Group()
push_block_sprites_group = pygame.sprite.Group()
enemy_sprites_group = pygame.sprite.Group()
white_map_sprites_group = pygame.sprite.Group()
black_map_sprites_group = pygame.sprite.Group()
map_sprites_group = pygame.sprite.Group()
border_sprites_group = pygame.sprite.Group()
tree_sprites_group = pygame.sprite.Group()
env_sprites_group = pygame.sprite.Group()



class Block(pygame.sprite.Sprite):
    def __init__(self):
        """A blue block"""
        super().__init__()

        self.image = pygame.Surface((20, 15))
        # change the colour of our image to blue
        self.image.fill(BLUE)

        # rect represents the hitbox of our sprite
        # the hitbox gives information about:
        #    - location of the sprite x, y
        #    - the size of the sprite width, height
        self.rect = self.image.get_rect()
        # change the location of our hitbox
        self.rect.centerx = 100
        self.rect.centery = 100


        self.point_value = 1

    def level_up(self, val: int):
        """Incr point value"""
        self.point_value *= val

class Mario(pygame.sprite.Sprite):
    def __init__(self):
        """Player sprite"""
        super().__init__()

        # Two copies of image: right-facing and left-facing
        self.image_right = pygame.image.load("assets/mario-snes.png")
        self.image_right = pygame.transform.scale_by(self.image_right, 0.5)
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right

        self.rect = self.image.get_rect()

        # Keep track of last x-coord
        self.last_x = 0

        # Mario's "Life"
        self.health = 100
        self.points = 0

    def decrease_health(self, mag: int) -> int:
        """Decrease player's health by magnitude.
        Returns:
            current health that Mario has after the change
        """
        self.health -= mag
        return self.health

    def increase_score(self, amt: int):
        self.points += amt

    def show_health_percentage(self) -> int:
        return self.health / 100

    def update(self):
        """Have Mario follow the mouse.
        Set the "right" Mario image based on where he's facing."""

        # Mario faces right if and only if the previous x
        # is less than the current x
        """
        if self.last_x < self.rect.x:
            self.image = self.image_right
        elif self.last_x > self.rect.x:
            self.image = self.image_left
        """

        # Update the last_x
        self.last_x = self.rect.x

class Circle(pygame.sprite.Sprite):
    def __init__(self):
        """Player sprite"""
        super().__init__()

        # Two copies of image: right-facing and left-facing
        self.image = pygame.drawcircle(pygame.Surface((50, 50)), WHITE, (25, 25), 25)
        self.image = self.image
        self.rect = self.image.get_rect()

        # Keep track of last x-coord
        self.last_x = 0

    def update(self):
        # Update the last_x
        self.last_x = self.rect.x

class Tree_bottom(pygame.sprite.Sprite):
    def __init__(self):
        """map sprite"""
        super().__init__()

        self.image = pygame.Surface((75, 75))
        # change the colour of our image to blue
        self.image.fill(BROWN)

        self.rect = self.image.get_rect()
class Tree(pygame.sprite.Sprite):
    def __init__(self):
        """map sprite"""
        super().__init__()

        self.image = pygame.Surface((75, 75))
        # change the colour of our image to blue
        self.image.fill(BROWN)

        self.rect = self.image.get_rect()
class Leaf(pygame.sprite.Sprite):
    def __init__(self):
        """map sprite"""
        super().__init__()

        self.image = pygame.Surface((600, 600))
        # change the colour of our image to blue
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

class Map(pygame.sprite.Sprite):
    def __init__(self):
        """map sprite"""
        super().__init__()

        self.image = pygame.Surface((200, 150))
        # change the colour of our image to blue
        self.image.fill(GREY)

        self.rect = self.image.get_rect()

class Borderx(pygame.sprite.Sprite):
    def __init__(self):
        """map sprite"""
        super().__init__()

        self.image = pygame.Surface((map_size * 2, map_size))
        self.image_90 = pygame.transform.rotate(self.image, 90)
        # change the colour of our image to blue
        self.image.fill(GREY)

        self.rect = self.image.get_rect()

class Bordery(pygame.sprite.Sprite):
    def __init__(self):
        """map sprite"""
        super().__init__()

        self.image = pygame.Surface((map_size, map_size * 2))
        # change the colour of our image to blue
        self.image.fill(GREY)

        self.rect = self.image.get_rect()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        """Goomba"""
        super().__init__()

        self.image = pygame.image.load("assets/goomba-nes.png")
        self.image = pygame.transform.scale_by(self.image, 2)
        self.rect = self.image.get_rect()
        # No initial location -> (0, 0)

        # Velocity of the Enemy
        self.vel_x = 0
        self.vel_y = 0

        self.damage = 1

    def level_up(self):
        # increase damage
        self.damage *= 2


    def update(self):
        # movement in the x- and y-axis
        # self.rect.x += self.vel_x
        #self.rect.y += self.vel_y
        # TODO: randomize movement
        pass

class HealthBar(pygame.Surface):
    def __init__(self):
        super().__init__((300, 10))
        self.fill(RED)

    def set_health(self, percentage: float):
        self.fill(RED)
        pygame.draw.rect(self, GREEN, (0, 0, (300 * percentage), 10))

def move(sprite, vel: int):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        sprite.rect.centerx += vel
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        sprite.rect.centerx -= vel
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        sprite.rect.centery += vel
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        sprite.rect.centery -= vel

def spawn_tree(pos: int):
    pass

def spawn_push_blocks(amount: int):
    for push_block in range(int(amount)):
        push_block = Map()
        push_block.image.fill(WHITE)
        push_block_size_x = random.randint(centerx - map_size, centerx + map_size)
        push_block_size_y = random.randint(centery - map_size, centery + map_size)
        push_block.rect.center = push_block_size_x, push_block_size_y
        push_block_last_center = push_block.rect.center
        all_sprites_group.add(push_block)
        white_map_sprites_group.add(push_block)
        push_block_sprites_group.add(push_block)
        map_sprites_group.add(push_block)

def spawn_map(amount: int):
    for map in range(int(amount)):
        map = Map()
        map.image.fill(BLACK)
        map_size_x = random.randint(centerx - map_size, centerx + map_size)
        map_size_y = random.randint(centery - map_size, centery + map_size)
        map.rect.center = map_size_x, map_size_y
        map_last_center = map.rect.center
        all_sprites_group.add(map)
        black_map_sprites_group.add(map)
        map_sprites_group.add(map)

def spawn_border():
    border_up = Borderx()
    border_up.rect.center = centerx + 0, centery + map_size
    border_right = Bordery()
    border_right.rect.center = centerx + map_size, centery + 0
    border_down = Borderx()
    border_down.rect.center = centerx + 0, centery - map_size
    border_left = Bordery()
    border_left.rect.center = centerx - map_size, centery + 0
    for border in [border_up, border_right, border_down, border_left]:
        all_sprites_group.add(border)
        border_sprites_group.add(border)
        map_sprites_group.add(border)

def game():
    pygame.init()

    # Creating the Screen
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Collect Blocks")
    pygame.mouse.set_visible(True)

    # Variables
    done = False

    clock = pygame.time.Clock()
    num_enemies = round(3 * (map_size / 1000))
    num_blocks = round(map_size / 5)
    healthbar = HealthBar()
    level = 1
    vel = 5
    pos_x = 0
    pos_y = 0
    pressing_left = False
    pressing_right = False
    pressing_up = False
    pressing_down = False
    pressing_space = False

    # light
    pygame.draw.circle(pygame.Surface((50, 50)), WHITE, (0, 0), 25)
    #light = Circle()
    #light.rect.center = WIDTH / 2, HEIGHT / 2
    #all_sprites_group.add(light)

    # push-able blocks
    spawn_push_blocks(round(int(map_size / 50)))

    # map
    spawn_map(round(int(map_size / 40)))

    # border
    spawn_border()

    # Create player sprite
    player = Mario()
    # Place Mario in the middle of the screen
    player.rect.centerx = WIDTH / 2
    player.rect.centery = HEIGHT / 2
    player_last_x = player.rect.centerx
    player_last_y = player.rect.centery
    all_sprites_group.add(player)

    # Create Enemies
    for _ in range(num_enemies):
        enemy = Enemy()
        # Randomize position at bottom-left
        random_x = random.randrange(centerx-map_size, centerx+map_size)
        random_y = random.randrange(centerx-map_size, centerx+map_size)
        enemy.rect.center = random_x, random_y
        enemy_last_center = enemy.rect.center
        # Randomize velocity
        enemy.vel_x = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        enemy.vel_y = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])

        all_sprites_group.add(enemy)
        enemy_sprites_group.add(enemy)

    # Create 100 blocks
    for _ in range(num_blocks):
        block = Block()
        # randomize their location
        block.rect.centerx = random.randrange(centerx-map_size, centerx+map_size)
        block.rect.centery = random.randrange(centery-map_size, centery+map_size)
        block_last_center = block.rect.center
        # add them to the sprite group
        all_sprites_group.add(block)
        block_sprites_group.add(block)

    # build tree
    for i in range(10):
        pass
        pos_tree = (random.randint(centerx - map_size, centerx + map_size), random.randint(centery - map_size, centery + map_size))
        # spawn_tree(pos_tree)

    test_pos = (WIDTH / 2, HEIGHT / 2)
    # tree bottom
    # from here to the next # is functioning... for now, i guess
    tree_bottom = Tree_bottom()
    tree_bottom.rect.center = test_pos

    all_sprites_group.add(tree_bottom)
    map_sprites_group.add(tree_bottom)
    border_sprites_group.add(tree_bottom)
    # tree height
    for i in range(20):
        tree = Tree()
        tree.rect.center = test_pos

        all_sprites_group.add(tree)
        env_sprites_group.add(tree)
        tree_sprites_group.add(tree)

    leaf = Leaf()
    leaf.rect.center = test_pos

    all_sprites_group.add(leaf)
    env_sprites_group.add(leaf)

    # delete overlapped map/blocks
    map_collided = pygame.sprite.spritecollide(player, map_sprites_group, True)
    for map in map_sprites_group:
        blocks_collided = pygame.sprite.spritecollide(map, block_sprites_group, True)

    # temp
    a = 1
    # ------------ MAIN GAME LOOP
    while not done:
        # ------ MAIN EVENT LISTENER
        # when the user does something
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.draw.circle(pygame.Surface((50, 50)), WHITE, (0, 0), 25)
        # ------ GAME LOGIC
        all_sprites_group.update()
        healthbar.set_health(player.show_health_percentage())

        # mario move
        keys = pygame.key.get_pressed()

        if a == 1:
            map_collided = pygame.sprite.spritecollide(player, black_map_sprites_group, False)
        else:
            map_collided = pygame.sprite.spritecollide(player, white_map_sprites_group, False)
        border_collided = pygame.sprite.spritecollide(player, border_sprites_group, False)

        # pushing_blocks = pygame.sprite.spritecollide(player, push_block_sprites_group, False)

        """
        # blocks wont move when touched
        if pushing_blocks:
            for push_block in pushing_blocks:
                move(push_block, 0)
        else:
            for push_block in push_block_sprites_group:
                move(push_block, vel)
        """

        if not map_collided and not border_collided:
            # map move
            for push_block in white_map_sprites_group:
                move(push_block, vel)

            for black_map in black_map_sprites_group:
                move(black_map, vel)

            for border in border_sprites_group:
                move(border, vel)

            for blocks in block_sprites_group:
                move(blocks, vel)

            for enemies in enemy_sprites_group:
                move(enemies, vel)

            height_tree = vel - 1
            for tree in tree_sprites_group:
                height_tree += 1
                move(tree, height_tree)
                move(leaf, 1)
            height_tree = vel + 0


        # shift mario a little bit
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.rect.centerx = (WIDTH / 2) - vel * 2
            #light.rect.centerx = player.rect.centerx
            pressing_left = True
            # flip mario
            player.image = player.image_left
        # release key detection
        elif pressing_left and not keys[pygame.K_LEFT] and not keys[pygame.K_a]:
            player.rect.centerx = (WIDTH / 2)
            #light.rect.centerx = player.rect.centerx
            pressing_left = False

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.rect.centerx = (WIDTH / 2) + vel * 2
            #light.rect.centerx = player.rect.centerx
            pressing_right = True
            # flip mario
            player.image = player.image_right
        # release key detection
        elif pressing_right and not keys[pygame.K_RIGHT] and not keys[pygame.K_d]:
            player.rect.centerx = (WIDTH / 2)
            #light.rect.centerx = player.rect.centerx
            pressing_right = False

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.rect.centery = (HEIGHT / 2) - vel * 2
            #light.rect.centery = player.rect.centery
            pressing_up = True
        # release key detection
        elif pressing_up and not keys[pygame.K_UP] and not keys[pygame.K_w]:
            player.rect.centery = (HEIGHT / 2)
            #light.rect.centery = player.rect.centery
            pressing_up = False

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.rect.centery = (HEIGHT / 2) + vel * 2
            #light.rect.centery = player.rect.centery
            pressing_down = True
        # release key detection
        elif pressing_down and not keys[pygame.K_DOWN] and not keys[pygame.K_s]:
            player.rect.centery = (HEIGHT / 2)
            #light.rect.centery = player.rect.centery
            pressing_down = False

        for enemy in enemy_sprites_group:
            enemy.rect.x += enemy.vel_x
            if a == 1:
                for black_map in black_map_sprites_group:
                    map_sprites_group.add(black_map)
                for white_map in white_map_sprites_group:
                    map_sprites_group.remove(white_map)
            else:
                for white_map in white_map_sprites_group:
                    map_sprites_group.add(white_map)
                for black_map in black_map_sprites_group:
                    map_sprites_group.remove(black_map)
            enemy_collide_map = pygame.sprite.spritecollide(enemy, map_sprites_group, False)
            for map in enemy_collide_map:
                # x collision - left to right
                if enemy.vel_x > 0:
                    enemy.vel_x = -enemy.vel_x
                    enemy.rect.right = map.rect.left - 1
                # x collision - right to left
                elif enemy.vel_x < 0:
                    enemy.vel_x = -enemy.vel_x
                    enemy.rect.left = map.rect.right + 1

            enemy.rect.y += enemy.vel_y
            if a == 1:
                for black_map in black_map_sprites_group:
                    map_sprites_group.add(black_map)
                for white_map in white_map_sprites_group:
                    map_sprites_group.remove(white_map)
            else:
                for white_map in white_map_sprites_group:
                    map_sprites_group.add(white_map)
                for black_map in black_map_sprites_group:
                    map_sprites_group.remove(black_map)

            enemy_collide_map = pygame.sprite.spritecollide(enemy, map_sprites_group, False)
            for map in enemy_collide_map:
                if enemy.vel_y < 0:
                    enemy.vel_y = -enemy.vel_y
                    enemy.rect.top = map.rect.bottom + 5
                # y collision - top to bottom
                elif enemy.vel_y > 0:
                    enemy.vel_y = -enemy.vel_y
                    enemy.rect.bottom = map.rect.top - 5

        # Check if Mario collides with a block
        blocks_collided = pygame.sprite.spritecollide(player, block_sprites_group, True)
        for block in blocks_collided:
            player.increase_score(block.point_value)

        # Check if Mario collides with enemies
        enemies_collided = pygame.sprite.spritecollide(player, enemy_sprites_group, False)
        for enemy in enemies_collided:
            # Decrease Mario's life by some number
            player.decrease_health(enemy.damage)

        # LEVEL UP
        # Refill blocks
        # Increase enemy damage
        # Increase block point value
        if not block_sprites_group:
            level += 1

            for _ in range(num_blocks):
                block = Block()
                block.rect.center = (random.randint(centerx - map_size, centerx + map_size), random.randint(centery - map_size, centery + map_size))
                for map in map_sprites_group:
                    blocks_collided = pygame.sprite.spritecollide(map, block_sprites_group, True)
                block.level_up(level)

                all_sprites_group.add(block)
                block_sprites_group.add(block)
                # delet over lapped blocks
            if a == 1:
                for map in white_map_sprites_group:
                    blocks_collided = pygame.sprite.spritecollide(map, block_sprites_group, True)
            else:
                for map in black_map_sprites_group:
                    blocks_collided = pygame.sprite.spritecollide(map, block_sprites_group, True)
            enemy = Enemy()
            enemy.vel_x, enemy.vel_y = random.choice([-5, -3, -1, 1, 3, 5]), random.choice([-5, -3, -1, 1, 3, 5])
            enemy.rect.center = (WIDTH/2, HEIGHT/2)
            all_sprites_group.add(enemy)
            enemy_sprites_group.add(enemy)

            for enemy in enemy_sprites_group:
                enemy.level_up()

        # End Game
        if player.health <= 0:
            done = True

        # ------ DRAWING TO SCREEN
        if keys[pygame.K_SPACE]:
            pressing_space = True
        elif pressing_space and not keys[pygame.K_SPACE]:
            a = -a
            pressing_space = False

        if a == 1:
            screen.fill(WHITE)
        else:
            screen.fill(BLACK)

        # Draw all the sprites
        all_sprites_group.draw(screen)
        screen.blit(healthbar, (5, 5))

        # Update screen
        pygame.display.flip()

        # ------ CLOCK TICK
        clock.tick(60) # 60 fps


    # Display final score:
    print("Thanks for playing!")
    print("Final score is:", player.points)

    pygame.quit()

if __name__ == "__main__":
    game()
