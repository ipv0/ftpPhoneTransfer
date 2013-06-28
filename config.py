# ping only once to save time
COMMAND = "ping -n 1 "

# IP pool to ping
IPS = [
  "192.168.2.3",
  "192.168.2.4",
  "192.168.2.5",
  "192.168.2.6"
]

# ftp port to connect, 21 is correct for most
PORT = 21

# credentials
LOGIN = "MYLOGIN"
PWD = "MYPASSWD"

COMPUTER_DIRS = {
  'photos': 'c:\\',
	'videos': 'c:\\',
	'music': 'c:\\',
	'fullbackup': 'c:\\'
}

PHONE_PATHS = {
	'photos': 'DCIM/CAMERA',
	'videos': 'DCIM/CAMERA/VIDEO',
	'music': 'Music',
	'fullbackup': '/'
}
