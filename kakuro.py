from csp import *
from utils import *
from search import *
import sys
from input_puzzles import *
import time
# puzzle0 = [
# [  '*'  ,  '*'  ,  '*'  ,(6,''),( 3,'')],
# [  '*'  ,( 4,''),( 3, 3),  '-'  ,  '-'  ],
# [('',10),  '-'  ,  '-'  ,  '-'  ,  '-'  ],
# [ ('', 3),  '-'  ,  '-'  ,  '*'  ,  '*'  ]]
 
def get_neighbors(puzzle):

	print("puzzle is ",len(puzzle), len(puzzle[0] ) )
	neighbors_dict = {}
	condict ={}
	for  row in range(len(puzzle))  :
		for column in range(len(puzzle[0])) :
			if(puzzle[row][column] == '-'):#an prokeitai gia metablhth
				condict[(row,column)] = {}
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
	return (neighbors_dict,condict)
#synarthsh pou epistrefei dictionary gia kathe metablhth tous periorismoys oyras kai sthlhs poy exoyn 
#dictionary ths morfhs (3, 2): {'father_row_con': (3, 0), 'father_col_con': (1, 2), 'col_con': 3, 'row_con': 3}
#opou father_col_con einai h thesh tou stoixeiou pou prokalei ton periorismo sthlhs 
#kai father_row_con einai h thesh tou stoixeiou pou prokalei ton periorismo grammhs
def get_constrains(puzzle,condict):


	for row in range(len(puzzle) ):
		for column in range(len(puzzle[0])):
			item =  puzzle[row][column]
			if( isinstance(item , tuple )):#an prokeitai gia tuple shmainei oti prokeite gia periorismo
				
				if(isinstance( item[0] ,int) ):#column constrain
					for i in range(row+1,len(puzzle)):
						if(puzzle[i][column] == '-'):
							condict[(i,column)]["col_con"] = item[0]
							#krataw kai apo poio shmeio toy pinaka proeilthe o periorismos
							print( (row,column) )

							condict[(i,column)]["father_col_con"] = (row,column)

						else :
							break;

				if(isinstance( item[1] ,int)  ) :

					for i in range(column+1,len(puzzle[0])):
						if(puzzle[row][i] == '-'):
							condict[(row,i)]["row_con"] = item[1]
							#krataw kai apo poio shmeio toy pinaka proeilthe o periorismos
							print( (row,column) )
							condict[(row,i)]["father_row_con"] = (row,column)

						else :
							break;



