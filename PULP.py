from pulp import*

def chess_me_a_board(choices, n):
	#print((n-int((n/4)))*"___")
	for i in range(n):
		pstring = "|"
		for x in range(n):
			pstring += ("Q" if int(value(choices[i][x])) == 1 else " ") +"|"
		print(pstring)
		#print((n-int((n/4)))*"___")

def queens_me_a_place(n):
	ROWS = COLS = range(n)

	prob = LpProblem("8 Queens", LpMaximize)


	choices = LpVariable.dicts("Fill", (ROWS, COLS),0,1, LpInteger)
	prob += 0 ,"tests"
	print(choices)

	for r in ROWS:
	    prob += lpSum([choices[r][c] for c in COLS]) == 1, 'rows({})'.format(r)
	    prob += lpSum([choices[c][r] for c in COLS]) == 1, 'cols({})'.format(r)


	for k in range(2-n, n-1):
		prob += lpSum([(choices[r][c] if r-c == k else None) for c in COLS]for r in ROWS) <= 1, 'dig1({})'.format(k)

	for k in range(1, 2*n):
		prob += lpSum([(choices[r][c] if r+c == k else None) for c in COLS] for r in ROWS) <= 1, 'dig2({})'.format(k)



	prob.writeLP("queens.lp")

	solved = prob.solve()
	if solved:
		chess_me_a_board(choices,n)

if __name__ == "__main__":
	n = input("how many squares ya want: ") 
	if not n.isdigit():
		print("we only take ints here")
		exit()
	else:
		if int(n) > 3 :
			queens_me_a_place(int(n))
		else:
			print("thats a non starter")
			exit()