from Colors import *
from Button import *

class SelectPage():
    def __init__(self, screen, setting):
        self.screen = screen
        self.setting = setting

        self.btn_choice_server = Button(0.5, 0.4, 200, 50, "Server")
        self.btn_choice_client = Button(0.5, 0.5, 200, 50, "Client")

    def running(self):
        selected_idx = None    

        while True:
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_choice_server.rect.collidepoint(event.pos):
                        return "multi_lobby", True
                    if self.btn_choice_client.rect.collidepoint(event.pos):
                        return "multi_setting"

            self.btn_choice_server.process(self.screen)
            pygame.draw.rect(self.screen, BLACK, self.btn_choice_server.rect, 2)
            self.btn_choice_client.process(self.screen)
            pygame.draw.rect(self.screen, BLACK, self.btn_choice_client.rect, 2)

            pygame.display.update()
