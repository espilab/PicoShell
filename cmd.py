#
# cmd.py --- microPython command shell 'Pico Shell'
#
# v0.26  2023-4-15
# 

if 'MYBOARD' in globals():
    from machine import Pin, SPI, I2C
    from common.device.sdcard import SDCard
    from common.device.pcf8563 import PCF8563
    from common.device.ws2812 import WS2812

import os
import sys
import time

# ------ const.------
file_type_normal = 0x8000
file_type_dir    = 0x4000

# check the file existance and attribute
#  Caution: in return value, file type is f_stat[0]
def file_attr(fname):
    ret = True
    f_stat = ''
    try:
        f_stat = os.stat(fname)
    except OSError as exc:
        #print('error no=',exc.errno)
        ret = False
    return ret, f_stat    

# chack the file existance
def is_exist(fname):
  ret, f_stat = file_attr(fname) 
  return ret
    
        
def copy_file(source_file, dest_file):
    if is_exist(dest_file):
        ret, f_stat = file_attr(dest_file)
        if f_stat[0] == file_type_normal:
            print(dest_file,'already exists!')
            return False
        elif f_stat[0] == file_type_dir:
            dest_file = dest_file + '/' + source_file
            return copy_file(source_file, dest_file)
    try:
        with open(source_file, 'rb') as fsrc:
            with open(dest_file, 'wb') as fdst:
                while True:
                    buf = fsrc.read(1024)
                    if not buf:
                        break
                    fdst.write(buf)
        return True
    except:
        return False

def move_file(src_path, dest_path):
    if is_exist(dest_path):
        print('dest=',dest_path) #DEBUG
        ret, f_stat = file_attr(dest_path)
        if f_stat[0] == file_type_normal:
            print(dest_path, 'alredey exists!')
            return False
        if f_stat[0] == file_type_dir:
            i = src_path.rfind('/')
            if i >= 0:
                src_fname = src_path[(i+1):]
            else:
                src_fname = src_path
            dest_path = dest_path + '/' + src_fname
            print('(dest_path=',dest_path,')')  #DEBUG
            if is_exist(dest_path):
               print(dest_path, 'alredey exists!') 
               return False
    if not is_exist(src_path):
        print(src_path, 'not found!')
        return False
    if src_path == dest_path:
        print('src and dest. are same!')
        return False
    if file_attr(src_path) == file_type_dir:
        print('source file should be a file (not directory)')
        return False
    
    if copy_file(src_path, dest_path):
        ok = True
        os.remove(src_path)
        print(src_path, '->', dest_path, 'done.')
        return ok
    else:
        ok = False
        print('move_file: copy error!')
        return ok
    
    
def list_dir(path):
    try:
        dir_entry = os.listdir(path)
    except OSError as exc:
        print('listdir failed, error no=',exc.errno)
        return
    for item in dir_entry:
        #print('path=',path,' item=',item, sep="") #DEBUG
        item_path = (path + '/'+ item).replace('//','/') #os.path.join(path, item)
        ar = os.stat(item_path)
        ftype = ar[0]
        fsize = ar[6]
        if (ftype == file_type_dir):
            print('{:<20}  <dir>'.format(item))
        else:
            print('{:<20}  {:>8d} bytes'.format(item, fsize))
    fs_stat = os.statvfs(path)
    print('  ', fs_stat[0] * fs_stat[4], 'bytes free')
    

def show_date():
    print('system:',time.localtime())
    if 'rtc' in globals():
        print('RTC:{0:02d}/{1:02d}/{2:02d} {4:02d}:{5:02d}:{6:02d}'.format(*rtc.datetime()))

    
def change_dir(path):
    os.chdir(path)
    # Update the prompt string with the current directory path
    global prompt_str
    prompt_str = os.getcwd() + '>'

def cat_file(fname):
    with open(fname) as f:
        print(f.read())


def invoke_cmd(cmd, cmd_line_str):
    #print('cmd=',cmd,' cmd_line_Str=',cmd_line_str, sep="")  #DEBUG
    global COMMAND_LINE
    COMMAND_LINE = cmd_line_str
    if not ('.py' in cmd):
       cmd = cmd + '.py'
       #print('cmd(2)=',cmd)  #DEBUG
    ok = True
    try:
        ar = os.stat(cmd)
    except OSError as exc:
        print('error no=',exc.errno, '(maybe the file',cmd,'not exist.)')
        ok = False
    if ok:
       if ar[0] == file_type_normal:
          #import cmd
          with open(cmd) as f:
              exec(f.read())   
    
    


