import os
import sys
import pygame
import random
import math
import time

from button import Button
from scripts.spark import Spark
from scripts.utils import load_image, load_images, Animation
from scripts.entities import NPC, PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from sfx import SFXController
from ui import UIDoctor, UIInventory, UIMerchant, UIPauseMenu, UITrainer, UITutorial, UIMainMenu

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("C")
        
        self.screen = pygame.display.set_mode((1280, 720))
        
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((320, 240))
        self.display_3 = pygame.Surface((320, 240))
        self.display_4 = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]

        
        self.assets = {
            # Tile assets
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player' : load_image('entities/player.png'),
            'background': load_image('background1.png'),
            'background2': load_image('background2.png', convert_alpha=True),
            'background3': load_image('background3.png', convert_alpha=True),
            'clouds': load_images('clouds'),

            # Entity assets
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player': load_image('entities/player/idle/__Idle1.png'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'player/jump': Animation(load_images('entities/player/jump')),
            'doctor/idle': Animation(load_images('entities/NPC/Doctor'), img_dur=12),
            'merchant/idle': Animation(load_images('entities/NPC/merchant/idle', convert_alpha=True)),
            'merchant': load_image('entities/NPC/merchant/idle/shop_anim_ver2_.png', convert_alpha=True),
            'trainer': load_image('entities/NPC/Trainer/idle/Warrior_Idle_1.png'),
            'trainer/idle': Animation(load_images('entities/NPC/Trainer/idle'), img_dur=8),


            # UI assets
            'button_inventory': load_image('ui/tas.png', color_key=(255,255,255), convert_alpha=True),
            'healthbar': load_images('icons/HealthBar', is_color_key=False, convert_alpha=True),
            'manabar': load_images('icons/Manabar', is_color_key=False, convert_alpha=True),
            'e_button': load_image('ui/e_button.png', is_color_key=False, convert_alpha=True),
            'terimakasih': load_image('ui/terimakasih.jpg'),

            # Particle assets
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
            
        }
        
        self.sfx = SFXController()
        self.sfx.add_sfx('jump', "jump.wav")
        self.sfx.add_sfx('dash', "dash.wav", 0.3)
        self.sfx.add_sfx('hit', "hit.wav", 0.8)
        self.sfx.add_sfx('shoot', "shoot.wav", 0.4)
        self.sfx.add_sfx('ambience', "ambience.wav", 0.2)
        self.sfx.add_sfx('cat', "cat.mp3", 0.5)
        self.sfx.add_sfx('background', "music.ogg")
        
        self.clouds = Clouds(self.assets['clouds'], count=4)        
        
        self.player = Player(self, (50,50), (8, 15))
        
        self.tilemap = Tilemap(self, tile_size=16)
        
        self.level = 0
        self.load_level(self.level)
        
        self.game_tutorial_ui = UITutorial()
        self.game_pause_ui = UIPauseMenu(self)
        self.game_main_menu_ui = UIMainMenu(self)
        self.game_inventory_ui = UIInventory(self)
        self.game_merchant_ui = UIMerchant(self)
        self.game_trainer_ui = UITrainer(self)
        self.game_doctor_ui = UIDoctor(self)

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

    def get_font(self,size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("data/images/ui/font.ttf", size)


    def run(self):        
        self.game_main_menu_ui.render(self.screen)
            
    #ini merupakan UI trainer
    def trainer(self):
        self.game_trainer_ui.render(self.screen)

    def merchant(self):
        self.game_merchant_ui.render(self.screen)

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        # self.tilemap.load('map.json')
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        
        self.enemies = []
        self.npcs = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1), ('spawners', 2), ('spawners', 3), ('spawners', 4)]):
            if spawner['variant'] == 0: # Player
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            if spawner['variant'] == 1: # Enemy
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))
            if spawner['variant'] == 2: # Doctor
                self.npcs.append(NPC(self, 'doctor', spawner['pos'], (8, 15)))
            if spawner['variant'] == 3: # Merchant
                self.npcs.append(NPC(self, 'merchant', spawner['pos'], (8, 15)))
            if spawner['variant'] == 4: # Trainer
                self.npcs.append(NPC(self, 'trainer', spawner['pos'], (8, 15)))
            
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
        
        self.show_interact_button = False
        self.current_interact = ''
        
        self.muted = False
    
    def next_level(self):
        if self.level < 2:
            self.level += 1
            self.load_level(self.level)
        else:
            self.win()
            
    def win(self):
        while True:
            # Load and scale images
            Train = pygame.transform.scale(self.assets['terimakasih'], (1280, 720))

            self.screen.blit(Train, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return


            pygame.display.update()
        

#ini merupakan UI 
    def doctor(self):
        self.game_doctor_ui.render(self.screen)           

    #Kalo play di main menu dipencet, bakal ngerun ini buat ke gameplay
    def game_on(self):
        self.sfx.play('background', True)
        
        while True:
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.display.fill((0, 0, 0, 0))

            self.display_2.blit(pygame.transform.scale(self.assets['background'],(320, 240)), (0, 0))
            self.display_2.blit(pygame.transform.scale(self.assets['background2'],(320, 240)), (0, 0))
            self.display_2.blit(pygame.transform.scale(self.assets['background3'],(320, 240)), (0, 0))
            
            self.screenshake = max(0, self.screenshake - 1)
            
            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    # self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    # self.load_level(self.level)
                    self.next_level()
            if self.transition < 0:
                self.transition += 1
            
            if self.dead:
                self.dead += 1
                self.player_hp = 8
                if self.dead == 2:
                    self.sfx.play('cat')
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:
                    self.load_level(self.level)

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
            
            self.clouds.update()
            self.clouds.render(self.display_2, render_scroll)
            
            self.tilemap.render(self.display, offset=render_scroll)
            
            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)
                    
            self.show_interact_button = False
            self.current_interact = ''
            for index, npc in enumerate(self.npcs.copy()):
                if self.player.rect().colliderect(npc.rect()):
                    self.show_interact_button = True
                    self.current_interact = npc.type
                    
                npc.update(self.tilemap, (0, 0))
                npc.render(self.display, offset=render_scroll)
            
            if not self.dead:
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

                        self.sfx.play('hit')
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

            if self.show_interact_button:
                self.e_button = pygame.transform.scale(self.assets['e_button'], (10, 10))
                self.display.blit(self.e_button, (self.player.pos[0] - render_scroll[0], self.player.pos[1] - render_scroll[1] - 20))

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
                        if self.player.jump():
                            self.sfx.play('jump')
                    if event.key == pygame.K_x:
                        self.player.dash()
                    if event.key == pygame.K_p:
                        self.next_level()
                    if event.key == pygame.K_ESCAPE:
                        self.game_pause_ui.render(self.screen)
                    if event.key == pygame.K_e:
                        if self.current_interact == 'doctor':
                            self.doctor()
                        if self.current_interact == 'trainer':
                            self.trainer()
                        if self.current_interact == 'merchant':
                            self.merchant()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if self.inv_button.checkForInput(scaled_pos):
                            self.game_inventory_ui.render(self.screen, self.assets['player'])

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

            pygame.display.update()

            self.clock.tick(75)