#!/usr/bin/python
# -*- coding: utf-8 -*-

AUTOMATIC = "AUTOMATIC"

def bool(value):
    return eval("%s" % str(value))

class Property(dict):
    """This class represents a single typed and XML representable/serializable property"""

    def __init__(self, name, value, type=AUTOMATIC):
        dict.__init__(self)
        self.name = name
        if type == AUTOMATIC:
            self.type = self.get_type_from_value(value)
            self.value = value
        else:
            self.type = type
            if type.startswith("objects."):
                location = str(type).split('.')
                objects = __import__('.'.join(location[0:2]), globals(), locals(), [location[-1]], -1)
                self.value = eval('objects.%s("%s")' % (location[-1], value))
            else:
                self.value = eval('%s("%s")' % (type, value))

    def get_type_from_value(self, value):
        return str(type(value)).split("'")[1]

    def get_value(self):
        return self.value

    def serialize(self):
        return "<property name=\"%s\" type=\"%s\" value=\"%s\"/>" % (self.name, self.type, self.value)

class Properties(dict):
    """This class represents a collection of properties"""

    def __init__(self):
        dict.__init__(self)

    def set_property(self, property):
        self[property.name] = property

    def get_property(self, name):
        return self[name].get_value()

    def serialize(self):
        representation = ""
        for property in self.values():
            representation += "%s" % property.serialize()
        return representation

class Holder(object):
    """This class represents a object properties container"""

    def __init__(self):
        self.properties = Properties()

    def __str__(self):
        return self.serialize()

    def __repr__(self):
        return self.serialize()

    def __setattr__(self, name, value):
        if name in self.get_xxx():
            self.set_property(name, value)
        else:
            super(Holder, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name in self.get_xxx():
            return self.get_property(name)
        try:
            value = super(Holder, self).__getattr__(name)
        except:
            raise AttributeError
        return value

    def get_xxx(self):
        return []

    def set_property(self, name, value, type=AUTOMATIC):
        self.properties.set_property(Property(name, value, type))

    def get_property(self, name):
        return self.properties.get_property(name)

    def serialize(self):
        representation = "<object type=\"%s\">" % self.__name__
        representation += self.properties.serialize()
        representation += "</object>"
        return representation
