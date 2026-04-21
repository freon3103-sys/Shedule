import os
import pygame
import pyperclip as pc
from module import (Figure, Links, Button, Image_button, Desk, Text, User_text,
                    writelinks, watch_func, parse_func, chec_func)

os.environ['SDL_VIDEO_WINDOW_POS'] = "300,200"

pygame.init()

width, height = 1400, 800
screen = pygame.display.set_mode((width, height))
base_font = pygame.font.SysFont("Arial", 36)
Figure.set_screen(screen, base_font)
pygame.display.set_caption("Shedule")
clock = pygame.time.Clock()
current_screen = "menu"

background = pygame.image.load("images/transport.jpg")
background = pygame.transform.scale(background, (width, height))
check_mark = pygame.image.load("images/check.png")
check_mark_big = pygame.transform.scale(check_mark, (80, 80))
check_mark = pygame.transform.scale(check_mark, (40, 40))

font = pygame.font.SysFont("Arial", 36)
font2 = pygame.font.SysFont("Arial", 50)
font3 = pygame.font.SysFont("Arial", 26)

user_text = ""
input_active = False
color_active = (150, 80, 80)
color_passive = pygame.Color("gray15")

lines = [[]]
lines_backup = None
parse = []
page = 0
x_posit = 0
Flag_pages = False

buttons_menu = {"НАЧАТЬ": Button("НАЧАТЬ", 140, (400, 50), (500, 250), color=(100, 200, 100)),
           "НАСТРОЙКИ": Button("НАСТРОЙКИ", 110, (400, 50), (500, 375), color=(100, 100, 200)),
           "ВЫХОД": Button("ВЫХОД", 145, (400, 50), (500, 500), color=(200, 100, 100)),
           "ДОБАВИТЬ ССЫЛКУ": Button("ДОБАВИТЬ ССЫЛКУ", 55, (400, 50), (500, 250), color=(100, 200, 100)),
           "ПОЛУЧЕНИЕ МАРШРУТОВ": Button("САМАРА", 140, (400, 50), (500, 375), color=(100, 200, 100)),
           }

buttons_get_shed = {"update": Image_button("КНОПКА ОБНОВЛЕНИЯ", (80, 80), (1070, 60), image=pygame.image.load("images/update.jpg"), border=2),
                    "left_arrow": Image_button("", (60, 60), (1100, 672), image=pygame.image.load("images/left_a.png")),
                    "right_arrow": Image_button("", (60, 60), (1170, 672), image=pygame.image.load("images/right_a.png")),
                    "ЧЕКИНГ": Button("ЧЕКИНГ", 40, (200, 60), (600, 672), color=(255, 255, 255), border=2, y_shift=10),
                    "ПАРСИНГ": Button("ПАРСИНГ", 30, (200, 60), (370, 672), color=(255, 255, 255), border=2, y_shift=10),
                    "ПРОСМОТР": Button("ПРОСМОТР", 15, (200, 60), (830, 672), color=(255, 255, 255), border=2, y_shift=10),
                    "all_flag": Image_button("ПРОСТАВИТЬ ВСЕ ФЛАГИ", (80, 80), (1160, 60), image=check_mark_big, border=2, background=True),
                    "ПОИСК": User_text((600, 50), (300, 75), border=2),
                    "НАДПИСЬ ПОИСК": Text("ПОИСК", (175, 75)),
                    "clear": Image_button("ОЧИСТКА",(80, 80), (980, 60), image=pygame.image.load("images/clear.png"),border=2, background=True)
                    }

tech_buttons = {"desk": Desk("", (1100, 700), (150, 50), border=3),
                "desk2": Desk("",(1100, 500), (150, 150), border=3)
                }

buttons_settings = {"НАСТРОЙКИ": Text("НАСТРОЙКИ", (575, 75), text_color=(0, 0, 0), font=font2),
                    "РАЗРЕШЕНИЕ": Text("РАЗРЕШЕНИЕ:",(175, 175)),
                    "ВВОД": User_text( (600, 55), (400, 170), border=2),
                    }

