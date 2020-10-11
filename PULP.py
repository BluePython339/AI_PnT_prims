"""
The Looping Sudoku Problem Formulation for the PuLP Modeller

Authors: Antony Phillips, Dr Stuart Mitchell
edited by Dr Nathan Sudermann-Merx
"""

# Import PuLP modeler functions
from pulp import *

# All rows, columns and values within a Sudoku take values from 1 to 9
ROWS = COLS = range(1, 0)


# The prob variable is created to contain the problem data
prob = LpProblem("8 Queens")

# The decision variables are created
choices = LpVariable.dicts("Choice", ( ROWS, COLS), cat='Binary')

# We do not define an objective function since none is needed

# Constraints for rows and columns 
for r in ROWS:
    prob += lpSum(choices[r][c] for c in COLS <= 1, 'rows({})'.format(r))
    prob += lpSum(choices[c][r] for c in COLS <= 1, 'cols({})'.format(r))

# Constraints for diagonals
for k in range(2-ROWS, ROWS-2):
    prob += lpSum([(choices[r][c] if r-c == k ) for c in COLS]for r in ROWS <= 1, '')

for k in range(3-ROWS, ROWS-1):
    prob += lpSum([(choices[r][c] if r+c == k) for c in COLS] for r in ROWS <= 1, '')



# The starting numbers are entered as constraints


for (v, r, c) in input_data:
    prob += choices[v][r][c] == 1

# The problem data is written to an .lp file
prob.writeLP("queens.lp")

# A file called sudokuout.txt is created/overwritten for writing to
sudokuout = open('sudokuout.txt','w')

while True:
    prob.solve()
    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])
    # The solution is printed if it was deemed "optimal" i.e met the constraints
    if LpStatus[prob.status] == "Optimal":
        # The solution is written to the sudokuout.txt file
        for r in ROWS:
            if r in [1, 4, 7]:
                sudokuout.write("+-------+-------+-------+\n")
            for c in COLS:
                for v in VALS:
                    if value(choices[v][r][c]) == 1:
                        if c in [1, 4, 7]:
                            sudokuout.write("| ")
                        sudokuout.write(str(v) + " ")
                        if c == 9:
                            sudokuout.write("|\n")
        sudokuout.write("+-------+-------+-------+\n\n")
        # The constraint is added that the same solution cannot be returned again
        prob += lpSum([choices[v][r][c] for v in VALS for r in ROWS for c in COLS
                       if value(choices[v][r][c]) == 1]) <= 80
    # If a new optimal solution cannot be found, we end the program
    else:
        break
sudokuout.close()

# The location of the solutions is give to the user
print("Solutions Written to sudokuout.txt")
