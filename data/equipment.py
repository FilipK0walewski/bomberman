import pygame
from data.images import Spritesheet


class Loot:

    def __init__(self, pos, level, type, text=''):

        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

        if type == 'lesser_health_potion':
            self.description = 'lesser health potion, regenerate 10hp'
            self.img = pygame.image.load('data/assets/sprites/health_potion.png')
        elif type == 'message':
            self.description = text
            self.img = pygame.image.load('data/assets/sprites/message.png')
        elif type == 'bomb':
            self.description = text
            bomb_sheet = Spritesheet('data/assets/sprites/spritesheet.png')
            self.img = bomb_sheet.parse_sprite('bomb_1')

        self.available = False
        self.level = level
        self.type = type

    def update(self, level):
        if self.level == level:
            self.available = True
        else:
            self.available = False

    def draw(self, display, camera):
        if self.available is True:
            display.blit(self.img, (self.rect.x - camera.x, self.rect.y - camera.y))


class ItemSlot:

    def __init__(self, pos, _id, player, window):

        self.id = _id
        self.empty = True
        self.description = 'EMPTY SLOT'
        self.selected = False

        self.stored = 0
        self.capacity = 16

        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
        self.img = None
        self.color = (64, 0, 0)
        self.font_size = 12

        self.player = player
        self.type = None

        self.draw_info = False
        self.info_rect = pygame.Rect(0, 0, window[0] / 8, window[1] / 8)
        self.info_rect.center = (window[0] / 4, window[1] * .4)

    def use(self, chest=False, take_all=False):

        if self.type == 'lesser_health_potion':
            if chest is False:
                self.player.heal(10)
            if take_all is True:
                self.stored = 0
                self.img = None
                self.empty = True
            else:
                self.stored -= 1
                if self.stored <= 0:
                    self.img = None
                    self.empty = True

        elif self.type == 'message':
            if chest is True:
                self.stored -= 1
                if self.stored <= 0:
                    self.img = None
                    self.empty = True
            else:
                temp = self.draw_info
                self.draw_info = not temp

        elif self.type == 'bomb':
            if chest is True:
                if take_all is True:
                    self.stored = 0
                    self.img = None
                    self.empty = True
                else:
                    self.stored -= 1
                    if self.stored <= 0:
                        self.img = None
                        self.empty = True

    def update(self):

        if self.selected is True:
            self.color = (0, 128, 0)
        else:
            self.color = (64, 0, 0)

        if self.empty is True:
            self.description = 'EMPTY SLOT'

    def draw(self, display, font, camera=(0, 0)):

        temp_rect = pygame.Rect(self.rect.x - camera[0], self.rect.y - camera[1], self.rect.width, self.rect.height)

        pygame.draw.rect(display, self.color, temp_rect, border_bottom_left_radius=10, border_top_right_radius=10)
        if self.img is not None:
            display.blit(self.img, (self.rect.x - camera[0], self.rect.y - camera[1]))
            draw_text((self.rect.centerx - camera[0], self.rect.centery - camera[1]), 'topleft', str(self.stored), display, (18, 18, 18), font, self.font_size)

            if self.draw_info is True:
                # pygame.draw.rect(display, (0, 255, 0), self.info_rect, border_radius=-10)
                draw_text(self.info_rect.center, 'center', self.description, display, (0, 0, 255), font, self.font_size)


class Chest:

    def __init__(self, pos, level, player, window):

        self.opened = False
        self.available = False
        self.sprite_sheet = Spritesheet('data/assets/sprites/chest.png')
        self.img = self.sprite_sheet.parse_sprite('front_closed')
        self.rect = self.img.get_rect()

        self.bg_color = (208, 208, 208)
        self.font_color = (51, 51, 51)

        self.rect.center = pos
        self.level = level

        self.item_rect = pygame.Rect(0, 0, 256, 48)
        self.item_rect.center = self.rect.topleft

        self.item_slots = 5
        self.items = []

        self.selected = 0
        self.move = False
        self.move_all = False

        x, y = self.item_rect.topleft
        _id = 0
        for i in range(self.item_slots):
            self.items.append(ItemSlot((x, y), _id, player, window))
            x += 48
            _id += 1

    def add_item(self, new_item):
        added = False
        for item in self.items:
            if item.description == new_item.description:
                item.stored += 1
                added = True
                break
        if added is False:
            for item in self.items:
                if item.empty is True:
                    item.empty = False
                    item.description = new_item.description
                    item.img = new_item.img
                    item.type = new_item.type
                    item.stored += 1
                    break

    def update(self, level, backpack):

        if self.level == level:
            self.available = True
        else:
            self.available = False

        if self.opened is False:
            self.img = self.sprite_sheet.parse_sprite('front_closed')
        else:
            self.img = self.sprite_sheet.parse_sprite('front_opened')

        if self.selected < 0:
            self.selected = self.item_slots - 1
        elif self.selected > self.item_slots - 1:
            self.selected = 0

        for item in self.items:
            if self.selected == item.id:
                item.selected = True
                item.update()
            else:
                item.selected = False
                item.update()

            if item.selected is True:
                if self.move is True:
                    item.empty = False
                    backpack.add_item(item)
                    item.use(True)
                    self.move = False
                elif self.move_all is True:
                    for i in range(item.stored):
                        backpack.add_item(item)
                    item.use(True, True)
                    self.move_all = False

    def draw(self, display, camera, font):
        if self.available:
            display.blit(self.img, (self.rect.x - camera.x, self.rect.y - camera.y))
            if self.opened is True:
                self.item_rect.center = (self.rect.centerx - camera.x, self.rect.centery - camera.y - 32)
                pygame.draw.rect(display, self.bg_color, self.item_rect, border_radius=10)
                pygame.draw.rect(display, self.font_color, self.item_rect, 2, border_radius=10)

                for item in self.items:
                    item.draw(display, font, (camera.x - 32, camera.y + 8))


