from datetime import datetime
import pymysql

# 创建连接
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='20-5-21')

# 创建游标
cur=conn.cursor()#获取游标
file = open('2020-05-21 11.txt')
substr = "$AGHTD"
attention = ["$AGHTD"]
table_dict = {}
table_dict["$AGHTD"] = "autopilothtd"

# 2020-05-21 11-26-59$AGHTD,V,2.3,R,S,T,15.0,10.0,,10.00,125.0,,,T,A,A,,123.09*1F
count = 0
def insert_into(tablename, formatnum, arr):

	format_str = "%s,"*formatnum
	format_str = format_str[:-1]
	sql = "insert into " + tablename + " values(" + format_str+ ")"
	print(sql)
	print(line_arr)
	insert = cur.execute(sql, tuple(arr))
	return insert
def data_change(str):
	obj = datetime.strptime(str, '%Y-%m-%d %H-%M-%S')
	return obj.strftime('%Y-%m-%d %H:%M:%S')
for line in file.readlines():
	if line[19] == "!":
		continue # !...* 的协议先跳过
	protocol = "$" + line.split("$")[1].split(',')[0]
	print(protocol)

	if protocol in attention:
		line_arr = line.split(",")
		line_arr[0] = line_arr[0].split("$")[0]
		line_arr[0] = data_change(line_arr[0])
		line_arr[-1] = line_arr[-1][:-3]
		size = len(line_arr)
		tmp = 0
		try:
			tmp = insert_into(table_dict[protocol], len(line_arr), line_arr)
		except pymysql.err.IntegrityError as e:
			if(e.args[0] == 1062):
				tmp = 0
			else:
				raise(e)
		count += tmp

print("insert nums:", count)

