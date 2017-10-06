import Genetic_Programming.Genetic_Programming as GPC
import random
import copy


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
terminal_1=GPC.Terminal(5)
terminal_2=GPC.Terminal(20)
terminal_3=GPC.Terminal(14)
functions=[add_function,subtract_function,multiply_function,division_function]
terminals=[terminal_1,terminal_2,terminal_3]

def linsolve_function(program,terminals,functions):
    value=GPC.evaluate_tree(program.Tree, terminals, functions)
    score=abs(5*value + 20 - 14)
    return(score)

population=GPC.create_random_program_population(100, functions, terminals, 7)
average_scores=[]
best_of_gen=[]
while population.Generation<500:
    population.assign_scores(linsolve_function,terminals,functions)
    best_of_gen.append(copy.deepcopy(population.best_of_gen_min_score()))
    average_scores.append(population.average_score())
    print(best_of_gen[-1].Score)
    population.invert_scores()
    population.transform_scores()
    population.normalise_scores()
    mating_pool=population.create_mating_pool()
    population=mating_pool.crossbreed(0.2)
    population.Programs[0] = best_of_gen[-1]

print('end')




