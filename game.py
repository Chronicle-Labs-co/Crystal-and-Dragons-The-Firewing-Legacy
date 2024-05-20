import sys
import pygame
import random
import math
import time

from button import Button
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("C")
        
        self.screen = pygame.display.set_mode((1280, 720))
        
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]
        
        self.assets = {
            # Tile assets
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player' : load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),

            # Player assets
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'player/jump': Animation(load_images('entities/player/jump')),


            # UI assets
            'button_inventory': load_image('ui/tas.png', color_key=(255,255,255), convert_alpha=True),
            'healthbar': load_images('icons/HealthBar', is_color_key=False, convert_alpha=True),
            'manabar': load_images('icons/Manabar', is_color_key=False, convert_alpha=True),

            # Particle assets
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False)

        }
        
        self.clouds = Clouds(self.assets['clouds'], count=16)        
        
        self.player = Player(self, (50,50), (8, 15))
        
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('map.json')

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
            print(self.leaf_spawners)
            
        self.particles = []

        self.scroll = [0,0]

        
        self.level = 0
        self.load_level(self.level)

        self.inv_button = Button(image=self.assets['button_inventory'], pos=(self.display.get_width() - 20, self.display.get_height() - 25), 
                                text_input="", font=self.get_font(7), base_color="#d7fcd4", hovering_color="White")
    
    def mana_regen(self):
        now = time.time()
        if now - self.last_regen_time >= self.mana_regen_rate:
            print("bisa regen")
            if self.player_mana < 8:
                print("regenareted")
                self.player_mana += 1
                self.player_mana = min(self.player_mana, 8)
                self.last_regen_time = now

    def update_health_bar(self):
        self.health_bar = pygame.transform.scale(self.assets['healthbar'][self.player_hp], (75, 32))
        self.display.blit(self.health_bar, (10, 10))

    def update_mana_bar(self):
        self.mana_bar = pygame.transform.scale(self.assets['manabar'][self.player_mana], (75, 32))
        self.mana_bar = pygame.transform.flip(self.mana_bar, flip_x=True, flip_y=False)
        self.display.blit(self.mana_bar, (self.display.get_width() - 85, 10))

    def options(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.fill("white")

            BG = pygame.image.load("data/images/ui/tutorial.png")
            BG = pygame.transform.scale(BG, (1280, 720))
            self.screen.blit(BG, (0, 0))

            OPTIONS_BACK = Button(image=None, pos=(1100, 650), 
                                text_input="BACK", font=self.get_font(75), base_color="White", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.run()

            pygame.display.update()      

    def get_font(self,size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("data/images/ui/font.ttf", size)


    def run(self):        
        while True:
            BG = pygame.image.load("data/images/ui/bg-menu.png")
            BG = pygame.transform.scale(BG, (1280, 720))
            self.screen.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(32).render("Crystal and Dragons:The Firewing Legacy", True, "#ba2313")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("data/images/ui/Play Rect.png"), pos=(640, 250), 
                                text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("data/images/ui/Options Rect.png"), pos=(640, 400), 
                                text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("data/images/ui/Quit Rect.png"), pos=(640, 550), 
                                text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)
            
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                            self.game_on()
                        if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                            self.options()
                        if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                            pygame.quit()
                            sys.exit()

            pygame.display.update()
            self.clock.tick(60)
#ini merupakan ui inventory
    def inventory(self):
        while True:
            INV = pygame.image.load("data/images/ui/copper_hud.png")
            INV = pygame.transform.scale(INV, (1280, 720))
            INV_TEXT = self.get_font(25).render("Inventory", True, "#dbdbdb")
            INV_RECT = INV_TEXT.get_rect(center = (self.screen.get_rect().width //2, 100))

            self.screen.blit(INV, (0, 0))
            self.screen.blit(INV_TEXT, INV_RECT)

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            RESUME_BUTTON = Button(image=None, pos=(self.screen.get_rect().width - 250 ,620), text_input="RESUME", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            RESUME_BUTTON.changeColor(MENU_MOUSE_POS)
            RESUME_BUTTON.update(self.screen)
            
            box_image = pygame.image.load("data/images/ui/itembox.png")
            box_image = pygame.transform.scale(box_image, (150,150))

            char_inv = pygame.image.load("data/images/entities/player/idle/00.png")
            char_inv = pygame.transform.scale(char_inv, (200,350))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                            self.game_on()

            self.screen.blit(char_inv, (150,150))

            for row in range(3):
                for col in range(5):
                    if col == 0:
                        x = 400 + col * (150 + 0)
                        y = 130 + row * (150 + 0)
                        self.screen.blit(box_image, (x, y))
                    else:
                        x = 450 + col * (150 + 0)
                        y = 130 + row * (150 + 0)
                        self.screen.blit(box_image, (x, y))

            pygame.display.update()

#ini merupakan UI trainer
    def trainer(self):
        while True:
            # Load and scale images
            Train = pygame.image.load("data/images/ui/copper_hud.png")
            Train = pygame.transform.scale(Train, (1280, 720))
            Train_TEXT = self.get_font(25).render("Trainer", True, "#dbdbdb")
            Train_RECT = Train_TEXT.get_rect(center = (self.screen.get_rect().width //2, 100))

            self.screen.blit(Train, (0, 0))
            self.screen.blit(Train_TEXT, Train_RECT)

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            #character
            trainer_char = pygame.image.load("data/images/entities/NPC/Trainer/idle/Warrior_Idle_1.png")
            trainer_char = pygame.transform.scale(trainer_char, (512,352))

            #Dialogue
            dialogue = pygame.image.load("data/images/ui/dialogue_box.png")
            dialogue = pygame.transform.scale(dialogue, (375,150))

            # Create and render the upgrade button as text-only
            upgrade_button = Button(image=None, pos=(1050, 600), text_input="UPGRADE", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            upgrade_button.changeColor(MENU_MOUSE_POS)
            upgrade_button.update(self.screen)

            #weapon
            weapon_box_image = pygame.image.load("data/images/ui/itembox.png")
            weapon_box_image = pygame.transform.scale(weapon_box_image, (150, 150))

            #arrow button
            arrowright_button = Button(image=pygame.image.load("data/images/ui/right_arrow.png"), pos=(1200, 225), text_input=None, font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            arrowright_button.changeColor(MENU_MOUSE_POS)
            arrowright_button.update(self.screen)

            arrowleft_button = Button(image=pygame.image.load("data/images/ui/left_arrow.png"), pos=(500, 225), text_input=None, font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            arrowleft_button.changeColor(MENU_MOUSE_POS)
            arrowleft_button.update(self.screen)

            #coin
            coin_image = pygame.image.load("data/images/items/weapons/coins/coin_1.png")
            coin_image = pygame.transform.scale(coin_image, (100, 100))
            
            # Render weapon slots
            for i in range(4):
                x = 550 + i * 150
                y = 150
                self.screen.blit(weapon_box_image, (x, y))

            # Render selected weapon slot
            self.screen.blit(weapon_box_image, (550, 350))
            
            # Render weapon stats
            weapon_name = self.get_font(20).render("Pedank", True, (0, 0, 0))
            weapon_damage = self.get_font(20).render("Damage: 126 + 15", True, (0, 0, 0))
            weapon_level = self.get_font(20).render("Level: 4 + 1", True, (0, 0, 0))
            self.screen.blit(weapon_name, (725, 380))
            self.screen.blit(weapon_damage, (725, 410))
            self.screen.blit(weapon_level, (725, 440))

            # Render coins and upgrade button
            self.screen.blit(coin_image, (825, 550))
            coin_amount = self.get_font(20).render("400", True, (255, 255, 0))
            self.screen.blit(coin_amount, (850, 640))
            
            self.screen.blit(trainer_char, (70,250))
            self.screen.blit(dialogue, (100, 145))
            multiline_text = (
                "Ah, a fellow warrior!\n"
                "You've come to\n"
                "the right place.\n"
                "Let me forge you\n"
                "a weapon that will make\n"
                "your enemies tremble!"
            )
            lines = multiline_text.splitlines()
            y_offset = 180
            font = self.get_font(13)
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, "#8c6e08")
                self.screen.blit(text_surface, (140, y_offset + 2 + i * font.get_linesize()))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if upgrade_button.checkForInput(MENU_MOUSE_POS):
                            print("Upgraded")
                        if arrowright_button.checkForInput(MENU_MOUSE_POS):
                            print("Kanan")
                        if arrowleft_button.checkForInput(MENU_MOUSE_POS):
                            print("Kiri")


            pygame.display.update()
    def merchant(self):
        while True:
            # Load and scale images
            Train = pygame.image.load("data/images/ui/copper_hud.png")
            Train = pygame.transform.scale(Train, (1280, 720))
            Train_TEXT = self.get_font(25).render("Merchant", True, "#dbdbdb")
            Train_RECT = Train_TEXT.get_rect(center = (self.screen.get_rect().width //2, 100))

            self.screen.blit(Train, (0, 0))
            self.screen.blit(Train_TEXT, Train_RECT)

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            #character
            trainer_char = pygame.image.load("data/images/entities/NPC/merchant/idle/merchant.png")
            trainer_char = pygame.transform.scale(trainer_char, (352,352))

            #Dialogue
            dialogue = pygame.image.load("data/images/ui/dialogue_box.png")
            dialogue = pygame.transform.scale(dialogue, (375,150))

            # Create and render the upgrade button as text-only
            upgrade_button = Button(image=None, pos=(1050, 625), text_input="BUY", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            upgrade_button.changeColor(MENU_MOUSE_POS)
            upgrade_button.update(self.screen)

            #weapon
            item_box_image = pygame.image.load("data/images/ui/itembox.png")
            item_box_image = pygame.transform.scale(item_box_image, (150, 150))

            arrowright_button = Button(image=pygame.image.load("data/images/ui/right_arrow.png"), pos=(1200, 350), text_input=None, font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            arrowright_button.changeColor(MENU_MOUSE_POS)
            arrowright_button.update(self.screen)

            arrowleft_button = Button(image=pygame.image.load("data/images/ui/left_arrow.png"), pos=(500, 350), text_input=None, font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            arrowleft_button.changeColor(MENU_MOUSE_POS)
            arrowleft_button.update(self.screen)

            #coin
            coin_image = pygame.image.load("data/images/items/weapons/coins/coin_1.png")
            coin_image = pygame.transform.scale(coin_image, (80, 80))
            
            # Render weapon slots
            for row in range(3):
                for col in range(4):
                        x = 550 + col * (150 + 0)
                        y = 130 + row * (150 + 0)
                        self.screen.blit(item_box_image, (x, y))

            # Render coins and upgrade button
            self.screen.blit(coin_image, (865, 580))
            coin_amount = self.get_font(20).render("400", True, (255, 255, 0))
            self.screen.blit(coin_amount, (900, 650))
            
            self.screen.blit(trainer_char, (100,300))
            self.screen.blit(dialogue, (100, 150))
            multiline_text = (
                "Welcome, traveler!\n"
                "Step right up\n"
                "and behold my wares—\n"
                "only the finest goods\n"
                "from distant lands, all\n"
                "at unbeatable prices!"
            )
            lines = multiline_text.splitlines()
            y_offset = 180
            font = self.get_font(13)
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, "#8c6e08")
                self.screen.blit(text_surface, (140, y_offset + 2 + i * font.get_linesize()))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if upgrade_button.checkForInput(MENU_MOUSE_POS):
                            print("Bought!")
                        if arrowright_button.checkForInput(MENU_MOUSE_POS):
                            print("Kanan")
                        if arrowleft_button.checkForInput(MENU_MOUSE_POS):
                            print("Kiri")


            pygame.display.update()

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        # self.tilemap.load('map.json')
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))
            
        self.projectiles = []
        self.particles = []
        self.sparks = []
        
        self.scroll = [0,0]
        self.dead = 0
        self.transition = -30

        self.player_hp = 8
        self.player_mana = 8
        self.mana_regen_rate = 3
        self.last_regen_time = time.time()
        self.screenshake = 0

#Kalo play di main menu dipencet, bakal ngerun ini buat ke gameplay
    def game_on(self):
        while True:

            self.display_2.blit(self.assets['background'], (0,0))
            
            self.screenshake = max(0, self.screenshake - 1)
            
            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1
            
            if self.dead:
                self.dead += 1
                self.player_hp = 8
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:
                    self.load_level(self.level)
            self.display.blit(self.assets['background'], (0,0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
            
            self.clouds.update()
            self.clouds.render(self.display, render_scroll)
            
            self.tilemap.render(self.display, offset=render_scroll)
            
            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)
            
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)
            
            # calculate realtime scaled mouse position
            pos = list(pygame.mouse.get_pos())
            ratio_x = (self.screen.get_rect().width // self.display.get_rect().width)
            ratio_y = (self.screen.get_rect().height // self.display.get_rect().height)
            scaled_pos = (pos[0] / ratio_x, pos[1] / ratio_y)

            # [[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing < 50): # not moving in dashing
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)

                        if self.player_hp > 1:
                            self.player_hp -= 1
                        else:
                            self.dead += 1

                        self.sfx['hit'].play()
                        if self.player_hp <= 0:
                            self.dead += 1
                            self.player_hp = 8
                            
                        self.screenshake = max(16, self.screenshake)
                        
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0,7)))
            
            if self.player_mana < 8:
                self.mana_regen()
            self.update_mana_bar()
            self.update_health_bar()

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)
                    
            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_sillhouette, offset)
                        

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3 # sin use to wave position
                if kill:
                    self.particles.remove(particle)

            self.inv_button.update(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT  or event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_UP  or event.key == pygame.K_w:
                        self.player.jump()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if self.inv_button.checkForInput(scaled_pos):
                            self.inventory()

            
            self.inv_button.update(self.display)
            

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))
                
            self.display_2.blit(self.display, (0, 0))
            
            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)

            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)
            self.inv_button.update(self.display)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            
            # self.screen.blit(self.display, (0,0))
            pygame.display.update()

            self.clock.tick(75)