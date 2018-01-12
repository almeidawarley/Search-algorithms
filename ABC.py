import sys
import random
import math

'''
@ Tests:



@ Parameters:
	population: 			number of food sources
	dimension:				dimension of the problem
	max_iteration: 			maximum cycle number
	max_limit: 				maximum limit for variables
	min_limit:				minimum limit for variables
	limit: 					limit of iterations without receiving a solution from a scout
	function:				defines which function will be used as fitness function
	error:					defines acceptable error between fitness value and optimum value
'''
population = 125
dimension = 10
max_iteration = 2000
max_limit = 15
min_limit = -15
limit = dimension*population
function = 1
error = 0

class FoodSource:
	# initializes a food source with a random position
	def __init__(self, name, size, function):
		self.name = name
		self.size = size
		self.function = function
		self.values = [0 for i in range (self.size)]
		self.scout()

	# copies the position of other food source
	def copy(self, foodsource):
		self.name = foodsource.name
		self.size = foodsource.size
		self.function = foodsource.function
		for i in range(self.size):
			self.values[i] = foodsource.values[i]

	# prints the position of the food source
	def position(self, text):
		sys.stdout.write(' | $ Food source '+ self.name + ': ' + '\n')
		for i in range(0, self.size):
			sys.stdout.write(' | ['+ str(i) + ']: ' + str(self.values[i]) + '\n')
		sys.stdout.write(' | Fitness: ' + str(self.fitness()) + '\n')

	# generates a new random position
	def scout(self):
		for i in range(0, self.size):
			self.values[i] = random.uniform(min_limit, max_limit)

	# calculates the fitness based on a selected function
	def fitness(self):
		if self.function == 0:
			return abs(self.sphere())
		elif self.function == 1:
			return abs(self.rastrigin())
		elif self.function == 2:
			return abs(self.griewank())
		elif self.function == 3:
			return abs(self.schwefel())
		else:
			return abs(self.sphere())

	# calculates the fitness following the Sphere Function - # 0
	def sphere(self):
		sum = 0
		for i in range(self.size):
			sum += math.pow(self.values[i],2)
		return sum

	# calculates the fitness following the Rastrigin Function - #1
	def rastrigin(self):
		sum = 0
		for i in range(self.size):
			sum += math.pow(self.values[i], 2) - 10*math.cos(2*math.pi*self.values[i]) + 10
		return sum 

	# calculates the fitness following the Griewank Function - #2
	def griewank(self):
		sum = 0
		mult = 1
		for i in range(self.size):
			sum += math.pow(self.values[i],2)
		sum *= (1/4000)
		sum += 1
		for i in range(self.size):
			mult *= math.cos((self.values[i]/math.sqrt(i+1)))
		sum -= mult
		return sum

	# calculates the fitness following the Schwefel Function - #3
	def schwefel(self):
		sum = self.size*418.9829
		for i in range(self.size):
			sum += (-1)*self.values[i]*math.sin(math.sqrt(abs(self.values[i])))
		return sum

	def rosenbrock(self):
		return 100*math.pow((self.values[1] - math.pow(self.values[0],2)), 2) + pow((self.values[0] - 1),2)


	# explores the neighbourhood of the food source following a specific formula
	def neighbourhood(self, foodsources):
		prototype = FoodSource('proto', self.size, self.function)
		prototype.copy(self)
		coefficient = random.uniform(-1,1)
		index = random.randint(0, self.size - 1)
		individual = random.randint(0, len(foodsources) - 1)
		# check whether the chosen individual is the same individual
		while foodsources[individual].name == self.name:
			individual = random.randint(0, len(foodsources) - 1)
		prototype.values[index] = prototype.values[index] + coefficient*(prototype.values[index] - foodsources[individual].values[index])
		# check maximum and minimum boundaries
		if prototype.values[index] < min_limit:
			prototype.values[index] = min_limit
		if prototype.values[index] > max_limit:
			prototype.values[index] = max_limit
		if prototype.fitness() <= self.fitness():
			self.copy(prototype)
			return True
		return False

def wait():	
	a = raw_input("Type anything to continue...")

# this function chooses based on a given probability and a random number whether a onlooker will choose the food source
def choose(probability):
	rand = float(random.randint(0,100))/float(100)
	if rand <= probability:
		return True
	else:
		return False

'''
# reads arguments
if len(sys.argv) > 1:
	population = int(sys.argv[1])
	if len(sys.argv) > 2:
		dimension = int(sys.argv[2])
		if len(sys.argv) > 3: 
			max_iteration = int(sys.argv[3])
			if len(sys.argv) > 4:
				max_limit = int(sys.argv[4])
				min_limit = -max_limit
				if len(sys.argv) > 5:
					limit = int(sys.argv[5])

'''
output = open('function' + str(function) + '.txt', 'a')
foodsources = [FoodSource(str(i), dimension, function) for i in range(population)]
best_solution = FoodSource('best', dimension, function)
trials = [0 for i in range(population)]
n_iteration = 0

# keeps going until the max_iteration is reached or the optimal solution is found
while best_solution.fitness() > error and n_iteration < max_iteration:
	n_iteration = n_iteration + 1

	# employed bees exploit the neighbourhood of its last position
	for i in range(population):
		if(foodsources[i].neighbourhood(foodsources)):
			trials[i] = 0
		else:
			trials[i] += 1

	# employed bees share the information with onlooker bees
	# the probability of each food source is calculated
	probability = []
	sumFitness = 0
	for i in range(population):
		sumFitness = sumFitness + foodsources[i].fitness()
	for i in range(population):
		probability.append(1-float(foodsources[i].fitness())/float(sumFitness))

	# onlookers choose the food sources and exploit them
	onlookers_index = 0
	food_index = 0
	while onlookers_index < population:		
		if choose(probability[food_index]):
			onlookers_index += 1
			if(foodsources[food_index].neighbourhood(foodsources)):
				trials[i] = 0
			else:
				trials[i] += 1
		food_index += 1
		if food_index >= population:
			food_index = 0

	# food sources are analyzed and a scout brings one new solution if necessary
	max_trials = 0
	for i in range(1, population):
		if(trials[i] > trials[max_trials]):
			max_trials = i
	if max_trials > limit:
		foodsources[max_trials].scout()
		trials[max_trials] = 0

	for i in range(population):
		if foodsources[i].fitness() < best_solution.fitness():
			best_solution.copy(foodsources[i])
	print "> Iteration " + str(n_iteration) + " - Best solution: " + str(best_solution.fitness())

#for i in range(population):
#	foodsources[i].position(str(i))
print "@ Parameters: \n $ Population size: " + str(population) + "\n $ Dimension: " + str(dimension) + "\n $ Maximum cycle number: " + str(n_iteration) 
print " $ Maximum limit: " + str(max_limit) + "\n $ Minimum limit: " + str(min_limit) + "\n $ Limit: " + str(limit)
if function == 1:
	print " $ Function: Rastrigin"
elif function == 2:
	print " $ Function: Griewank"
elif function == 3:
	print " $ Function: Schwefel"
else:
	print " $ Function: Sphere"
print " $ Error: " + str(error)
best_solution.position('Best solution: ')
output.write(str(best_solution.fitness())+'\n')


population = 125
dimension = 10
max_iteration = 2000
max_limit = 600
min_limit = -600
limit = dimension*population
function = 0
error = 0