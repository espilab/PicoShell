# line_edit.py
#
# v0.5   2023-4-15  

import sys
import os
import re

# check file existance
def is_exist(fname):
  ret = True
  try:
    os.stat(fname)
  except OSError as exc:
    #print('error no=',exc.errno)
    ret = False
  return ret

# return start,end line number from command
def l_range(str, idx_max):
    if (str[0] == '%') or (len(str) == 1):
        return 1, idx_max
    else:
        #str = str[:(len(str) - 1)]
        str = re.sub("[a-zA-Z#].*$", "", str)
    if ',' in str:
        s1, s2 = str.split(',')
        v1 = int(s1)
        if s2 == '$':    # last line
            v2 = idx_max
        else:
            v2 = int(s2)
        if v2 > idx_max:
            v2 = idx_max 
        return v1, v2
    else:
        return int(str), int(str)

# text editor
def textedit(fname):
    global text_content
    editing = True
    insert = False
    while editing:
        cmd_str = input(':')
        if cmd_str == 'q':
            return
        elif cmd_str == 'a':
            insert = True
            while insert:
                ins_text = input('')
                if ins_text == '.':
                    insert = False
                else:
                    text_content.append(ins_text)
                    #print('len=',len(text_content))  #DEBUG
        elif cmd_str[-1] == '#':
            line_start, line_end = l_range(cmd_str, len(text_content) - 1)
            for j in range(line_start, line_end + 1):
                print("{:>5}: {}".format(j, text_content[j]))
        elif cmd_str[-1] == 'p':
            line_start, line_end = l_range(cmd_str, len(text_content) - 1)
            for j in range(line_start, line_end + 1):
                print(text_content[j], sep="")
        elif cmd_str[-1] == 'd':
            line_start, line_end = l_range(cmd_str, len(text_content) - 1)
            del text_content[line_start:line_end+1]
        elif cmd_str[-1] == 'i':
            line_num = int(cmd_str[:-1])
            insert = True
            while insert:
                ins_text = input('')
                if ins_text == '.':
                    insert = False
                else:
                    text_content.insert(line_num, ins_text)
                    line_num += 1
        elif 's/' in cmd_str:
            line_start, line_end = l_range(cmd_str, len(text_content) - 1)
            s = cmd_str.split('/')
            for j in range(line_start, line_end + 1):
                text_content[j] = text_content[j].replace(s[1], s[2])

        elif cmd_str.startswith('w'):
            if len(cmd_str) > 1:
                fname = cmd_str[2:]
            line_start = 1
            line_end = len(text_content) - 1
            cnt = 0
            with open(fname, "w") as f:
              for j in range(line_start, line_end + 1):
                a_line = ''.join(text_content[j].splitlines())
                f.write(a_line + "\r\n")
                cnt += 1
            print('"',fname,'", ', cnt, ' lines', sep="")


# -------- main --------
current_fname = 'noname.txt'
text_content = ['']

status = 'COMMAND_LINE' in globals()

if status == False:
  print('ed.py --- text editor (invoked directly)')
  if len(sys.argv) >= 2:
      current_fname = sys.argv[1]
  else:
      current_fname = input('Enter file name:')
  with open(current_fname) as f:
      content = f.read()
  text_content[1:] = content.split("\n")
  textedit(current_fname)
  sys.exit()

# the var. "cmd_line" should be set by cmd.py program as global variable.

ar = COMMAND_LINE.split(' ')
if len(ar) > 1:
    current_fname = ar[1]

if is_exist(current_fname):
    #print(current_fname,'is exists.')  #DEBUG
    with open(current_fname) as f:
        content = f.read()
    text_content[1:] = content.split("\n")
    print('"', current_fname, '", ', len(text_content) -1, ' lines', sep="")
else:
    print('"', current_fname, '", (New file)')
    
textedit(current_fname)
