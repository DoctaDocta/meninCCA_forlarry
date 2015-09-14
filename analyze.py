import csv
import sqlite3 as lite
import sys
#setting up the outfile for out results!
con = lite.connect('sampleTissueTypeCounts.db'); #initilazing output file
cur = con.cursor() #save cursor to var
cur.execute("DROP TABLE IF EXISTS tissue") #if this table doesn't exist, create it.
cur.execute("CREATE TABLE tissue (sample text, ntcount real, tncount real)")#vals in each col of table

meninFile = 'menin_cca';
cabinet = [];
tmpList = [];
listCheck = [];

class Sample:
    def __init__(self, samplename, tissuetype, expressionvalue):
        self.name = samplename[:12]
        self.add_tissue_expression(tissuetype, expressionvalue)

    def add_tissue_expression(self, tissuetype, expressionvalue):
        if (tissuetype == 'NT'):
            self.nt_count = expressionvalue
        else:
            self.tn_count = expressionvalue

    tn_count = -1
    nt_count = -1
fileFound = False;
#This script reads in all samples but if they don't have doubles
# by the end, i delete them. Then write to db.
print "\nReading in meninFile. Saving double to DB.",'\n',"-"*63
with open (meninFile, 'rb') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
            print 'line:', line
            #searching to see if this already exists.
            for x in cabinet:
                if (x.name == line[2][:12]):
                    print "\tFound matching tissue sample name!"
                    x.add_tissue_expression(line[3], line[1])
                    print "\tAdding expressionvalue to sample.\n"
                    fileFound = True;
            if (fileFound == False):
                print '\ttemporarily adding new sample to cabinet.\n'
                x = Sample(line[2],line[3],line[1])
                cabinet.append(x)

print '\n',"-"*63, '\n',"Now executing the cabinet to table, 'tissue', in database file."
print "Only executing Sampels with both tissue types.",'\n',"-"*63
for x in cabinet:
    if (x.tn_count == -1.0 or x.nt_count == -1.0):
        del x
    else:
        tmpList = [];
        tmpList.extend([x.name, x.nt_count, x.tn_count]);
        cur.execute('INSERT INTO tissue VALUES (?,?,?)', tmpList)

print '\n', "-"*36,'\n','Printing current table from database','\n',"-"*36
print "samplename\t\t  nt_count\ttn_count.",'\n',"-"*36
cur.execute("SELECT * FROM tissue") #this is basic mysqlite and it's pretty simple!
# you can also select from genes to see the other table!
rows = cur.fetchall()
for row in rows:
    print row
print "-"*36

con.commit() #close the connection
con.close()