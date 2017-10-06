import Genetic_Programming.Genetic_Programming as GPC
import copy
import math

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
terminals=[]
terminals.append(None)
functions=[add_function,subtract_function,multiply_function,division_function]
def utility_function(program,terminals,functions):
    score=0
    for i in range(1,25):
        terminals[-1]=GPC.Terminal(i * 2)
        score+= (GPC.evaluate_tree(program.Tree, terminals, functions) - (1 / (i * 2))) ** 2
    score=math.sqrt(score)
    return(score)

population=GPC.create_random_program_population(500, functions, terminals, 7)
average_scores=[]
best_of_gen=None
while population.Generation<300:
    population.assign_scores(utility_function, terminals, functions)
    if best_of_gen==None:
        best_of_gen = copy.deepcopy(population.best_of_gen_min_score())
    if best_of_gen.Score>population.best_of_gen_min_score().Score:
        best_of_gen=copy.deepcopy(population.best_of_gen_min_score())
    average_scores.append(population.average_score())
    print(str(best_of_gen.Score) + '      ' + str(population.average_score()))
    population.invert_scores()
    population.transform_scores()
    population.normalise_scores()
    mating_pool = population.create_mating_pool()
    population = mating_pool.crossbreed(0.5)


print('end')