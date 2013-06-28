import os, sys, re, socket, ftplib
import config
from ftplib import FTP


# Remore directory on the ftp server
rem_dir = ""

# Path where to put the files (has to exist)
dest_path = ""

namelist = []

def ask_rem_dir():
  """ ask the user what needs to be transfered and set rem_dir and dest_path accordingly """
  global rem_dir
  global dest_path
  srcdir = ""

  if len(sys.argv) != 2:
    srcdir = raw_input("What needs to be transfered? Enter the letter.\n(P)hotos, (V)ideos, (M)usic, (F)ull Backup:  ")

  if srcdir == "P" or sys.argv[1] == "-P":
    rem_dir = config.PHONE_PATHS['photos']
    dest_path = config.COMPUTER_DIRS['photos']
    print "*** Will be transfering from %s to %s" % (rem_dir, dest_path)

  elif srcdir == "V"  or sys.argv[1] == "-V":
    rem_dir=config.PHONE_PATHS['videos']
    dest_path = config.COMPUTER_DIRS['videos']
    print "*** Will be transfering from %s to %s" % (rem_dir, dest_path)

  elif srcdir == "M"  or sys.argv[1] == "-M":
    rem_dir=config.PHONE_PATHS['music']
    dest_path = config.COMPUTER_DIRS['music']
    print "*** Will be transfering from %s to %s" % (rem_dir, dest_path)

  elif srcdir == "F"  or sys.argv[1] == "-W":
    rem_dir=config.PHONE_PATHS['fullbackup']
    dest_path = config.COMPUTER_DIRS['fullbackup']
    print "*** Will be transfering from %s to %s" % (rem_dir, dest_path)

  else:
    print "You need to make a choice."
    ask_rem_dir()


# --------------------------------- checks for responsive hosts ------------------------------- #
def check_responce(ip_list, command):
  """ uses the standard os ping command to check for responsive hosts, returns the list of such hosts """
  config.IPS_resp_ok = []
  ping_resp_text = []
  res_list = []

  for addr in ip_list:
    print "Trying " + addr + "..."
    ping_process = os.popen(command + addr)
    s = ping_process.read()
    if s.count("unreachable", 0, len(s)) == 0: # host IS reachable
      config.IPS_resp_ok.append(addr)
      ping_resp_text.append(s)
  res_list.append(config.IPS_resp_ok)
  res_list.append(ping_resp_text)
  return res_list


# ---------------------------- guessing which device is the phone ---------------------------#
def guess_phone(ips_resp_ok):
  """ go throught the ones that responded and try to resolve host names """
  didnt_resolve = []
  for c in ips_resp_ok:
    try:
      (name, bla, addr) = socket.gethostbyaddr(c)
      print addr[0] + " resolved into: " + name
    except:
      print c + " didn't resolve..."
      didnt_resolve.append(c)

  if len(didnt_resolve) == 1:
    return didnt_resolve[0]
  else:
    print "More then one device failed to resolve!"
    manual_ip = raw_input("Manually enter the IP to connect to: ")
    return manual_ip

# ---------------------------------- retrieves the files ---------------------------------------#
def download(handle, filename):
  """ downloads the given file via ftp, using the ftp object supplied as a parameter """
  filename_dest = dest_path + filename
  if os.path.exists(filename_dest) == False:
    f2 = open(filename_dest, "wb")
    try:
      handle.retrbinary("RETR " + filename, f2.write)
    except Exception:
      print "Error in downloading the remote file."
      return
    f2.close()
    return
  else:
    print "Skipping " + filename + " - already exists."

# -------------------------- callback function for the ftp client ------------------------------#
def process_line(string):
  """ this function is executed on every line of the ftp server output of LIST, extracts filenames from the output """
  matches = re.findall("^.*\s\d\d\:\d\d\s(.*)$", string)
  if len(matches) == 1:
    match = matches[0]
    global namelist
    namelist.append(match)

# ----------------------- perform ftp transfer with the given address -----------------------#
def do_ftp_transfer(ip):
  """ creates the connection, gets directory listing locally and remotely, makes the list of new files, downloads them """
  print "Proceeding with the transfer --- ip: " + ip
  try:
    ftp_c = FTP()
    ftp_c.connect(ip, config.PORT)
    ftp_c.login(config.LOGIN, config.PWD)
    ftp_c.getwelcome()
    ftp_c.cwd(rem_dir)
    ftp_c.dir(process_line)
  except:
    print "FTP server is not running, wrong server info or wrong credentials."
    return

  # listing of the local directory
  destlist = os.listdir(dest_path)

  to_download = [i for i in namelist if i not in destlist]

  if len(to_download) > 0:
    print "*** " + str(len(to_download)) + " new files were found!"
    for current in to_download:
      sys.stdout.write( str(to_download.index(current) + 1) + " / " + str(len(to_download)) + " --- " + current + "\n")
      download(ftp_c, current)
  else:
    print "*** No new files were found!"

# ---------------------------------------- main code ---------------------------------------------#

ask_rem_dir()

print "IP POOL: "
print config.IPS

(config.IPS_resp_ok, ping_rep_text) = check_responce(config.IPS, config.COMMAND)

if len(config.IPS_resp_ok) > 1:
  ip = guess_phone(config.IPS_resp_ok)
  if  ip != 0:
    do_ftp_transfer(ip)
  else:
    print "ERROR - CANNOT PROCEED!"
else:
  do_ftp_transfer(config.IPS_resp_ok[0])

raw_input("Press any key to exit the script...")
