import pygame
from math import sqrt

from constants import *
from config import *
from things import calculateColor


class Node:
    
    def __init__(self, data=0, x_cord=0, y_cord=0, indexloc=None):
        self.data = data
        self.index = data
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.color=(255, 0, 0)
        self.houseDistance=0
        self.overallDistance=0
        self.house3Distance=0
        self.metroDistance=0
        self.business = 0

    def setBusiness(self, b):
        self.business = b
        self.color = (calculateColor(self.business/10))
        # print("c", self.color)
    

    def setHouseDistance(self, distance):
        self.houseDistance = distance*pixelsToMeters
    
    def setMetroDistance(self, distance):
        self.metroDistance = distance*pixelsToMeters
    
    def calculateOverallDistance(self):
        self.overallDistance = self.metroDistance + self.houseDistance

    def __str__(self):
        print("data: " + self.data + " x_cord: " + self.x_cord + " y_cord: " + self.y_cord)
        return "{data: " + self.data + " x_cord: " + self.x_cord + " y_cord: " + self.y_cord+"}"
    
    # def toJSON(self):
    #     return "("+str(self.index)+","+str(self.x_cord)+","+str(self.y_cord)+")"
    
    def set_data(self, data):
        self.data = data[0]
        self.index = data[0]
        self.x_cord = data[1]
        self.y_cord = data[2]
        self.color = data[3]
        return self

    def get_data(self):
        return [self.data, self.x_cord, self.y_cord, self.color]
    
    def show(self, screen, *args, thikness=8):
        font = pygame.font.SysFont('Corbel', 30)

        text = font.render(str(self.business), True, BLACK)
        textRect = text.get_rect(topleft = (self.x_cord, self.y_cord))
        screen.blit(text, textRect)
        pygame.draw.circle(screen, self.color, (self.x_cord, self.y_cord), thikness)
        # pygame.display.update()
    def position(self):
        return (self.x_cord, self.y_cord)
    def setColor(self, color:tuple((int, int, int))=(255, 0, 0)):
        self.color = color


class Connection:
    def __init__(self, start:Node, end:Node, color:tuple((int, int, int))=(100, 255, 100), *args):
        self.node1=start
        self.node2=end
        self.color = color
    def show(self, screen, *args, thikness=8):
        pygame.draw.line(screen, self.color, self.node1.position(),
                                             self.node2.position(), thikness)
    def get_data(self):
        return [self.node1.data, self.node2.data, self.color]
    
    def set_data(self, data, _nodes):
        self.node1=_nodes[data[0]]
        self.node2=_nodes[data[1]]
        self.color = data[2]
        return self
    def setColor(self, color:tuple((int, int, int))=(100, 255, 100)):
        self.color = color
    def updateColor(self):
        r=(self.node1.color[0]+self.node1.color[0])/2
        g=(self.node1.color[1]+self.node1.color[1])/2
        b=(self.node1.color[2]+self.node1.color[2])/2
        self.color = (r, g, b)
    def get_length(self):
        return sqrt((abs(self.node1.x_cord-self.node2.x_cord)**2)+(abs(self.node1.y_cord-self.node2.y_cord)**2))
        
        
        
