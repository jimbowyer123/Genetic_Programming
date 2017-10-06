import Genetic_Programming.Genetic_Programming as GPC



def add(a,b):
    return(a+b)

def subtract(a,b):
    return(a-b)

def multiply(a,b):
    return(a*b)

def protected_division(numerator,denominator):
    if denominator==0:
        return(1)
    else:
        return(numerator/denominator)

add_function=GPC.Function(add, 2)
subtract_function=GPC.Function(subtract, 2)
multiply_function=GPC.Function(multiply, 2)
division_function=GPC.Function(protected_division, 2)
functions=[add_function,subtract_function,multiply_function,division_function]
terminal_1=GPC.Terminal(0)
terminal_2=GPC.Terminal(1)
terminal_3=GPC.Terminal(2)
terminals=[terminal_1,terminal_2,terminal_3]
tree=GPC.create_new_function_tree(functions, terminals, 3)
x=GPC.evaluate_tree(tree, terminals, functions)
y=GPC.count_nodes(tree)
test_tree=[GPC.Node(0, 0), [GPC.Node(0, 1), [GPC.Node(1, 1)], [GPC.Node(1, 2)]], [GPC.Node(1, 2)]]
what_is_wrong=GPC.get_subtree(test_tree, 4)
replacement_tree=[GPC.Node(1, 2)]
new_tree=GPC.replace_subtree(test_tree, replacement_tree, 2)
new_peeps=GPC.crossover(tree, test_tree, 1)
print('done')


