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
#epishs epistrefei gia kathe constrain lista metablhtwn pou yparxoun 
def get_constrains(puzzle,condict):
	constrain_variables ={} #dicionary pou periexei gia kathe periorismo tis metablhtes pou emplekontai se ayton 


	for row in range(len(puzzle) ):
		for column in range(len(puzzle[0])):
			item =  puzzle[row][column]
			if( isinstance(item , tuple )):#an prokeitai gia tuple shmainei oti prokeite gia periorismo
				constrain_variables[(row,column)] ={'col_con_list_vars':[],'row_con_list_vars':[],'col_con':'' ,'row_con':''}

				if(isinstance( item[0] ,int) ):#column constrain
					constrain_variables[(row,column)]['col_con'] = item[0] 
					for i in range(row+1,len(puzzle)):
						if(puzzle[i][column] == '-'):
							constrain_variables[(row,column)]['col_con_list_vars'].append((i,column))
							condict[(i,column)]["col_con"] = item[0]
							#krataw kai apo poio shmeio toy pinaka proeilthe o periorismos
							#print( (row,column) )

							condict[(i,column)]["father_col_con"] = (row,column)

						else :
							break;

				if(isinstance( item[1] ,int)  ) :
					constrain_variables[(row,column)]['row_con'] = item[1] 

					for i in range(column+1,len(puzzle[0])):
						if(puzzle[row][i] == '-'):
							constrain_variables[(row,column)]['row_con_list_vars'].append((row,i))

							condict[(row,i)]["row_con"] = item[1]
							#krataw kai apo poio shmeio toy pinaka proeilthe o periorismos
							#print( (row,column) )
							condict[(row,i)]["father_row_con"] = (row,column)

						else :
							break;

	return constrain_variables

