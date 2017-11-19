import pickle,sqlite3

a = "ERERERERERE"
b = pickle.dumps(a)
c = str(b)

try:
	db = sqlite3.connect("ex1")
	cur = db.cursor()
except Exception as e:
	print("SQL ERROR",e)

try:
	#cur.execute('insert into map values("{}");'.format(blob) )
	#db.commit()
	cur.execute('insert into map2 values({0},{1})'.format(1,b))
	db.commit()

	#insert into map values("b'\x80\x03X\x02\x00\x00\x00asq\x00.'")
except Exception as e:
	print (e)

try:
	b = cur.execute("select * from map2" )
	for row in b:
		print(row)
except Exception as e:
	print(e)
