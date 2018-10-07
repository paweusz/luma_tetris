class Block(object):

    def __init__(self):
        self.xy = (0,0)
        self.rotation = 0

    def move(self, xy):
        self.xy = (self.xy[0] + xy[0], self.xy[1] + xy[1])

    def get_xy(self, point_idx):
        return (self._points[self.rotation][point_idx][1] + self.xy[0],
                self._points[self.rotation][point_idx][0] + self.xy[1])

    def render(self, device):
        for i in range(4):
            device.point(
                (self.xy[0] + self._points[self.rotation][i][1],
                 self.xy[1] + self._points[self.rotation][i][0]))

class OBlock(Block): 

    def __init__(self):
        super(OBlock, self).__init__()
        self._points = [[(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)]]

class LBlock(Block): 

    def __init__(self):
        super(LBlock, self).__init__()
        self._points = [[(0, 1), (1, 1), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (1, 2), (0, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 0)],
            [(1, 0), (1, 1), (1, 2), (2, 0)]]

class IBlock(Block): 

    def __init__(self):
        super(IBlock, self).__init__()
        self._points = [[(0, 1), (1, 1), (2, 1), (3, 1)],
            [(1, 0), (1, 1), (1, 2), (1, 3)],
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(1, 0), (1, 1), (1, 2), (1, 3)]]

class ZBlock(Block):

    def __init__(self):
        super(ZBlock, self).__init__()
        self._points = [[(0, 0), (1, 0), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (0, 2)]]
        
class SBlock(Block):

    def __init__(self):
        super(SBlock, self).__init__()
        self._points = [[(1, 0), (2, 0), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (1, 1), (1, 2)]]

class JBlock(Block):
    
    def __init__(self):
        super(JBlock, self).__init__()
        self._points = [[(0, 1), (1, 1), (2, 1), (2, 0)],
            [(1, 0), (1, 1), (1, 2), (2, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2), (0, 0)]]

class TBlock(Block):

    def __init__(self):
        super(TBlock, self).__init__()
        self._points = [[(1, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (1, 1), (2, 1), (1, 2)]]


