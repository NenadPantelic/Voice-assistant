
import subprocess
from subprocess import run as run

#date example
#run('date')
#process = subprocess.Popen(['date'])
p = subprocess.Popen("date", stdout=subprocess.PIPE, shell=True, encoding='utf-8')

x = p.communicate(timeout=15)
#output,error
print(subprocess.Popen(['echo',x[0]]))
p = subprocess.Popen("google-chrome", stdout=subprocess.PIPE, shell=True, encoding='utf-8')

x = p.communicate(timeout=15)

#print(p.communicate())
#print(process.check_output())
#process.wait()
#print(dir(process.stdout))
#run calculator
#run('date', stdout=PIPE)



class OSService:

    def __init__(self):
        pass

"""
commands:
- open program
- ls
- date
- find file
- find and open
- restart
- poweroff
- check computer status
- ubij neki program
- obrisi neki fajl
"""