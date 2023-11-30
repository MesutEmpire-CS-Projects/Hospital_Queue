import random

import pygame

from AdaptableHeapPriorityQueue import AdaptableHeapPriorityQueue
from PriorityQueue import Empty

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1440, 960
RECEPTION_WIDTH = 50
IMAGE_PATH = ['patient-male.png', 'patient-female.png']
PATIENT_HEIGHT = 100

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hospital Queue")
font = pygame.font.Font('freesansbold.ttf', 20)

# Initialize the Queue
hospital_queue = AdaptableHeapPriorityQueue()


# 1. The Button class
class Button:
    def __init__(self, name, x, y):
        self._name = name
        self._width = 150
        self._height = 50
        self._rect = pygame.rect.Rect(x, y, self._width, self._height)
        self._enabled = True

    def draw(self):
        pygame.draw.rect(screen, 'black', self._rect, 2)
        text = font.render(self._name, True, 'black')
        screen.blit(text, (self._rect.centerx - text.get_width() // 2, self._rect.centery - text.get_height() // 2))

    def is_clicked(self, mouse_pos):
        return self._rect.collidepoint(mouse_pos)

    def get_name(self):
        return self._name


# 2. The Display Class
class Display:
    def __init__(self):
        self.input = {'name': "", 'age': None}
        self._result = None
        self._color = 'black'
        self._rect = pygame.Rect(50, 300, 200, 50)

    def show(self):
        tag = "Result: " if self._color is not 'red' else 'Error:'
        text = font.render(str(tag) + str(self._result), True, self._color)
        text_rect = pygame.Rect(WIDTH // 2, HEIGHT * 1 / 5, 300, 50)
        screen.blit(text, text_rect)

    def set_result(self, info, color='black'):
        self._result = info
        self._color = color

    def reset_result(self):
        self._result = None

    def get_result(self):
        return self._result


# 3. The Input Class
class Input:
    def __init__(self):
        self.patient_input = {'name': None, 'age': None, 'index': None, 'condition': None}
        self._input_rects = {'name': pygame.Rect(300, 100, 200, 50), 'age': pygame.Rect(300, 200, 200, 50),
                             'index': pygame.Rect(300, 300, 200, 50), 'condition': pygame.Rect(300, 400, 200, 50),
                             'label_name': pygame.Rect(30, 100, 250, 50), 'label_age': pygame.Rect(30, 200, 250, 50),
                             'label_index': pygame.Rect(30, 300, 250, 50),
                             'label_condition': pygame.Rect(30, 400, 250, 50),
                             'label_condition_explanation': pygame.Rect(30, 450, 250, 30)}
        self._labels = {}
        self.active = True

    def show(self):
        self._labels = {'label_name': font.render(f' Enter Patient Name: ', True, 'black'),
                        'label_age': font.render(f' Enter Patient Age: ', True, 'black'),
                        'label_condition': font.render(f' Enter Patient Condition:', True, 'black'),
                        'label_condition_explanation': pygame.font.Font('freesansbold.ttf', 14).render(
                            f'(CRITICAL = 0, SEVERE = 1, FAIR = 2)', True, 'black'),
                        'label_index': font.render(f' Enter Patient Index: ', True, 'black'),
                        'name': font.render(f'{self.patient_input["name"]}', True, 'black'),
                        'age': font.render(f' {str(self.patient_input["age"])} ', True, 'black'),
                        'condition': font.render(f' {str(self.patient_input["condition"])} ', True, 'black'),
                        'index': font.render(f' {str(self.patient_input["index"])} ', True, 'black')}
        for key, rect in self._input_rects.items():
            if key is not 'label_condition_explanation':
                pygame.draw.rect(screen, 'black', rect, 2)
                screen.blit(self._labels[key], (rect.centerx - self._labels[key].get_width() // 2,
                                                rect.centery - self._labels[key].get_height() // 2))
            else:
                screen.blit(self._labels[key], (rect.centerx - self._labels[key].get_width() // 2,
                                                rect.centery - self._labels[key].get_height() // 2))

    def get_input_name(self):
        return self.patient_input['name']

    def get_input_age(self):
        return self.patient_input['age']

    def get_input_index(self):
        return self.patient_input['index']

    def get_input_condition(self):
        return self.patient_input['condition']

    def reset_input(self):
        self.patient_input = {'name': None, 'age': None, 'index': None, 'condition': None}


# 4. The Patient Class
class Patient:
    def __init__(self, name, age, condition):
        self.index = random.randint(0, 1)
        self._name = name
        self._age = age
        self._condition = condition

    def draw(self, x, y):
        condition = None
        if self._condition == 0:
            condition = {'name': 'CRITICAL', 'color': 'red'}
        elif self._condition == 1:
            condition = {'name': 'SEVERE', 'color': 'orange'}
        elif self._condition == 2:
            condition = {'name': 'FAIR', 'color': 'blue'}
        image = pygame.image.load(IMAGE_PATH[self.index])
        image = pygame.transform.scale(image, (150, 110))
        screen.blit(image, (x, y, 5, 150))
        label_name = font.render(str(self._name), True, 'black')
        label_name_rect = pygame.rect.Rect(x + 65, y - 40, 40, 30)
        label_condition = pygame.font.Font('freesansbold.ttf', 14).render(str(condition['name']), True,
                                                                          condition['color'])
        label_condition_rect = pygame.rect.Rect(x + 65, y - 20, 40, 30)
        screen.blit(label_name, label_name_rect)
        screen.blit(label_condition, label_condition_rect)

    def get_patient_name(self):
        return self._name

    def get_patient_age(self):
        return self._age

    def get_patient_condition(self):
        return self._condition

    def update_condition(self, condition):
        self._condition = condition
        return self


# 5. The Reception Class
class Reception:
    def __init__(self, x, y):
        self._x = x
        self.y = y

    def draw(self):
        image = pygame.image.load('desk.png')
        image = pygame.transform.scale(image, (700, 600))
        screen.blit(image, (self._x, self.y, 5, 500))


# Initialize the classes
reception = Reception(RECEPTION_WIDTH, HEIGHT * 1 / 3)
display_info = Display()
input_box = Input()

buttons = [Button('Add', 10, 10), Button('Remove min', 180, 10), Button('Min', 350, 10), Button('Is Empty', 520, 10),
           Button('Len', 690, 10), Button('Remove', 860, 10), Button('Update', 1030, 10)]


def add_patient():
    try:
        if x + 160 > WIDTH and y - 210 < HEIGHT * 1 / 3:
            display_info.set_result('The queue is full', 'red')
        elif input_box.get_input_name() and input_box.get_input_age() and input_box.get_input_condition() is not None:
            new_patient = Patient(input_box.get_input_name(), input_box.get_input_age(),
                                  input_box.get_input_condition())
            hospital_queue.add(new_patient.get_patient_condition(), new_patient)
            input_box.reset_input()
            display_info.reset_result()
        else:
            display_info.set_result('Input data is None', 'red')

    except Empty:
        display_info.set_result('Queue is empty', 'red')

    except Exception as e:
        display_info.set_result(f' {str(e)}', 'red')


def remove_min_patient():
    try:
        remove_patient = hospital_queue.remove_min()
        display_info.set_result(f'(Key : {remove_patient[0]}, Value : {remove_patient[1].get_patient_name()})')
        input_box.reset_input()
    except Empty:
        display_info.set_result(' Queue is empty', 'red')
    except Exception as e:
        display_info.set_result(f'{str(e)}', 'red')


def min():
    try:
        next_patient = hospital_queue.min()
        display_info.set_result(f'(Key : {next_patient[0]}, Value : {next_patient[1].get_patient_name()})')
        input_box.reset_input()
    except Empty:
        display_info.set_result(' Queue is empty', 'red')
    except Exception as e:
        display_info.set_result(f'{str(e)}', 'red')


def is_empty():
    try:
        is_queue_empty = hospital_queue.is_empty()
        if is_queue_empty:
            display_info.set_result('Queue is empty')
        else:
            display_info.set_result('Queue is not empty', 'black')
        input_box.reset_input()

    except Empty:
        display_info.set_result('Queue is empty', 'red')
    except Exception as e:
        display_info.set_result(f' {str(e)}', 'red')


def length():
    try:
        queue_length = len(hospital_queue)
        display_info.set_result(f'Length : {queue_length}')
        input_box.reset_input()
    except Empty:
        display_info.set_result('Queue is empty', 'red')
    except Exception as e:
        display_info.set_result(f'{str(e)}', 'red')


def remove_patient():
    try:
        if hospital_queue.is_empty():
            display_info.set_result("Queue is empty", 'red')
        elif input_box.get_input_index() is not None:
            patient_loc = hospital_queue.get_data()[input_box.get_input_index()]
            removed_patient = hospital_queue.remove(patient_loc)
            display_info.set_result(f'(Key : {removed_patient[0]}, Value : {removed_patient[1].get_patient_name()})')
            input_box.reset_input()
        else:
            display_info.set_result('Input index is None', 'red')
    except IndexError:
        display_info.set_result("Invalid Locator", 'red')
    except Empty:
        display_info.set_result('Queue is empty', 'red')
    except Exception as e:
        display_info.set_result(f' {str(e)}', 'red')


def update_queue():
    try:
        if hospital_queue.is_empty():
            display_info.set_result("Queue is empty", 'red')
        else:
            input_index = input_box.get_input_index()
            input_condition = input_box.get_input_condition()

            if input_index is not None and input_condition is not None:
                patient_loc = hospital_queue.get_data()[input_box.get_input_index()]

                if patient_loc is not None:
                    updated_patient = patient_loc._value.update_condition(input_condition)

                    hospital_queue.update(patient_loc, input_condition, updated_patient)
                    input_box.reset_input()
                    display_info.reset_result()
                else:
                    display_info.set_result(" Invalid Locator", 'red')
            else:
                display_info.set_result(' Input index or other details are None', 'red')

    except Empty:
        display_info.set_result(' Queue is empty', 'red')
    except Exception as e:
        display_info.set_result(f' {str(e)}', 'red')


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = pygame.mouse.get_pos()
            for button in buttons:
                if button.is_clicked(mouse_position):
                    if button.get_name() == 'Add':
                        add_patient()
                    elif button.get_name() == 'Remove min':
                        remove_min_patient()
                    elif button.get_name() == 'Min':
                        min()
                    elif button.get_name() == 'Is Empty':
                        is_empty()
                    elif button.get_name() == 'Len':
                        length()
                    elif button.get_name() == 'Remove':
                        remove_patient()
                    elif button.get_name() == 'Update':
                        update_queue()
        elif event.type == pygame.KEYDOWN and input_box.active:
            mouse_position = pygame.mouse.get_pos()
            if event.key == pygame.K_RETURN:
                input_box.active = False
            elif event.key == pygame.K_BACKSPACE:
                if input_box._input_rects['name'].collidepoint(mouse_position):
                    temp_name = input_box.patient_input["name"]
                    input_box.patient_input["name"] = temp_name[:-1] if type(temp_name) is not None else None
                elif input_box._input_rects['age'].collidepoint(mouse_position):
                    temp_age = str(input_box.patient_input["age"]) if input_box.patient_input["age"] is not None else ''
                    temp_age = temp_age[:-1]
                    input_box.patient_input["age"] = int(temp_age) if len(temp_age) > 0 else None
                elif input_box._input_rects['index'].collidepoint(mouse_position):
                    temp_index = str(input_box.patient_input["index"]) if input_box.patient_input[
                                                                              "index"] is not None else ''
                    temp_index = temp_index[:-1]
                    input_box.patient_input["index"] = int(temp_index) if len(temp_index) > 0 else None
                elif input_box._input_rects['condition'].collidepoint(mouse_position):
                    temp_condition = str(input_box.patient_input["condition"]) if input_box.patient_input[
                                                                                      "condition"] is not None else ''
                    temp_condition = temp_condition[:-1]
                    input_box.patient_input["condition"] = int(temp_condition) if len(temp_condition) > 0 else None

            else:
                if input_box._input_rects['name'].collidepoint(mouse_position):
                    temp_name = input_box.patient_input["name"] if input_box.patient_input["name"] is not None else ''
                    temp_name += event.unicode
                    input_box.patient_input["name"] = temp_name
                elif input_box._input_rects['age'].collidepoint(mouse_position):
                    try:
                        temp_age = str(input_box.patient_input["age"]) if input_box.patient_input[
                                                                              "age"] is not None else ''
                        temp_age += event.unicode
                        input_box.patient_input["age"] = int(temp_age)
                        display_info.reset_result()
                    except ValueError:
                        display_info.set_result('Enter an Integer for the age', 'red')
                elif input_box._input_rects['index'].collidepoint(mouse_position):
                    try:
                        temp_index = str(input_box.patient_input["index"]) if input_box.patient_input[
                                                                                  "index"] is not None else ''
                        temp_index += event.unicode
                        input_box.patient_input["index"] = int(temp_index)
                        display_info.reset_result()
                    except ValueError:
                        display_info.set_result('Enter an Integer for the index', 'red')
                elif input_box._input_rects['condition'].collidepoint(mouse_position):
                    try:
                        temp_condition = str(input_box.patient_input["condition"]) if input_box.patient_input[
                                                                                          "condition"] is not None else ''
                        temp_condition = event.unicode if int(event.unicode) in [0, 1, 2] else ''
                        input_box.patient_input["condition"] = int(temp_condition)
                        display_info.reset_result()
                    except ValueError:
                        display_info.set_result('Enter 0, 1, or 2 for the condition', 'red')

    screen.fill('white')

    # Draw buttons
    for button in buttons:
        button.draw()
    input_box.show()

    if display_info.get_result():
        display_info.show()

    reception.draw()

    # Draw the patients
    global x
    x = WIDTH // 2
    global y
    y = HEIGHT * 5 / 6

    for patient in hospital_queue:
        if x + 160 > WIDTH:
            x = WIDTH // 2
            y -= 150
            patient._value.draw(x, y)
            x += 160
        else:
            patient._value.draw(x, y)
            x += 160

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
