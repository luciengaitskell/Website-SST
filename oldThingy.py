for ii in range(len(fileNames)): # for each file
  newDate=(fileNames[ii])[(len(fileSubFolder)+len(fileBeginning)):str(fileNames[ii]).find("-")] # Date of the file
  dateNew=True
  for jj in uniqueDates: # Finding if the date of the file is new
    if jj == newDate:
      dateNew=False

  if dateNew == True:
    uniqueDates.append(newDate) # adding file date if its good

uniqueDates.sort(reverse=True) # sorting the dates so the latest ones are first

for ii in range(len(uniqueDates)):
  fileNamesNew=[]

  for jj in fileNames:
    #testVar=testVar+1
    if uniqueDates[ii] == (jj)[(len(fileSubFolder)+len(fileBeginning)):str(jj).find("-")]:
      fileNamesNew.append((jj)[(len(fileSubFolder)+len(fileBeginning)):len(jj)-len(fileExtention)])

  fileNamesNew.sort(reverse=True)

  for jj in fileNamesNew:
    fileNamesSorted.append(str(fileBeginning) + str(jj) + str(fileExtention))
