class Scene:

    def __init__(self, dev, size):
        self.block = None
        self.dev = dev
        self.size = size
        self.bg = [[0 for i in range(size[1])] for i in range(size[0])]

    def set_current_block(self, block):
        self.block = block

    def render(self):
        self.dev.clean()

        self.block.render(self.dev)
        for x in range(len(self.bg)):
        	for y in range(len(self.bg[x])):
        		if self.bg[x][y]:
        			self.dev.point((15 - y, x))

        self.dev.render()
        
    def hydrate_block(self, block):
        for my_i in range(4):
            my_xy = block.get_xy(my_i)
            self.bg[my_xy[0]][my_xy[1]] = 1

    def collides(self, block):
        for my_i in range(4):
            my_xy = block.get_xy(my_i)

            if (my_xy[0] == self.size[0] or my_xy[0] == -1 or my_xy[1] == self.size[1] or my_xy[1] == -1):
                return True
            
            if (self.bg[my_xy[0]][my_xy[1]]) == 1:
            	return True
            
        return False

