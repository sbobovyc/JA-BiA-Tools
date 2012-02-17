class Anchor_point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def get_point(self):
        return (self.x, self.y, self.z)
    
class Texture:
    def __init__(self, id, full_path): 
        self.id = id
        self.full_path = full_path
        
class Picture(Texture):
    def __init__(self, picutre_id, picture_full_path):
        self.__init__(id, picture_full_path)
        
class Icon(Texture):        
    def __init__(self, icon_id, icon_full_path, x, y, width, height):
        self.__init__(id, icon_full_path)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Item:
    def __init__(self):
        self.id
        
class Weapon(Item):
    def __init__(self): 
        self.armament 
        self.weight 
        self.price 
        self.resource_id 
        self.damage 
        self.best_range 
        self.quality 
        self.icon_id 
        self.icon_location 
        self.picture 
        self.deliverable  

class Rifle(Weapon):
    def __init__(self):        
        self.shot_effect_id
        self.stance_factor 
        self.clip_size 
        self.ammunition 
        self.rpm 
        self.gun_type 
        self.anchor_point 

class Hand_gun(Weapon, Rifle):
    def __init__(self, *args):
        pass
    
class Knife(Weapon):
    def __init__(self):
        pass

if __name__ == "__main__":
    # example of object reflection
    tex = type("Texture", (object,), dict(id=1, full_path="."))
    print tex.id
    item = type("Item", (object,), dict(id=55))
    print item.id
