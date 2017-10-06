import random
import copy

def mate(program_1,program_2,max_depth):
    new_trees=crossover(program_1.Tree,program_2.Tree,max_depth)
    new_programs=[Program(new_trees[0]),Program(new_trees[1])]
    return(new_programs)

def create_random_program_population(number_people,functions,terminals,max_depth):
    population=Program_Population([])
    for i in range(number_people):
        population.Programs.append(Program(create_new_function_tree(functions, terminals, max_depth)))
    return(population)

def crossover(tree_1,tree_2,max_depth):
    new_trees=[]
    node_count_1=count_nodes(tree_1)
    node_count_2=count_nodes(tree_2)
    crossover_point_1=random.randint(0,node_count_1-1)
    crossover_point_2=random.randint(0,node_count_2-1)
    subtree_1=get_subtree(tree_1,crossover_point_1)
    subtree_2=get_subtree(tree_2,crossover_point_2)
    new_tree_1=replace_subtree(tree_1,subtree_2,crossover_point_1)
    new_tree_2=replace_subtree(tree_2,subtree_1,crossover_point_2)
    if find_tree_depth(new_tree_1)>max_depth:
        new_tree_1=tree_1
    if find_tree_depth(new_tree_2)>max_depth:
        new_tree_2=tree_2
    new_trees.append(new_tree_1)
    new_trees.append(new_tree_2)
    return(new_trees)

def find_tree_depth(tree):
    if tree[0].Type==1:
        return(1)
    subtree_depths=[]
    for  i in range(1,len(tree)-1):
        subtree_depths.append(find_tree_depth(tree[i]))
    return(1+max(subtree_depths))

def get_subtree(tree,subtree_number,current_value=0):
    if current_value==subtree_number:
        return(copy.deepcopy(tree))
    counter = current_value
    if tree[0].Type == 1:
        return(counter)
    for i in range(1,len(tree)):
        counter=counter+1
        counter = get_subtree(tree[i],subtree_number,counter )
        if not isinstance(counter,int):
            return(counter)
    return(counter)

def replace_subtree(tree,replacement_tree,replacement_point,current_value=0):
    if current_value==replacement_point:
        return(replacement_tree)
    counter=current_value
    if tree[0].Type==1:
        return(counter)
    for i in range(1,len(tree)):
        counter+=1
        counter=replace_subtree(tree[i],replacement_tree,replacement_point,counter)
        if not isinstance(counter,int):
            new_tree=copy.deepcopy(tree)
            new_tree[i]=counter
            return(new_tree)
    return(counter)



def count_nodes(tree):
    if len(tree)==1:
        return(1)
    else:
        nodes=1
        for i in range(1,len(tree)):
            nodes=nodes + count_nodes(tree[i])
        return(nodes)
def evaluate_tree(tree,terminals,functions):
    if tree[0].Type==1:
        return(terminals[tree[0].Number].Terminal)
    if tree[0].Type==0:
        arguments=[]
        for i in range(1,len(tree)):
            arguments.append(evaluate_tree(tree[i],terminals,functions))
        return(functions[tree[0].Number].evaluate(arguments))

def continue_function_tree(functions,terminals,max_depth,current_depth,terminal_probability):
    if current_depth==max_depth:
        return([Node(1,random.randint(0,len(terminals)-1))])
    random_number=random.random()
    if random_number<terminal_probability:
        return([Node(1,random.randint(0,len(terminals)-1))])
    else:
        function_number=random.randint(0,len(functions)-1)
        tree=[]
        tree.append(Node(0,function_number))
        number_arguments=functions[function_number].Number_Arguments
        for i in range(number_arguments):
            tree.append(continue_function_tree(functions,terminals,max_depth,current_depth+1,terminal_probability))
        return(tree)


def create_new_function_tree(functions,terminals,max_depth,terminal_probability=0.5):
    tree=[]
    random_number = random.random()
    if random_number<terminal_probability:
        tree.append(Node(1,random.randint(0,len(terminals)-1)))
        return(tree)
    else:
        function_number=random.randint(0,len(functions)-1)
        tree.append(Node(0,function_number))
        number_arguments=functions[function_number].Number_Arguments
        for i in range(number_arguments):
            tree.append(continue_function_tree(functions,terminals,max_depth,1,terminal_probability))
        return(tree)



