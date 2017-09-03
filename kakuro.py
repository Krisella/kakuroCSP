from csp import*
import sys
import timeit

grid=[]

def kakuro_constraints(A, a, B, b,assignment):

	sizex=len(grid)
	sizey=len(grid[0])
	unassigned_count=1
	flag=0
	sum_so_far=0
	if a!=b :
		if A[0] == B[0] :
			row_sum=0
			i=A[0]
			j=A[1]-1
			while grid[i][j]=='.' :
				if tuple((i,j)) in assignment:
					sum_so_far+=int(assignment[tuple((i,j))])
				else:
					unassigned_count+=1
					flag=1
				j-=1
			sums=grid[i][j].split('|')
			row_sum=int(sums[0])
			j=A[1]+1
			while j<sizey and grid[i][j]=='.' :
				if tuple((i,j)) in assignment:
					sum_so_far+=int(assignment[tuple((i,j))])
				else:
					unassigned_count+=1
					flag=1
				j+=1
			max=row_sum-sum_so_far-((unassigned_count*(unassigned_count-1))/2)
			min=row_sum-sum_so_far-((20-unassigned_count)*(unassigned_count-1)/2)
			if a <= max and a >= min :
				if flag == 0 and sum_so_far+a == row_sum:
					return True
				if sum_so_far+a < row_sum and flag == 1 :
					return True
		elif A[1] == B[1] :
			col_sum=0
			i=A[0]-1
			j=A[1]
			while grid[i][j]=='.' :
				if tuple((i,j)) in assignment:
					sum_so_far+=int(assignment[tuple((i,j))])
				else:
					unassigned_count+=1
					flag=1
				i-=1
			sums=grid[i][j].split('|')
			col_sum=int(sums[1])
			i=A[0]+1
			while i<sizex and grid[i][j]=='.' :
				if tuple((i,j)) in assignment:
					sum_so_far+=int(assignment[tuple((i,j))])
				else:
					unassigned_count+=1
					flag=1
				i+=1
			max=col_sum-sum_so_far-((unassigned_count*(unassigned_count-1))/2)
			min=col_sum-sum_so_far-((20-unassigned_count)*(unassigned_count-1)/2)
			if a <= max and a >= min :
				if sum_so_far+a == col_sum and flag==0:
					return True
				if sum_so_far+a < col_sum and flag==1:
					return True
	return False


