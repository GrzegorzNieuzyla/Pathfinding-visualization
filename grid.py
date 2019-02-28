import pygame


class GridDisplay():
    """
    Display grid using pygame
        """
    BLACK = (0x00, 0x00, 0x00)
    WHITE = (0xFF, 0xFF, 0xFF)
    RED = (0xFF, 0x00, 0x00)
    GREEN = (0x00, 0xFF, 0x00)
    BLUE = (0x00, 0x00, 0xFF)
    YELLOW = (0xFF, 0xFF, 0x0)
    CYAN = (0x0, 0xFF, 0xFF)
    MAGENTA = (0xFF, 0x00, 0xFF)
    DARK_GREEN = (0x05, 0x30, 0x0c)

    class Tile():
        def __init__(self, color, textColor, data=None):
            self.data = data
            self.text = None
            self.color = color
            self.textColor = textColor

        def setText(self, text):
            self.text = text

    class Grid():
        def __init__(self, offsetx: int, offsety: int, width: int = 0, height: int = 0):
            self.pos_x = offsetx
            self.pos_y = offsety
            self.size = (width, height)
            self.board = []
            self.__row_count = 0
            self.__col_count = 0
            self.__tile_height = 0
            self.__tile_width = 0
            self.__offset_x = 0
            self.__offset_y = 0
            self.fontFace = None
            self.font = None
            self.fontSize = 0
            self.outline = 1
            self.backgroundColor = (0x00, 0x00, 0x00)
            self.tileColor = (0xFF, 0xFF, 0xFF)
            self.textColor = self.backgroundColor
            self.fontRatio = 1
            self.active = True

        def resize(self, ratio):
            self.pos_y = int(self.pos_y * ratio[1])
            self.pos_x = int(self.pos_x * ratio[0])
            self.size = (int(self.size[0] * ratio[0]),
                         int(self.size[1] * ratio[1]))
            self.populate(self.__row_count, self.__col_count)
            self.font = pygame.font.Font(
                self.fontFace, (int(self.__tile_width * self.fontRatio)))
            self.fontSize = int(self.__tile_width * self.fontRatio)

        def setFontSize(self, size: int):
            self.fontRatio = size / self.__tile_width
            self.font = pygame.font.Font(self.fontFace, size)
            self.fontSize = size

        def setFontFace(self, font):
            self.fontFace = font
            self.font = pygame.font.Font(self.fontFace, self.fontSize)

        def setActive(self, active: bool):
            self.active = active

        def populate(self, x_count: int, y_count: int):
            if x_count == 0 or y_count == 0:
                return
            self.__row_count = y_count
            self.__col_count = x_count
            self.__tile_width = self.size[0] // x_count
            self.__offset_x = (self.size[0] % x_count) // 2
            self.__tile_height = self.size[1] // y_count
            self.__offset_y = (self.size[1] % y_count) // 2
            if self.fontSize == 0:
                self.setFontSize(int(self.__tile_width*0.75))
            if len(self.board) == 0 or (len(self.board) != self.__col_count or len(self.board[0]) != self.__row_count):
                for _ in range(self.__row_count):
                    self.board.append([])
                    for __ in range(self.__col_count):
                        self.board[-1].append(GridDisplay.Tile(
                            self.tileColor, self.textColor))

        def getTileSize(self) -> tuple:
            return (self.__tile_width, self.__tile_height)

        # (0,0) - bottom left
        def getTile(self, x: int, y: int):
            if y < 0 or y >= self.__row_count or x < 0 or x >= self.__col_count:
                raise IndexError("Out of range")
            return self.board[self.__row_count - 1-y][x]

        # create grid
        def split(self, tileWidth: int, tileHeight: int) -> tuple:
            if tileHeight <= 0 or tileHeight <= 0:
                raise ValueError("Tile size must be > 0")
            tileWidth = min(self.size[0], tileWidth)
            tileHeight = min(self.size[1], tileHeight)
            self.__offset_x = (self.size[0] % tileWidth) // 2
            self.__offset_y = (self.size[1] % tileHeight) // 2
            self.__row_count = self.size[0] // tileWidth
            self.__col_count = self.size[1] // tileHeight
            self.__tile_width = tileWidth
            self.__tile_height = tileHeight
            if self.fontSize == 0:
                self.setFontSize(int(self.__tile_width * 0.75))
            self.board = []
            for _ in range(self.__row_count):
                self.board.append([])
                for __ in range(self.__col_count):
                    self.board[-1].append(GridDisplay.Tile(
                        self.tileColor, self.textColor))
            return self.getBoardSize()

        def draw(self, screen):
            r = 0
            for row in self.board:
                c = 0
                for tile in row:
                    pygame.draw.rect(screen, tile.color, pygame.Rect(
                        self.pos_x + self.__offset_x + c * self.__tile_width,
                        self.pos_y + self.__offset_y + r * self.__tile_height,
                        self.__tile_width, self.__tile_height))
                    if tile.color != self.backgroundColor:
                        pygame.draw.rect(screen, self.backgroundColor, pygame.Rect(
                            self.pos_x + self.__offset_x + c * self.__tile_width,
                            self.pos_y + self.__offset_y + r * self.__tile_height,
                            self.__tile_width, self.__tile_height), self.outline)
                    if tile.text is not None:
                        text = self.font.render(
                            tile.text, True, tile.textColor)
                        text_rect = text.get_rect(center=(self.pos_x + self.__offset_x + c * self.__tile_width + self.__tile_width/2,
                                                          self.pos_y + self.__offset_y + r * self.__tile_height + self.__tile_height/2))
                        if text_rect.width > self.__tile_width:
                            tmp_font = pygame.font.Font(
                                self.fontFace, int(self.__tile_width * 0.8))
                            text = tmp_font.render(
                                tile.text, True, tile.textColor)
                            text_rect = text.get_rect(center=(self.pos_x + self.__offset_x + c * self.__tile_width + self.__tile_width/2,
                                                              self.pos_y + self.__offset_y + r * self.__tile_height + self.__tile_height/2))
                        if text_rect.height > self.__tile_height:
                            tmp_font = pygame.font.Font(
                                self.fontFace, int(self.__tile_height * 1))
                            text = tmp_font.render(
                                tile.text, True, tile.textColor)
                            text_rect = text.get_rect(center=(self.pos_x + self.__offset_x + c * self.__tile_width + self.__tile_width/2,
                                                              self.pos_y + self.__offset_y + r * self.__tile_height + self.__tile_height/2))
                        screen.blit(text, text_rect)
                    c += 1
                r += 1

        def getBoardSize(self) -> tuple:
            return (self.__col_count, self.__row_count)

    #######################################################################################

    def __init__(self, width: int, height: int, fullscreen: bool = False, title='Grid'):
        pygame.init()
        pygame.display.set_caption(title)
        if fullscreen:
            self.screen = pygame.display.set_mode(
                (width, height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(
                (width, height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.fullscreen = fullscreen
        self.size = self.screen.get_size()
        self.backgroundColor = (0, 0, 0)
        self.FPS = 60
        self.outline = 3
        self.tileColor = (0x00, 0x00, 0xFF)
        self.textColor = (0x00, 0x00, 0x00)
        self.__offset_x = 0
        self.__offset_y = 0
        self.__tile_width = 1
        self.__tile_height = 1
        self.__row_count = 0
        self.__col_count = 0
        self.board = []
        self.toRender = []
        self.font = None
        self.fontSize = 0
        self.closeRequest = False
        self.drawable = []

    def tick(self, fps: int):
        self.clock.tick(fps)

    def getWindowSize(self):
        return self.size

    def pollEvents(self):
        return pygame.event.get()

    def createGrid(self, offsetx: int, offsety: int, width: int, height: int, colors=((0xFF, 0xFF, 0xFF), (0, 0, 0))):
        grid = GridDisplay.Grid(offsetx, offsety, width, height)
        grid.tileColor = colors[0]
        grid.backgroundColor = grid.textColor = colors[1]
        self.toRender.append(grid)
        return grid

    def drawGrid(self, grid):
        grid.draw(self.screen)

    def render(self):
        self.screen.fill(self.backgroundColor)
        for grid in filter(lambda g: g.active, self.toRender):
            grid.draw(self.screen)
        for obj in self.drawable:
            obj.draw()
        pygame.display.flip()
