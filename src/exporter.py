from pprint import pprint
import xml.etree.ElementTree as ET

class Xmi():
    """ Given a data tree, builds an XMI document and writes to a file """

    # ET.Element
    __tree = None

    # Map between human intuitive attribute names and XMI’s
    __attr_map = {
        'type': 'xmi:type',
        'signature': 'signature'
    }

    __types = {
        'class': 'uml:Class'
    }

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
        toplevel = False

        if self.__tree is None:
            self.__tree = ET.Element('{http://www.w3.org/2005/Atom}feed', attrib={'{`namespace`}lang': 'en'})

        if parent is None:
            toplevel = True
            parent = self.__tree

        # pprint(branches)
        for branch in branches:
            type_ = type(branch)
            if type_ is tuple:
                if branch[1]['type'] is 'class':
                    self.__addPackagedElement(parent, branch)
                elif branch[1]['type'] in ['function', 'method', 'constructor']:
                    node = self.__addOwnedOperation(parent, branch)
                elif branch[1]['type'] in ['attribute', 'variable', 'import']:
                    self.__addOwnedAttribute(parent, branch)
                elif branch[1]['type'] is 'comment':
                    self.__addOwnedComment(parent, branch[0])
                else:
                    raise ValueError('Unknown node type {}'.format(branch[1]['type']))
            elif type_ is list:
                if toplevel or 'type' in branch[0][1] and branch[0][1]['type'] is 'class':
                    node = self.__addPackagedElement(parent, branch[0])
                else:
                    node = self.__addOwnedOperation(parent, branch[0])
                self.__addBranches(branch[1:], node)

    def __addPackagedElement(self, parent, node):
        """ packagedElement nodes are the highest level entries
        """
        print('\t__addPackagedElement')
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
        print('\t__addOwnedOperation')
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
        print('_addOwnedAttribute')
        attrs = {'name': node[0]}
        attrs['xmi:id'] = '0'
        if 'type' in node[1]:
            attrs['xmi:type'] = node[1]['type']
        if 'visibility' in node[1]:
            attrs['visibility'] = node[1]['visibility']

        return ET.SubElement(parent, 'ownedAttribute', attrs)

    def __addOwnedParameters(self, parent, signature):
        print('__addOwnedParameters')
        for s in range(len(signature)):
            ET.SubElement(parent, 'ownedParameter', {
                'name': signature[s],
                'xmi:id': '0'
            })
        return parent

    def __addOwnedComment(self, parent, value):
        print('__addOwnedComment')
        ET.SubElement(parent, 'ownedComment', {
            'body': value,
            'xmi:id': '0'
        })
        return parent
