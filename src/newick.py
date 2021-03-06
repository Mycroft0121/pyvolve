#! /usr/bin/env python

##############################################################################
##  pyvolve: Python platform for simulating evolutionary sequences.
##
##  Written by Stephanie J. Spielman (stephanie.spielman@gmail.com) 
##############################################################################

'''
Read/parse a newick tree.
'''

import re
import os


class Tree():
    '''
        Defines a Tree() object, which is ultimately comprised of a series of nested Tree() objects.
        In effect, each Tree() instance represents a node within a larger phylogeny.
    '''
    def __init__(self):
            
        self.name           = None # Internal node unique id or leaf name
        self.children       = []   # List of children, each of which is a Tree() object itself. If len(children) == 0, this tree is a tip.
        self.branch_length  = None # Branch length leading up to node
        self.model_flag     = None # Flag indicate that this branch evolves according to a distinct model from parent
        self.seq            = None # Contains sequence (represented by integers) for a given node. EVENTUALLY THIS WILL BE REPLACED BY A LIST OF Site() OBJECTS.



def read_tree(**kwargs):
    
    '''
        Parse a newick phylogeny, provided either via a file or a string. The tree does not need to be bifurcating, and may be rooted or unrooted.
        Returns a Tree() object along which sequences may be evolved.  
            
        Trees can either read from a file or given directly to ``read_tree`` as a string. One of these two keyword arguments is required.
        
            1. **file**, the name of the file containing a newick tree for parsing. If this argument is provided in addition to tstring, the tree in the file will be used and tstring will be ignored.
            2. **tree**, a newick tree string. If a file is additionally provided, the tstring argument will be ignored.   
        
        To implement branch (temporal) heterogeneity, place "model flags" at particular nodes within the tree. Model flags must be in the format *#flagname#* (i.e. with both a leading and a trailing pound sign), and they should be placed *after* the branch lengths.
        Model flags may be repeated throughout the tree, but the model associated with each model flag will always be the same. Note that these model flag names **must** have correspondingly named model objects.


        Examples:
            .. code-block:: python
                
               tree = read_tree(file = "/path/to/tree/file.tre")
               tree = read_tree(tree = "(t4:0.785,(t3:0.380,(t2:0.806,(t5:0.612,t1:0.660):0.762):0.921):0.207);")
               
               # Tree containing model flags named m1 and m2
               tree = read_tree(tree = "(t4:0.785,(t3:0.380,(t2:0.806,(t5:0.612,t1:0.660):0.762#m1#):0.921)#m2#:0.207);"
    '''    
    
    filename           = kwargs.get('file')
    tstring            = kwargs.get('tree')
        
    if filename:
        assert (os.path.exists(filename)), "File does not exist. Check path?"
        t = open(filename, 'r')
        tstring = t.read()
        t.close()
    else:
        assert (tstring is not None), "You need to either specify a file with a tree or give your own."
        assert (type(tstring) is str), "Trees provided with the flag `tree` must be in quotes to be considered a string."
        
    tstring = re.sub(r"\s", "", tstring)
    tstring = tstring.rstrip(';')
    
    flags = []
    internal_node_count = 1
    (tree, flags, internal_node_count, index) = _parse_tree(tstring, flags, internal_node_count, 0) 
    _assign_model_flags_to_nodes(tree)
    
    return tree


def print_tree(tree, level=0):
    '''
        Prints a Tree() object in graphical, nested format. 
        This function takes two arguments:
            
            1. **tree** is a Tree object to print
            2. **level** is used internally for printing. DO NOT PROVIDE THIS ARGUMENT.
        
        Each node in the tree is represented by a string in the format, "name   branch.length   model.flag", and levels are represented by indentation.
        Names for tree tips are taken directly from the provided tree, and internal node names are assigned automatically by the ``read_tree`` function.
        The node with a branch length of None will be the root node where sequence evolution will begin.
        Note that the model.flag field will be None under cases of branch homogeneity.       
        
        For example,
            .. code-block:: python
            
               >>> my_tree = read_tree(tree = "(t4:0.785,(t3:0.380,(t2:0.806,(t5:0.612,t1:0.660):0.762):0.921):0.207);")
               >>> print_tree(my_tree)
                    internal_node4 None None
                        t4 0.785 None
                            internal_node3 0.207 None
                                t3 0.38 None
                                internal_node2 0.921 None
                                    t2 0.806 None
                                    internal_node1 0.762 None
                                        t5 0.612 None
                                        t1 0.66 None
            
               >>> flagged_tree = newick.read_tree(tree = "(t4:0.785,(t3:0.380,(t2:0.806,(t5:0.612,t1:0.660):0.762#m1#):0.921)#m2#:0.207);")
               >>> newick.print_tree(flagged_tree)  
                    internal_node4 None None
                    	t4 0.785 None
                    	internal_node3 None m2
                    		t3 0.38 m2
                    		internal_node2 0.921 m2
                    			t2 0.806 m2
                    			internal_node1 0.762 m1
                    				t5 0.612 m1
                    				t1 0.66 m1
                    	0.207 None None                 
                            
    ''' 
    indent=''
    for i in range(level):
        indent+='\t'
    print indent, tree.name, tree.branch_length, tree.model_flag
    if len(tree.children) > 0:
        for node in tree.children:
            print_tree(node, level+1)    
    


