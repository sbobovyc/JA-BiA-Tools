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
        
class Weapon:
    def __init__(self, id, armament, weight, price, resource_id, damage, 
                 best_range, quality, icon_id, icon_location, picture, deliverable):
        self.id = id
        self.armament = armament
        self.weight = weight
        self.price = price
        self.resource_id = resource_id
        self.damage = damage
        self.best_range = best_range
        self.quality = quality
        self.icon_id = icon_id
        self.icon_location = icon_location
        self.picture = picture
        self.deliverable = deliverable 

class Rifle(Weapon):
    def __init__(self, shot_effect_id, stance_factor, clip_size, ammunition, rpm, gun_type, anchor_point, *args):
        self.__init__(args)
        self.shot_effect_id
        self.stance_factor = stance_factor
        self.clip_size = clip_size
        self.ammunition = ammunition
        self.rpm = rpm
        self.gun_type = gun_type
        self.anchor_point = anchor_point

class Hand_gun(Weapon, Rifle):
    def __init__(self, *args):
        
class Knife(Weapon):
    def __init__(self, *args):
        self.__init__(args)
