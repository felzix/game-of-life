class GameOfLife(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = make_tiles(width, height)
        self.__other_tiles = make_tiles(width, height)
        self.iteration = 0

    def evolve(self):
        """
        Apply the Game of Life rules to the board.

        Swaps self.tile and self.__other_tiles.
        """
        for y in xrange(self.height):
            for x in xrange(self.width):
                live_neighbors = self.__neighbor_count(x, y)
                if self[y][x]:  # is alive
                    if live_neighbors < 2:
                        self.__other_tiles[y][x] = False
                    elif live_neighbors in (2, 3):
                        self.__other_tiles[y][x] = True
                    elif live_neighbors > 3:  # else
                        self.__other_tiles[y][x] = False
                else:  # is dead
                    if live_neighbors == 3:
                        self.__other_tiles[y][x] = True
                    else:
                        self.__other_tiles[y][x] = False  # stays dead
        # swap, for next generation
        self.tiles, self.__other_tiles = self.__other_tiles, self.tiles
        self.iteration += 1

    def __neighbor_count(self, x, y):
        neighbors = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= i + x < self.height and 0 <= j + y < self.width and not (i == 0 and j == 0):
                    neighbors.append(self[y + j][x + i])
        return len([n for n in neighbors if n])

    def __getitem__(self, item):
        return self.tiles.__getitem__(item)

    def __str__(self):
        return '\n'.join([''.join(['M' if self[y][x] else ' '
                                   for x in xrange(self.width)])
                          for y in xrange(self.height)])


def make_tiles(width, height):
    return [[False for x in xrange(width)] for y in xrange(height)]

