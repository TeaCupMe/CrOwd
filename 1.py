import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import sys
import json

from CrGraph import Button, Node, Graph, Connection
from constants import *

pygame.init()

point_cord = [0, 0]
buildings_are_reqiered = [0, 0]  # первое -  это кол-во зданий , второе - наличие ТЦ

click_counter = 0
click_id = 0
empty_flag = 0
click_flag_point_bool = True
click_flag_home_bool = 0
click_flag_sell_bool = False
nodes_massive = ""

NODES = []
CONNECTIONS = []
TARGETS = []

sc = pygame.display.set_mode((W, H), pygame.RESIZABLE)
cursor_poses = [[0, 0], [0, 0]]
sc.fill(GREY)


def click_inside_of_screen():
    if pygame.mouse.get_pos()[0] < picture_scale[0] and pygame.mouse.get_pos()[1] < picture_scale[1]:
        return 1
    return 0


def load_the_points_to_file():
    with open("graph.txt", 'w') as file:
        json.dump([node.get_data() for node in NODES], file)


def load_the_points_on_map():
    try:
        with open("graph.txt", 'r') as file:
            global NODES
            NODES = [Node().set_data(data) for data in json.load(file)]
            print(NODES)
        print("NODES LEN: " + str(len(NODES)))
    except:
        print("НЕТ НАЧАЛЬНЫХ ТОЧЕК")


def load_the_connections_to_file():
    with open("connections.txt", 'w') as file:
        json.dump([connection.get_data() for connection in CONNECTIONS], file)
        print("writing", [connection.get_data() for connection in CONNECTIONS])


def load_the_connections_on_map():
    # try:
    with open("connections.txt", 'r') as file:
        global CONNECTIONS
        # print(file.read()
        CONNECTIONS = [Connection(Node(), Node()).set_data(data, NODES) for data in json.load(file)]
        print(CONNECTIONS)
    print("CONNECTIONS LEN: " + str(len(CONNECTIONS)))


# except:
#     print("НЕТ НАЧАЛЬНЫХ СОЕДИНЕНИЙ")


font = pygame.font.SysFont('Corbel', 30)  # инициализация начального текста(blit ниже)
text_point = font.render('points: on', True, BLACK)
text_home = font.render('home: off', True, BLACK)
text_sell = font.render('sell: off', True, BLACK)

city_surf = pygame.image.load('city.png')  # загрузка картинок
krest_png = pygame.image.load("krest.png")
galochka_png = pygame.image.load("galochka.png")
home_png = pygame.image.load("home.png")
sell_png = pygame.image.load("sell.png")
house_present_png = pygame.image.load("house_present.png")
office_present_png = pygame.image.load("office_present.png")
point_present_png = pygame.image.load("point_present.png")


new_krest = pygame.transform.scale(krest_png, (120, 120))  # скейл фоток до одного размера
new_galochka = pygame.transform.scale(galochka_png, (120, 120))
new_galochka_home = pygame.transform.scale(galochka_png, (120, 120))
new_galochka_sell = pygame.transform.scale(galochka_png, (120, 120))
new_krest_home = pygame.transform.scale(krest_png, (120, 120))
new_krest_sell = pygame.transform.scale(krest_png, (120, 120))
new_city = pygame.transform.scale(city_surf, picture_scale)
new_home = pygame.transform.scale(home_png, (80, 150))
new_home2 = pygame.transform.scale(home_png, (80, 150))
new_home3 = pygame.transform.scale(home_png, (80, 150))
new_sell = pygame.transform.scale(sell_png, (160, 300))
new_house_present = pygame.transform.scale(house_present_png, (80, 70))
new_office_present = pygame.transform.scale(office_present_png, (80, 80))
new_point_present = pygame.transform.scale(point_present_png, (50, 50))


new_city_rect = new_city.get_rect()  # получение их коллайдеров
new_galochka_rect = new_galochka.get_rect()
new_galochka_home_rect = new_galochka_home.get_rect()
new_galochka_sell_rect = new_galochka_sell.get_rect()
new_krest_sell_rect = new_krest_sell.get_rect()
new_krest_home_rect = new_krest_home.get_rect()
new_krest_rect = new_krest.get_rect()
new_home_rect = new_home.get_rect()
new_home2_rect = new_home2.get_rect()
new_home3_rect = new_home3.get_rect()
new_sell_rect = new_sell.get_rect()
new_house_present_rect = new_house_present.get_rect()
new_office_present_rect = new_office_present.get_rect()
new_point_present_rect = new_point_present.get_rect()


new_galochka_rect.center = (110, 954)  # отцентровка креста и галочки
new_galochka_home_rect = (453, 893)
new_galochka_sell_rect = (854, 894)
new_krest_rect.center = (47, 954)
new_krest_home_rect.center = (450, 954)
new_krest_sell_rect.center = (850, 954)
new_home_rect.center = (410, 600)
new_home2_rect.center = (510, 575)
new_home3_rect.center = (610, 550)
new_sell_rect.center = (1200, 300)
new_house_present_rect.center = (405, 915)
new_office_present_rect.center = (810, 918)
new_point_present_rect.center = (25, 923)


