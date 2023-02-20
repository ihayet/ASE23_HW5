import re
import os
from DATA import DATA

def clean(val):
    for (src, dest) in zip(["cols=", "rows=", "_", "'", "{", "}", ","], ["", "", "", "", "", "", ""]):
        val = val.replace(src, dest)
    return val

def arrayfy(val):
    records = []
    for record in val.split("\n"):
        recarray = [rec for rec in record.strip().split(" ") if len(rec) > 0]
        if len(recarray) > 0:
            records.append(recarray)
    return records

def tocsv(fname, attributes, examples):
    try:
        os.remove(fname + '_attributes.csv')
    except FileNotFoundError:
        pass

    try:
        os.remove(fname + '_examples.csv')
    except FileNotFoundError:
        pass

    with open(fname + '_attributes.csv', 'a') as attrfile, open(fname + '_examples.csv', 'a') as examplefile:
        # Writing to attributes file
        for i in range(len(examples)-1, -1, -1):
            attrfile.write(str(examples[i][0]))
            attrfile.write(',')
        attrfile.write('attributes!\n')
        
        for i in range(len(attributes)): 
            for k in range(1, len(attributes[i])-1):
                attrfile.write(str(attributes[i][k]) + ',')
            attrfile.write(attributes[i][0] + ':' + attributes[i][k+1])
            attrfile.write('\n') if i < len(attributes)-1 else ''

        #Writing to examples file
        for i in range(len(attributes)):
            examplefile.write(str(attributes[i][0]) + ':' + str(attributes[i][len(attributes[i])-1]))
            examplefile.write(',')
        examplefile.write('examples!\n')

        for i in range(len(examples)):
            for k in range(len(attributes)):
                examplefile.write(str(attributes[k][i+1]))
                examplefile.write(',')
            examplefile.write(str(examples[len(examples)-1-i][0]))
            examplefile.write('\n') if i < len(examples)-1 else ''

def repcols(fname):
    with open(fname) as repgridfile:
        replines = repgridfile.read()

        attributes = arrayfy(clean(re.search("(cols=[\s\S]*\}\s*\},)", replines).group(1)))
        examples = arrayfy(clean(re.search("(rows=[\s\S]*\}\s*\})", replines).group(1)))

        tocsv(fname, attributes, examples)

        return DATA(fname+'_attributes.csv')

def reprows(fname):
    with open(fname) as repgridfile:
        replines = repgridfile.read()

        attributes = arrayfy(clean(re.search("(cols=[\s\S]*\}\s*\},)", replines).group(1)))
        examples = arrayfy(clean(re.search("(rows=[\s\S]*\}\s*\})", replines).group(1)))

        tocsv(fname, attributes, examples)

        return DATA(fname+'_examples.csv')
    