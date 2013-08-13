'''
The following classes will be used as containers in the Digester stack
'''

class StackNode():
    ''' will be used as a base container in the digester stack '''
    def __init__(self, typeName, aclNode=None):
        assert isinstance(typeName, str), 'Invalid node type name %s' % typeName
        self.Type = typeName
        self.Children = []
        self.AclNode = aclNode

    def __repr__(self):
        return str(self.__dict__)

class ActionContainer:
    def __init__(self, path, label=None, script=None, navbar=None, parent=None):
        self.Path = path
        self.Label = label
        self.Script = script
        self.NavBar = navbar
        if parent != None:
            self.Path = str.format('{0}.{1}', self.Path, parent)
        
    def getPath(self):
        return self.Path

    def __repr__(self):
        return str(self.__dict__)

class RightContainer:
    def __init__(self, name, description=''):
        self.Name = name
        self.Description = description
        self.Actions = []
        self.Filters = []
        
    def addActions(self, actions):
        self.Actions.extend(actions)
    
    def addFilter(self, filter):
        self.Filters.append(filter)
    
    def addToDescription(self, description):
        if self.Description == None: self.setDescription('')
        if description: self.Description += description
    
    def setDescription(self, description):
        self.Description = description
    
    def __repr__(self):
        return str(self.__dict__)

class FilterContainer:
    def __init__(self, name):
        self.Name = name
        self.URLs = []
        self.methods = []
    
    def addMethods(self, methods):
        self.methods.extend(methods)
    
    def addUrl(self, url):
        self.URLs.append(url)

    def __repr__(self):
        return str(self.__dict__)