class Kakuro(CSP):

	def __init__(self,starting_grid, sizex, sizey):

		vars=[]
		domains_list=range(1,10)
		self.domains=dict()
		self.neighbors=dict()
		starting_grid_sum=0

		global grid
		grid=[range(sizey) for x in range(sizex)]
		"""scanning grid"""
		for i in range(sizex) :
			for j in range(sizey) :
				grid[i][j] = starting_grid[starting_grid_sum]
				"""creating variables"""
				if grid[i][j] == '.' :
					vars.append(tuple((i,j)))
					self.neighbors[tuple((i,j))]=[]
					"""storing domains"""
					self.domains[tuple((i,j))]=domains_list
				starting_grid_sum+=1
		self.variables=vars

		"""creating neighbors"""
		for i in range(sizex) :
			for j in range(sizey) :

				if grid[i][j] == '.' :

					k=i-1
					while k>=0 and grid[k][j]=='.' :
						self.neighbors[tuple((i,j))].append(tuple((k,j)))
						k-=1

					k=i+1
					while k<sizex and grid[k][j]=='.' :
						self.neighbors[tuple((i,j))].append(tuple((k,j)))
						k+=1

					k=j-1
					while k>=0 and grid[i][k]=='.' :
						self.neighbors[tuple((i,j))].append(tuple((i,k)))
						k-=1

					k=j+1
					while k<sizey and grid[i][k]=='.' :
						self.neighbors[tuple((i,j))].append(tuple((i,k)))
						k+=1
		CSP.__init__(self,self.variables,self.domains,self.neighbors,kakuro_constraints)
	
	def nconflicts(self, var, val, assignment):
		"""Return the number of conflicts var=val has with other variables."""
		# Subclasses may implement this more efficiently
		def unassigned_check(var1):
			return var1 in assignment
		def conflict(var2):
			return (var2 in assignment
					and not self.constraints(var, val, var2, assignment[var2],assignment))
		def row_neighbor(var3):
			return ( var[0]==var3[0])
		def col_neighbor(var4):
			return var[1]==var4[1]
		empty=count_if(unassigned_check, self.neighbors[var])
		
		if empty == 0 :
			
			row_var=tuple((var[0],1))
			col_var=tuple((var[0]+1,var[1]))
			sums=0
			if not self.constraints(var,val,row_var,val+1,assignment):
				sums+=count_if(row_neighbor, self.neighbors[var])
			if not self.constraints(var,val,col_var,val+1,assignment):
				sums+=count_if(col_neighbor, self.neighbors[var])
			return sums

		else:
			return count_if(conflict, self.neighbors[var])

	def display(self,assignment) :

		sizex=len(grid)
		sizey=len(grid[0])
		for i in range(sizex) :
			for j in range(sizey) :
				if grid[i][j]=='.' :
					if tuple((i,j)) in assignment:
						print assignment[tuple((i,j))],
				else :
					print grid[i][j],
			print

	def forward_checking(csp, var, value, assignment, removals):
		"Prune neighbor values inconsistent with var=value."
		for B in csp.neighbors[var]:
			if B not in assignment:
				for b in csp.curr_domains[B][:]:
					 if not csp.constraints(var, value, B, b, assignment):
						 csp.prune(B, b, removals)
				if not csp.curr_domains[B]:
					 return False
		return True

"""SIZE 7*7"""
p1=['B','B','|4','|10','B','B','B','B','4|','.','.','B','|3','|4','B','3|','.','.','4|11','.','.','B','|3','10|4','.','.','.','.','11|','.','.','.','.','|4','B','4|','.','.','4|','.','.','B','B','B','B','3|','.','.','B']
"""SIZE 10*8"""
m=['B','B','|22','|17','B','B','|3','|16','B','9|11','.','.','|41','10|17','.','.','41|','.','.','.','.','.','.','.','4|','.','.','9|23','.','.','|38','B','22|','.','.','.','.','.','.','|13','41|','.','.','.','.','.','.','.','B','22|','.','.','.','.','.','.','B','|3','3|16','.','.','12|5','.','.','38|','.','.','.','.','.','.','.','8|','.','.','B','6|','.','.','B']
"""SIZE 8*6"""
small_hard=['B','|15','|29','|23','|42','|11','17|','.','.','.','.','.','35|','.','.','.','.','.','25|','.','.','.','.','.','4|','.','.','4|14','.','.','B','24|7','.','.','.','|8','31|','.','.','.','.','.','4|','.','.','5|','.','.']


"""INPUT PROBLEM NAME AND SIZE HERE"""
p=small_hard
sizex=8
sizey=6



k=Kakuro(p,sizex,sizey)

print "Running Kakuro with BT"
start = timeit.default_timer()
backtracking_search(k);
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

k=Kakuro(p,sizex,sizey)

print "Running Kakuro with FC"
start = timeit.default_timer()
backtracking_search(k, inference=Kakuro.forward_checking)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

k=Kakuro(p,sizex,sizey)

print "Running Kakuro with FC+MRV"
start = timeit.default_timer()
backtracking_search(k, select_unassigned_variable=mrv, inference=Kakuro.forward_checking)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print

k=Kakuro(p,sizex,sizey)

print "Running Kakuro with BT+MRV"
start = timeit.default_timer()
backtracking_search(k, select_unassigned_variable=mrv)
stop = timeit.default_timer()
print stop - start, "time elapsed"
print k.nassigns, "assigns made"
k.display(k.infer_assignment())
print