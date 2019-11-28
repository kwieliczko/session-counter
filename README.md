# session-counter
### "Session Counter" - a program that helps determine estimated base loads at different times of the day and thus find the best time for a service window.

As the parameter calling the program, we give the name of the database that interests us. The program connects to the set base and counts the connections for each hour of the last 7 days.

It also defines the maximum and minimum number of connections and for each number from a given hour colors the cell green. If the connections were few, the color was lighter. If much, darker accordingly.

In the current directory, he assumes an Excel file with the name consistent with the name of the database in which he places the calculated data.