class Node:
    def __init__(self,type,number):
        self.Type=type
        self.Number=number

    def __repr__(self):
        if self.Type==1:
            return('T-'+str(self.Number))
        if self.Type==0:
            return('F-'+str(self.Number))

class Function:
    def __init__(self,function,number_arguments):
        self.Function=function
        self.Number_Arguments=number_arguments

    def evaluate(self,arguments):
        return(self.Function(*arguments))

class Terminal:
    def __init__(self,terminal):
        self.Terminal=terminal

class Program:
    def __init__(self,tree,score=0):
        self.Tree=tree
        self.Score=score


class Program_Population:
        def __init__(self, people, generation=0):
            self.Programs = people
            self.Generation = generation

        def assign_scores(self,utility_function,terminals,functions):
            for program in self.Programs:
                program.Score=utility_function(program,terminals,functions)

        def retrieve_scores_list(self):
            scores_list=[]
            for program in self.Programs:
                scores_list.append(program.Score)
            return(scores_list)

        def invert_scores(self):
            for program in self.Programs:
                current_score = program.Score
                program.Score = current_score * -1

        def transform_scores(
                self):  # To implement the algorithm we must make all the scores greater than or equal to zero but maintain the same order
            scores = self.retrieve_scores_list()  # Get the current list of scores
            min_score = min(scores)  # Find the minimum score in the list of sores
            if min_score < 0:  # Check to see if the minimum is negative, If it is not then we do not need to do any transformations
                for i in range(len(scores)):
                    self.Programs[i].Score = scores[i] - min_score

        def normalise_scores(self):  # Want to assign scores as proportions of total population score
            scores = self.retrieve_scores_list()  # Retrieve a current list of the scores for the population
            sum_scores = sum(scores)  # Find the sum of all scores
            for i in range(len(scores)):
                self.Programs[i].Score = scores[i] / sum_scores

        def create_mating_pool(self):
            population_size = len(self.Programs)  # Find how many people are in our population
            Mating_Pool = Program_Population([],
                                             self.Generation)  # Let the mating pool be a new population but with same generation count
            for i in range(
                    population_size):  # Run iteration through population size to create mating pool of the same size
                random_number = random.random()  # produce psuedorandom number between 0 and 1 which will be used to choose who makes it to the mating pool
                score_count = 0  # Start a score count to add up the scores till the random number is within the range of a persons score interval
                for Person in self.Programs:  # Run an iteration through the population to choose who gets added to the mating pool
                    score_count = score_count + Person.Score  # Add new persons score to the score count creating an interval between last score count and new score count
                    if random_number < score_count:  # See if the random number is within the relevant interval
                        Mating_Pool.Programs.append(copy.deepcopy(Person))  # If it is within the interval then add said person to the mating pool
                        break  # Break so we do not add more people from this iteration
            return (Mating_Pool)

        def crossbreed(self,crossover_coefficient):
            New_Population=Program_Population([],self.Generation+1)
            while len(self.Programs)>0:
                if len(self.Programs)==1:
                    New_Population.Programs.append(self.Programs.pop())
                else:
                    random_number=random.random()
                    if random_number<crossover_coefficient:
                        New_Population.Programs=New_Population.Programs + mate(self.Programs.pop(),self.Programs.pop(),7)
                    else:
                        New_Population.Programs.append(self.Programs.pop())
            return(New_Population)


        def average_score(self):
            scores = self.retrieve_scores_list()
            average_score = sum(scores) / len(scores)
            return (average_score)

        def best_of_gen_min_score(self):
            best_score=min(self.retrieve_scores_list())
            for program in self.Programs:
                if program.Score==best_score:
                    return(program)

        def best_of_gen_max_score(self):
            best_score = max(self.retrieve_scores_list())
            for program in self.Programs:
                if program.Score == best_score:
                    return (program)

