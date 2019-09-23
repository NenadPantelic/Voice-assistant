import subprocess
from subprocess import run as run


# date example
# run('date')
# process = subprocess.Popen(['date'])
# p = subprocess.Popen("date", stdout=subprocess.PIPE, shell=True, encoding='utf-8')

# x = p.communicate(timeout=15)
# output,error
# print(subprocess.Popen(['echo',x[0]]))
# p = subprocess.Popen("google-chrome", stdout=subprocess.PIPE, shell=True, encoding='utf-8')

# x = p.communicate(timeout=15)

# print(p.communicate())
# print(process.check_output())
# process.wait()
# print(dir(process.stdout))
# run calculator
# run('date', stdout=PIPE)


class OSService:

    def __init__(self):
        pass

    def execute_command_2(self, command):
        p = subprocess.Popen(["ls", "-la"], stdout=subprocess.PIPE, shell=True, encoding='utf-8')
        x = p.communicate(timeout=15)
        return x

    def execute_command(self, command):
        command_result = run(args=command, stdout=subprocess.PIPE, shell=True, encoding='utf-8')
        # print(dir(command_result))
        # print(command_result.args)
        # print(command_result)
        # print(command_result.returncode)
        # print(command_result.stderr)
        # (command_result.stdout)
        # print(command_result.check_returncode())
        if (command_result.stdout is not None or command_result.returncode == 0 and command_result.stderr is None):
            return command_result.stdout
        else:
            pass
            # command cannot be executed

    def search_file(self, filename, starting_point="/home/"):
        sudo_mode = False
        if starting_point == "/":
            sudo_mode = True
        args = ["find", starting_point, "-name", filename]
        if sudo_mode: args.insert(0, "sudo")
        # print(' '.join(args))
        files = self.execute_command(' '.join(args))
        if files is not None:
            files = files.split('\n')
            if len(files) > 0:
                return files[0]
            else:
                pass
                # file cannot be found

    def open_file(self, file):
        assert (isinstance(file, str)), "File cannot be None value"
        # handle null file
        open_with_map = {
            "image": "eog",
            "audio": "amarok",
            "pdf": "xdg-open",
            "text": "kwrite",
            "tabular": "libreoffice",
            "code": "kwrite"
        }
        extension = self.check_file_type(file)
        open_with = open_with_map.get(extension, None)
        # amarok must be killed after play outs
        if open_with is not None:
            self.execute_command(command=open_with + " " + file)
        else:
            pass

    #def delete_file(self, ):
    def check_file_type(self, filename):
        extension_map = {"image": ('.png', '.jpg', '.jpeg', 'tiff', 'gif', 'bmp'),
                         "audio": (".mp3", "flacc", "wav"),
                         "text": ("txt",),
                         "pdf": ("pdf",),
                         "tabular": ("xls", "xlsx", "csv", "odt"),
                         "code": ("py", "java", "c", "cpp", "js", "cs", "html", "css", "php", "sql")}
        extension = [type_value for type_value, type_extension in extension_map.items() if filename.lower()
            .endswith(type_extension)]
        if len(extension) > 0:
            return extension[0]
        else:
            pass
            # raise unsupported file format

    def run_program(self, program):
        command = self.get_program_command(program.split(' '))
        print("DEBUG " + command)
        return self.execute_command(command)

    def get_program_command(self, program):
        #program = program
        programs = {
            "google-chrome": ("google", "chrome", "browser"),
            "libreoffice": ("office", "ppt", "power point", "presentation", "sheets", "writer"),
            "gnome-terminal": ("terminal", "konsole", "console"),
            "xdg-open /home/": ("file manager", "files")
        }
        for program_command, commands in programs.items():
            if any(program_word in commands for program_word in program):
                #execute = self.execute_command(program_command)
                # TODO:handle result from execution
                return program_command
            else:
                # raise invalid command
                pass
    def get_computer_status(self):
        command = "echo \"CPU `LC_ALL=C top -bn1 | grep \"Cpu(s)\" | sed \"s/.*, *\([0-9.]*\)%* us.*/\1/\" | awk '{print 100 - $1}'" \
                  "`% RAM `free -m | awk '/Mem:/ { printf(\"%3.1f%%\", $3/$2*100) }'` HDD `df -h / | awk '/\// {print $(NF-1)}'`\""
        cpu_usage = 'top -b -d1 -n1|grep -i \"Cpu(s)\"|head -c21|cut -d \' \' -f3|cut -d \'%\' -f1'
        ram_usage = 'free -m | awk \'/Mem:/ { printf(\"%3.1f%%\", $3/$2*100) }\''
        hdd_usage = 'df -h / | awk \'/\// {print $(NF-1)}\''
        print(cpu_usage, ram_usage, hdd_usage)
        return self.execute_command(hdd_usage)

    def get_pid(self, process_name):
        command = "ps -aux | grep " + process_name
        command = "ps axf | grep " + process_name + "| grep -v grep | awk \'{print \"kill -9 \" $1}\' | sh"
        return self.execute_command(command)

    #dangerous commands

    def reboot(self):
        command = "sudo reboot"
        #command = "sudo shutdown -r now"
        return self.execute_command(command)

    def poweroff(self):
        command = "sudo shutdown now"
        return self.execute_command(command)



"""
commands:
- open program Y
- ls N
- date N
- find file Y
- find and open Y
- restart Y
- poweroff Y
- check computer status Y
- ubij neki program Y
- obrisi neki fajl N
"""