class Kakuro(CSP):
	def __init__(self,puzzle):

		self.puzzle= puzzle
		neighbors = get_neighbors(puzzle)
		self.condict = neighbors[1]

		#self.assignment = CSP.assignment
		neighbors = neighbors[0]
		#print("neighbors == ",neighbors)

		domain = {}
		for key in neighbors.keys():
			domain[key] = [x for x in range(1,10)]
		variables = [x for x in neighbors.keys()]
		#print("domain == ",domain)
		#print("neighbors == ",neighbors)
		#print("variables == ",variables )

		self.constrain_variables = get_constrains(puzzle,self.condict)
		#print("condict == ",self.condict)
		#print("constrain_variables ==  ",self.constrain_variables)
		# CSP(list(neighbors.keys()), UniversalDict(colors), neighbors,
  #              different_values_constraint)

  		#arxikopoiw to problhma klasshs CSP
		CSP.__init__(self, list(neighbors.keys()), domain,neighbors,self.Kakuro_constraint)
		#Kakuro_constraint(self, A, 1, B, 2)
	#constrain gia dyo metablhtes
	#epistrefei true an oi metablhtes prokaloun conflict h oxi 
	# to  assignent einai dictionary me metablhth (x,y) kai value assignment == {(1, 3): 1, (2, 1): 1, (1, 4): 2, (2, 2): 2}
	
	# def check_if_ok():
	# 	self.assignment = self.infer_assignment()
	# 	for con in self.constrain_variables.keys():
	# 		for()






 	#constrain_variables = {(0, 1): [(1, 1), (2, 1), (3, 1)], (6, 4): [(6, 5), (6, 6)]}

	#function that checks if there are no conflicts between variables
	def check_if_everything_ok(self):
		assigned_vars  = self.infer_assignment()

		for constrain in self.constrain_variables.keys(): #gia kathe constrain 
			athrisma_grammhs = 0 
			#gia to row
			athrisma_sthlhs =0
			for var1 in self.constrain_variables[constrain]['row_con_list_vars']: #gia kathe metablhth tou constrain 
				if(var1 in assigned_vars.keys()):
					athrisma_grammhs += assigned_vars[var1]
			for var2 in  self.constrain_variables[constrain]['col_con_list_vars']:
				if(var2 in assigned_vars.keys()):
					athrisma_sthlhs += assigned_vars[var2]

			

			if(athrisma_grammhs != self.constrain_variables[constrain]['row_con']  and self.constrain_variables[constrain]['row_con'] !=''):
				print("GAMIETAI GIA ROW_CON == ",constrain,"  me athrisma grammhs = ",athrisma_grammhs , "  enw prepei na einai ",self.constrain_variables[constrain]['row_con'])
				return False
			if(athrisma_sthlhs != self.constrain_variables[constrain]['col_con'] and self.constrain_variables[constrain]['col_con']!=''):
				print("GAMIETAI GIA COL_CON == ",constrain)
				return False
		return True
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
						printing_list[i].append(self.curr_domains[(i,j)][0])
						
				else:
					sys.stdout.write("          " + str(self.puzzle[i][j]) )
					printing_list[i].append(self.puzzle[i][j])

			sys.stdout.write("\n")

		
	def Kakuro_constraint(self, A, a, B, b):
		
		if(a == b):#epistrefw False an anhkoun ston idio periorismo gia na einai diaforetikoi
			return False
		self.assignment = self.infer_assignment()
		if(A[0] == B[0]):#anhkoun ston idio periorismo grammhs
			
			#se periptwsh poy ston periorismo ayto einai mones toys kai den yparxei allh metablhth 
			#lista apo (i,j) variables pou anhkoyn kai aytes ston periorismo thw A,B
			con = self.condict[A]["row_con"]
			father_con = self.condict[A]["father_row_con"]
			list_of_variables_of_same_con = self.constrain_variables[father_con]['row_con_list_vars']
			var_number = len(list_of_variables_of_same_con)
			if(var_number == 2  ):#an ston periorismo ayto anhkoun mono 2 metablhtes dhladh mono h A, B
				return (a+b) == con
			
			else:
				
				#oi metablhtes den einai mones tous ston periorismo grammhs

				#pairnw thn lista apo metablhtes pou exoun ginei assign kai anhkoun ston idio periorismo grammhs
				#h lista assignment einai ths morfhs curr_domains ==  {(3, 2): [2], (1, 3): [2], (2, 3): [4], (2, 1): [3], (2, 2): [1], (3, 1): [1], (2, 4): [2], (1, 4): [1]}
				#sthn periptwsh pou len(self.assignment[x] )==1 shmainei oti h metablhth exei ginei assign
				temp_list = [x for x in list_of_variables_of_same_con if  x!= A and x!= B and x in self.assignment.keys()]

				assignment_list =[x for x in list_of_variables_of_same_con if  x!= A and x!= B and x in self.assignment.keys()]
				#den yparxei kamia assign
				if(len(temp_list) == 0):#an oi ypoloipes metablhtes einai oles unassigned 
					return (a+b) < con #prepei to athrisma toys na einai mikrotero apo ton periorismo
			
				assignment_list = []
				for x in temp_list:
					assignment_list.append(self.assignment[x])
				if(var_number-2 == len(temp_list) ): #an oi ypoloipes metablhtes einai oles assigned
					return (a+b) + sum(assignment_list)  == con 
				else :#an exw kai assigned kai unassigned 
					return (a+b) + sum(assignment_list)  < con 
		
		if(A[1] == B[1]):#anhkoun ston idio periorismo sthlhs
		
			#se periptwsh poy ston periorismo ayto einai mones toys kai den yparxei allh metablhth 
			#lista apo (i,j) variables pou anhkoyn kai aytes ston periorismo thw A,B
			con = self.condict[A]["col_con"]
			father_con = self.condict[A]["father_col_con"]
			list_of_variables_of_same_con = self.constrain_variables[father_con]['col_con_list_vars']

			var_number = len(list_of_variables_of_same_con)

			if(var_number == 2  ):#an ston periorismo ayto anhkoun mono 2 metablhtes dhladh mono h A, B
				return (a+b) ==con

			
			else:
				#yparxoun perissoteres apo dyo metablhtes ston periorismo ayto
				#oi metablhtes den einai mones tous ston periorismo grammhs
				
				#print("oi metablhtes A , B  DENNNN einai mones tous ston periorismo Sthlhs")
				#pairnw thn lista apo metablhtes pou exoun ginei assign kai anhkoun ston idio periorismo grammhs
				
				
				temp_list = [x for x in list_of_variables_of_same_con if  x!= A and x!= B and x in self.assignment.keys()]
				if(len(temp_list) == 0):#an oi ypoloipes metablhtes einai oles unassigned 
					return (a+b) < con #prepei to athrisma toys na einai mikrotero apo ton periorismo
				
				assignment_list = []
				for x in temp_list:
					assignment_list.append(self.assignment[x])

				if(var_number-2 == len(temp_list) ): #an oi ypoloipes metablhtes einai oles assigned
					return (a+b) + sum(assignment_list)  == con 
				else :#an exw kai assigned kai unassigned 
					return (a+b) + sum(assignment_list)  < con 


