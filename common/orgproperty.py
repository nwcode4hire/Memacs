# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-20 15:13:31 awieser>
import hashlib


class OrgProperties(object):
    """
    Class for handling Memacs's org-drawer:

    :PROPERTIES:
    ...
    :<tag>: value
    ...
    :ID:  - id is generated from all above tags/values
    :END:
    """

    def __init__(self, data_for_hashing=""):
        """
        Ctor
        @param data_for_hashing: if no special properties are set,
        you can add here data only for hash generation
        """
        self.__properties = {}
        self.__data_for_hashing = data_for_hashing

    def add(self, tag, value):
        """
        Add an OrgProperty(tag,value) to the properties
        @param tag: property tag
        @param value: property value
        """
        tag = unicode(tag).strip().upper()
        value = unicode(value).strip()
        if tag == "ID":
            raise Exception("you should not specify an :ID: property " + \
                            "it will be generated automatically")

        self.__properties[tag] = unicode(value)

    def __get_property_max_tag_width(self):
        width = 14  # :MEMACS_CREATED: has width 14
        for key in self.__properties.keys():
            if width < len(key):
                width = len(key)
        return width

    def __format_tag(self, tag):
        num_whitespaces = self.__get_property_max_tag_width() - len(tag)
        whitespaces = ""
        for w in range(num_whitespaces):
            whitespaces += " "
        return "   :" + tag + ": " + whitespaces

    def __unicode__(self):
        """
        for representig properties in unicode with org formatting
        """
        ret = "   :PROPERTIES:\n"

        for tag, value in self.__properties.iteritems():
            ret += self.__format_tag(tag) + value + "\n"

        ret += self.__format_tag("ID") + self.get_id() + "\n"
        ret += "   :END:"
        return ret

    def get_id(self):
        """
        generates the hash string for all properties
        @return: sha1(properties)
        """
        to_hash = "".join(map(unicode, self.__properties.values()))
        to_hash += "".join(map(unicode, self.__properties.keys()))
        to_hash += self.__data_for_hashing
        return hashlib.sha1(to_hash.encode('utf-8')).hexdigest()
