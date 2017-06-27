def difference(file1,file2):
    data1 = open(file1).read()
    data2 = open(file2).read()
    fileDifference= difflib.SequenceMatcher(None,data1,data2);
    fileRatio= fileDifference.ratio()
    diffPercentage = fileRatio*100
    return diffPercentage
print "input file1"
file1 = raw_input()
print "input file2"
file2 = raw_input()
difference(file1,file2)