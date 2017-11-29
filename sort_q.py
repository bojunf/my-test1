import os
import sys
import numpy as np

wh_tag = ['who_whom', 'where', 'when', 'how_many', 'why', 'which', 'whose', 'how', 'what', 'binary']




def sort(qfilename, N):
	dic = {}
	out = []
	for wh in wh_tag:
		dic[wh] = []
	with open(qfilename, 'r') as f:
		for line in f.readlines():
			arr = line.replace('\n', '').split('\t')
			dic[arr[0]].append(arr[1])

	cnt = 0
	for wh in wh_tag:
		for quest in dic[wh]:
			tmp = quest + ' ?' + '\n'
			tmp = tmp.replace('-LRB-', '(').replace('-RRB-', ')').replace('-lrb-', '(').replace('-rrb-', ')')
			print(tmp)
			out.append(tmp)
			cnt += 1
			if (cnt == N):
				break
		if (cnt == N):
			break
	newfile = 'sort-' + qfilename
	open(newfile, 'w').writelines(out)

if __name__ == '__main__':
	fname = 'q-a7-head.txt'
	sort(fname, 10)