buttons_add_link = {"ССЫЛКА": Text("ССЫЛКА:", (250, 175)),
                    "ПОЛЕ ВВОДА": User_text((600, 55), (400, 170), border=2)}

buttons_result = {"РЕЗУЛЬТАТ": Text("Результат сохранен в текстовые файлы в папке с программой", (280, 300))}

buttons_one_result = {"left_arrow": Image_button("", (60, 60), (1100, 672), image=pygame.image.load("images/left_a.png")),
                    "right_arrow": Image_button("", (60, 60), (1170, 672), image=pygame.image.load("images/right_a.png")),
                    "up_arrow": Image_button("", (60, 60), (1270, 320), image=pygame.image.load("images/up_a.png")),
                    "down_arrow": Image_button("", (60, 60), (1270, 380), image=pygame.image.load("images/down_a.png")),
                    "ЗАГОЛОВОК": Text("", (450, 75)),
                    "ПОДЗАГОЛОВОК": Text("", (190, 150)),
                    "РАСПИСАНИЕ": Text("", (190, 190))
                    }

running = True
while running:

    screen.fill((0, 0, 0))  # Очистка экрана (черный фон)

    #Запуск цикла в котором pygame отслеживает действия пользователя
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Глобальное возвращение в меню при нажатии Esc
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:

            if current_screen == "add_link" or current_screen == "get_shed" or current_screen == "one_shed":

                current_screen = "app"

            elif current_screen == "result" or current_screen == "one_result":

                page = 0
                current_screen = "get_shed"

            else:

                current_screen = "menu"

        # Обработка кликов мышью
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if current_screen == "menu":

                # Кнопка "Начать"
                if buttons_menu["НАЧАТЬ"].rect.collidepoint(mouse_pos):

                    current_screen = "app"

                # Кнопка "Настройки"
                elif buttons_menu["НАСТРОЙКИ"].rect.collidepoint(mouse_pos):

                    current_screen = "settings"

                # Кнопка "Выход"
                elif buttons_menu["ВЫХОД"].rect.collidepoint(mouse_pos):

                    running = False

            elif current_screen == "app":

                # Кнопка "Добавить ссылку"
                if buttons_menu["ДОБАВИТЬ ССЫЛКУ"].rect.collidepoint(mouse_pos):

                    current_screen = "add_link"

                # Кнопка "получение расписаний"
                elif buttons_menu["ПОЛУЧЕНИЕ МАРШРУТОВ"].rect.collidepoint(mouse_pos):

                    current_screen = "get_shed"

            elif current_screen == "add_link":

                buttons_add_link["ПОЛЕ ВВОДА"].check(mouse_pos)

            elif current_screen == "settings":

                # Клик по полю ввода
                buttons_settings["ВВОД"].check(mouse_pos)

            elif current_screen == "get_shed":

                if buttons_get_shed["update"].rect.collidepoint(mouse_pos):

                    lines = Links.readlinks()
                    lines_backup = lines
                    Flag_pages = True

                elif buttons_get_shed["all_flag"].rect.collidepoint(mouse_pos):

                    Links.all_flags(lines)

                elif buttons_get_shed["right_arrow"].rect.collidepoint(mouse_pos):

                    page += 1 if page < len(lines) - 1 else 0

                elif buttons_get_shed["left_arrow"].rect.collidepoint(mouse_pos):

                    page -= 1 if page > 0 else 0

                elif buttons_get_shed["clear"].rect.collidepoint(mouse_pos):

                    buttons_get_shed["ПОИСК"].user_text = ""
                    lines = lines_backup
                    lines = Links.clear_search(lines)

                elif buttons_get_shed["ЧЕКИНГ"].rect.collidepoint(mouse_pos):

                    current_screen = "result"

                    page = 0

                    chec_func(lines)

                elif buttons_get_shed["ПАРСИНГ"].rect.collidepoint(mouse_pos):

                    current_screen = "result"

                    page = 0

                    parse_func(lines)

                elif buttons_get_shed["ПРОСМОТР"].rect.collidepoint(mouse_pos):

                    page = 0

                    current_screen = "one_result"

                    parse, parse_title = watch_func(lines)

                elif buttons_get_shed["ПОИСК"].rect.collidepoint(mouse_pos):

                    buttons_get_shed["ПОИСК"].check(mouse_pos)

                for x in lines[page]:

                    if x.get_coordinates()[0] - 50 <= mouse_pos[0] <= x.get_coordinates()[0] + 400 and x.get_coordinates()[1] <= mouse_pos[1] <= x.get_coordinates()[1] + 40:

                        x.toggle()

            elif current_screen == "one_result":

                if buttons_one_result["right_arrow"].rect.collidepoint(mouse_pos):

                    x_posit = 0
                    page += 1 if page < len(parse) - 1 else 0

                elif buttons_one_result["left_arrow"].rect.collidepoint(mouse_pos):

                    x_posit = 0
                    page -= 1 if page > -1 else 0

                elif buttons_one_result["down_arrow"].rect.collidepoint(mouse_pos):

                        x_posit -= 1400

                elif buttons_one_result["up_arrow"].rect.collidepoint(mouse_pos):

                        x_posit += 1400

        # Обработка нажатий клавиатуры
        elif event.type == pygame.KEYDOWN:
            if current_screen == "settings" and buttons_settings["ВВОД"].input:

                if event.key == pygame.K_RETURN:

                    width, height = buttons_settings["ВВОД"].send()
                    background = pygame.transform.scale(background, (width, height))
                    screen = pygame.display.set_mode((width, height))
                    Figure.set_screen(screen, base_font)
                    Figure.set_widescreen(width, height)

                elif event.key == pygame.K_BACKSPACE:

                    buttons_settings["ВВОД"].clear()

                else:

                    buttons_settings["ВВОД"].add_text(event.unicode)

            elif current_screen == "add_link" and buttons_add_link["ПОЛЕ ВВОДА"].input:

                if event.key == pygame.K_RETURN:

                    writelinks(buttons_add_link["ПОЛЕ ВВОДА"].user_text)
                    buttons_add_link["ПОЛЕ ВВОДА"].user_text = ""

                elif event.key == pygame.K_BACKSPACE:

                    buttons_add_link["ПОЛЕ ВВОДА"].clear()

                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_LCTRL:

                    buttons_add_link["ПОЛЕ ВВОДА"].add_text(pc.paste())

                else:

                    buttons_add_link["ПОЛЕ ВВОДА"].add_text(event.unicode)

            elif current_screen == "get_shed" and buttons_get_shed["ПОИСК"].input:

                if event.key == pygame.K_RETURN:

                    page = 0

                    if buttons_get_shed["ПОИСК"].user_text == "":

                        lines = lines_backup
                        lines = Links.clear_search(lines)

                    else:

                        lines = lines_backup

                        for x in lines:

                            for y in x:

                                y.bool = False

                        lines = Links.clear_search(lines)
                        lines = Links.search(lines, buttons_get_shed["ПОИСК"].user_text)

                elif event.key == pygame.K_BACKSPACE:

                    buttons_get_shed["ПОИСК"].clear()

                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_LCTRL:

                    buttons_get_shed["ПОИСК"].add_text(pc.paste())

                else:
                    buttons_get_shed["ПОИСК"].add_text(event.unicode)

    # Отрисовка содержимого по текущему экрану
    if current_screen == "menu":

        # Фон
        screen.blit(background, (0, 0))

        # Кнопка "НАЧАТЬ"
        buttons_menu["НАЧАТЬ"].draw()

        # Кнопка "НАСТРОЙКИ"
        buttons_menu["НАСТРОЙКИ"].draw()

        # Кнопка "ВЫХОД"
        buttons_menu["ВЫХОД"].draw()

    elif current_screen == "settings":

        # фон
        screen.blit(background, (0, 0))

        # отрисовка стола
        tech_buttons["desk"].draw()
        tech_buttons["desk2"].draw()

        buttons_settings["НАСТРОЙКИ"].draw()
        buttons_settings["РАЗРЕШЕНИЕ"].draw()
        buttons_settings["ВВОД"].draw()

    elif current_screen == "app":

        # Фон
        screen.blit(background, (0, 0))

        # Кнопка "ДОБАВИТЬ ССЫЛКУ"
        buttons_menu["ДОБАВИТЬ ССЫЛКУ"].draw()

        # Кнопка "ПОЛУЧЕНИЕ МАРШРУТОВ"
        buttons_menu["ПОЛУЧЕНИЕ МАРШРУТОВ"].draw()

    elif current_screen == "add_link":

        # фон
        screen.blit(background, (0, 0))

        # отрисовка стола

        tech_buttons["desk"].draw()
        tech_buttons["desk2"].draw()

        buttons_add_link["ССЫЛКА"].draw()

        # отрисовка текста пользователя
        buttons_add_link["ПОЛЕ ВВОДА"].draw()

    elif current_screen == "get_shed":

        # фон
        screen.blit(background, (0, 0))

        # отрисовка стола

        tech_buttons["desk"].draw()
        tech_buttons["desk2"].draw()

        # отрисовка кнопки "update"
        buttons_get_shed["update"].draw()

        if Flag_pages:

            buttons_get_shed["ПОИСК"].draw()
            buttons_get_shed["НАДПИСЬ ПОИСК"].draw()
            buttons_get_shed["left_arrow"].draw()
            buttons_get_shed["right_arrow"].draw()
            buttons_get_shed["ЧЕКИНГ"].draw()
            buttons_get_shed["ПАРСИНГ"].draw()
            buttons_get_shed["ПРОСМОТР"].draw()
            buttons_get_shed["all_flag"].draw()
            buttons_get_shed["clear"].draw()

        Links.draw(lines[page], check_mark) # отрисовка одной страницы с помощью метода класса Links

    elif current_screen == "result":

        # фон
        screen.blit(background, (0, 0))

        tech_buttons["desk2"].draw()

        buttons_result["РЕЗУЛЬТАТ"].draw()

    elif current_screen == "one_result":

        # фон
        screen.blit(background, (0, 0))

        # отрисовка стола

        tech_buttons["desk"].draw()
        tech_buttons["desk2"].draw()

        x_pos = x_posit

        buttons_one_result["left_arrow"].draw()
        buttons_one_result["right_arrow"].draw()
        buttons_one_result["up_arrow"].draw()
        buttons_one_result["down_arrow"].draw()

        new_x, new_y = buttons_one_result["ПОДЗАГОЛОВОК"].get_coord()
        new2_x, new2_y = buttons_one_result["РАСПИСАНИЕ"].get_coord()

        if page > -1:

            for key, value in parse[page].result.items():

                screen.blit(font.render(f"{parse[page].name}", True, (0, 0, 0)),
                            buttons_one_result["ЗАГОЛОВОК"].get_coord())

                screen.blit(font.render(f"{key}", True, (0, 0, 0)), (new_x + x_pos, new_y))

                y_pos = 0

                for i_t in value:
                    screen.blit(font3.render(f"{i_t}", True, (0, 0, 0)), (new2_x + x_pos, new2_y + y_pos))
                    y_pos += 30

                    if y_pos == 450:

                        y_pos = 0
                        x_pos += 60

                        if 1400 > (x_pos/width - int(x_pos/width)) * width > 1000 and x_pos > 0:
                            x_pos += 300
                        elif 0 > (x_pos/width - int(x_pos/width)) * width > -400 and x_pos < 0:
                            x_pos += 300

                x_pos += 300

        else:

            y_pos = 160

            if len(parse_title) > 1:

                for day, colors_flight in parse_title.items():

                    screen.blit(font.render(f"{day}", True, (0, 0, 0)), (new_x + x_pos, y_pos))

                    y_pos += 50

                    for color_flight in colors_flight:

                        screen.blit(font3.render(f"{color_flight}", True, (0, 0, 0)), (new2_x + x_pos, y_pos))
                        y_pos += 30

            else:

                for day, colors_flight in parse_title.items():

                    screen.blit(font.render(f"{day}", True, (0, 0, 0)), (new_x + x_pos, y_pos))

                    y_pos += 50

                    for color_flight in colors_flight:

                        screen.blit(font3.render(f"{color_flight}", True, (0, 0, 0)), (new2_x + x_pos, y_pos))
                        y_pos += 30

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

# Завершение приложения
pygame.quit()