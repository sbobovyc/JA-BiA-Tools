import struct


class JABIA_sound:

    def __init__(self, id, filename):
        self.id = id
        self.filename = filename

    def get_packed_data(self):
        import binascii
        data_buffer = struct.pack("<II%is" % len(self.filename),
                                  self.id, len(self.filename), self.filename)
#        print binascii.hexlify(data_buffer)
        return data_buffer

    def __repr__(self):
        return "%s(name=%r, id=%r, filename=%r)" % (
            self.__class__.__name__, self.id, self.filename)

    def __str__(self):
        return "Sound ID: %s = %s" % (self.id, self.filename)


class JABIA_font:

    def __init__(self, id, font_name, filename):
        self.id = id
        self.font_name = font_name
        self.filename = filename

    def get_packed_data(self):
        import binascii
        data_buffer = struct.pack("<II%isI%is" % (len(self.font_name), len(self.filename)),
                                  self.id, len(self.font_name), self.font_name, len(self.filename), self.filename)
#        print binascii.hexlify(data_buffer)
        return data_buffer

    def __repr__(self):
        return "%s(name=%r, id=%r, font_name=%r, filename=%r)" % (
            self.__class__.__name__, self.id, self.font_name, self.filename)

    def __str__(self):
        return "Font ID: %s, %s = %s" % (self.id, self.font_name, self.filename)

# classes below are experimental


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
    print(tex.id)
    item = type("Item", (object,), dict(id=55))
    print(item.id)
    id = 57
    item = type("Item", (object,), dict(id=id))
    print(item.id)
