import matplotlib.pyplot as plt
from subprocesses import *



if __name__ == "__main__":
	vertice_start = 5
	vertice_end = 800
	min_w = 1
	max_w = 300
	res = []
	while vertice_start <= vertice_end:
		mst_start = Popen([
		            'python3 prims.py -rf {} --min{} --max{}'],
		            shell=True, stdout=PIPE,
		            stderr=PIPE)
		     	mst_res, mst_error = mst_start.communicate()
		        res.append((vertice_start,float(mst_res.decode('utf-8'))))
