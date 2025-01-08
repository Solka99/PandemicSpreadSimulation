import pygame
import pygame_gui


class UIManager:
    def __init__(self, screen_width, screen_height):

        self.manager = pygame_gui.UIManager((screen_width, screen_height))

        self.label_population = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 150), (200, 50)),
            text="Enter population number:",
            manager=self.manager,
        )
        self.input_population = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((300, 150), (200, 50)),
            manager=self.manager
        )
        self.label_infection_distance = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 250), (200, 50)),
            text="Enter infection distance:",
            manager=self.manager,
        )
        self.input_infection_distance = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((300, 250), (200, 50)),
            manager=self.manager
        )
        self.label_vaccinated_agents_number = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 350), (250, 50)),
            text="Enter vaccinated agents number:",
            manager=self.manager,
        )
        self.vaccinated_agents_number = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((300, 350), (200, 50)),
            manager=self.manager
        )
        self.confirm_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 450), (200, 50)),
            text="Confirm Settings",
            manager=self.manager
        )

        self.input_population.set_text("100")
        self.input_infection_distance.set_text("30")
        self.vaccinated_agents_number.set_text("30")

    def show_menu(self, screen):
        running = True
        clock = pygame.time.Clock()

        user_settings = {}

        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                self.manager.process_events(event)

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.confirm_button:
                            # Pobierz dane użytkownika
                            population = self.input_population.get_text()
                            infection_distance = self.input_infection_distance.get_text()
                            vaccinated_agents_number = self.vaccinated_agents_number.get_text()

                            user_settings = {
                                "population": int(population) if population.isdigit() else 100,
                                "infection_distance": float(infection_distance) if infection_distance.replace('.', '',
                                                                                                  1).isdigit() else 30,
                                "vaccinated_agents_number": int(vaccinated_agents_number) if vaccinated_agents_number.isdigit() else 50,
                            }
                            running=False

            self.manager.update(time_delta)

            screen.fill((0, 0, 0))
            self.manager.draw_ui(screen)
            pygame.display.update()

        return user_settings
