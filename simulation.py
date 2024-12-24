import pygame
import pygame_gui
import random
import numpy as np
from dataclasses import dataclass
from typing import List

# Инициализация pygame
pygame.init()

# Константы
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
ROAD_Y = WINDOW_HEIGHT - 200
CAR_WIDTH = 40
CAR_HEIGHT = 20

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

@dataclass
class Car:
    x: float  # позиция
    speed: float  # текущая скорость
    desired_speed: float  # желаемая скорость
    color: tuple  # цвет машины
    
    # Константы для каждой машины
    max_acceleration: float
    comfortable_deceleration: float
    min_gap: float  # минимальный промежуток между машинами
    reaction_time: float  # время реакции водителя



class TrafficSimulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Traffic Simulation")
        
        # Инициализация GUI
        self.gui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Параметры симуляции по умолчанию
        self.params = {
            'spawn_probability': 0.3,
            'min_speed': 2.0,
            'max_speed': 5.0,
            'max_acceleration': 2.0,
            'comfortable_deceleration': 2.0,
            'min_gap': 2.0,
            'reaction_time': 1.5
        }
        
        # Создание слайдеров
        self.sliders = {}
        self.labels = {}
        y_pos = 10
        
        # Слайдеры для каждого параметра
        self.slider_configs = {
            'spawn_probability': ('Вероятность', 0.0, 1.0),
            'min_speed': ('Мин. скорость', 0.0, 5.0),
            'max_speed': ('Макс. скорость', 2.0, 10.0),
            'max_acceleration': ('Ускорение', 0.5, 5.0),
            'comfortable_deceleration': ('Торможение', 0.5, 5.0),
            'min_gap': ('Промежуток', 1.0, 5.0),
            'reaction_time': ('Реакция', 0.5, 3.0)
        }
        
        for param, (label, min_val, max_val) in self.slider_configs.items():
            # Создаем подпись
            self.labels[param] = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((10, y_pos), (150, 20)),
                text=f"{label}: {self.params[param]:.1f}",
                manager=self.gui_manager
            )
            
            # Создаем слайдер
            self.sliders[param] = pygame_gui.elements.UIHorizontalSlider(
                relative_rect=pygame.Rect((170, y_pos), (200, 20)),
                start_value=self.params[param],
                value_range=(min_val, max_val),
                manager=self.gui_manager
            )
            
            y_pos += 30
        
        # Кнопка сброса параметров
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, y_pos), (150, 30)),
            text='Сброс параметров',
            manager=self.gui_manager
        )
        

        # Добавляем параметры для определения пробки
        self.traffic_jam_detected = False
        self.jam_duration = 0
        self.jam_params = None
        
        # Параметры для определения пробки
        self.JAM_SPEED_THRESHOLD = 1.5  # Средняя скорость ниже этого значения
        self.JAM_DENSITY_THRESHOLD = 10  # Минимальное количество машин
        self.JAM_DETECTION_TIME = 180  # Количество кадров (3 секунды при 60 FPS)
        
        # Добавляем текстовое поле для отображения информации о пробке
        self.jam_info_label = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect((WINDOW_WIDTH - 400, 100), (350, 200)),
            manager=self.gui_manager
        )
        self.jam_info_label.hide()


        self.clock = pygame.time.Clock()
        self.cars: List[Car] = []
        self.running = True

    def spawn_car(self):
        """Создание новой машины"""
        if len(self.cars) == 0 or self.cars[-1].x > CAR_WIDTH * 2:
            if random.random() < self.params['spawn_probability']:
                desired_speed = random.uniform(self.params['min_speed'], self.params['max_speed'])
                color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                new_car = Car(
                    x=0,
                    speed=desired_speed,
                    desired_speed=desired_speed,
                    color=color,
                    max_acceleration=self.params['max_acceleration'],
                    comfortable_deceleration=self.params['comfortable_deceleration'],
                    min_gap=self.params['min_gap'],
                    reaction_time=self.params['reaction_time']
                )
                self.cars.append(new_car)

    def update_cars(self):
        """Обновление позиций и скоростей машин"""
        dt = 1/60
        
        for i, car in enumerate(self.cars):
            if i > 0:
                front_car = self.cars[i-1]
                gap = front_car.x - car.x - CAR_WIDTH
                
                safe_gap = (car.min_gap + 
                          max(0, car.speed * car.reaction_time +
                              (car.speed * (car.speed - front_car.speed)) /
                              (2 * np.sqrt(car.max_acceleration * car.comfortable_deceleration))))
                
                free_road_term = (1 - (car.speed / car.desired_speed) ** 4)
                interaction_term = (safe_gap / max(gap, 0.1)) ** 2
                acceleration = car.max_acceleration * (free_road_term - interaction_term)
            else:
                acceleration = car.max_acceleration * (1 - (car.speed / car.desired_speed) ** 4)
            
            car.speed = max(0, min(car.speed + acceleration * dt, car.desired_speed))
            car.x += car.speed * dt * 60

        self.cars = [car for car in self.cars if car.x < WINDOW_WIDTH]

    def check_traffic_jam(self):
        """Проверка наличия пробки"""
        if len(self.cars) >= self.JAM_DENSITY_THRESHOLD:
            avg_speed = np.mean([car.speed for car in self.cars])
            
            if avg_speed < self.JAM_SPEED_THRESHOLD:
                self.jam_duration += 1
                
                if self.jam_duration >= self.JAM_DETECTION_TIME and not self.traffic_jam_detected:
                    self.traffic_jam_detected = True
                    self.jam_params = self.params.copy()
                    self.show_jam_info()
            else:
                self.jam_duration = 0
                if self.traffic_jam_detected:
                    self.traffic_jam_detected = False
                    self.jam_info_label.hide()
        else:
            self.jam_duration = 0
            if self.traffic_jam_detected:
                self.traffic_jam_detected = False
                self.jam_info_label.hide()

    def show_jam_info(self):
        """Отображение информации о пробке"""
        info_text = "<b><font color='#FF0000'>Образовалась пробка!</font></b><br><br>"
        info_text += "<b>Параметры, приведшие к пробке:</b><br><br>"
        
        for param, value in self.jam_params.items():
            label = self.slider_configs[param][0]
            info_text += f"{label}: {value:.2f}<br>"
        
        info_text += f"<br>Количество машин: {len(self.cars)}"
        avg_speed = np.mean([car.speed for car in self.cars])
        info_text += f"<br>Средняя скорость: {avg_speed:.2f}"
        
        self.jam_info_label.html_text = info_text
        self.jam_info_label.rebuild()
        self.jam_info_label.show()

    def update_gui(self):
        """Обновление значений параметров из слайдеров"""
        for param, slider in self.sliders.items():
            self.params[param] = slider.get_current_value()
            self.labels[param].set_text(f"{self.slider_configs[param][0]}: {self.params[param]:.1f}")

    def draw(self):
        """Отрисовка всех элементов"""
        self.screen.fill(WHITE)
        
        # Рисуем дорогу
        pygame.draw.rect(self.screen, GRAY, (0, ROAD_Y - 40, WINDOW_WIDTH, 80))
        pygame.draw.line(self.screen, WHITE, (0, ROAD_Y), (WINDOW_WIDTH, ROAD_Y), 2)
        
        # Рисуем машины
        for car in self.cars:
            pygame.draw.rect(self.screen, car.color, 
                           (int(car.x), ROAD_Y - CAR_HEIGHT//2, CAR_WIDTH, CAR_HEIGHT))
        
        # Отображаем статистику
        font = pygame.font.Font(None, 36)
        stats = font.render(f"Машин на дороге: {len(self.cars)}", True, BLACK)
        avg_speed = np.mean([car.speed for car in self.cars]) if self.cars else 0
        speed_stats = font.render(f"Средняя скорость: {avg_speed:.1f}", True, BLACK)
        
        self.screen.blit(stats, (WINDOW_WIDTH - 250, 10))
        self.screen.blit(speed_stats, (WINDOW_WIDTH - 250, 50))
        
        # Отрисовка GUI
        self.gui_manager.draw_ui(self.screen)
        
        pygame.display.flip()

    def reset_params(self):
        """Сброс параметров к значениям по умолчанию"""
        default_params = {
            'spawn_probability': 0.3,
            'min_speed': 2.0,
            'max_speed': 5.0,
            'max_acceleration': 2.0,
            'comfortable_deceleration': 2.0,
            'min_gap': 2.0,
            'reaction_time': 1.5
        }
        
        for param, value in default_params.items():
            self.params[param] = value
            self.sliders[param].set_current_value(value)

    def run(self):
        """Основной цикл симуляции"""
        while self.running:
            time_delta = self.clock.tick(60)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.reset_button:
                            self.reset_params()
                            self.traffic_jam_detected = False
                            self.jam_duration = 0
                            self.jam_info_label.hide()
                
                self.gui_manager.process_events(event)

            self.gui_manager.update(time_delta)
            self.update_gui()
            self.spawn_car()
            self.update_cars()
            self.check_traffic_jam()
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    simulation = TrafficSimulation()
    simulation.run()