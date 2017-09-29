import os
inp = "i"
lst = os.listdir(inp)
for fl in lst:
    os.system("/Users/margaritaberseneva/Desktop/2-course-2017-2018/classwork/2017-09-23/mystem -nd " + inp + os.sep + fl + " o" + os.sep + fl)
print("Done")
