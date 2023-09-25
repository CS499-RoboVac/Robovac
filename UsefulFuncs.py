class Vec2():
    def __init__(self, x, y = None):
        if isinstance(x, (tuple, list, Vec2)):
            if len(x) != 2:
                raise ValueError("Input tuple or list must have exactly 2 elements")
            self.x, self.y = x
        else:
            if y == None:
                raise ValueError("Vec2() takes 2 values or 1 list/tuple but only 1 was value was given")
            self.x = x
            self.y = y

    # funky way of making the operator stuff smaller
    def selector(self,b,op):
        return Vec2(op(self.x,b.x),op(self.y,b.y)) if type(b) == Vec2 else Vec2(op(self.x,b),op(self.y,b)) 
    
    def __add__(self,b):
        return self.selector(b,lambda x,y: x + y)

    def __sub__(self,b):
        return self.selector(b,lambda x,y: x - y) 
    
    def __mul__(self,b):
        return self.selector(b,lambda x,y: x * y)  
    
    def __truediv__(self,b):
        return self.selector(b,lambda x,y: x / y)  
    
    def __eq__(self,b):
        return type(b) == Vec2 and self.x == b.x and self.y == b.y

    # Allows for list like indexing, example Vec2(2,3)[0], returns 2
    def __getitem__(self, index):
        return self.y if index else self.x
    
    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"
    
    def __len__(self):
        return 2
    
    def __iter__(self):
        return iter((self.x,self.y))
    
    def length(self):
        return math.sqrt(self.x**2+self.y**2)
    
    def unit(self):
        return self/math.sqrt(self.x**2+self.y**2)

def Collision(pos, r, m): #(float, float) pos, float r, {(int, int):FloorTile} m -> bool
    for x in range(floor(pos.x-r), ceil(pos.x+r)+1):
        for y in range(floor(pos.y-r), ceil(pos.y+r)+1):
            if (Vec2(x, y)-pos).length()<r: #we looped over a square; now we're using the ones within a radius in that square
                if not (x, y) in m:
                    return True #there was a collision
    return False #no collisions, we can go onwards