import pygame

pygame.init()

class Figure():

    w_screen_ = 1400 # базовое разрешение
    h_screen_ = 800 # базовое разрешение
    recalculation_flag = 1 # флаг отвечающий за версию разрешения
    screen = None
    base_font = pygame.font.SysFont("Arial", 36)

    @classmethod
    def get_flag(cls): # получение версии флага разрешения для дочерних классов

        return cls.recalculation_flag

    @classmethod
    def set_widescreen(cls, width, height): # обновление разрешения и изменение версии флага разрешения

        cls.w_screen_, cls.h_screen_ = width, height
        cls.recalculation_flag += 1

    @classmethod
    def set_screen(cls, screen, font):

        cls.screen = screen
        cls.base_font = font

class Links(Figure):

    start_x = 560
    start_y = 200
    w = 200
    h = 60
    subclass_flag = 0

    @classmethod
    def get_pos(cls): # получение стартовых координат для отрисовки

        return cls.start_x, cls.start_y

    @staticmethod
    def readlinks():  ### открывает файл со ссылками и создает список

        # открытие файла со ссылками
        with open("files//Links.txt", "r", encoding='utf-8') as urls:
            lines = [[]]  # список для объектов класса для отрисовки

            i = 0  # значение чтобы на одной странице отрисовывалось не больше 10 ссылок
            z = 0  # значение, которое отображает номер страницы

            x_pos, y_pos = Links.get_pos()  # получение начальных координат из класса

            for url in urls.readlines():  # перебор ссылок

                url = url.replace("\n", "")  # удаление ненужных пробелов

                if i == 10:  # 10 - максимальное кол-во отображаемых ссылок на одной странице

                    i = 0
                    z += 1
                    lines.append([])
                    y_pos = Links.get_pos()[1]

                url = Links(url)  # создание объекта класса
                lines[z].append(url)  # добавление этого объекта в список
                url.set_coordinates(x_pos, y_pos)
                y_pos += 40
                i += 1

        return lines  # возвращение двумерного списка с объектами класса Links

    @staticmethod
    def clear_search(links):

        lines = [[]]

        i = 0
        z = 0

        x_pos, y_pos = Links.get_pos()

        for x in links:

            for y in x:

                if i == 10:
                    i = 0
                    z += 1
                    lines.append([])
                    y_pos = Links.get_pos()[1]

                lines[z].append(y)
                y.set_coordinates(x_pos, y_pos)
                y_pos += 40
                i += 1

        return lines

    @staticmethod
    def search(links, text):

        lines = [[]]
        text = text.split()

        i = 0
        z = 0

        x_pos, y_pos = Links.get_pos()

        for x in links:

            for y in x:

                if i == 10:
                    i = 0
                    z += 1
                    lines.append([])
                    y_pos = Links.get_pos()[1]

                if isinstance(text, list):

                    for part in text:

                        y.search = True if part.lower() in y.url.lower() else False

                        if not y.search:
                            break

                if y.search:
                    lines[z].append(y)
                    y.set_coordinates(x_pos, y_pos)
                    y_pos += 40
                    i += 1

        return lines

    @staticmethod
    def all_flags(links):

        if not links[0][0].bool:

            for x in links:

                for y in x:
                    y.bool = True

        else:

            for x in links:

                for y in x:
                    y.bool = False

    @classmethod
    def draw(cls, lines, check_mark):  # список из объектов класса Links с одной страницы и их отрисовка

        if cls.recalculation_flag != cls.get_flag():

            cls.recalculation_flag = cls.get_flag()

        for link in lines:  # перебираем объекты класса Links в рамках одной страницы

            x_pos, y_pos = link.get_coordinates()
            pygame.draw.rect(Figure.screen, (0, 0, 0), pygame.Rect(x_pos - 50, y_pos, 40, 40), 2)

            if link.bool:  # проверка на знак того что отмечена галочка напротив маршрута

                Figure.screen.blit(check_mark, (x_pos - 50, y_pos))  # отрисовка галки

            Figure.screen.blit(Figure.base_font.render(link.text_name(), True, (0, 0, 0)),
                        (x_pos + 20, y_pos, 400, 50))  # отрисовка основного текста маршрута

    def __init__(self, url):

        self.url = str(url).strip()
        self.bool = False # необходим для отображения выбранных вариантов
        self.info = self.url.split("title=")[1].split("_") # разбивает ссылку на город, тип ОТ, номер ОТ
        self.city = self.info[0] # город
        self.type_ot = self.info[1] # тип ОТ
        self.number = self.info[2] # номер ОТ
        self.x = 0 # координаты для отрисовки
        self.y = 0 # координаты для отрисовки
        self.search = True # переключатель для отображения результата во время поиска
        self.recalculation_flag = 0 # флаг для пересчета размера и начальных координат

    def toggle(self): # переключает bool

        self.bool = not self.bool

    def set_coordinates(self, x, y): # установка координат для каждого объекта для отображения

        self.x = x
        self.y = y

    def get_coordinates(self): # получение координат

        return self.x, self.y

    def text_name(self): # получение текста для отрисовки

        return f"{self.city}_{self.type_ot}_{self.number}"

    def __str__(self):

        return f"{self.url}"

    def __repr__(self):

        return self.__str__()