class Kakuro(CSP):
	def __init__(self,puzzle):
		self.puzzle= puzzle
		neighbors = get_neighbors(puzzle)
		self.condict = neighbors[1]
		#print(self.condict)
		#self.assignment = CSP.assignment
		neighbors = neighbors[0]
		domain = {}
		for key in neighbors.keys():
			domain[key] = [x for x in range(1,10)]
		variables = [x for x in neighbors.keys()]
		#print("domain == ",domain)
		#print("neighbors == ",neighbors)
		#print("variables == ",variables )

		get_constrains(puzzle,self.condict)
		#print("condict == ",self.condict)
		# CSP(list(neighbors.keys()), UniversalDict(colors), neighbors,
  #              different_values_constraint)

  		#arxikopoiw to problhma klasshs CSP
		CSP.__init__(self, list(neighbors.keys()), domain,neighbors,self.Kakuro_constraint)
		#Kakuro_constraint(self, A, 1, B, 2)
	#constrain gia dyo metablhtes
	#epistrefei true an oi metablhtes prokaloun conflict h oxi 
	# to  assignent einai dictionary me metablhth (x,y) kai value assignment == {(1, 3): 1, (2, 1): 1, (1, 4): 2, (2, 2): 2}
	
	#synarthsh pou epistrefei ton arithmo twn variables pou anhkoun sto constrain 
	#opou con einai (i,j) tuple pou deixnei thn thesh pou patera pou dhmiourgei ton periorismo grammhs
	def number_of_variables_of_row_con(self,constrain ):
		temp_list = [x for x in self.condict.keys() if(self.condict[x]["father_row_con"] == constrain) ]
		return len(temp_list)

	def number_of_variables_of_col_con(self,constrain ):
		temp_list = [x for x in self.condict.keys() if(self.condict[x]["father_col_con"] == constrain) ]
		return len(temp_list)

	#function pou epistrefei true or false an oi metablhtes A,B einai mones toys sto sygkekrimmeno constrain
	def variables_are_alone_in_constrain(self,A,B,string):
		temp_list = [x for x in self.condict.keys() if(x!= A and x!= B and self.condict[x][string] == self.condict[A][string]) ]
		return len(temp_list)==0

	#function that checks if there are no conflicts between variables
	
	def display(self ):
		x = len(self.puzzle)
		y = len(self.puzzle[0])
		printing_list = []
		
		print("displaying port x == ",x, "  y ==  ",y)
		for i in range(x):
			printing_list.append([])
			for j in range(y):
				if self.puzzle[i][j] == '-':
					if tuple((i,j)) in self.curr_domains.keys():
						sys.stdout.write("          " +str(self.curr_domains[(i,j)][0]))
						#sys.stdout.write(" ")
						printing_list[i].append(self.curr_domains[(i,j)][0])
						#print(self.curr_domains[(i,j)])
 						#print (assignment [tuple((i,j))]),
				else:
					sys.stdout.write("          " + str(self.puzzle[i][j]) )
					#sys.stdout.write(" ")
					printing_list[i].append(self.puzzle[i][j])



					#print (self.puzzle[i][j])
			sys.stdout.write("\n")

		# for item in printing_list:
		# 	print(item)
	def Kakuro_constraint(self, A, a, B, b):
		#print("\n\n")
		#print ("A == ",A , "  B == ",B)
		self.assignment = self.curr_domains
		#print("curr_domains == " , self.curr_domains)
		#an oi dyo metablhtes anhkoun sto idio constrain grammhs
		#print("self.condict[A][\"father_row_con\"]  == ",self.condict[A]["father_row_con"])
		#print("self.condict[B][\"father_row_con\"] == ",self.condict[B]["father_row_con"])

		if(self.condict[A]["father_row_con"] == self.condict[B]["father_row_con"]):
			#print("AAAAAAAA")
			if(a == b):#epistrefw False an anhkoun ston idio periorismo gia na einai diaforetikoi
				#print("oi mteblhtes den ginetai na paroun idia timh")
				return False
			#se periptwsh poy ston periorismo ayto einai mones toys kai den yparxei allh metablhth 
			#lista apo (i,j) variables pou anhkoyn kai aytes ston periorismo thw A,B
			con = self.condict[A]["row_con"]
			father_con = self.condict[A]["father_row_con"]
			if(self.variables_are_alone_in_constrain(A,B,"father_row_con")):
			#	print("oi metablhtes A , B einai mones tous ston periorismo grammhs")
				return (a+b) == con #prepei to athrisma toys na einai iso me ton periorismo
			else:
				#yparxoun perissoteres apo dyo metablhtes ston periorismo ayto
				#oi metablhtes den einai mones tous ston periorismo grammhs
				
			#	print("oi metablhtes A , B  DENNNN einai mones tous ston periorismo grammhs")
				#pairnw thn lista apo metablhtes pou exoun ginei assign kai anhkoun ston idio periorismo grammhs
				#h lista assignment einai ths morfhs curr_domains ==  {(3, 2): [2], (1, 3): [2], (2, 3): [4], (2, 1): [3], (2, 2): [1], (3, 1): [1], (2, 4): [2], (1, 4): [1]}
				#sthn periptwsh pou len(self.assignment[x] )==1 shmainei oti h metablhth exei ginei assign
			
				if(self.assignment != None):
					temp_list = [x for x in self.assignment.keys() if x!= A and x!= B and len(self.assignment[x] )==1 and self.condict[x]["father_row_con"] ==father_con  ]
				else :
					temp_list = []
				
				#an oles oi ypoloipes einai unassign 
				#synarthsh pou epistrefei ton arithmo twn variables pou anhkoun sto constrain 
				var_number = self.number_of_variables_of_row_con(father_con)
				#temp_list = [x for x in self.assignment.keys() if x!= A and x!= B and len(self.assignment[x] )==1 and self.condict[x]["father_row_con"] ==con  ]
			#	print("var_number == ",var_number)

				#print("assignement_list == ",assignement_list)
			#	print("temp_list == ",temp_list)

				assignment_list = []
				for x in temp_list:
					assignment_list.append(self.assignment[x][0])


				if(len(temp_list) == 0):#an oi ypoloipes metablhtes einai oles unassigned 
					return (a+b) < con #prepei to athrisma toys na einai mikrotero apo ton periorismo
			
				
				elif(var_number-2 == len(temp_list) ): #an oi ypoloipes metablhtes einai oles assigned
					return (a+b) + sum(assignment_list)  == con 
				else :#an exw kai assigned kai unassigned 
				#	print("assignment == ",self.assignment)
					#assignment_list = list(self.assignment.values())
			#		print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
				#	print("assignement_list == ",assignment_list)
					return (a+b) + sum(assignment_list)  < con 

		if(self.condict[A]["father_col_con"] == self.condict[B]["father_col_con"]):
			#print("BBBBBBBBBBB")
			if(a == b):#epistrefw False an anhkoun ston idio periorismo gia na einai diaforetikoi
				#print("oi mteblhtes den ginetai na paroun idia timh")
				return False
			#se periptwsh poy ston periorismo ayto einai mones toys kai den yparxei allh metablhth 
			#lista apo (i,j) variables pou anhkoyn kai aytes ston periorismo thw A,B
			con = self.condict[A]["col_con"]
			father_con = self.condict[A]["father_col_con"]

			if(self.variables_are_alone_in_constrain(A,B,"father_col_con")):
				#print("oi metablhtes A , B einai mones tous ston periorismo Sthlhs")
				return (a+b) == con #prepei to athrisma toys na einai iso me ton periorismo
			else:
				#yparxoun perissoteres apo dyo metablhtes ston periorismo ayto
				#oi metablhtes den einai mones tous ston periorismo grammhs
				
				#print("oi metablhtes A , B  DENNNN einai mones tous ston periorismo Sthlhs")
				#pairnw thn lista apo metablhtes pou exoun ginei assign kai anhkoun ston idio periorismo grammhs
				
				if(self.assignment != None):
					temp_list = [x for x in self.assignment.keys() if x!= A and x!= B and len(self.assignment[x] )==1 and self.condict[x]["father_col_con"] ==father_con  ]
				else :
					temp_list = []
				#an oles oi ypoloipes einai unassign 
				var_number = self.number_of_variables_of_col_con(father_con )
				#print("var_number == ",var_number)
				#print("temp_list == ",temp_list)
				assignment_list = []
				for x in temp_list:
					assignment_list.append(self.assignment[x][0])
				if(len(temp_list) == 0):#an oi ypoloipes metablhtes einai oles unassigned 
					return (a+b) < con #prepei to athrisma toys na einai mikrotero apo ton periorismo
			
				elif(var_number-2 == len(temp_list) ): #an oi ypoloipes metablhtes einai oles assigned
					return (a+b) + sum(assignment_list)  == con 
				else :#an exw kai assigned kai unassigned 
					#print("assignment == ",self.assignment)
					#assignment_list = list(self.assignment.values())
					return (a+b) + sum(assignment_list)  < con 


	# def nconflicts(self, var, val, assignment):
 #        """Return the number of conflicts var=val has with other variables."""
 #        # Subclasses may implement this more efficiently
 #        self.assignment = assignment
 #        def conflict(var2):
 #            return (var2 in assignment and
 #                    not self.constraints(var, val, var2, self.assignment[var2]))
 #        return count(conflict(v) for v in self.neighbors[var])

