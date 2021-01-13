import pygame


class Terminal:
    def __init__(self, w, h):
        self.use = False
        self.locked = True
        self.python = False

        self.screen_w = w / 2
        self.screen_h = h / 2
        padding = 40
        self.border_size = 20
        self.screen = pygame.Rect(padding, padding, self.screen_w - 2 * padding, self.screen_h - 2 * padding)
        self.screen_border = pygame.Rect(padding, padding, self.screen_w - 2 * padding, self.screen_h - 2 * padding)

        self.padding = padding
        self.fans = False

        self.border_color = (27, 27, 27)
        self.screen_color = (0, 0, 0)
        self.font_color = (0, 255, 0)
        self.font_name = 'data/assets/fonts/bank_gothic.ttf'
        self.font_size = 16

        self.input = 0
        self.lines = []
        self.previous_commands = ['FANS --TURN OFF']
        self.command_number = 0
        self.cursor = '_'
        self.cursor_pos = 0

        self.start_line = 'PASSWORD: '
        self.current_line = 'PASSWORD: '
        self.passwd = 'PASSWORD14'
        self.input_passwd = ''

    def update_terminal(self):
        if 122 >= self.input >= 97:
            sign = chr(self.input - 32)
            if self.locked is True:
                self.current_line += '*'
                self.input_passwd += sign
            else:
                self.current_line += sign
        elif 57 >= self.input >= 48 or self.input == 32:
            sign = chr(self.input)
            if self.locked is True:
                self.current_line += '*'
                self.input_passwd += sign
            else:
                self.current_line += sign
        # backspace
        elif self.input == 8:
            if self.current_line != self.start_line:
                temp = self.current_line[0:-1]
                self.current_line = temp
                temp = self.input_passwd[0:-1]
                self.input_passwd = temp
            if self.current_line == '':
                temp = self.lines[-1]
                # !!!
                self.current_line = temp[0:-1]
                self.lines.pop(-1)
        # enter
        elif self.input == 13:
            self.lines.append(self.current_line)
            if self.locked is False and self.python is False:
                n = len(self.start_line)
                self.previous_commands.append(self.current_line[n:])
            self.check_command()
            self.current_line = self.start_line
            self.command_number = 0

        elif self.input == 45:
            self.current_line += chr(45)
        # arrows
        elif self.input == 1073741906:
            if len(self.previous_commands) != 0:
                if abs(self.command_number) != len(self.previous_commands):
                    self.command_number -= 1
                self.current_line = self.start_line + self.previous_commands[self.command_number]

        elif self.input == 1073741905:
            if len(self.previous_commands) != 0:

                if self.command_number < -1:
                    self.command_number += 1
                    self.current_line = self.start_line + self.previous_commands[self.command_number]
                else:
                    self.command_number = 0
                    self.current_line = self.start_line

        elif self.input == 1073741904:
            # left arrow
            pass
        elif self.input == 1073741903:
            # right arrow
            pass
        else:
            if self.input != 0:
                print(self.input)

        self.input = 0

    def check_command(self):
        if self.locked is True:
            if self.input_passwd != self.passwd:
                self.lines.append('INCORRECT')
                self.input_passwd = ''
                print(self.input_passwd)
            else:
                self.lines.append('CORRECT')
                self.locked = False
                self.start_line = 'ROOT:~$ '
        else:
            if self.python is True:
                pass
            else:
                n = len(self.start_line)
                command = self.current_line[n:]
                if command == 'CLEAR':
                    self.lines.clear()
                elif command == 'PYTHON3':
                    self.python = True
                    self.start_line = '>>> '
                elif command == 'FANS --TURN ON':
                    self.lines.append('FANS ONLINE')
                    self.fans = True
                else:
                    self.lines.append('UNKNOWN COMMAND')

    def draw_terminal(self, display):
        pygame.draw.rect(display, self.screen_color, self.screen)
        pygame.draw.rect(display, self.border_color, self.screen_border, self.border_size)
        self.draw_text(self.current_line, self.font_size, 50, 50, display)

    def draw_text(self, text, size, x, y, display):

        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.font_color)
        text_rect = text_surface.get_rect()
        text_rect.x = x

        n = 0
        for line in self.lines:
            line_surface = font.render(line, True, self.font_color)
            line_rect = line_surface.get_rect()
            line_rect.x = x
            line_rect.y = y + self.font_size * n
            display.blit(line_surface, line_rect)
            n += 1

        text_rect.y = y + self.font_size * n

        if text_rect.width >= self.screen.width - 2 * self.border_size - 10:
            self.lines.append(self.current_line)
            self.current_line = ''
        if text_rect.bottom >= self.screen_h - 2 * self.border_size:
            self.lines.pop(0)

        display.blit(text_surface, text_rect)
