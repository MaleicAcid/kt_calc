import pandas as pd
from math import *

path = r'./初次计算.xlsx '

data=pd.read_excel(path)
df = pd.DataFrame(data)

def to_degree(num): # 3652.5255 ==> 36.8754
	degree = num//100
	fen = (num - degree*100)/60
	return degree+fen

def degree_change(course, x, y):
	course = course-90
	course = radians(-course)
	newx = x*cos(course) + y*sin(course)
	newy = -x*sin(course) + y*cos(course)
	return newx,newy, course
print("SAMPLE_TIMESTAMP   | HTD_COURSE | newx      | newy             | 原x | 原y")
for index, row in df.iterrows():
	row.RMC_LATITUDE = to_degree(row.RMC_LATITUDE)
	row.RMC_LONGITUDE = to_degree(row.RMC_LONGITUDE)
	if(row.HTD_COURSE == 0 or row.HTD_COURSE == 180):
		row.x = row.RMC_LATITUDE
		row.y = row.RMC_LONGITUDE
	else:
		row.x, row.y,_ = degree_change(row.HTD_COURSE, row.RMC_LATITUDE, row.RMC_LONGITUDE)
	print(row.SAMPLE_TIMESTAMP,row.HTD_COURSE, row.x, row.y, row.RMC_LATITUDE, row.RMC_LONGITUDE)