class Equipment:

    def __init__(self, window, font, player):

        self.visible = False

        self.window_w = window[0] / 2
        self.window_h = window[1] / 2
        self.font = font
        self.font_size = int(window[1] / 50)

        self.padding_top = self.window_h * .1
        self.padding_side = self.window_w * .1
        self.spacing_top = self.window_h * .02
        self.spacing_side = self.window_w * .02

        self.equipment_surface = pygame.Surface((200, 200))
        self.equipment_surface.fill((0, 128, 0))
        self.bg_rect = pygame.Rect(self.padding_side, self.window_h,
                                   self.window_w - 2 * self.padding_side, self.window_h - 2 * self.padding_top)

        self.bg_color = (208, 208, 208)
        self.font_color = (51, 51, 51)

        # menu

        self.side_menu = [['STATS', 0], ['ITEMS', 1]]
        self.menu_position = 0
        self.use = False

        # items

        self.item_slots = 20
        self.items = []
        self.in_line = 0

        x = self.bg_rect.x + self.bg_rect.width * .2 + self.spacing_side
        y = self.bg_rect.y + self.spacing_top
        for item in range(self.item_slots):
            self.items.append(ItemSlot((x, y), item, player, window))

            x += 32 + self.spacing_side
            if x >= self.padding_side + self.bg_rect.width * .8:
                x = self.bg_rect.x + self.bg_rect.width * .2 + self.spacing_side
                y += 32 + self.spacing_top

        self.selected = 0
        self.item_size = 32

        self.move_tick = pygame.time.get_ticks()

        # stats

        self.coins = player.coins
        self.level = player.level
        self.bomb_number = 0

    def add_item(self, new_item):
        added = False
        for item in self.items:
            if item.description == new_item.description:
                item.stored += 1
                added = True
                break
        if added is False:
            for item in self.items:
                if item.empty is True:
                    item.empty = False
                    item.description = new_item.description
                    item.img = new_item.img
                    item.type = new_item.type
                    item.stored += 1
                    break

    def empty_slots_number(self):
        number = 0
        for item in self.items:
            if item.empty is True:
                number += 1

        return number

    def update(self, player, dt):

        self.coins = player.coins
        self.level = player.level

        if self.menu_position >= len(self.side_menu):
            self.menu_position = 0
        if self.menu_position < 0:
            self.menu_position = len(self.side_menu) - 1

        if self.selected >= self.item_slots:
            self.selected = 0
        if self.selected < 0:
            self.selected = self.item_slots - 1

        temp = 0
        for item in self.items:
            if self.selected == item.id:
                item.selected = True
                item.update()
            else:
                item.draw_info = False
                item.selected = False
                item.update()

            if item.selected is True:
                if self.use is True:
                    item.use()
                    self.use = False

            if item.type == 'bomb':
                temp += item.stored

        self.bomb_number = temp

        if dt > 50:
            dt = 1

        if self.visible is True:
            if self.bg_rect.y >= self.padding_top:
                self.bg_rect.y -= 5 * dt

                for item in self.items:
                    item.rect.y -= 5 * dt
        else:
            if self.bg_rect.y <= self.window_h:
                self.bg_rect.y += 5 * dt
                for item in self.items:
                    item.rect.y += 5 * dt

    def draw(self, display):
        if self.bg_rect.y <= self.window_h:

            pygame.draw.rect(display, self.bg_color, self.bg_rect, border_radius=20)
            pygame.draw.rect(display, self.font_color, self.bg_rect, 5, border_radius=20)
            pygame.draw.line(display, self.font_color, (self.bg_rect.left + self.bg_rect.width * .15, self.bg_rect.top + self.spacing_top),
                             (self.bg_rect.left + self.bg_rect.width * .15, self.bg_rect.bottom - self.spacing_top), 2)

            y = self.bg_rect.y + self.spacing_top
            for text in self.side_menu:

                if text[1] == self.menu_position:
                    color = (128, 0, 0)
                else:
                    color = self.font_color
                draw_text((self.bg_rect.x + self.spacing_side, y), 'topleft',
                          text[0], display, color, self.font, self.font_size)
                y += 16 + self.spacing_top

            if self.menu_position == 0:
                draw_text((self.bg_rect.x + self.bg_rect.width * .2 + self.spacing_side, self.bg_rect.y + self.spacing_top),
                          'topleft',
                          'COINS: ' + str(self.coins), display, self.font_color, self.font, self.font_size)

                draw_text(
                    (self.bg_rect.x + self.bg_rect.width * .2 + self.spacing_side,
                     self.bg_rect.y + 16 + 2 * self.spacing_top),
                    'topleft',
                    'LEVEL: ' + str(self.level), display, self.font_color, self.font, self.font_size)

                draw_text(
                    (self.bg_rect.x + self.bg_rect.width * .2 + self.spacing_side,
                     self.bg_rect.y + 32 + 2 * self.spacing_top),
                    'topleft',
                    'BOMBS: ' + str(self.bomb_number), display, self.font_color, self.font, self.font_size)

            elif self.menu_position == 1:
                for item in self.items:
                    item.draw(display, self.font)


def draw_text(pos, pos_placement, text, display, color, font, font_size):
    font = pygame.font.Font(font, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if pos_placement == 'topleft':
        text_rect.topleft = pos
    elif pos_placement == 'topright':
        text_rect.topright = pos
    elif pos_placement == 'center':
        text_rect.center = pos

    display.blit(text_surface, text_rect)
