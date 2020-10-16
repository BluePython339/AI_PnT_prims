from pulp import*

#function takes a n*n matrix of values supplied by pulp 
#prints a chessboard like structure that shows where the queens are placed
def chess_me_a_board(choices, n):
	for i in range(n):
		pstring = "|"
		for x in range(n):
			pstring += ("Q" if int(value(choices[i][x])) == 1 else " ") +"|"
		print(pstring)

#function that calculates the NQueens problem, takes in an int and returns the solution
def queens_me_a_place(n):
	ROWS = COLS = range(n)

	prob = LpProblem("8 Queens", LpMaximize)


	choices = LpVariable.dicts("Fill", (ROWS, COLS),0,1, LpInteger)

#constraints for columns and rows
	for r in ROWS:
	    prob += lpSum([choices[r][c] for c in COLS]) == 1, 'rows({})'.format(r)
	    prob += lpSum([choices[c][r] for c in COLS]) == 1, 'cols({})'.format(r)

#constraints for the diagonals
	for k in range(2-n, n-1):
		prob += lpSum([(choices[r][c] if r-c == k else None) for c in COLS]for r in ROWS) <= 1, 'dig1({})'.format(k)

	for k in range(1, 2*n):
		prob += lpSum([(choices[r][c] if r+c == k else None) for c in COLS] for r in ROWS) <= 1, 'dig2({})'.format(k)



	prob.writeLP("queens.lp")

	solved = prob.solve()
	if solved:
		chess_me_a_board(choices,n) #draw the chessboard

if __name__ == "__main__":
	n = input("how many squares ya want: ") 
	if not n.isdigit(): #check for ints
		print("we only take ints here")
		exit()
	else:
		if int(n) > 3 : #n = 1 is a trivial case so ignored
			queens_me_a_place(int(n))  #calculate a board setting
		else:
			print("thats a non starter")
			exit()