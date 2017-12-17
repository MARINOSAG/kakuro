from csp import *
from utils import *
from search import *

puzzle0 = [
[  '*'  ,  '*'  ,  '*'  ,(6,''),( 3,'')],
[  '*'  ,( 4,''),( 3, 3),  '-'  ,  '-'  ],
[('',10),  '-'  ,  '-'  ,  '-'  ,  '-'  ],
[ ('', 3),  '-'  ,  '-'  ,  '*'  ,  '*'  ]]
 
def get_neighbors(puzzle):

	print("puzzle is ",len(puzzle), len(puzzle[0] ) )
	neighbors_dict = {}
	for  row in range(len(puzzle))  :
		for column in range(len(puzzle0[0])) :
			if(puzzle[row][column] == '-'):#an prokeitai gia metablhth
				neighbors_dict[(row,column)] = []
				#gia toys katakoryfous geitones apo katw tou 
				for i in range (column+1, len(puzzle[0]) ) :
					if(puzzle[row][i] ==  '-'):#an o geitonas einai variable
						neighbors_dict[(row,column)].append((row,i))
					elif(puzzle[row][i] !=  '*'): #an brethei deyteros kanonas athrismatos
						break
				#gia toys katakoryfous geitones apo panw tou 
				for i in range (column-1,0,-1 ) :
					if(puzzle[row][i] ==  '-'):#an o geitonas einai variable
						neighbors_dict[(row,column)].append((row,i))
					elif(puzzle[row][i] !=  '*'): #an brethei deyteros kanonas athrismatos
						break;
				#gia toys orizontioys geitones apo ta deksia toy
				for i in range (row+1, len(puzzle) ) :
					if(puzzle[i][column] ==  '-'):#an o geitonas einai variable
						neighbors_dict[(row,column)].append((i,column))
					elif(puzzle[i][column] !=  '*'): #an brethei deyteros kanonas athrismatos
						break;
				#gia toys orizontioys geitones apo ta deksia toy
				for i in range (row-1,0,-1 ) :
					if(puzzle[i][column] ==  '-'):#an o geitonas einai variable
						neighbors_dict[(row,column)].append((i,column))
					elif(puzzle[i][column] !=  '*'): #an brethei deyteros kanonas athrismatos
						break;
			#print(puzzle[row][column])
	return neighbors_dict

class Kakuro(CSP):
	def __init__(self,puzzle):
		neighbors = get_neighbors(puzzle)
		domain = {}
		for key in neighbors.keys():
			domain[key] = [x for x in range(1,10)]
		variables = [x for x in neighbors.keys()]
		print("domain == ",domain)
		print("neighbors == ",neighbors)
		print("variables == ",variables )





print("ready to run")
puzzle = puzzle0
kakuro_prob = Kakuro(puzzle)

#gia binary constrain borw na exw to diaforo mono me kathe geitona 
#kai ola ta alla na ta periorizw se epipedo domain 
#to hconflicts mporei na tropopoihthei kai to contrain na einai apla to diaforetiko X != Y opws sto maping
#nconflicts san to has_conflict