def _assign_model_flags_to_nodes(tree, parent_flag = None):
    '''
        Determine the evolutionary model to be used at each node.
        Note that parent_flag = None means root model!!
    '''
    
    # Assign model if there was none in the tree
    if tree.model_flag is None:
        tree.model_flag = parent_flag

    if len(tree.children) > 0:
        for node in tree.children:
            parent_flag = _assign_model_flags_to_nodes(node, tree.model_flag)
    return parent_flag
    

def _read_model_flag(tstring, index):
    '''
        Read a model flag id while parsing the tree from the function _parse_tree.
        Model flags are expected to be in the format _flag_, and they must come **after** the branch length associated with that node, before the comma.
    '''
    index +=1 # Skip the leading underscore
    end = index
    while True:
        end+=1
        if tstring[end]=='#':
            break
    model_flag = tstring[index:end]
    return model_flag, end+1
     
     
def _read_branch_length(tstring, index):
    '''
        Read a branch length while parsing the tree from the function _parse_tree.
    '''
    end = index
    while True:
        end += 1
        if end==len(tstring):
            break
        if tstring[end]==',' or tstring[end]==')' or tstring[end] == '#':
            break
    BL = float( tstring[index+1:end] )
    return BL, end


def _read_leaf(tstring, index):
    '''
        Read a leaf (taxon name) while parsing the tree from the function _parse_tree.
    '''
    end = index
    node = Tree()
    while True:
        end += 1
        assert( end<len(tstring) ), "\n\nUh-oh! I seem to have reached the end of the tree, but I'm still trying to parse something. Please check that your tree is in proper newick format."
        # Leaf has no branch length
        if tstring[end]==',' or tstring[end]==')':
            node.name = tstring[index+1:end]
            node.branch_length = None
            break    
        # Leaf has branch length    
        if tstring[end]==':' :
            node.name = tstring[index:end]
            node.branch_length, end = _read_branch_length(tstring, end)
            break       
    # Does leaf have a model? 
    if tstring[end] == '#':
        node.model_flag, end = _read_model_flag(tstring, end)
    return node, end


def _parse_tree(tstring, flags, internal_node_count, index):
    '''
        Recursively parse a newick tree string and convert to a Tree object. 
        Uses the functions _read_branch_length(), _read_leaf(), _read_model_flag() during the recursion.
    '''
    assert(tstring[index]=='(')
    index += 1
    node = Tree()
    while True:
        
        # New subtree (node) to parse
        if tstring[index]=='(':
            subtree, flags, internal_node_count, index=_parse_tree(tstring, flags, internal_node_count, index)
            node.children.append( subtree ) 
             
        
        # March to sister
        elif tstring[index]==',':
            index += 1            
        
        # End of a subtree (node)
        elif tstring[index]==')':
            index+=1
            node.name = "internal_node" + str(internal_node_count)
            internal_node_count += 1
            # Now we have either a model flag, BL or both. But the BL will be *first*.            
            if index<len(tstring):
                if tstring[index]==':':
                    BL, index = _read_branch_length(tstring, index)
                    node.branch_length = BL
                if tstring[index]=='_':
                    model_flag, index = _read_model_flag(tstring, index)
                    node.model_flag = model_flag
                    flags.append(model_flag)
            break
        # Terminal leaf
        else:
            subtree, index = _read_leaf(tstring, index)
            node.children.append( subtree )
    return node, flags, internal_node_count, index    
    

            
