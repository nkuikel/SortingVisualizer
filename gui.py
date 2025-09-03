import pygame   # imports pygame for graphics
import time     # imports time to add delays
import random   # imports random to generate random numbers
import sys      # imports sys for system exit functions

from logic import SortAlgorithm   # imports the base sorting class
from util import parse_custom_input # imports helper to parse custom input

class Visualizer:
    def __init__(self, width=800, height=600, bg=(0,0,0)):
        '''
        this module initializes the visualizer class
        ''' 
        pygame.init()  # initializes all pygame modules
        self.width, self.height, self.bg = width, height, bg  # this line stores window size and background color
        self.screen = pygame.display.set_mode((width, height))  # this line creates the display window
        pygame.display.set_caption("Sorting Visualization with Speed Slider")  # this line sets the window title
        self.font = pygame.font.SysFont(None, 24)  # this line sets the font for text rendering
        self.clock = pygame.time.Clock()  # this line creates a clock to control frame rate
        self.buttons: list[tuple[pygame.Rect, str]] = []  # this line prepares a list for menu buttons
        self.sort_mode = 'random'  # this line sets default mode to random
        self.input_string = ''  # this line stores input string for custom numbers, initially it is empty string

        # slider state (speed control)
        self.slider_rect = pygame.Rect(50, 10, self.width - 100, 20)  # this is the slider track area
        self.knob_rect = pygame.Rect(0, 0, 10, self.slider_rect.h + 6)  # this is slider knob size
        self.reset_knob()  # this knob of the slider is initially centered
        self.dragging = False 

        # slider maps to speed [0.0, 2.0]
        self.speed = 1.0

        # delay = max_delay - speed
        self.max_delay = 2.0
        self.delay = self.max_delay - self.speed  # current delay calculation

    def reset_knob(self):
        '''
        this resets the knob position
        '''
        # this block centers the knob on init
        center_x = self.slider_rect.x + self.slider_rect.w // 2  # calculates center x position
        self.knob_rect.center = (center_x, self.slider_rect.centery)  # updates knob center

    def draw_slider(self): 
        '''
        this enders the slider on top of the sorting screen
        ''' 
        # this block draws the slider track and knob along with a text label
        pygame.draw.rect(self.screen, (100, 100, 100), self.slider_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), self.knob_rect)
        label = f"Speed: {self.speed:.2f}x"
        txt = self.font.render(label, True, (255,255,255))
        self.screen.blit(txt, (self.slider_rect.x, self.slider_rect.bottom + 5))

    def draw_bars(self, data: list[int], boundary: int, highlights: list[int] | None = None):
        '''
        this accepts the sort array data, boundary and positions to highlight and draw the corresponding bars at each time step
        '''
        # this block clears screen and draws bars
        self.screen.fill(self.bg)
        self.draw_slider()

        top_offset = self.slider_rect.bottom + 30
        n = len(data)
        bar_width = self.width / n
        max_val = max(data)  # this line finds maximum data value
        # this block loops through data values
        for i, val in enumerate(data):
            x = i * bar_width
            bar_height = (val / max_val) * (self.height - top_offset - 40)
            y = self.height - bar_height - 40
            if highlights and i in highlights:
                color = (255, 0, 0)  # highlight color
            elif i <= boundary:
                color = (0, 255, 0)  # sorted color
            else:
                color = (255, 255, 255)  # default bar color
            pygame.draw.rect(self.screen, color, (x, y, bar_width - 1, bar_height))
            val_txt = self.font.render(str(val), True, (255, 255, 255))
            self.screen.blit(val_txt, (x + bar_width/2 - val_txt.get_width()/2,
                                       y - val_txt.get_height()))
        pygame.display.flip()  # this line updates the display

    def handle_slider_events(self, event):
        '''
        A module to detect mouse events on slider area and update delay accordingly
        '''
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # check mouse down
            if self.knob_rect.collidepoint(event.pos) or self.slider_rect.collidepoint(event.pos):  # check click on slider
                self.dragging = True # starts dragging
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # check mouse up
            self.dragging = False # stops dragging
        elif event.type == pygame.MOUSEMOTION and self.dragging:  # check mouse move while dragging
            mx = event.pos[0]
            half_w = self.knob_rect.w // 2
            new_x = max(self.slider_rect.x, min(mx - half_w, self.slider_rect.right - self.knob_rect.w))
            self.knob_rect.x = new_x
            rel = (self.knob_rect.centerx - self.slider_rect.x) / self.slider_rect.w
            self.speed = rel * 2.0
            self.delay = max(0.0, self.max_delay - self.speed)  # this line updates delay

    def visualize(self, algorithm: SortAlgorithm):
        '''
        Renders the final visualization
        '''
        for data, boundary, highlights in algorithm.sort():  # this line iterates sorting steps
            for event in pygame.event.get():  # process events
                if event.type == pygame.QUIT:  # check quit event
                    pygame.quit(); sys.exit()  # this line quits program
                self.handle_slider_events(event)  # this line handles slider events
            self.draw_bars(data, boundary, highlights)  # draw the bars for each step
            time.sleep(self.delay)  #add delay between frames
        time.sleep(1)  # pause the sorted array screen for 1 second before returing to main menu

    def draw_menu(self, options: dict[str, type[SortAlgorithm]]):  # this line defines method to draw menu
        '''
        Renders the menu screen with all available options
        '''
        self.screen.fill(self.bg)
        title = self.font.render("Choose Sorting Algorithm", True, (255, 255, 255))
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 20))
        y = 80  # this line sets starting y for radio buttons
        for mode in ['random', 'custom']:  # this line loops radio options
            circle_color = (0, 200, 0) if self.sort_mode == mode else (200, 200, 200)
            pygame.draw.circle(self.screen, circle_color, (50, y), 10)
            label = 'Sort Random Numbers' if mode=='random' else 'Sort Custom Numbers'
            txt = self.font.render(label, True, (255,255,255))
            self.screen.blit(txt, (70, y-12))
            y += 30
        if self.sort_mode == 'custom':
            prompt_txt = self.font.render("Please enter the numbers separated by ','", True, (255,255,0))
            self.screen.blit(prompt_txt, (50, y + 5))
            rect = pygame.Rect(50, y + 30, 300, 30)
            pygame.draw.rect(self.screen, (255,255,255), rect, 2)
            txt = self.font.render(self.input_string, True, (255,255,255))
            self.screen.blit(txt, (rect.x+5, rect.y+2))
        btn_w, btn_h, gap = 300, 40, 15  # this line sets button dimensions and gap
        start_y = self.height//2  # this line sets buttons start y
        self.buttons.clear()  # this line clears any old buttons from previous sorting visualizations
        for idx, (name, _) in enumerate(options.items()):
            rect = pygame.Rect(self.width//2-btn_w//2,
                               start_y + idx*(btn_h+gap), btn_w, btn_h)
            pygame.draw.rect(self.screen, (100,100,100), rect)
            txt = self.font.render(name, True, (255,255,255))
            self.screen.blit(txt, (rect.x+10, rect.y+5))
            self.buttons.append((rect, name))
        rect = pygame.Rect(self.width//2-btn_w//2,
                           start_y + len(options)*(btn_h+gap), btn_w, btn_h)
        pygame.draw.rect(self.screen, (150,0,0), rect)
        txt = self.font.render("Exit", True, (255,255,255))
        self.screen.blit(txt, (rect.x+10, rect.y+5))
        self.buttons.append((rect, "Exit"))
        pygame.display.flip()  # this line updates menu display

    def menu_loop(self, options: dict[str, type[SortAlgorithm]]):  # this line defines menu loop method
        '''
        Runs the menu loop
        '''
        while True:
            self.draw_menu(options)  # this line draws menu at each frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if (mx-50)**2 + (my-80)**2 <= 10**2:
                        self.sort_mode = 'random'
                    if (mx-50)**2 + (my-110)**2 <= 10**2:
                        self.sort_mode = 'custom'
                    for rect, name in self.buttons:  # this line loops through the sorting algorithms buttons
                        if rect.collidepoint(event.pos):
                            if name == 'Exit':
                                pygame.quit(); sys.exit()
                            if self.sort_mode == 'random':
                                data = [random.randint(1,100) for _ in range(10)]
                            else:
                                data = parse_custom_input(self.input_string)  # this line calls the utility function to parse custom input
                            algorithm = options[name](data)
                            self.visualize(algorithm)  # this line starts visualization
                if event.type == pygame.KEYDOWN and self.sort_mode == 'custom':
                    if event.key == pygame.K_BACKSPACE:
                        self.input_string = self.input_string[:-1]
                    else:
                        char = event.unicode  # this line gets typed char
                        if char.isdigit() or char == ',':  # this line checks valid char (only numbers and comma are valid)
                            self.input_string += char
            self.clock.tick(30)  # this line limits to 30 FPS
