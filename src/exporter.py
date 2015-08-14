import xml.etree.ElementTree as ET

class Xmi():
    """ Given a data tree, builds an XMI document and writes to a file """

    # ET.Element
    __tree = None

    def setTree(self, data):
        """ Public interface to recursive __addBranches

            @param list data (see __addBranches)
        """
        self.__addBranches(data)

    def write(self, filepath):
        """ Writes file

            @raise RuntimError
            @raise OSError
            Returns written byte count (0 for none, -1 for error)
        """
        if self.__tree is None:
            raise RuntimeError
        document = ET.ElementTree(self.__tree)
        document.write(filepath, 'UTF-8')

    def __addBranches(self, branches, parent=None):
        """ Convert data to ET.Element

            @param list branches such as (str induced)
            @param ET.Element parent
            [
              [(master, {type: class}),
                (randval, {type: method}), [(init, {type: method, signature: [...]}),
                  (change, {type: function}) ] ] ]
            @raise ValueError
        """
        if self.__tree is None:
            self.__tree = ET.Element('{http://www.w3.org/2005/Atom}feed', attrib={'{`namespace`}lang': 'en'})

        parent = self.__tree if parent is None else parent

        for branch in branches:
            if isinstance(branch, tuple):
                ET.SubElement(parent, branch[0])
            else:
                item = ET.SubElement(parent, branch[0][0])
                self.__addBranches(branch[1:], item)
