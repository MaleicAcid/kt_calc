from datetime import datetime
import pymysql
import os
from six.moves import configparser

# 创建连接
db = {}
# db['host'] = '127.0.0.1'
# db['port'] = 3306
# db['user'] = 'root'
# db['passwd'] = 'root'
# db['db'] = '20-5-21'

def readConfig():
	config = configparser.ConfigParser()
	config.read("config.ini")
	db['host'] = config.get('db', 'host')
	db['port'] = int(config.get('db', 'port'))
	db['user'] = config.get('db', 'user')
	db['passwd'] = config.get('db', 'passwd')
	db['db'] = config.get('db', 'db')
	db['dir'] = config.get('dir', 'target_dir')
readConfig()
print("your db param: %s " % (db))
if not db['dir'].strip():
    target_dir = os.getcwd() + "\data"
else:
	target_dir = db['dir']
print("your target_dir: %s " % (target_dir))
conn = pymysql.connect(host=db['host'], port=db['port'], user=db['user'], passwd=db['passwd'], db=db['db'])

# 创建游标
cur=conn.cursor()#获取游标

substr = "$AGHTD"
attention = ["$AGHTD"]
table_dict = {}
table_dict["$AGHTD"] = "autopilothtd"
cancel_strict_sql = "set global sql_mode=''"
cur.execute(cancel_strict_sql)
# 2020-05-21 11-26-59$AGHTD,V,2.3,R,S,T,15.0,10.0,,10.00,125.0,,,T,A,A,,123.09*1F
count = 0

class IncorrectProtocolException(Exception):
    "this is user's Exception for check the Protocol format"
    def __init__(self, filename):
        self.filename = filename
    def __str__(self):
        return "filename:"+str(self.filename)+", 文件格式错误, 已跳过"

def insert_into(tablename, formatnum, arr):

	format_str = "%s,"*formatnum
	format_str = format_str[:-1]
	sql = "insert into " + tablename + " values(" + format_str+ ")"
	#print(sql)
	#print(line_arr)
	insert = cur.execute(sql, tuple(arr))
	return insert
def data_change(str):
	obj = datetime.strptime(str, '%Y-%m-%d %H-%M-%S')
	return obj.strftime('%Y-%m-%d %H:%M:%S')


def run(dir):
	fileList = os.listdir(dir)
	os.chdir(dir)
	allFilenum = len(fileList)
	#print(fileList)
	for index, filename in enumerate(fileList):
		try:
			print("%d/%d " %(index+1, allFilenum), end='')
			import_per_file(filename)
		except IncorrectProtocolException as e:
			print(e)

def import_per_file(filename):
	file = open(filename)
	print('filename:'+filename+' ', end='')
	file_count=0
	for line in file.readlines():

		if line[19] != "!" and line[19] != "$":
			file.close()
			raise IncorrectProtocolException(filename)
		if line[19] == "!":
			continue # !...* 的协议先跳过
		protocol = "$" + line.split("$")[1].split(',')[0]
		#print(protocol)

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
			file_count+=tmp
			global count
			count += tmp
	file.close()
	print(" insert: %d " % (file_count), end='')
	print(" total: %d " % (count))

run(target_dir)
print("insert nums:", count)
print(" 按任意键即可关闭...", end='')
input()
