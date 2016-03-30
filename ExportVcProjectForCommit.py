
import os
import shutil

projectName = "Gs9330"
projectDir  = "D:\Project.Vc\Gs9330"
oldSlnNmae = "Gs9330.sln"
newSlnNmae = "Gs9330NoUnit.sln"

tempDir = "D:/Temp/" + projectName
if os.path.exists(tempDir):
    shutil.rmtree(tempDir)

os.system("svn export " + projectDir + " " + tempDir)
os.chdir("D:/Temp/" + projectName)

if os.path.exists("VcUnitTestProject"):
    shutil.rmtree("VcUnitTestProject")
if os.path.exists("UnitTestCodes"):
    shutil.rmtree("UnitTestCodes")
os.remove("ReadMe.txt")
os.remove(oldSlnNmae)
os.rename(newSlnNmae, oldSlnNmae)