# A = (2, 1)
# B =  (3, 1)

# print("ready to run")
# puzzle = puzzle0
# kakuro_prob = Kakuro(puzzle)
# apotelesma = kakuro_prob.Kakuro_constraint(A,2,B,2)
# print(apotelesma)

#gia binary constrain borw na exw to diaforo mono me kathe geitona 
#kai ola ta alla na ta periorizw se epipedo domain 
#to hconflicts mporei na tropopoihthei kai to contrain na einai apla to diaforetiko X != Y opws sto maping
#nconflicts san to has_conflict

while (1):    
	user_selection = input( "Please choose a puzzle(0 for puzzle0, 1 for puzzle1, 2 for puzzle2, 3 for puzzle3 or 4 for puzzle4 ): " )
	sel = 5 
	if ( user_selection == "0" ):
		sel = puzzle0
	elif (user_selection == "1" ):
		sel = puzzle1
	elif ( user_selection == "2" ):
		sel = puzzle2
	elif ( user_selection == "3" ):
		sel = puzzle3
	elif ( user_selection == "4" ):
		sel = puzzle4
	elif ( user_selection == "exit" ):
		break
	else:
		print( "Invalid Command" )
		continue

	


	kakuro = Kakuro(sel)    
	print ("Forward Checking")
	start_time = time.clock()
	result = backtracking_search( kakuro, inference=forward_checking )
	print ("Running time: ", time.clock() - start_time) 
	kakuro.display()

	kakuro = Kakuro(sel)        
	print( "\nForward Checking - MRV")
	start_time = time.clock()
	result = backtracking_search( kakuro, inference=forward_checking, select_unassigned_variable=mrv)
	print ("Running time: ", time.clock() - start_time) 
	kakuro.display()
	    
	kakuro = Kakuro(sel)    
	print( "\nBackTracking")
	start_time = time.clock()
	result = backtracking_search( kakuro )
	print ("Running time: ", time.clock() - start_time )
	kakuro.display()
    
	kakuro = Kakuro(sel)    
	print( "\nBackTracking - MRV")
	start_time = time.clock()
	result = backtracking_search( kakuro, select_unassigned_variable=mrv)
	print ("Running time: ", time.clock() - start_time) 
	kakuro.display()
	print ("\n") 