while (1):    
	user_selection = input( "Please choose a puzzle(0 for puzzle0, 1 for puzzle1, 2 for puzzle2, 3 for puzzle3 or 4 for puzzle4 ): " )
	sel = 5 
	if ( user_selection == "0" ):
		sel = puzzle0
	elif (user_selection == "1" ):
		sel = puzzle1
	elif (user_selection == "66" ):
		sel = puzzle66
	elif (user_selection == "55" ):
		sel = puzzle55
	elif (user_selection == "11" ):
		sel = puzzle11
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

	
	print("\n MAC\n\n")
	kakuro = Kakuro(sel)        

	start_time = time.clock()
	#AC3(kakuro)
	result = backtracking_search( kakuro, inference=mac, select_unassigned_variable=mrv)

	print("number of assins == ", kakuro.nassigns)

	print ("Running time: ", time.clock() - start_time) 

	kakuro.display()
	if(kakuro.check_if_everything_ok()):
		print("THE BOARD IS OK WITH THE CONSTRAINS\n\n\n\n\n")
	else:
		print("THE BOARD DOES IS NOTTT OK WITH THE CONSTRAINS\n\n\n\n")
		exit()


	kakuro = Kakuro(sel)    
	print ("Forward Checking")
	start_time = time.clock()
	result = backtracking_search( kakuro, inference=forward_checking )
	print("number of assins == ", kakuro.nassigns)

	print ("Running time: ", time.clock() - start_time) 
	kakuro.display()
	if(kakuro.check_if_everything_ok()):
		print("THE BOARD IS OK WITH THE CONSTRAINS\n\n\n\n\n")
	else:
		print("THE BOARD DOES IS NOTTT OK WITH THE CONSTRAINS\n\n\n\n")
		exit()

	kakuro = Kakuro(sel)        
	print( "\nForward Checking - MRV")
	start_time = time.clock()
	result = backtracking_search( kakuro, inference=forward_checking, select_unassigned_variable=mrv)
	print("number of assins == ", kakuro.nassigns)

	print ("Running time: ", time.clock() - start_time) 
	kakuro.display()
	if(kakuro.check_if_everything_ok()):
		print("THE BOARD IS OK WITH THE CONSTRAINS\n\n\n\n\n")
	else:
		print("THE BOARD DOES IS NOTTT OK WITH THE CONSTRAINS\n\n\n\n")
		exit()


	
	


	kakuro = Kakuro(sel)    
	print( "\nBackTracking - MRV")
	start_time = time.clock()
	result = backtracking_search( kakuro , select_unassigned_variable=mrv)
	print("number of assins == ", kakuro.nassigns)
	print ("Running time: ", time.clock() - start_time) 
	kakuro.display()
	print ("\n") 
	print(kakuro.infer_assignment())

	if(kakuro.check_if_everything_ok()):
		print("THE BOARD IS OK WITH THE CONSTRAINS\n\n\n\n\n")
	else:
		print("THE BOARD DOES IS NOTTT OK WITH THE CONSTRAINS\n\n\n\n")
		exit()
