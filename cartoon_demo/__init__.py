# import pygame module in this program
import pygame
from speech.speech import Speech

colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'black': (0, 0, 0)
}

sign = lambda x: x and (1, -1)[x<0]

class GameObject():
    def __init__(self):
        pass

    def draw(self, win):
        pass

    def update(self):
        pass

    def handle_event(self, event):
        pass

class Square(GameObject):
    def __init__(self, pos, dimensions, color):
        self.pos = pos
        self.dimensions = dimensions
        self.vel = 10
        self.color = color
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.dragging = False

    def draw(self, win):
        # drawing object on screen which is rectangle here
        pygame.draw.rect(win, colors[self.color], (self.pos[0], self.pos[1], self.dimensions[0], self.dimensions[1]))

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                x, y = self.pos
                width, height = self.dimensions
                if x < mouse_x < (x+width) and y < mouse_y < (y+height):
                    self.dragging = True
                    self.drag_offset_x = x - mouse_x
                    self.drag_offset_y = y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.pos = mouse_x + self.drag_offset_x, mouse_y + self.drag_offset_y

class Fetcher(GameObject):
    def __init__(self, pos):
        self.pos = pos
        self.vel = 1
        self.color = 'black'
        self.carried = None
        self.target = None
        self.return_point = (200, 200)

    def draw(self, win):
        # drawing object on screen which is rectangle here
        pygame.draw.circle(win, colors[self.color], self.pos, 8)

    def move_towards(self, pos):
        x, y = self.pos
        t_x, t_y = pos
        x = x + sign(t_x-x) * min(self.vel, abs(t_x-x))
        y = y + sign(t_y-y) * min(self.vel, abs(t_y-y))
        self.pos = x, y

    def update(self):
        if self.target is not None:
            if self.carried is not None:
                if self.carried == self.target:
                    self.move_towards(self.return_point)
                    self.carried.pos = self.pos
                    if self.return_point == self.pos:
                        self.target = None
                        self.carried = None
                else:
                    self.carried = None
            else:
                self.move_towards(self.target.pos)
                if self.pos == self.target.pos:
                    self.carried = self.target
        else:
            self.move_towards(self.return_point)

def run():
    # activate the pygame library .
    # initiate pygame and give permission
    # to use pygame's functionality.
    pygame.init()

    # create the display surface object
    # of specific dimension..e(500, 500).
    win = pygame.display.set_mode((500, 500))

    # set the pygame window name
    pygame.display.set_caption("Cube Fetching")

    fetcher = Fetcher((200, 200))
    ro = Square((150, 100), (20, 20), 'red')
    go = Square((300, 100), (20, 20), 'green')

    objects = [ro, go, fetcher]

    speech = Speech()

    def handle_speech(msg):
        msg = msg.lower()
        if 'red' in msg:
            fetcher.target = ro

        if 'green' in msg:
            fetcher.target = go

    speech.add_listener(handle_speech)

    # Indicates pygame is running
    run = True

    # infinite loop
    while run:
        # creates time delay of 10ms
        pygame.time.delay(10)

        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get():

            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                # it will make exit the while loop
                run = False

            for object in objects:
                object.handle_event(event)

        # stores keys pressed
        for object in objects:
            object.update()

        # completely fill the surface object
        # with white colour
        win.fill((255, 255, 255))

        for object in objects:
            object.draw(win)

        # it refreshes the window
        pygame.display.update()

    # closes the pygame window
    pygame.quit()