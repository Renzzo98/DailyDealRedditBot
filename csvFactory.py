#!/usr/bin/python3
import csv
import pandas

file_name = "deals_database.csv"


def initCSVfile():
  global file_name
  with open(file_name, mode ='w') as database_file:
      fieldnames = ['Title', 'Category','Price','Posted']
      database_writer = csv.DictWriter(database_file, fieldnames=fieldnames)
      
      database_writer.writeheader()
      database_writer.writerow({'Title': 'Razor BlackWidoow', 'Category':'KEYBOARD','Price':'$120','Posted':False})
      

def parseCSVfile():
  global file_name
  df = pandas.read_csv(file_name)
  print(df)
  
def appendToDatabase(rowData):
  if (rowData != None):
    global file_name
    row = [rowData.title, rowData.category, rowData.price, True]
    with open(file_name, 'a') as fd:
      writer = csv.writer(fd)
      writer.writerow(row)
    
    
def checkPrevPosted(title):
  if (title != None):
    global file_name
    postedBefore = False
    f = open (file_name)
    csv_f = csv.reader(f)
    for row in csv_f:
      if (row[0] == title) and (row[3] == 'True'):
        postedBefore = True
    if (postedBefore):
      return False
    else:
      return True
  else:
    raise ValueError("Title was Null when checking for previous posts")
  
