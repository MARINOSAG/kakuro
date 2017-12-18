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
		neighbors = get_neighbors(puzzle)
		self.condict = neighbors[1]
		print(self.condict)

		neighbors = neighbors[0]
		domain = {}
		for key in neighbors.keys():
			domain[key] = [x for x in range(1,10)]
		variables = [x for x in neighbors.keys()]
		print("domain == ",domain)
		print("neighbors == ",neighbors)
		print("variables == ",variables )

		get_constrains(puzzle,self.condict)
		print("condict == ",self.condict)
		
		#Kakuro_constraint(self, A, 1, B, 2)
	#constrain gia dyo metablhtes
	#epistrefei true an oi metablhtes prokaloun conflict h oxi 
	# to  assignent einai dictionary me metablhth (x,y) kai value assignment == {(1, 3): 1, (2, 1): 1, (1, 4): 2, (2, 2): 2}
	
	#synarthsh pou epistrefei ton arithmo twn variables pou anhkoun sto constrain 
	#opou con einai (i,j) tuple pou deixnei thn thesh pou patera pou dhmiourgei ton periorismo grammhs
	def number_of_variables_of_row_con(self,con ):
		temp_list = [x for x in self.condict.keys() if(self.condict[x]["father_row_con"] == con) ]
		return len(temp_list)


	#function pou epistrefei true or false an oi metablhtes A,B einai mones toys sto sygkekrimmeno constrain
	def varibles_are_alone_in_constrain(self,A,B):
		temp_list = [x for x in self.condict.keys() if(x!= A and x!= B and self.condict[x]["father_row_con"] == self.condict[A]["father_row_con"]) ]
		return len(temp_list)==0
		

	def Kakuro_constraint(self, A, a, B, b):

		#an oi dyo metablhtes anhkoun sto idio constrain grammhs
		if(self.condict[A]["father_row_con"] == self.condict[A]["father_row_con"]):
			#se periptwsh poy ston periorismo ayto einai mones toys kai den yparxei allh metablhth 
			#lista apo (i,j) variables pou anhkoyn kai aytes ston periorismo thw A,B
			con = self.condict[A]["row_con"]
			if(self.varibles_are_alone_in_constrain(A,B)):
				print("oi metablhtes A , B einai mones tous ston periorismo grammhs\n")
				return (a+b) == con #prepei to athrisma toys na einai iso me ton periorismo
			else:
				#yparxoun perissoteres apo dyo metablhtes ston periorismo ayto
				#oi metablhtes den einai mones tous ston periorismo grammhs
				
				print("oi metablhtes A , B  DENNNN einai mones tous ston periorismo grammhs\n")
				#pairnw thn lista apo metablhtes pou exoun ginei assign kai anhkoun ston idio periorismo grammhs
				temp_list = [x for x in self.assignment.keys() if x!= A and x!= B and self.condict[x]["father_row_con"] ==con ]
				#an oles oi ypoloipes einai unassign 
				var_number = number_of_variables_of_row_con(con )

				if(len(temp_list) == 0):
					return (a+b) < con #prepei to athrisma toys na einai mikrotero apo ton periorismo
				#an yparxoyn metablhtes pou exoun ginei assign alla yparxoun kai kapoies alles pou exoun ginei unassign 
				#to meiwn 2 gia tis A, B
				#an exw kai assign kai unassign
				#elif(var_number-2 >temp_list )
				#	return
				else : 
					return (a+b) + values twn assigned  <= con 


A = (1, 3)
B =  (1, 4)

print("ready to run")
puzzle = puzzle0
kakuro_prob = Kakuro(puzzle)
apotelesma = kakuro_prob.Kakuro_constraint(A,2,B,1)
print(apotelesma)
#gia binary constrain borw na exw to diaforo mono me kathe geitona 
#kai ola ta alla na ta periorizw se epipedo domain 
#to hconflicts mporei na tropopoihthei kai to contrain na einai apla to diaforetiko X != Y opws sto maping
#nconflicts san to has_conflict