#  process command-line string as shell command
def process_cmd_line(cmd_line):
    args = cmd_line.split(' ')
    cmd = args[0]
    if cmd == 'ls':
        if len(args) <= 1:
          list_dir('.')
        else:
          list_dir(args[1])
    elif cmd == 'mkdir':
        if len(args) <= 1:
          print('specify direcrotry name')
        else:
          exist, f_stat = file_attr(args[1])
          if exist:
              if f_stat[0] == file_type_dir:
                  print('Dir:',args[1], 'already exists!')
              elif f_stat[0] == file_type_normal:
                  print('File:', args[1], 'already exists!')
          else:
              os.mkdir(args[1])
    elif cmd == 'rmdir':
        if len(args) <= 1:
          print('specify direcrotry name')
        else:
          exist, f_stat = file_attr(args[1])
          if exist:
              if f_stat[0] == file_type_dir:
                  os.rmdir(args[1])
              elif f_stat[0] == file_type_normal:
                  print(args[1], 'is a file.')
          else:
              print(args[1], 'not found')
              
    elif cmd == 'date':
        if len(args) <= 1:
            show_date()
        elif len(args) >= 7:
            print('ent')
        else:
            print('usage: date [<year> <month> <day> <hour> <minutes> <second>]')
            
    elif cmd == 'cd':
        path = ''.join(args[1:])
        change_dir(path)
    elif cmd == 'cat':
        cat_file(args[1])
    elif cmd == 'touch':
        if len(args) <= 1:
            print('specify filename!')
        else:
            filename = args[1]
            open(filename, 'a').close()
            print(f'{filename} made.')

    elif cmd == 'cp':
        if len(args) < 3:
            print('file name not specified')
        else:
            src_file = args[1]
            dest_file = args[2]
            if copy_file(src_file, dest_file):
               print(f'{src_file} is copied to {dest_file}')
            else:
               print(f'copy the file:{src_file} faild')
    elif cmd == 'mv':
        if len(args) < 3:
            print('file name not specified')
        else:
            src_path = args[1]
            dest_path = args[2]
            move_file(src_path, dest_path)

    elif cmd == 'rm':
        if len(args) < 2:
            print('file name not specified')
        else:
            filename = args[1]
            if is_exist(filename):
                os.remove(filename)
                print(f'{filename} removed')
            else:
                print(f'{filename} not found')

    elif cmd == 'ren':
        if len(args) < 3:
            print('usage: ren <old_fname> <new_fname>')
        else:
            fname1 = args[1]
            fname2 = args[2]
        if is_exist(fname1):
            if is_exist(fname2):
                print(fname2, 'alredy exists!')
            else:
                os.rename(fname1, fname2)
        else:
            print(fname1, 'not found')
    
    elif cmd == 'sdmount':
        if len(args) < 2:
            print('usage: sdmount [on|off]')
        else:
            if args[1] == 'on':
                sdmount(True)
            elif args[1] == 'off':
                sdmount(False)
            else:
                print('use "on" or "off"')

    elif cmd == '!':
        exec('ret = ' + cmd_line[1:])
        print('ret=',ret)
    elif cmd == 'pause':
        if len(args) < 2:
            print('usage: pause <sec>')
        else:
            time.sleep(int(args[1]))
        
    elif (cmd == 'bye') or (cmd == 'off') or (cmd == 'exit') or (cmd == '.'):
        end_message()
        sys.exit()
    elif len(cmd_line) == 0:
        return
    elif '.bat' in cmd:
        process_bat_file(cmd)
    else:
        invoke_cmd(cmd, cmd_line)
        #print('type exit to quit.')
    
def process_bat_file(fname):
    if is_exist(fname):
        with open (fname) as f:
            content_ar = (f.read()).split("\r\n")
        #print('content_ar=',content_ar) #DEBUG
        for a_line in content_ar:
            #print('bat line=',a_line,' len=',len(a_line))  #DEBUG
            process_cmd_line(a_line)
    else:
        print(fname, 'not found!')

def sdmount(onoff_flag):
    global spi,sd
    
    # try to use SD card I/F on spi
    ok = True
    try:
        sd = SDCard(spi, Pin(28))
    except OSError as exc:
        print('error no=',exc.errno,'maybe no sd card') 
        ok = False
    if not ok:
        print('spi for sd assignment error')
        return

    if onoff_flag:   # flag == True --> mount
        try:
            os.mount(sd, '/sd')
        except OSError as exc:
            print('sd mount fail, error no=',exc.errno)
            ok = False
        if ok:
            print('sd card mounted.')

    else:  # flag == false --> unmount
        try:
            os.umount('/sd')
        except OSError as exc:
            print('sd unmount fail, error no=',exc.errno)
            ok = False
        if ok:
            print('sd card unmounted.')
    return ok


def start_message():
    print('Pico shell --- microPython command shell. 2023 by espilab')
    print(' Type "bye" or "off" to quit and return to REPL prompt.')

def end_message():
    print('If you want to re-start CMD prompt, execute the following code:')
    print('  import cmd       (if nothing happen, try: sys.modules.pop("cmd") in advance.')
    print('or,')
    print('  with open("cmd.py") as f:')
    print('      exec(f.read())')



#-------- main --------
if 'MYBOARD' in globals():
    spi = SPI(0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=200000)
    rtc = PCF8563(i2c)
    #print('MYBOARD found.')   #DEBUG

prompt_str = os.getcwd() + '>'
start_message()

fname = 'autoexec.bat'
if is_exist(fname):
    process_bat_file(fname)

while True:
    cmd_line_str = input(prompt_str)
    process_cmd_line(cmd_line_str)
