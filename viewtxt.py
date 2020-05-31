
#
from datetime import datetime
import pymysql
import os
import time
from six.moves import configparser
from sql_comm import table_dict, create_table_sql
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
cur = conn.cursor()#获取游标

attention = {
 	"$AGHTD": 0,
 	"$TIROT": 0,
 	"$IIHRM": 0,
 	"$WIMWV": 0,
 	"$GPRMC": 0
}

# attention = {
#  	"$GPRMC": 0
# }

#cancel_strict_sql = '''set global sql_mode='NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';'''
cancel_strict_sql1 = '''set @@global.sql_mode ='';'''
cancel_strict_sql2 = '''set @@sql_mode ='';'''

cur.execute(cancel_strict_sql1)
cur.execute(cancel_strict_sql2)
# 2020-05-21 11-26-59$AGHTD,V,2.3,R,S,T,15.0,10.0,,10.00,125.0,,,T,A,A,,123.09*1F
count = 0 # 成功插入的计数
line_err_num = 0 # 错误的行数计数
class IncorrectProtocolException(Exception):
    "this is user's Exception for check the Protocol format"
    def __init__(self, filename):
        self.filename = filename
    def __str__(self):
        return "filename:"+str(self.filename)+", 文件格式错误, 已跳过"

def insert_into(protocol, tablename, formatnum, arr):
	if (attention[protocol] == 0) :
		cur.execute(create_table_sql[protocol])
		attention[protocol] = 1

	format_str = "%s,"*formatnum
	format_str = format_str[:-1]
	sql = "insert into " + tablename + " values(" + format_str+ ")"
	# print(sql)
	# print(arr)

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
			line_arr[0] = data_change(line_arr[0]) # 日期转换
			line_arr[-1] = line_arr[-1].split("*")[0]
			size = len(line_arr)
			tmp = 0
			try:
				tmp = insert_into(protocol, table_dict[protocol], len(line_arr), line_arr)
			except pymysql.err.IntegrityError as e:
				if(e.args[0] == 1062): # 1062错误代表重复插入
					tmp = 0
				else:
					raise (e)
			except pymysql.err.InternalError as e:
				if(e.args[0] == 1136): # 1062错误代表参数数目不匹配
					print("遇到一行数据错误, 已经跳过", line_arr)
					global line_err_num
					line_err_num += 1
				else:
					raise (e)


			file_count+=tmp
			global count
			count += tmp
	file.close()
	print(" insert: %d " % (file_count), end='')
	print(" total: %d " % (count))

run(target_dir)
print("insert nums:", count)
print("line_err_num nums(跳过的失败行数):", line_err_num)

print(" 按任意键即可关闭...", end='')
input()
