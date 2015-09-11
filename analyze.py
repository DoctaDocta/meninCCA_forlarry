import csv


import sqlite3 as lite
import sys
#setting up the outfile for out results!
con = lite.connect('sampleTissueTypeCounts.db'); #initilazing output file
cur = con.cursor() #save cursor to var
cur.execute("DROP TABLE IF EXISTS tissue") #if this table doesn't exist, create it.
cur.execute("CREATE TABLE tissue (sample text, ntcount real, tncount real)")#vals in each col of table


matchFile = "match.txt";
meninFile = 'menin_cca';
cabinet = [];
tmpList = [];

class Sample:
    def __init__(self, samplename, tissuetype, expressionvalue):
        self.name = samplename
        if (tissuetype == 'NT'):
            self.nt_count = expressionvalue
        else:
            self.tn_count = expressionvalue

    tn_count = -1
    nt_count = -1

print "Reading in matchFile."
print "Creating an object with the samplename, tissuetype, and expressionvalue, for each line."
with open (matchFile, 'rb') as f:
    reader = csv.reader(f, delimiter=" ")
    for line in reader:
        print "line:", line
        samplename = line[2][:12]
        tissuetype = line[3]
        expressionvalue = line[1]
        x = Sample(samplename,tissuetype,expressionvalue)
        cabinet.append(x)

listCheck = [];
print '\n',"-"*36
print 'Printing current cabinet'
print "-"*36
print "samplename\t\tnt_count\ttn_count."
print "-"*36

for x in cabinet:
    print x.name,'\t',x.nt_count,'\t',x.tn_count
print "-"*36


print "\nReading in meninFile"
with open (meninFile, 'rb') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        if (line[3] == 'TN'):
            print 'line:', line
            for x in cabinet:
                if (x.name == line[2][:12]):
                    print "\tFound matching tissue sample name!"
                    x.tn_count = line[1]
                    print "\tAdding expressionvalue to tn_count of sample.\n"


print '\n',"-"*63
print "Now executing the cabinet to table, 'tissue', in database file."
print "-"*63
for x in cabinet:
    #print x.name, x.nt_count, x.tn_count
    tmpList = [];
    tmpList.extend([x.name, x.nt_count, x.tn_count]);
    cur.execute('INSERT INTO tissue VALUES (?,?,?)', tmpList)

print '\n', "-"*36
print 'Printing current table from database'
print "-"*36
print "samplename\t\t  nt_count\ttn_count."
print "-"*36
cur.execute("SELECT * FROM tissue") #this is basic mysqlite and it's pretty simple!
# you can also select from genes to see the other table!
rows = cur.fetchall()
for row in rows:
    print row
print "-"*36

con.commit() #close the connection
con.close()