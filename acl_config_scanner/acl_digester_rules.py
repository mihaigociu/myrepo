from ally.xml.digester import Rule, Node
from acl_auxiliary_classes import *

class ActionRule(Rule):
    def begin(self, digester, **attributes):
        #action nodes can be nested; if this is the case, concat parent path and child path
        parent = None
        if digester.stack[-1].Type == 'Action': parent = digester.stack[-1].AclNode

        path = attributes.get('path')
        if parent and not path.startswith(parent.getPath()):
            path = str.format('{0}.{1}', parent.getPath(), path)
        
        action = ActionContainer(path, attributes.get('label'), \
                             attributes.get('script'), attributes.get('navbar'), \
                             attributes.get('parent'))
        digester.stack.append(StackNode('Action', action))
                
    def content(self, digester, content):
        pass
        
    def end(self, node, digester):
        actionNode = digester.stack.pop()
        if digester.stack[-1].Type == 'Right':
            digester.stack[-1].AclNode.addActions([actionNode.AclNode])
            #also add the children of the Action to the Right
            digester.stack[-1].AclNode.addActions([child.AclNode for child in actionNode.Children])
        else:
            #we have some nested Actions here; we will attach the action to its Action parent (in Children list), which will then pass all the Children to its own parent or to a Right object 
            assert digester.stack[-1].Type in ('Action', 'Actions')
            digester.stack[-1].Children.append(actionNode)

class ActionsRule(Rule):
    def begin(self, digester, **attributes):
        digester.stack.append(StackNode('Actions'))
        pass
    
    def content(self, digester, content):
        pass
        
    def end(self, node, digester):
        #add all the actions in this node to the Right node that contains it
        actionsNode = digester.stack.pop()
        assert digester.stack[-1].Type == 'Right'
        digester.stack[-1].AclNode.addActions([child.AclNode for child in actionsNode.Children])

class RightsRule(Rule):
    def begin(self, digester, **attributes):
        digester.stack.append(StackNode('Rights'))
                
    def content(self, digester, content):
        pass
        
    def end(self, node, digester):
        pass

class RightRule(Rule):
    def begin(self, digester, **attributes):
        node = digester._nodes[-1]
        assert isinstance(node, Node)
        right = RightContainer(attributes.get('name', node.name), attributes.get('description'))
        digester.stack.append(StackNode('Right', right))

    def content(self, digester, content):
        pass
        
    def end(self, node, digester):
        rightNode = digester.stack.pop()
        digester.stack[-1].Children.append(rightNode)

class FilterRule(Rule):
    def begin(self, digester, **attributes):
        filter = FilterContainer(attributes.get('filter'))
        filter.addMethods([m.strip() for m in attributes.get('methods', '').split(',') if m != ''])
        digester.stack.append(StackNode('Allows', filter))
                
    def content(self, digester, content):
        pass
        
    def end(self, node, digester):
        filterNode = digester.stack.pop()
        assert digester.stack[-1].Type == 'Right'
        digester.stack[-1].AclNode.addFilter(filterNode.AclNode)

class URLRule(Rule):
    def begin(self, digester, **attributes):
        pass
                
    def content(self, digester, content):
        assert isinstance(content, str)
        assert digester.stack[-1].Type == 'Allows'
        digester.stack[-1].AclNode.addUrl(content)
        
    def end(self, node, digester):
        pass

class DescriptionRule(Rule):
    def begin(self, digester, **attributes):
        pass
                
    def content(self, digester, content):
        assert isinstance(content, str)
        assert digester.stack[-1].Type == 'Right'
        digester.stack[-1].AclNode.addToDescription(content)
        
    def end(self, node, digester):
        pass
