import random

import pygame

from PriorityQueue import Empty

import threading

from AdaptableHeapPriorityQueue import AdaptableHeapPriorityQueue

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1440, 960
CANDY_SIZE = (90, 35)
SPRING_WIDTH = 50
SPRING_HEIGHT = (HEIGHT * 3 / 4 - 40)
EXTENSION = CANDY_SIZE[1]
IMAGE_PATH = ['patient-male.png', 'patient-female.png']
PATIENT_HEIGHT = 100

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hospital Queue")
font = pygame.font.Font('freesansbold.ttf', 20)

# Initialize the Stack
hospital_queue = AdaptableHeapPriorityQueue()


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


class Display:
    def __init__(self):
        self.input = {
            'name': "",
            'age': None
        }
        self._result = None
        self._color = 'black'
        self._rect = pygame.Rect(50, 300, 200, 50)

    def show(self):
        text = font.render("Result: " + str(self._result), True, self._color)
        text_rect = pygame.Rect(WIDTH // 2, HEIGHT * 1 / 5, 300, 50)
        screen.blit(text, text_rect)

    def set_result(self, info, color='black'):
        self._result = info
        self._color = color

    def reset_result(self):
        self._result = None

    def get_result(self):
        return self._result


class Input:
    def __init__(self):
        self.patient_input = {
            'name': None,
            'age': None,
            'index':None
        }
        self._input_rects = {
            'name': pygame.Rect(300, 100, 200, 50),
            'age': pygame.Rect(300, 200, 200, 50),
            'index': pygame.Rect(300, 300, 200, 50),
            'label_name': pygame.Rect(50, 100, 200, 50),
            'label_age': pygame.Rect(50, 200, 200, 50),
            'label_index': pygame.Rect(50, 300, 200, 50)
        }
        self._labels = {
            'label_name': font.render(f' Enter Patient Name: ', True, 'black'),
            'label_age': font.render(f' Enter Patient Age: ', True, 'black'),
            'label_index': font.render(f' Enter Patient Index: ', True, 'black'),
            'name': font.render(f'{self.patient_input["name"]}', True, 'black'),
            'age': font.render(f' {self.patient_input["age"]} ', True, 'black'),
            'index': font.render(f' {self.patient_input["index"]} ', True, 'black')
        }
        self.active = True

    def show(self):
        self._labels = {
            'label_name': font.render(f' Enter Patient Name: ', True, 'black'),
            'label_age': font.render(f' Enter Patient Age: ', True, 'black'),
            'label_index': font.render(f' Enter Patient Index: ', True, 'black'),
            'name': font.render(f'{self.patient_input["name"]}', True, 'black'),
            'age': font.render(f' {str(self.patient_input["age"])} ', True, 'black'),
            'index': font.render(f' {str(self.patient_input["index"])} ', True, 'black')
        }
        for key, rect in self._input_rects.items():
            pygame.draw.rect(screen, 'black', rect, 2)
            screen.blit(self._labels[key], (
                rect.centerx - self._labels[key].get_width() // 2, rect.centery - self._labels[key].get_height() // 2))

    def get_input_name(self):
        return self.patient_input['name']

    def get_input_age(self):
        return self.patient_input['age']

    def get_input_index(self):
        return self.patient_input['index']


    def reset_input(self):
        self.patient_input = {
            'name': None,
            'age': None,
            'index':None
        }


class Patient:
    def __init__(self, age, name):
        self.index = random.randint(0, 1)
        self._name = name
        self._age = age

    def draw(self, x, y):
        image = pygame.image.load(IMAGE_PATH[self.index])
        image = pygame.transform.scale(image, (150, 110))
        screen.blit(image, (x, y, 5, 150))
        label_name = font.render(str(self._name), True, 'black')
        label_name_rect = pygame.rect.Rect(x + 65, y - 20, 40, 30)
        label_age = font.render(str(self._age), True, 'black')
        label_age_rect = pygame.rect.Rect(x + 65, y - 40, 40, 30)
        screen.blit(label_name, label_name_rect)
        screen.blit(label_age, label_age_rect)

    def get_patient_name(self):
        return self._name

    def get_patient_age(self):
        return self._age


class Reception:
    def __init__(self, x, y):
        self._x = x
        self.y = y

    def draw(self):
        image = pygame.image.load('desk.png')
        image = pygame.transform.scale(image, (700, 600))
        screen.blit(image, (self._x, self.y, 5, 500))


reception = Reception(SPRING_WIDTH, HEIGHT * 1 / 5)
display_info = Display()
input_box = Input()

buttons = [Button('Add', 10, 10), Button('Remove min', 180, 10), Button('Min', 350, 10), Button('Is Empty', 520, 10),
           Button('Len', 690, 10), Button('Remove', 860, 10), Button('Update', 1030, 10)]


def add_patient():
    try:
        if x + 160 > WIDTH and y + 210 > HEIGHT:
            display_info.set_result('Error: The queue is full', 'red')
        elif input_box.get_input_name() and input_box.get_input_age():
            new_patient = Patient(input_box.get_input_name(), input_box.get_input_age())
            print(f'ADD-patient key: {input_box.get_input_age()} and Value : {new_patient}')
            hospital_queue.add(input_box.get_input_age(), new_patient)
            input_box.reset_input()
            display_info.reset_result()
        else:
            display_info.set_result('Error input data is None', 'red')

    except Empty:
        display_info.set_result('Error in adding patient', 'red')


def remove_min_patient():
    try:
        remove_patient = hospital_queue.remove_min()
        print(remove_patient[0])
        print(remove_patient[1].get_patient_name())
        print(remove_patient[1].get_patient_age())
        display_info.set_result(f'(Key : {remove_patient[0]}, Value : {remove_patient[1].get_patient_age()})')
    except Empty:
        display_info.set_result('Error removing the next patient', 'red')


def min():
    try:
        next_patient = hospital_queue.min()
        display_info.set_result(f'(Key : {next_patient[0]}, Value : {next_patient[1]._age})')
    except Empty:
        display_info.set_result('Error in determining the next patient', 'red')


def is_empty():
    try:
        is_queue_empty = hospital_queue.is_empty()
        display_info.set_result(f'{is_queue_empty}')
    except Empty:
        display_info.set_result('Error in determining if the queue is empty patient', 'red')


def length():
    try:
        queue_length = len(hospital_queue)
        display_info.set_result(f'Length : {queue_length}')
    except Empty:
        display_info.set_result('Error in determining the length of the queue', 'red')


def remove_patient():
    try:
        if hospital_queue.is_empty():
            display_info.set_result("Error: Queue is empty", 'red')
        elif input_box.get_input_index():
            patient_loc = hospital_queue._data[input_box.get_input_index()]
            removed_patient = hospital_queue.remove(patient_loc)
            # print(f"Removed Patient: Age - {removed_patient[0]}, Name - {removed_patient[1][1]}")
            display_info.set_result(f'(Key : {removed_patient[0]}, Value : {removed_patient[1].get_patient_age()})')
            # display_info.set_result(f"Removed Patient: Age - {removed_patient[0]}, Name - {removed_patient[1]._name}")
        else:
            display_info.set_result('Error input index is None', 'red')
    except IndexError:
        # print("Invalid Locator or Queue is empty")
        display_info.set_result("Error : Invalid Locator", 'red')
    except Empty:
        display_info.set_result('Error in removing patient from the queue', 'red')




def update_queue():
    try:
        if hospital_queue.is_empty():
            display_info.set_result("Error: Queue is empty", 'red')
        elif input_box.get_input_index() and input_box.get_input_name() and input_box.get_input_age():
            patient_loc = hospital_queue._data[input_box.get_input_index()]
            new_patient = Patient(input_box.get_input_name(), input_box.get_input_age())
            hospital_queue.update(patient_loc,input_box.get_input_age(), new_patient)
            input_box.reset_input()
            input_box.reset_input()
        else:
            display_info.set_result('Error input index is None', 'red')
    except IndexError:
        # print("Invalid Locator or Queue is empty")
        display_info.set_result("Error : Invalid Locator", 'red')
    except Empty:
        display_info.set_result('Error in removing patient from the queue', 'red')

    # try:
    #     old_age, patient = hospital_queue.min()
    #     hospital_queue.update(locator, new_age, (new_age, patient[1]))
    #     print(f"Updated priority for Patient: {patient[1]} - New Age: {new_age}")
    # except ValueError:
    #     print("Invalid Locator or Queue is empty")


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
                    temp_index = str(input_box.patient_input["index"]) if input_box.patient_input["index"] is not None else ''
                    temp_index = temp_index[:-1]
                    input_box.patient_input["index"] = int(temp_index) if len(temp_index) > 0 else None
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
                        display_info.set_result('Error: Enter an Integer for the age', 'red')
                elif input_box._input_rects['index'].collidepoint(mouse_position):
                    try:
                        temp_index = str(input_box.patient_input["index"]) if input_box.patient_input[
                                                                              "index"] is not None else ''
                        temp_index += event.unicode
                        input_box.patient_input["index"] = int(temp_index)
                        display_info.reset_result()
                    except ValueError:
                        display_info.set_result('Error: Enter an Integer for the index', 'red')

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
    y = HEIGHT * 1 / 3

    for patient in hospital_queue._data:
        # if y + 150 > HEIGHT:
        #     display_info.set_result('Error: The queue is full', 'red')
        if x + 160 > WIDTH:
            x = WIDTH // 2
            y += 150
            patient._value.draw(x, y)
            x += 160
            # display_info.reset_result()
        else:
            patient._value.draw(x, y)
            x += 160
            # display_info.reset_result()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
