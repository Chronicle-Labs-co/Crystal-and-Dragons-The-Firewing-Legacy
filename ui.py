import sys
import pygame
from abc import ABC, abstractmethod

from button import Button
from scripts.utils import get_font, load_image

# Kelas abstrak untuk komponen UI
class UIComponent(ABC):
    @abstractmethod
    def render(self, screen):
        pass
    
    @abstractmethod
    def handle_event(self, event):
        pass

# Implementasi Game Option
class UITutorial(UIComponent):
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.is_active = True
        
        self.back_btn = Button(image=None, pos=(1100, 650), text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
    
    def render(self, screen):
        self.background = load_image("ui/tutorial.png")
        self.background = pygame.transform.scale(self.background, (1280, 720))
        
        self.is_active = True
        
        while self.is_active:
            mouse_pos = pygame.mouse.get_pos()
            
            screen.blit(self.background, (0, 0))

            self.back_btn.changeColor(mouse_pos)
            self.back_btn.update(screen)

            self.handle_event(mouse_pos)
                
            pygame.display.update()      
    
    def handle_event(self, mouse_pos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_btn.checkForInput(mouse_pos):
                    self.is_active = False

# Implementasi Pause Menu
class UIPauseMenu(UIComponent):
    def __init__(self, game):
        self.font = pygame.font.Font(None, 72)
        self.is_active = True
        
        self.resume_btn = Button(image=None, pos=(640 , 240), text_input="RESUME", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        self.tutorial_btn = Button(image=None, pos=(640 , 320), text_input="TUTORIAL", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        self.exit_to_menu_btn = Button(image=None, pos=(640 , 400), text_input="EXIT TO MENU", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        self.exit_to_desktop_btn = Button(image=None, pos=(640 , 480), text_input="EXIT TO DESKTOP", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        self.mute_btn = Button(image=None, pos=(1100 , 650), text_input="MUTE", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        self.background = load_image("ui/pause-menu.png")
        self.background = pygame.transform.scale(self.background, (1280, 720))
        
    def render(self, screen):
        self.is_active = True
        
        while self.is_active:
            
            screen.blit(self.background, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            
            for button in [self.resume_btn, self.tutorial_btn, self.exit_to_menu_btn, self.exit_to_desktop_btn, self.mute_btn]:
                button.changeColor(mouse_pos)
                button.update(screen)
            
            self.handle_event(mouse_pos)
            
            pygame.display.update()
    
    def handle_event(self, mouse_pos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.resume_btn.checkForInput(mouse_pos):
                        self.is_active = False
                    if self.tutorial_btn.checkForInput(mouse_pos):
                        self.game_option_ui.render(screen)
                    if self.exit_to_menu_btn.checkForInput(mouse_pos):
                        self.run()
                    if self.exit_to_desktop_btn.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    if self.mute_btn.checkForInput(mouse_pos):
                        self.game.sfx.mute()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_active = False
                    
class UIMainMenu(UIComponent):
    def __init__(self, game):
        self.game = game
        
        self.background = load_image("ui/bg-menu.png")
        self.background = pygame.transform.scale(self.background, (1280, 720))
        
        self.menu_txt = get_font(32).render("Crystal and Dragons:The Firewing Legacy", True, "#ba2313")
        self.menu_rect = self.menu_txt.get_rect(center=(640, 100))
        
        self.play_btn = Button(image=load_image("ui/Play Rect.png", convert_alpha=True), pos=(640, 250), text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.tutorial_btn = Button(image=load_image("ui/Options Rect.png", convert_alpha=True), pos=(640, 400), text_input="TUTORIAL", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.quit_btn = Button(image=load_image("ui/Quit Rect.png", convert_alpha=True), pos=(640, 550), text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    
    def render(self, screen):
        while True:
            screen.blit(self.background, (0, 0))

            mouse_pos = pygame.mouse.get_pos()

            screen.blit(self.menu_txt, self.menu_rect)
            
            for button in [self.play_btn, self.tutorial_btn, self.quit_btn]:
                button.changeColor(mouse_pos)
                button.update(screen)
                
            self.handle_event(mouse_pos)

            pygame.display.update()   
    
    def handle_event(self, mouse_pos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.play_btn.checkForInput(mouse_pos):
                        self.game.game_on()
                    if self.tutorial_btn.checkForInput(mouse_pos):
                        self.game_tutorial_ui.render(screen)
                    if self.quit_btn.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()
                        
class UIInventory(UIComponent):
    def __init__(self, game):
        self.game = game
        
        self.background = load_image("ui/copper_hud.png")
        self.background = pygame.transform.scale(self.background, (self.game.screen.get_width(), self.game.screen.get_height()))

        self.inventory_txt = get_font(25).render("Inventory", True, "#dbdbdb")
        self.inventory_rect = self.inventory_txt.get_rect(center = (self.game.screen.get_rect().width //2, 100))
        
        self.resume_btn = Button(image=None, pos=(self.game.screen.get_rect().width - 250 ,620), text_input="RESUME", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        self.box_image = load_image("ui/itembox.png")
        self.box_image = pygame.transform.scale(self.box_image, (150, 150))

        self.is_active = True
        
    
    def render(self, screen, player_img):
        self.is_active = True
        
        while self.is_active:
            screen.blit(self.background, (0, 0))
            screen.blit(self.inventory_txt, self.inventory_rect)

            mouse_pos = pygame.mouse.get_pos()
            
            self.resume_btn.changeColor(mouse_pos)
            self.resume_btn.update(screen)

            char_inv = pygame.transform.scale(player_img, (200,350))

            screen.blit(char_inv, (150,150))

            for row in range(3):
                for col in range(5):
                    if col == 0:
                        x = 400 + col * (150 + 0)
                        y = 130 + row * (150 + 0)
                        screen.blit(self.box_image, (x, y))
                    else:
                        x = 450 + col * (150 + 0)
                        y = 130 + row * (150 + 0)
                        screen.blit(self.box_image, (x, y))
                        
            self.handle_event(mouse_pos)

            pygame.display.update() 
    
    def handle_event(self, mouse_pos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.resume_btn.checkForInput(mouse_pos):
                        self.is_active = False
                        
class UIMerchant(UIComponent):
    def __init__(self, game):
        self.game = game
        
        self.background = load_image("ui/copper_hud.png")
        self.background = pygame.transform.scale(self.background, (1280, 720))

        self.merchant_txt = get_font(25).render("Merchant", True, "#dbdbdb")
        self.merchant_rect = self.merchant_txt.get_rect(center = (game.screen.get_rect().width //2, 100))
        self.merchant_char = load_image('entities/NPC/merchant/idle/shop_anim_ver2_.png', convert_alpha=True)
        self.merchant_char = pygame.transform.scale(self.merchant_char, (352,352))

        self.dialog_box = load_image("ui/dialogue_box.png", convert_alpha=True)
        self.dialog_box = pygame.transform.scale(self.dialog_box, (375,150))
        
        self.coin_img = load_image("items/weapons/coins/coin_1.png", convert_alpha=True)
        self.coin_img = pygame.transform.scale(self.coin_img, (80, 80))
        self.player_coin_image = pygame.transform.scale(self.coin_img, (60, 60))

        self.item_box = load_image("ui/itembox.png", convert_alpha=True)
        

        self.upgrade_btn = Button(image=None, pos=(1050, 625), text_input="BUY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        self.arrowright_btn = Button(image=load_image("ui/right_arrow.png"), pos=(1200, 350), text_input=None, font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        self.arrowleft_btn = Button(image=load_image("ui/left_arrow.png"), pos=(500, 350), text_input=None, font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        self.is_active = True
    
    def render(self, screen):
        self.is_active = True
        
        while self.is_active:
            # Load and scale images
            screen.blit(self.background, (0, 0))
            screen.blit(self.merchant_txt, self.merchant_rect)

            mouse_pos = pygame.mouse.get_pos()

            for button in [self.upgrade_btn, self.arrowleft_btn, self.arrowright_btn]:
                button.changeColor(mouse_pos)      
                button.update(screen)


            #player's coin
            screen.blit(self.player_coin_image, (1050, 60))
            player_coin_amount_txt = get_font(16).render("400", True, (255, 255, 0))
            screen.blit(player_coin_amount_txt, (1075, 115))
            
            # Render weapon slots
            for row in range(3):
                for col in range(4):
                        x = 550 + col * (150 + 0)
                        y = 130 + row * (150 + 0)
                        screen.blit(self.item_box, (x, y))

            # Render coins and upgrade button
            screen.blit(self.coin_img, (865, 580))
            coin_amount = get_font(20).render("400", True, (255, 255, 0))
            screen.blit(coin_amount, (900, 650))
            
            screen.blit(self.merchant_char, (100,300))
            screen.blit(self.dialog_box, (100, 150))
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
            font = get_font(13)
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, "#8c6e08")
                screen.blit(text_surface, (140, y_offset + 2 + i * font.get_linesize()))

            self.handle_event(mouse_pos)

            pygame.display.update()
    
    def handle_event(self, mouse_pos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.arrowright_btn.checkForInput(mouse_pos):
                        print("Kanan")
                    if self.arrowleft_btn.checkForInput(mouse_pos):
                        print("Kiri")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_active = False
                    
class UITrainer(UIComponent):
    def __init__(self, game):
        self.game = game
        
        self.background = load_image("ui/copper_hud.png")
        self.background = pygame.transform.scale(self.background, (1280, 720))
        
        self.train_txt = get_font(25).render("Trainer", True, "#dbdbdb")
        self.train_rect = self.train_txt.get_rect(center = (self.game.screen.get_rect().width //2, 100))

        #character
        self.trainer_char = load_image("entities/NPC/Trainer/idle/Warrior_Idle_1.png")
        self.trainer_char = pygame.transform.scale(self.trainer_char, (512,352))

        #Dialogue
        self.dialog_box = load_image("ui/dialogue_box.png")
        self.dialog_box = pygame.transform.scale(self.dialog_box, (375,150))

        # Create and render the upgrade button as text-only
        self.upgrade_btn = Button(image=None, pos=(1050, 600), text_input="UPGRADE", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        #weapon
        self.weapon_box_img = load_image("ui/itembox.png")
        self.weapon_box_img = pygame.transform.scale(self.weapon_box_img, (150, 150))

        #arrow button
        self.arrowright_btn = Button(image=load_image("ui/right_arrow.png", convert_alpha=True), pos=(1200, 225), text_input=None, font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        self.arrowleft_btn = Button(image=load_image("ui/left_arrow.png", convert_alpha=True), pos=(500, 225), text_input=None, font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        #coin
        self.coin_image = load_image("items/weapons/coins/coin_1.png")
        self.coin_image = pygame.transform.scale(self.coin_image, (100, 100))
        self.player_coin_image = pygame.transform.scale(self.coin_image, (80,80))
        
        self.is_active = True
    
    def render(self, screen):
        self.is_active = True

        while True:
            # Load and scale images
            

            screen.blit(self.background, (0, 0))
            screen.blit(self.train_txt, self.train_rect)

            mouse_pos = pygame.mouse.get_pos()

            for button in [self.arrowleft_btn, self.arrowright_btn, self.upgrade_btn]:
                button.changeColor(mouse_pos)
                button.update(screen)
            
            # Render weapon slots
            for i in range(4):
                x = 550 + i * 150
                y = 150
                screen.blit(self.weapon_box_img, (x, y))

            # Render selected weapon slot
            screen.blit(self.weapon_box_img, (550, 350))
            
            # Render weapon stats
            weapon_name = get_font(20).render("Pedank", True, (0, 0, 0))
            weapon_damage = get_font(20).render("Damage: 126 + 15", True, (0, 0, 0))
            weapon_level = get_font(20).render("Level: 4 + 1", True, (0, 0, 0))
            screen.blit(weapon_name, (725, 380))
            screen.blit(weapon_damage, (725, 410))
            screen.blit(weapon_level, (725, 440))

            # Render coins cost and upgrade button
            screen.blit(self.coin_image, (825, 550))
            coin_amount = get_font(20).render("400", True, (255, 255, 0))
            screen.blit(coin_amount, (850, 640))

            #Player's coin
            screen.blit(self.player_coin_image, (1050, 50))
            player_coin_amount = get_font(20).render("400", True, (255, 255, 0))
            screen.blit(player_coin_amount, (1075, 125))
            
            screen.blit(self.trainer_char, (70,250))
            screen.blit(self.dialog_box, (100, 145))

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
            font = get_font(13)
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, "#8c6e08")
                screen.blit(text_surface, (140, y_offset + 2 + i * font.get_linesize()))

            pygame.display.update()
    
    def handle_event(self, mouse_pos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.upgrade_btn.checkForInput(mouse_pos):
                        print("Upgraded")
                    if self.arrowright_btn.checkForInput(mouse_pos):
                        print("Kanan")
                    if self.arrowleft_btn.checkForInput(mouse_pos):
                        print("Kiri")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                
class UIDoctor(UIComponent):
    def __init__(self, game):
        self.game = game
        
        self.background = load_image("ui/copper_hud.png")
        self.background = pygame.transform.scale(self.background,(1280,720))
        self.doctor_txt = get_font(25).render("Doctor", True, "#dbdbdb")
        self.doctor_rect = self.doctor_txt.get_rect(center = (self.game.screen.get_rect().width //2, 100))

        #meditate button
        self.meditation_btn_bg = load_image("ui/meditate_button.png")
        self.meditation_btn_bg = pygame.transform.scale(self.meditation_btn_bg,(150,50))
        
        #meditation button
        self.meditation_btn = Button(image=self.meditation_btn_bg, pos=(620, 175), text_input="Meditate", font=get_font(15), base_color="#d7fcd4", hovering_color="White")      
    
        #buy button
        self.buy_btn = Button(image=None, pos=(1050, 620), text_input="Buy", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        
        #weapon box
        self.box_img = load_image("ui/itembox.png")
        self.box_img = pygame.transform.scale(self.box_img, (150, 150))
        
        #coin
        self.coin_img = load_image("items/weapons/coins/coin_1.png")
        self.coin_img = pygame.transform.scale(self.coin_img, (100, 100))
        
        self.doctor_char = load_image("entities/NPC/Doctor/Sprite-0002.png")
        self.doctor_char = pygame.transform.scale(self.doctor_char,(500,375))
        
        self.text_box = load_image("ui/doctor_text_box.png")
        self.text_box = pygame.transform.scale(self.text_box,(400,200))
        
        #potion spec
        self.meditation_spec = load_image("ui/health_potion.png")
        self.meditation_spec = pygame.transform.scale(self.meditation_spec,(600,150))

        self.is_active = True
    
    def render(self, screen):
        self.is_active = True
        
        while self.is_active:
            #load bg image
            screen.blit(self.background,(0,0))
            screen.blit(self.doctor_txt, self.doctor_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            
            for button in [self.meditation_btn, self.buy_btn]:
                button.changeColor(mouse_pos)
                button.update(screen)
            
            #Char doctor
            screen.blit(self.doctor_char,(30,275))
            
            #text box doctor
            screen.blit(self.text_box,(100,100))

            #box potion
            for i in range(4):
                x = 550 + i * 150
                y = 240
                screen.blit(self.box_img, (x, y))
            
            #meditation text
            meditation_name = get_font(13).render("Restore HP and MANA ", True, (0,0,0))
            screen.blit(meditation_name,(710,150))
            
            multiline_text = (
                "Find a quiet spot and sit down to meditate,\n"
                "as you focus your mind and breathe deeply,\n"
                "you'll feel your health and mana gradually\n"
                "restore,bringing you back to full strength."
            )
            
            lines = multiline_text.splitlines()
            y_offset = 170
            font = get_font(12)
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, (0,0,0))
                screen.blit(text_surface, (710, y_offset + i * font.get_linesize()))
            
            #potion text
            screen.blit(self.meditation_spec,(550,400))
            
            self.handle_event(mouse_pos)
            
            pygame.display.update()
    
    def handle_event(self, mouse_pos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.meditation_btn.checkForInput(mouse_pos):
                        self.__meditate()
                    if self.buy_btn.checkForInput(mouse_pos):
                        self.__buy_potion()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_active = False
                
    def __meditate(self):
        pass

    def __buy_potion(self):
        pass