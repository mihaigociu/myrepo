from ally.xml.digester import Rule, Digester, Node
from acl_digester_rules import *
from acl_auxiliary_classes import *

class AclConfigScanner:
    '''
    Parses the Acl rights file and builds the Rights, Actions, and Filters structures
    '''
    
    def __init__(self):
        self._root = self.defineNodesStructure()
        self._digester = Digester(self._root)
        self._cleanDigester = True
    
    def scanAclFile(self, aclFile):
        f = open(aclFile, 'r')
        if not self._cleanDigester: self.cleanupDigester()
        
        try:
            self._digester.parse('UTF-8',f)
        except Exception as e:
            self.cleanupDigester()
            #also do some error handling - print out a message describing the error
            print(e) 
        
        self._cleanDigester = False
        f.close()
    
    def cleanupDigester(self):
        self._digester.stack = []
        self._digester.errors = []
        self._digester._nodes = []
    
    def defineNodesStructure(self):
        '''
        defines the structure of the Acl xml file
        '''
        
        root = Node('ROOT')
        root.addRule(RightsRule(), 'Rights')
        
        #define here the structure of the sub-nodes in order to be re-used 
        #action node will be recursive (we can have action inside action)
        action = Node('Action')
        action.addRule(ActionRule())
        action.childrens = {'Action': action}
        
        actions = Node('Actions')
        actions.addRule(ActionsRule())
        actions.childrens = {'Action': action}
        
        allows = Node('Allows')
        allows.addRule(FilterRule())
        allows.addRule(URLRule(), 'URL')
        
        description = Node('Description')
        description.addRule(DescriptionRule())
        
        #sub-nodes of the root node
        root.addRule(RightRule(), 'Rights/Anonymous')
        root.addRule(RightRule(), 'Rights/Captcha')
        root.addRule(RightRule(), 'Rights/Right')
        
        #sub-nodes of the Right nodes
        for name, node in root.childrens['Rights'].childrens.items():
            node.childrens['Actions'] = actions
            node.childrens['Action'] = action
            node.childrens['Allows'] = allows
            node.childrens['Description'] = description    

        return root



