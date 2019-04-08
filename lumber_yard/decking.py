from math import ceil, floor

from lumber_yard.two_bys import TwoBySix

class Decking:
    """
    l is the length of the 2by's, x-axis
    w is the width of the deck, y-axis

    the boards run parellel to the y-axis.
    """

    def __init__(self, name, l, w, h, type='2by6'):
        self.spacing = 0.25
        self.board_width = self.get_board_width(type)

        num_boards = self.get_num_boards(w)
        self.boards = []

        label = '{0}_{1}'.format(name, type)
        dx = self.spacing + self.board_width
        x_offset = 0.0
        for i in range(num_boards):
            location = (x_offset, 0, h)
            board = TwoBySix(label, l, location)
            self.boards.append(board.object)
            x_offset = x_offset + dx



    def get_num_boards(self, total_width):
        w = self.board_width + self.spacing
        num_boards = ceil(total_width / w)
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
        label = '{0}_{1}'.format(name, self.type)
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

