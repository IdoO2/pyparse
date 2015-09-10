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
        toplevel = False

        if self.__tree is None:
            self.__tree = ET.Element('{http://www.w3.org/2005/Atom}feed', attrib={'{`namespace`}lang': 'en'})

        if parent is None:
            toplevel = True
            parent = self.__tree

        for branch in branches:
            type_ = type(branch)
            if type_ is tuple:
                if branch[1]['type'] == 'class':
                    self.__addPackagedElement(parent, branch)
                elif branch[1]['type'] in ['function', 'method', 'constructor']:
                    node = self.__addOwnedOperation(parent, branch)
                elif branch[1]['type'] in ['attribute', 'variable', 'import']:
                    self.__addOwnedAttribute(parent, branch)
                elif branch[1]['type'] == 'comment':
                    self.__addOwnedComment(parent, branch[0])
                else:
                    raise ValueError('Unknown node type {}'.format(branch[1]['type']))
            elif type_ is list:
                if toplevel or 'type' in branch[0][1] and branch[0][1]['type'] == 'class':
                    node = self.__addPackagedElement(parent, branch[0])
                else:
                    node = self.__addOwnedOperation(parent, branch[0])
                self.__addBranches(branch[1:], node)

    def __addPackagedElement(self, parent, node):
        """ packagedElement nodes are the highest level entries
        """
        attrs = {
            'name': node[0],
            'xmi:type': node[1]['type'],
            'xmi:id': '0'
        }
        if 'visibility' in node[1]:
            attrs['visibility'] = node[1]['visibility']

        return ET.SubElement(parent, 'packagedElement', attrs)

    def __addOwnedOperation(self, parent, node):
        """ ownedOperation nodes represent a callable (function, method)
        """
        attrs = {
            'name': node[0],
            'xmi:type': 'uml:Operation',
            'xmi:id': '0'
        }
        if 'visibility' in node[1]:
            attrs['visibility'] = node[1]['visibility']

        scope = ET.SubElement(parent, 'ownedOperation', attrs)

        if 'signature' in node[1]:
            self.__addOwnedParameters(scope, node[1]['signature'])

        return scope

    def __addOwnedAttribute(self, parent, node):
        """ ownedAttribute nodes represent a class attribute
        """
        attrs = {'name': node[0]}
        attrs['xmi:id'] = '0'
        if 'type' in node[1]:
            attrs['xmi:type'] = node[1]['type']
        if 'visibility' in node[1]:
            attrs['visibility'] = node[1]['visibility']

        return ET.SubElement(parent, 'ownedAttribute', attrs)

    def __addOwnedParameters(self, parent, signature):
        for s in range(len(signature)):
            ET.SubElement(parent, 'ownedParameter', {
                'name': signature[s],
                'xmi:id': '0'
            })
        return parent

    def __addOwnedComment(self, parent, value):
        ET.SubElement(parent, 'ownedComment', {
            'body': value,
            'xmi:id': '0'
        })
        return parent
