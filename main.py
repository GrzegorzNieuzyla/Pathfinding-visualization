#!/bin/env python3
from grid import *
import sys
import math
from random import randint


class AstarAlgorithm:
    def __init__(self, start, goal, grid):
        self.start = start
        self.goal = goal
        self.grid = grid
        self.closedSet = set()
        self.openSet = set()
        self.openSet.add(self.start)
        self.pathFound = False
        self.pathDrawn = False
        self.path = []
        self.start.g_score = 0

    def iter(self):
        if not self.pathFound:
            if not self.openSet:
                return
            x = min(self.openSet, key=lambda v: v.f_score)
            if x is self.goal:
                self.pathFound = True
                self.constructPath()
                return
            self.openSet.remove(x)
            self.closedSet.add(x)
            for y in [self.grid.getTile(*v).data for v in x.connections]:
                if y in self.closedSet:
                    continue
                tent_g = x.g_score + 1  # default weight = 1
                better = False
                if y not in self.openSet:
                    self.openSet.add(y)
                    y.h_score = self.heuristic(y)
                    better = True
                elif tent_g < y.g_score:
                    better = True
                if better:
                    y.prev = x.pos
                    y.g_score = tent_g
                    y.f_score = y.g_score + y.h_score
                    self.grid.getTile(*y.pos).color = GridDisplay.CYAN
                    self.grid.getTile(*y.pos).setText(str(y.g_score))
        elif not self.pathDrawn:
            if len(self.path) == 0:
                self.pathDrawn = True
            else:
                self.grid.getTile(
                    *self.path.pop()).color = GridDisplay.DARK_GREEN

    def constructPath(self):
        self.grid.getTile(*self.goal.pos).color = GridDisplay.GREEN
        node = self.grid.getTile(*self.goal.prev).data
        while node is not self.start:
            self.path.append(node.pos)
            node = self.grid.getTile(*node.prev).data

    def heuristic(self, node):
        return abs(node.pos[0] - self.goal.pos[0]) + abs(node.pos[1] - self.goal.pos[1])


class PathFinder():
    class Node():
        def __init__(self, obs, pos):
            self.obstacle = obs
            self.visited = False
            self.connections = []
            self.pos = pos
            self.dist = math.inf
            self.prev = None
            self.h_score = math.inf  # heuristic score
            self.g_score = math.inf  # dist to source
            self.f_score = math.inf  # g(x) + h(x)

    def __init__(self, argv):
        if len(argv) < 2:
            print('Usage: {} file'.format(argv[0]))
            exit(1)
        self.display = GridDisplay(1600, 900, False, '[float]')
        self.grid = self.display.createGrid(10, 10, self.display.getWindowSize()[0] - 20,
                                            self.display.getWindowSize()[1] - 20, (GridDisplay.BLUE, GridDisplay.BLACK))
        self.data = []
        self.grid.outline = 3
        self.source = (0, 0)
        self.target = (0, 0)
        self.readFile(argv[1])
        self.fillBoard()
        self.grid.setFontFace('fonts/Hack-Bold.ttf')
        self.grid.setFontSize(14)
        self.graphify()

    def readFile(self, file):
        with open(file, 'r') as f:
            try:
                lines = [line for line in f.read().split(
                    '\n') if len(line.strip()) > 0]
                count = -1
                for line in lines:
                    if 't' in line:
                        self.target = (line.index('t'), len(self.data))
                        line = line.replace('t', '0')
                    if 's' in line:
                        self.source = (line.index('s'), len(self.data))
                        line = line.replace('s', '0')
                    self.data.append([int(c) for c in line])
                    if count != -1 and len(self.data[-1]) != count:
                        print("Lines are not of equal length")
                        exit(-2)
                    count = len(self.data[-1])
            except Exception as e:
                print("File format error: {}".format(e))
                exit(-1)
        self.source = (self.source[0], len(self.data) - 1 - self.source[1])
        self.target = (self.target[0], len(self.data) - 1 - self.target[1])

    def graphify(self):
        xlen = self.grid.getBoardSize()[0]
        ylen = self.grid.getBoardSize()[1]
        for y in range(ylen):
            for x in range(xlen):
                tile = self.grid.getTile(x, y)
                if tile.data.obstacle:
                    continue
                if y > 0 and not self.grid.getTile(x, y-1).data.obstacle:
                    tile.data.connections.append((x, y-1))
                if y < ylen-1 and not self.grid.getTile(x, y+1).data.obstacle:
                    tile.data.connections.append((x, y+1))
                if x > 0 and not self.grid.getTile(x-1, y).data.obstacle:
                    tile.data.connections.append((x-1, y))
                if x < xlen-1 and not self.grid.getTile(x+1, y).data.obstacle:
                    tile.data.connections.append((x+1, y))

    def fillBoard(self):
        len_x = len(self.data[0])
        len_y = len(self.data)
        self.grid.populate(len_x, len_y)
        for y in range(len_y):
            for x in range(len_x):
                self.grid.getTile(x, y).data = PathFinder.Node(
                    self.data[len_y-1-y][x] == 1, (x, y))
                if self.grid.getTile(x, y).data.obstacle:
                    self.grid.getTile(x, y).color = GridDisplay.RED
        self.grid.getTile(*self.source).color = GridDisplay.MAGENTA
        self.grid.getTile(*self.target).color = GridDisplay.GREEN

    def processDijkstra(self, vertices, path):
        if len(path) == 1:
            return
        pos = self.DijkstraAlgorithmIter(self.source, self.target, vertices)
        if pos is None:
            if len(path) == 0:
                tile = self.grid.getTile(*self.target)
                while tile.data.pos != self.source:
                    if tile.data.prev == None:
                        path = [0]
                        return
                    path.append(tile.data.pos)
                    tile = self.grid.getTile(*tile.data.prev)
            self.grid.getTile(*path.pop()).color = (0x38, 0x38, 0x38)

        elif pos != self.source and pos != self.target:
            self.grid.getTile(*pos).color = GridDisplay.CYAN
            self.grid.getTile(
                *pos).setText(str(self.grid.getTile(*pos).data.dist))

    def run(self):
        astar = AstarAlgorithm(
            self.grid.getTile(*self.source).data,
            self.grid.getTile(*self.target).data,
            self.grid)
        while not self.display.closeRequest:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.display.closeRequest = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.display.closeRequest = True

            for _ in range(3):
                astar.iter()
            self.display.render()
            self.display.tick(20)

    def DijkstraAlgorithmSetup(self, source):
        vertices = set()
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                vertices.add(self.grid.getTile(x, y).data)
        self.grid.getTile(*source).data.dist = 0
        return vertices

    def DijkstraAlgorithmIter(self, source, target, vertices):
        self.grid.getTile(0, 0).setText(str(len(vertices)))
        if len(vertices) == 0:
            return None
        min_v = iter(vertices).__next__()
        for vertex in vertices:
            if vertex.dist < min_v.dist:
                min_v = vertex
        if min_v.pos == target or min_v.dist == math.inf:
            return None
        vertices.remove(min_v)
        for conn in min_v.connections:
            v = self.grid.getTile(*conn).data
            alt = min_v.dist + 1
            if alt < v.dist:
                v.dist = alt
                v.prev = min_v.pos
        return min_v.pos


if __name__ == '__main__':
    PathFinder(sys.argv).run()