class Graph:

    @classmethod
    def create_from_nodes(self, nodes):
        return Graph(len(nodes), len(nodes), nodes)

    def __init__(self, row, col, nodes=None):
        # установка матрица смежности
        self.adj_mat = [[0] * col for _ in range(row)]
        self.nodes = nodes
        for i in range(len(self.nodes)):
            self.nodes[i].index = i

    # Связывает node1 с node2
    # Обратите внимание, что ряд - источник, а столбец - назначение
    # Обновлен для поддержки взвешенных ребер (поддержка алгоритма Дейкстры)
    def connect_dir(self, node1, node2, weight=1):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        self.adj_mat[node1][node2] = weight

    # Опциональный весовой аргумент для поддержки алгоритма Дейкстры
    def connect(self, node1, node2, weight=1):
        self.connect_dir(node1, node2, weight)
        self.connect_dir(node2, node1, weight)

    # Получает ряд узла, отметить ненулевые объекты с их узлами в массиве self.nodes
    # Выбирает любые ненулевые элементы, оставляя массив узлов
    # которые являются connections_to (для ориентированного графа)
    # Возвращает значение: массив кортежей (узел, вес)
    def connections_from(self, node):
        node = self.get_index_from_node(node)
        return [(self.nodes[col_num], self.adj_mat[node][col_num]) for col_num in range(len(self.adj_mat[node])) if
                self.adj_mat[node][col_num] != 0]

    # Проводит матрицу к столбцу узлов
    # Проводит любые ненулевые элементы узлу данного индекса ряда
    # Выбирает только ненулевые элементы
    # Обратите внимание, что для неориентированного графа
    # используется connections_to ИЛИ connections_from
    # Возвращает значение: массив кортежей (узел, вес)
    def connections_to(self, node):
        node = self.get_index_from_node(node)
        column = [row[node] for row in self.adj_mat]
        return [(self.nodes[row_num], column[row_num]) for row_num in range(len(column)) if column[row_num] != 0]

    def print_adj_mat(self):
        for row in self.adj_mat:
            print(row)

    def node(self, index):
        return self.nodes[index]

    def remove_conn(self, node1, node2):
        self.remove_conn_dir(node1, node2)
        self.remove_conn_dir(node2, node1)

    # Убирает связь в направленной манере (nod1 к node2)
    # Может принять номер индекса ИЛИ объект узла
    def remove_conn_dir(self, node1, node2):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        self.adj_mat[node1][node2] = 0

        # Может пройти от node1 к node2

    def can_traverse_dir(self, node1, node2):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        return self.adj_mat[node1][node2] != 0

    def has_conn(self, node1, node2):
        return self.can_traverse_dir(node1, node2) or self.can_traverse_dir(node2, node1)

    def add_node(self, node):
        self.nodes.append(node)
        node.index = len(self.nodes) - 1
        for row in self.adj_mat:
            row.append(0)
        self.adj_mat.append([0] * (len(self.adj_mat) + 1))

    # Получает вес, представленный перемещением от n1
    # к n2. Принимает номера индексов ИЛИ объекты узлов
    def get_weight(self, n1, n2):
        node1, node2 = self.get_index_from_node(n1), self.get_index_from_node(n2)
        return self.adj_mat[node1][node2]

    # Разрешает проводить узлы ИЛИ индексы узлов
    def get_index_from_node(self, node):
        if not isinstance(node, Node) and not isinstance(node, int):
            raise ValueError("node must be an integer or a Node object")
        if isinstance(node, int):
            return node
        else:
            return node.index

    def calculatePeopleleInNode(self, nodeIndex:int):
        pass

    def calculatePeopleleInCoonection(self):
        pass
    def dijkstra(self, node):
        # Получает индекс узла (или поддерживает передачу int)
        nodenum = self.get_index_from_node(node)
        # Заставляет массив отслеживать расстояние от одного до любого узла
        # в self.nodes. Инициализирует до бесконечности для всех узлов, кроме 
        # начального узла, сохраняет "путь", связанный с расстоянием. 
        # Индекс 0 = расстояние, индекс 1 = перескоки узла
        dist = [None] * len(self.nodes)
        for i in range(len(dist)):
            dist[i] = [float("inf")]
            dist[i].append([self.nodes[nodenum]])
        
        dist[nodenum][0] = 0
        # Добавляет в очередь все узлы графа
        # Отмечает целые числа в очереди, соответствующие индексам узла
        # локаций в массиве self.nodes 
        queue = [i for i in range(len(self.nodes))]
        # Набор увиденных на данный момент номеров 
        seen = set()
        while len(queue) > 0:
            # Получает узел в очереди, который еще не был рассмотрен
            # и который находится на кратчайшем расстоянии от источника
            min_dist = float("inf")
            min_node = None
            for n in queue: 
                if dist[n][0] < min_dist and n not in seen:
                    min_dist = dist[n][0]
                    min_node = n
            
            # Добавляет мин. расстояние узла до увиденного, убирает очередь
            queue.remove(min_node)
            seen.add(min_node)
            # Получает все следующие перескоки
            connections = self.connections_from(min_node)
            # Для каждой связи обновляет путь и полное расстояние от  
            # исходного узла, если полное расстояние меньше
            # чем текущее расстояние в массиве dist
            for (node, weight) in connections: 
                tot_dist = weight + min_dist
                if tot_dist < dist[node.index][0]:
                    dist[node.index][0] = tot_dist
                    dist[node.index][1] = list(dist[min_node][1])
                    dist[node.index][1].append(node)
        return dist

class Button:
    def __init__(self, xPos, yPos, width, height): 
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height

    def isClicked(self, mousePosition:list((int, int)), *args, x=0, y=0):
        if mousePosition[0] > self.xPos and mousePosition[0] < (self.xPos+self.width) and mousePosition[1] > self.yPos and mousePosition[1] < (self.yPos+self.height):
            return True
        return False


class Plate:
    def __init__(self, index:int, coords:tuple((int, int)), dataAbsolute:int, dataRelative:float):
        self.xStart = coords[0]
        self.yStart = coords[1]

        self.dataAbsolute = int(dataAbsolute)
        self.dataRelative = int(dataRelative)

    def show(self, screen:pygame.display):
        font = pygame.font.SysFont('Corbel', 25)
        text1 = font.render(str(self.dataAbsolute), True, BLACK, GREY)
        text2 = font.render(str(self.dataRelative) + "%", True, BLACK, GREY)
        textRect1 = text1.get_rect(topleft =(self.xStart, self.yStart))
        textRect2 = text2.get_rect(topleft =(self.xStart, self.yStart + text1.get_height()))
        # text.set_colorkey(GREY)

        
        rect_w = max(text1.get_width(), text2.get_width())
        surf = pygame.Surface((rect_w+20, text1.get_height() + text2.get_height()+2))
        surf.fill(GREY)
        rect = surf.get_rect(topleft =(self.xStart-10, self.yStart-1))

        screen.blit(surf, rect)
        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)

    def updateData(self, dataAbsolute:int, dataRelative:float):
        self.dataAbsolute = int(dataAbsolute)
        self.dataRelative = int(dataRelative)

    def updateCoord(self, x, y):
        self.xStart = x
        self.yStart = y
        return self