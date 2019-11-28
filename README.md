# session-counter
### "Session Counter" - a program that helps determine estimated base loads at different times of the day and thus find the best time for a service window.

First, set up a set of tables using the queries available in the .sql file

The source of the program's information is a table with a list of hosts and access parameters to all our databases.


 ```
 ID HOST_NAME                DB_PO DB_SERVICE_NAME   DB_USER     DB_PASSWORD 
 -- ----------------------   ----- ----------------  ---------   -------------
 01 dbhost001.domain.com     1523  hr                dbsnmp      password     
 02 dbhost002.domain.com     1521  crm               dbsnmp      password     
 03 dbhost003.domain.com     1521  sales             dbsnmp      password     
 04 dbhost004.domain.com     1521  db_sap            dbsnmp      password  
 ```
 
As the parameter calling the program, we give the name of the database that interests us. The program connects to the set base and counts the connections for each hour of the last 7 days.

It also defines the maximum and minimum number of connections and for each number from a given hour colors the cell green. If the connections were few, the color was lighter. If much, darker accordingly.

In the current directory, he assumes an Excel file with the name consistent with the name of the database in which he places the calculated data.