sc.blit(new_city, new_city_rect)  # показ всез начальных положений
sc.blit(new_galochka, new_galochka_rect)
sc.blit(new_krest_home, new_krest_home_rect)
sc.blit(new_krest_sell, new_krest_sell_rect)
sc.blit(text_point, (120, 910))
sc.blit(text_home, (521, 910))
sc.blit(text_sell, (945, 910))


load_the_points_on_map()
load_the_connections_on_map()
print("loaded", CONNECTIONS)

pygame.draw.rect(sc, BLACK, (50, 900, 200, 50), 2)
points_button = Button(50, 900, 200, 50)
pygame.draw.rect(sc, BLACK, (450, 900, 200, 50), 2)
home_button = Button(450, 900, 200, 50)
pygame.draw.rect(sc, BLACK, (850, 900, 200, 50), 2)
sell_button = Button(850, 900, 200, 50)

slider = Slider(sc, 1080, 914, 400, 20, min=1, max=24, step=1)

#pygame.display.update()


while True:
    load_the_points_on_map()
    load_the_connections_on_map()
    has_changes = False
    events = pygame.event.get()
    for event in events:

        if event.type == pygame.QUIT:
            load_the_points_to_file()
            load_the_connections_to_file()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            has_changes = True
            click_id = len(NODES)
            if click_inside_of_screen():  # режим постановки точек
                if click_flag_point_bool:
                    point_cord[0] = event.pos[0]
                    point_cord[1] = event.pos[1]
                    NODES.append(Node(len(NODES), point_cord[0], point_cord[1]))
                    if debug:
                        print(
                            "data: " + str(NODES[-1].data) + " x_cord: " + str(
                                NODES[-1].x_cord) + " y_cord: " + str(NODES[-1].y_cord))
                    # pygame.draw.circle(sc, RED, point_cord, 8)
                    # pygame.display.update()
                    click_id += 1

                else:  # режим соединения точек
                    with open("graph.txt", 'r') as file:
                        # nodes_massive_read = file.readline()[:-1]
                        obj = json.load(file)

                        nodes_massive_read = [Node().set_data(data) for data in obj]  # ! UNUSED
                        # print(nodes_massive_read)
                        # print("МАССИВ С ФАЙЛА: " + str(nodes_massive_read))

                    point_cord[0] = event.pos[0]
                    point_cord[1] = event.pos[1]

                    for node in NODES:
                        index, node_cord_x, node_cord_y = map(int, node.get_data())
                        # pygame.draw.circle(sc,RED,(node_cord_x,node_cord_y),8)
                        if (abs(node_cord_x - point_cord[0]) ** 2 + abs(node_cord_y - point_cord[1]) ** 2) ** 0.5 < 8:
                            cursor_poses[click_counter][0] = node_cord_x
                            cursor_poses[click_counter][1] = node_cord_y
                            print("I FOUND ROOT")
                            click_counter += 1
                            TARGETS.append(node)
                        # else:
                        #     TARGETS=[]
                        #     # pygame.display.update()
                        #     click_counter = 0

                        # print(index,node_cord_x,node_cord_y, end= " ")
                    # pygame.display.update()
                    print("clicks:", click_counter)
                    if click_counter == 2:  #
                        # pygame.draw.line(sc, (100, 100, 100),
                        #                  cursor_poses[0],
                        #                  cursor_poses[1], 6)
                        CONNECTIONS.append(Connection(TARGETS[0], TARGETS[1]))
                        TARGETS = []
                        # pygame.display.update()
                        click_counter = 0

            else:
                print(str(pygame.mouse.get_pos()[0]) + ' ' + str(pygame.mouse.get_pos()[1]))
                # обработки кнопки point
                if points_button.isClicked(pygame.mouse.get_pos()):
                    click_flag_point_bool = not click_flag_point_bool
                    if click_flag_point_bool == 0:
                        load_the_points_to_file()
                        load_the_connections_to_file()
                # обраюотка кнопки home
                if home_button.isClicked(pygame.mouse.get_pos()):
                    print("HOME BUTTON WORK " + str(click_flag_home_bool))

                    if click_flag_home_bool >= 0 and click_flag_home_bool < 3:

                        # click_flag_home_bool = (click_flag_home_bool+1)%4
                        # sc.fill(GREY, (450, 900, 200, 50))
                        text_home = font.render('home: ' + str(click_flag_home_bool + 1), True, BLACK)
                        # sc.blit(text_home, (520, 910))
                        # sc.blit(new_galochka_home, new_galochka_home_rect)
                        # if click_flag_home_bool == 1:
                        #     sc.blit(new_home, new_home_rect)
                        # elif click_flag_home_bool == 2:
                        #     sc.blit(new_home2, new_home2_rect)
                        # elif click_flag_home_bool == 3:
                        #     sc.blit(new_home3, new_home3_rect)
                        # else:
                        pygame.draw.rect(sc, BLACK, (450, 900, 200, 50), 2)
                        pygame.display.update()



                    else:
                        load_the_points_to_file()
                        load_the_connections_to_file()
                        click_flag_home_bool = 3
                        # sc.fill(GREY, (450, 900, 200, 50))
                        # sc.blit(new_city, new_city_rect)
                        text_home = font.render('home: off', True, BLACK)
                        # sc.blit(text_home, (520, 910))
                        # sc.blit(new_krest_home, new_krest_home_rect)
                        pygame.draw.rect(sc, BLACK, (450, 900, 200, 50), 2)
                        # pygame.display.update()
                    click_flag_home_bool += 1
                    click_flag_home_bool %= 4

                    # обработка нажатия на коммерцию
                if sell_button.isClicked(pygame.mouse.get_pos()):
                    click_flag_sell_bool = not click_flag_sell_bool
                    print("SELL BUTTON WORK ")
                    if click_flag_sell_bool:
                        # sc.fill(GREY, (850, 900, 200, 50))
                        text_sell = font.render('sell: on', True, BLACK)
                        # sc.blit(text_sell, (920, 910))
                        # sc.blit(new_galochka_sell, new_galochka_sell_rect)
                        # pygame.draw.rect(sc, BLACK, (850, 900, 200, 50), 2)
                        # pygame.display.update()

                    else:
                        load_the_points_to_file()
                        load_the_connections_to_file()
                        # sc.fill(GREY, (850, 900, 200, 50))
                        text_sell = font.render('sell: off', True, BLACK)
                        # sc.blit(text_sell, (920, 910))
                        # sc.blit(new_krest_sell, new_krest_sell_rect)

                        # pygame.draw.rect(sc, BLACK, (850, 900, 200, 50), 2)
                        # pygame.display.update()

                # отрисовываем объекты по новой для смены галочки
                if click_flag_point_bool:
                    sc.fill(GREY, (50, 900, 200, 50))
                    text_point = font.render('points: on', True, BLACK)
                    # sc.blit(text_point, (120, 910))
                    # sc.blit(new_galochka, new_galochka_rect)
                    # pygame.draw.rect(sc, BLACK, (50, 900, 200, 50), 2)
                    # pygame.display.update()
                    print("button state: " + str(click_flag_point_bool))
                else:
                    sc.fill(GREY, (50, 900, 250, 950))
                    text_point = font.render('points: off', True, BLACK)
                    # sc.blit(text_point, (120, 910))
                    # sc.blit(new_krest, new_krest_rect)
                    # pygame.draw.rect(sc, BLACK, (50, 900, 200, 50), 2)
                    # pygame.display.update()
                    print("button state: " + str(click_flag_point_bool))

    sc.fill(GREY)
    sc.blit(new_city, new_city_rect)

    sc.fill(GREY, (450, 900, 200, 50))
    sc.blit(new_house_present, new_house_present_rect)
    sc.blit(new_office_present, new_office_present_rect)
    sc.blit(new_point_present, new_point_present_rect)
    #sc.blit (new_cr_tech, new_cr_tech_rect)
    sc.blit(text_sell, (920, 910))

    if not click_flag_sell_bool:
        sc.blit(new_krest_sell, new_krest_sell_rect)
    else:
        sc.blit(new_galochka_sell, new_galochka_sell_rect)

    for node in NODES:
        node.show(sc)
    for connection in CONNECTIONS:
        connection.show(sc)
    if click_flag_point_bool:
        sc.blit(text_point, (120, 910))
        sc.blit(new_galochka, new_galochka_rect)

    else:
        sc.blit(text_point, (120, 910))
        sc.blit(new_krest, new_krest_rect)
    pygame.draw.rect(sc, BLACK, (50, 900, 200, 50), 2)
    pygame.draw.rect(sc, BLACK, (450, 900, 200, 50), 2)
    pygame.draw.rect(sc, BLACK, (1560, 890, 130, 50),2)
    sc.blit(text_home, (520, 910))
    pygame.draw.rect(sc, BLACK, (850, 900, 200, 50), 2)
    if click_flag_home_bool >= 1:
        sc.blit(new_galochka_home, new_galochka_home_rect)
        sc.blit(new_home, new_home_rect)
        if click_flag_home_bool >= 2:
            sc.blit(new_home2, new_home2_rect)
            if click_flag_home_bool >= 3:
                sc.blit(new_home3, new_home3_rect)
    else:
        sc.blit(new_krest_home, new_krest_home_rect)
    if click_flag_sell_bool:
        sc.blit(new_sell, new_sell_rect)
    # if has_changes:

    load_the_points_to_file()
    load_the_connections_to_file()
    pygame_widgets.update(events)
    text_hours = font.render('hours: ' + str(slider.getValue()), True, BLACK)
    sc.blit(text_hours, (1570, 900))
    pygame.display.update()
w_graph = Graph.create_from_nodes(NODES)

w_graph.connect(a, b, 5)
w_graph.connect(a, c, 10)
w_graph.connect(a, e, 2)
w_graph.connect(b, c, 2)
w_graph.connect(b, d, 4)
w_graph.connect(c, d, 7)
w_graph.connect(c, f, 10)
w_graph.connect(d, e, 3)

w_graph.print_adj_mat()
