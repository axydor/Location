import sqlite,pickle,random

a = "Some String"
b = pickle.dumps(a)

i = random.randint(1,100000)

a = a + "{0}".format(i)
b = pickle.dumps(a)

try:
        db = sqlite3.connect("ex1")
        cur = db.cursor()

except Exception as e:
        print ("SQL error ",e)

try:
        cur.execute("CREATE TABLE map (id int,b BLOB ) ")
except:
        print("error ignored")

try:
        cur.execute('INSERT INTO map VALUES(?,?)', (i, b))
        db.commit()
except Exception as e:
        print(e)
        print("Haahaha")
try:
        cur.execute("select * from map")
        rows = cur.fetchall()
        for row in rows:
                print(row[1])
		print(pickle.loads(row[1]))
	print(type(row[1]))  # Check the type
except Exception as e:
        print(e)
