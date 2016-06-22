import os
import sys

def Main(envVarName, envVarValue):
    oldEnvVarValue= os.popen('echo %' + envVarName + '%').read().replace('\n', '');
    path = os.popen('echo %PATH%').read().replace('\n', '');
    
    #set home environment
    cmd = 'setx /m ' + envVarName + ' "' + envVarValue + '"';
    os.system(cmd);
    print(cmd);
    #add home/bin into path environment
    
    oldSubStr = oldEnvVarValue + '\\bin';
    newSubStr = envVarValue + '\\bin';
    if oldSubStr in path:
        cmd = 'setx /m PATH "' + path.replace(oldSubStr, newSubStr) + '"';
        os.system(cmd);
    else:
        cmd = 'setx /m PATH "' + newSubStr + ';' + path + '"';
        if envVarValue + '\\bin' not in path:
            os.system(cmd);
    print(cmd);
    
    
if __name__ == '__main__':
    assert len(sys.argv) == 3;
    Main(sys.argv[1], sys.argv[2]);