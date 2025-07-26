# note: when i upgraded to python 3.13 everything broke.
import netsblox
import eNBy
import time
import random
import keyboard
import typing
import pygame
import pygame_gui

Client = netsblox.Client(project_name="hamburgler")
RoboScape = netsblox.RoboScape(client=Client)
print("Initialized RoboScape")
enby = eNBy.enby(Client, RoboScape, "37ac")

i = 0
robots = enby.getRobots()
print(robots)
for robot in robots:
    i += 1
    print(f"{i}: {robot}")

# init movement
# keyboard.on_press_key("up", lambda: enby.this.setSpeed(40, 40))
# keyboard.on_release_key("up", lambda: enby.this.stop())
# keyboard.on_press_key("down", lambda: enby.this.setSpeed(-40, -40))
# keyboard.on_release_key("down", lambda: enby.this.stop())
# keyboard.on_press_key("right", lambda: enby.this.setSpeed(20, -20))
# keyboard.on_release_key("right", lambda: enby.this.stop())
# keyboard.on_press_key("left", lambda: enby.this.setSpeed(-20, 20))
# keyboard.on_release_key("left", lambda: enby.this.stop())

# init gui i guess???
pygame.init()
pygame.display.set_caption("hamburgler <sylvyon@disroot.org>")
window_surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color("#000000"))
manager = pygame_gui.UIManager((800, 600))
# button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)), text='button1', manager=manager)

ScanAllButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0, 10, 75, 75), text="ScanAll", manager=manager
)
BeepAllButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0, 95, 75, 75), text="BeepAll", manager=manager
)
BeepOthersButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0, 180, 75, 75), text="BeepOthers", manager=manager
)
KillMineButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0, 265, 75, 75), text="KillMine", manager=manager
)
BeepMineButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0, 265+85, 75, 75), text="BeepMine", manager=manager
)
ListenAllButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0, 265+85+85, 75, 75), text="ListenAll", manager=manager
)

@Client.on_message()
def t(x): print(x)
@Client.on_message(enby.message.robotCommand, enby.message.robotMessage)
def y(x): print(x)

clock = pygame.time.Clock()
is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == ScanAllButton:
                robots = enby.getRobots()
                print(robots)
                print(f"Robot connected: {enby.this.connected()}")
            if event.ui_element == BeepAllButton:
                for robot in enby.getRobots():
                    enby.beep(robot, 100, random.randint(100, 4000))
            if event.ui_element == BeepOthersButton:
                for robot in enby.getOthers():
                    enby.beep(robot, 100, random.randint(100, 4000))
            if event.ui_element == KillMineButton:
                enby.setEncryption(enby.this.id, 'caesar', 3)
            if event.ui_element == BeepMineButton:
                enby.this.beep(100, 300)
            if event.ui_element == ListenAllButton:
                enby.roboscape.listen(enby.roboscape.get_robots())
        manager.process_events(event)
    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    pygame.display.update()
pygame.quit()
