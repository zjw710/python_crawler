ps -aux|grep firefox| grep -v grep

pyinstaller -F MainLinux.py

nohup ./MainLinux &

ps -aux|grep MainLinux| grep -v grep