class Button(Figure):

    def __init__(self, name, x_shift, size=(10, 10), coord=(0, 0),
                 color=(0, 0, 0), text_color=(0, 0, 0), y_shift = 5, border=0, border_color=(0, 0, 0)):

        self.name = name # текст кнопки
        self.x, self.y = coord
        self.w, self.h = size
        self.x_shift, self.y_shift = x_shift, y_shift # сдвиг текста кнопки
        self.color = color # цвет кнопки
        self.text_color = text_color # цвет текста
        self.w_screen_ = 1400  # базовое разрешение
        self.h_screen_ = 800  # базовое разрешение
        self.recalculation_flag = 0  # флаг версии разрешения
        self.border, self.border_color = border, border_color # толщина и цвет границы кнопки

    def draw(self):

        if self.recalculation_flag != self.get_flag(): # пересчет размеров и местоположения если оно глобально изменилось

            self.recalculating()

        # отрисовка границы
        if self.border:

            pygame.draw.rect(self.screen, self.border_color,
                             (self.x - self.border, self.y - self.border, self.w + self.border * 2,
                              self.h + self.border * 2))

        # отрисовка кнопки и текста на ней
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.w, self.h))
        Figure.screen.blit(Figure.base_font.render(self.name, True, self.text_color),
                           (self.x + self.x_shift, self.y + self.y_shift, self.w, self.h))

    def recalculating(self):

        # если сдвиг больше нуля, то применяется формула пересчета (((новый сдвиг) * новая ширина экрана) - (старая ширина кнопки - (старый сдвиг * 2))) / 2
        self.x_shift = self.x_shift if self.x_shift < 0 else (((self.w / self.w_screen_) * Figure.w_screen_) - (self.w - (self.x_shift * 2))) / 2

        # применяется формула пересчета (((новый сдвиг) * новая высота экрана) - (старая высота кнопки - (старый сдвиг * 2))) / 2
        self.y_shift = (((self.h / self.h_screen_) * Figure.h_screen_) - (self.h - (self.y_shift * 2))) / 2

        # пересчет высоты и ширины кнопки
        self.w = (self.w / self.w_screen_) * Figure.w_screen_
        self.h = (self.h / self.h_screen_) * Figure.h_screen_

        # пересчет координат кнопки
        self.x = self.x / self.w_screen_ * Figure.w_screen_
        self.y = self.y / self.h_screen_ * Figure.h_screen_

        # создание объекта Rect для отрисовки
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        # обновление данных разрешения экрана и версии флага объекта класса
        self.w_screen_ = Figure.w_screen_
        self.h_screen_ = Figure.h_screen_
        self.recalculation_flag = self.get_flag()

class Image_button(Figure):

    def __init__(self, name, size=(10, 10), coord=(0, 0),
                 color=(255, 255, 255), border=0, border_color=(0, 0, 0), image=None, background=False):
        self.name = name  # текст кнопки
        self.x, self.y = coord
        self.w, self.h = size
        self.color = color  # цвет кнопки
        self.w_screen_, self.h_screen_ = 1400, 800  # базовое разрешение
        self.recalculation_flag = 0  # флаг версии разрешения
        self.border, self.border_color = border, border_color  # толщина и цвет границы кнопки
        self.image = image
        self.background = background

    def draw(self):

        if self.recalculation_flag != self.get_flag(): # пересчет размеров и местоположения если оно глобально изменилось

            self.recalculating()

        # отрисовка границы
        if self.border:

            pygame.draw.rect(self.screen, self.border_color,
                             (self.x - self.border, self.y - self.border, self.w + self.border * 2,
                              self.h + self.border * 2))

        # отрисовка задника
        if self.background:

            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.w, self.h))

        # отрисовка каринки
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        Figure.screen.blit(self.image, self.rect)

    def recalculating(self):

        # пересчет высоты и ширины кнопки
        self.w = (self.w / self.w_screen_) * Figure.w_screen_
        self.h = (self.h / self.h_screen_) * Figure.h_screen_

        # пересчет координат кнопки
        self.x = self.x / self.w_screen_ * Figure.w_screen_
        self.y = self.y / self.h_screen_ * Figure.h_screen_

        # создание объекта Rect для отрисовки
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        # обновление данных разрешения экрана и версии флага объекта класса
        self.w_screen_ = Figure.w_screen_
        self.h_screen_ = Figure.h_screen_
        self.recalculation_flag = self.get_flag()

