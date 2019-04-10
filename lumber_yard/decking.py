from math import ceil, floor, pi

from lumber_yard.two_bys import TwoBySix, TwoByEight
from lumber_yard.utils import feet


class Decking:
    """
    dy is the length of the 2by's, x-axis
    dx is the width of the deck, y-axis

    the boards run parellel to the y-axis.
    """

    def __init__(self, name, dy, dx, height, type='2by6'):
        self.name = name
        self.dx = dx
        self.dy = dy
        self.height = height
        self.spacing = 0.25
        self.beam_center = feet(4)

        self.board_width = self.get_board_width(type)

        self.num_boards = self.get_num_boards()
        self.num_beams = self.get_num_beams()
        self.boards = self.get_surface()

        beams = self.get_beams()
        self.boards.extend(beams)


    def get_surface(self):
        label = self.name
        dx = self.spacing + self.board_width
        x_offset = 0.0
        boards = []
        for i in range(self.num_boards):
            location = (x_offset, 0, self.height)
            board = TwoBySix(label, self.dy, location)
            boards.append(board.object)
            x_offset = x_offset + dx
        return boards


    def get_beams(self):
        label = self.name
        dy = self.beam_center
        y_offset = 0.0
        beams = []

        for i in range(self.num_beams)[:-1]:
            location = (0, y_offset + 1.5, self.height)
            board = TwoByEight(label, self.dx, location)
            board.object.rotation_euler = (pi/2, pi/2, 0)
            beams.append(board.object)
            y_offset = y_offset + dy

        # # Add the last board
        # location = (0, self.dy, self.height)
        # board = TwoByEight(label, self.dx, location)
        # board.object.rotation_euler = (pi/2, pi/2, 0)
        # beams.append(board.object)
        return beams


    def get_num_beams(self):
        num_beams = floor(self.dy / self.beam_center)
        return num_beams + 2


    def get_num_boards(self):
        w = self.board_width + self.spacing
        num_boards = ceil(self.dx / w)
        return num_boards


    def get_board_width(self, type):
        if type == '2by6':
            board_width = 5.5
        else:
            raise Exception("not implemented for {0}".format(type))
        return board_width


class Stairs:

    def __init__(self, name, rise, height, length, board_width, boards_per_step):
        self.type = '2by6'
        self.spacing = 0.25
        self.board_thickness = 1.5
        self.height = height
        self.rise = rise

        z_offset = self.height
        x_offset = 0.0
        num_steps = self.get_num_steps()
        label = name
        self.boards = []
        for i in range(num_steps):
            for j in range(boards_per_step):
                location = (x_offset, 0, z_offset)
                board = TwoBySix(label, length, location)
                self.boards.append(board.object)
                x_offset = x_offset + board_width + self.spacing
            z_offset = z_offset - self.board_thickness - self.rise


    def get_num_steps(self):
        combined_rise = self.rise + self.board_thickness
        num_steps = floor(self.height / combined_rise)
        return num_steps

