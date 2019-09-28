from services.system.os_service import OSService

os_srv = OSService()
os_srv.execute_command("date")
print(os_srv.execute_command("sudo find / -name 'subprocess.py'"))
file = os_srv.search_file("cat.jpg")
print(file)
file = os_srv.search_file("temporary.mp3")
print(file)
print(os_srv.open_file(file))
print(os_srv.get_computer_status())
print(os_srv.kill_process("chrome"))