class Desk(Figure):

    def __init__(self, name, size=(10, 10), coord=(0, 0),
                 color=(255, 255, 255), border=0, border_color=(0, 0, 0)):

        self.name = name  # текст кнопки
        self.x, self.y = coord
        self.w, self.h = size
        self.color = color  # цвет кнопки
        self.w_screen_ = 1400  # базовое разрешение
        self.h_screen_ = 800  # базовое разрешение
        self.recalculation_flag = 0  # флаг версии разрешения
        self.border, self.border_color = border, border_color  # толщина и цвет границы кнопки

    def draw(self):

        if self.recalculation_flag != self.get_flag(): # пересчет размеров и местоположения если оно глобально изменилось

            self.recalculating()

        # отрисовка границы
        if self.border:

            pygame.draw.rect(self.screen, self.border_color,
                             (self.x - self.border, self.y - self.border, self.w + self.border * 2,
                              self.h + self.border * 2))

        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.w, self.h))

    def recalculating(self):

        # пересчет высоты и ширины кнопки
        self.w = (self.w / self.w_screen_) * Figure.w_screen_
        self.h = (self.h / self.h_screen_) * Figure.h_screen_

        # пересчет координат кнопки
        self.x = self.x / self.w_screen_ * Figure.w_screen_
        self.y = self.y / self.h_screen_ * Figure.h_screen_

        # создание объекта Rect для отрисовки
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        # обновление данных разрешения экрана и версии флага объекта класса
        self.w_screen_ = Figure.w_screen_
        self.h_screen_ = Figure.h_screen_
        self.recalculation_flag = self.get_flag()

class Text(Figure):

    def __init__(self, name, coord=(0, 0), text_color=(0, 0, 0), font=Figure.base_font):

        self.name = name  # текст кнопки
        self.x, self.y = coord
        self.w, self.h = 200, 40
        self.text_color = text_color  # цвет текста
        self.w_screen_ = 1400  # базовое разрешение
        self.h_screen_ = 800  # базовое разрешение
        self.recalculation_flag = 0  # флаг версии разрешения
        self.font = font # шрифт

    def draw(self):

        if self.recalculation_flag != self.get_flag(): # пересчет размеров и местоположения если оно глобально изменилось

            self.recalculating()

        # отрисовка текста
        Figure.screen.blit(self.font.render(self.name, True, self.text_color),
                           (self.x, self.y, self.w, self.h))

    def recalculating(self):

        # пересчет координат кнопки
        self.x = self.x / self.w_screen_ * Figure.w_screen_
        self.y = self.y / self.h_screen_ * Figure.h_screen_

        # обновление данных разрешения экрана и версии флага объекта класса
        self.w_screen_ = Figure.w_screen_
        self.h_screen_ = Figure.h_screen_
        self.recalculation_flag = self.get_flag()

    def get_coord(self):

        return self.x, self.y

class User_text(Figure):

    def __init__(self, size=(200, 40), coord=(0, 0), x_shift=10, color=(255, 255, 255),
                 text_color=(0, 0, 0), y_shift = 5,
                 border=0, border_color=(0, 0, 0),
                 font=Figure.base_font, color_active=(150, 80, 80), color_passive=pygame.Color("gray15")):

        self.input = False # флаг ввода текста
        self.x, self.y = coord # коориднаты
        self.w, self.h = size # размеры окна
        self.color = color # цвет окна
        self.x_shift, self.y_shift = x_shift, y_shift # сдвиг текста внутри окна
        self.text_color = text_color  # цвет текста
        self.border, self.border_color = border, border_color # цвет и толщина границы окна
        self.w_screen_, self.h_screen_ = 1400, 800  # базовое разрешение
        self.recalculation_flag = 0  # флаг версии разрешения
        self.font = font  # шрифт
        self.color_passive = color_passive # цвет границы окна когда оно не активно
        self.color_active = color_active # цвет границы окна когда оно не активно
        self.user_text = "" # текст пользователя

    def draw(self):

        if self.recalculation_flag != self.get_flag(): # пересчет размеров и местоположения если оно глобально изменилось

            self.recalculating()

        # отрисовка границы
        if self.border:

            pygame.draw.rect(self.screen, self.border_color,
                             (self.x - self.border, self.y - self.border, self.w + self.border * 2,
                              self.h + self.border * 2))

        # отрисовка поля для ввода
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.w, self.h))

        # отрисовка текста пользователя
        text_surface = self.font.render(self.user_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (self.x + self.x_shift, self.y + self.y_shift))


    def check(self, mouse_pos): # Проверка выбрано ли поля для ввода

        self.input, self.border_color = (True, self.color_active) if self.rect.collidepoint(mouse_pos) else (False, self.color_passive)

    def recalculating(self):

        # пересчет высоты и ширины кнопки
        self.w = (self.w / self.w_screen_) * Figure.w_screen_
        self.h = (self.h / self.h_screen_) * Figure.h_screen_

        # пересчет координат кнопки
        self.x = self.x / self.w_screen_ * Figure.w_screen_
        self.y = self.y / self.h_screen_ * Figure.h_screen_

        # обновление данных разрешения экрана и версии флага объекта класса
        self.w_screen_ = Figure.w_screen_
        self.h_screen_ = Figure.h_screen_
        self.recalculation_flag = self.get_flag()
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def send(self): # обработка результата ввода

        parts = self.user_text.split(",")
        width = int(parts[0].strip())
        height = int(parts[1].strip())
        self.user_text = ""
        return width, height

    def clear(self): # стирание текста

        self.user_text = self.user_text[:-1]

    def add_text(self, unicode): # добавление текста

        self.user_text += unicode
