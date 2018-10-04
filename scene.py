class Scene:

    def __init__(self, dev):
        self.blocks = []
        self.dev = dev

    def add_block(self, block):
        self.blocks.append(block)

    def render(self):
        self.dev.clean()
        for block in self.blocks:
            block.render(self.dev)
        self.dev.render()

    def does_collide(self, block):
        for my_i in range(4):
            my_xy = block.get_xy(my_i)

            if (my_xy[0] == 8 or my_xy[0] == -1 or my_xy[1] == 16 or my_xy[1] == -1):
                return True
            
            for b in self.blocks:
                if (b != block):
                    for other_i in range(4):
                        other_xy = b.get_xy(other_i)
                        if (other_xy == my_xy):
                            return True
        return False

