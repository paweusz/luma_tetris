class Scene:

    def __init__(self, dev, size):
        self.block = None
        self.dev = dev
        self.size = size
        self.bg = [[False for i in range(size[0])] for i in range(size[1])]

    def set_current_block(self, block):
        self.block = block

    def render(self):
        self.dev.clean()

        self.block.render(self.dev)
        for x in range(self.size[0]):
        	for y in range(self.size[1]):
        		if self.bg[y][x]:
        			self.dev.point((x, y))

        self.dev.render()
        
    def hydrate_block(self, block):
        for my_i in range(4):
            my_xy = block.get_xy(my_i)
            self.bg[my_xy[1]][my_xy[0]] = 1

    def collides(self, block):
        for my_i in range(4):
            my_xy = block.get_xy(my_i)

            if (my_xy[0] == self.size[0] or my_xy[0] == -1 or my_xy[1] == self.size[1] or my_xy[1] == -1):
                return True
            
            if (self.bg[my_xy[1]][my_xy[0]]):
            	return True
            
        return False

    def process_lines(self):
        for y in range(self.size[1]):
            if self.full_line(y):
                del self.bg[y]
                self.bg.insert(0, [False for i in range(self.size[0])])
    
    def full_line(self, y):
        for x in range(self.size[0]):
            if not self.bg[y][x]:
                return False
        return True


