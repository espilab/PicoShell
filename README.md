# PicoShell
Command shell program for microPython 

This program is command line shell-like program.  


# 0. NOTICE
This program is no warranty. There is some risk of lost any file, break the file system, etc.
USE AT YOUR OWN RISK.

# 1. How to install
Copy the "cmd.py" file into microPython storage area using Thonny.
Also refer the following section; "Flle/Directory structure on micro-controller "

# 2. How to start
From REPL prompt ">>>", execute

    import cmd

or,

    with open("cmd.py") as f: exec(f.read())

(after input above, hit <enter> 2 times) 
If the "import cmd"  dosen't work properly, try the second code in above. (Tring: sys.modules.pop('cmd.py') and import again may works, if lucky..)
    

# 3. How to invoke a python program
      From the prompt '>',  type the <filename.py>  and enter to execute, or <filename> only.
    ".py" can be omit.


# 4. Available commands
      ls  [<path>]       : list the files 
      cd                 : change current directory
      touch <filenmame>  : make a new file 
      rm <filenmame>     : remove the new  
      cp <fname1> <fname2> : copy the file         
      mv <fname1> <fname2> : move or rename the file
      ren                : rename a file
      mkdir <dirname>    : make new directory
      rmdir <dirname>    : remove the directory
      sdmount [on|off]   : mount/unmount the SD card as directory "/sd".
      ! <string>         : evaluate the string as python statement
      exit, bye, off, "."  : exit cmd.py and return to the REPL prompt.

    Currentry, wild-card is not supported.  
      example:  ls *.py   # this command is unavailable.    


# 5. Flle/Directory structure on micro-controller 

     This program was developed on Seeed Studio XIAO Expansion board and XIAO RP2040.

    directory example:

      /
      +------------- lib <dir> 
      |                  |
      +- cmd.py          +- common <dir>
      +- autoexec.bat           |  
      |                         +- config <dir> 
      +- ed.py                  |    +- __init__.py
      |                         |    +- pico.py
      +- boot.py                |    +- picow.py
                                |    +- esp32.py
                                |
                                +- device <dir>
                                    +- __init__.py
                                    +- hcsr04.py
                                    +- pcf8563.py
                                    +- sdcard.py
                                    +- sht31.py
                                    +- ssd1306.py
                                    +- ssd1331.py
                                    +- ws2812.py

         boot.py set the global variable as follows:
            MYBOARD = "pico"

         (cf. Interface magazine (CQ publish), Mar-2023 p42)


# 6. URL for download modules of each device
  
      https://wiki.seeedstudio.com/XIAO-RP2040-with-MicroPython
          Download a file: XIAO-RP2040-MicroPython-Grove.zip and copy modules as follows
          into /lib/common/device directory.
             ws2812.py  
             ssd1306.py

      https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/storage/sdcard
             sdcard.py 


# 7. Batch file
       Filename *.bat can be used as batch file.
      The file "autoexec.bat" is executed automatically when start the cmd.py program.


# 8. Command line parameter
     About a python program invoked from cmd.py, it can receive the command-line parameter
    string in global variable COMMAND_LINE.  
    The cmd.py and invoked program shares the name space.


# 9. ed.py --- simple text editor
     ed.py is line editor for editing a text file.  
    It has command like "ex" editor of unix.
 
    After invoked, the command prompt ":" appears and command mode.

    Available commands:
       a            :  text append mode.  '.' and enter for return to command mode.
       <line>i      :  text insert mode.  '.' and enter for return to command mode.
       q            :  quit
       w [filename] :  file-out the text content.
       <range>p    :  show text content
       <range>#    :  show text content with line number

      <range> is line number range.  format is <start_line>,<end_line> or "%" means all lines. 
  
      Session example:

        />ed sample.txt
        " sample.txt ", (New file)
        :a              # enter append mode
        hello           # enter the first line
        world           # enter the second line
        .               # return to the command mode
        :%#             # show the content with line number
            1: hello
            2: world
        :2i             # insert text
        small
        .
        :1,3#           # show the content with line number
            1: hello
            2: small
            3: world
        :w                        # Output the text file as sample.txt
        "sample.txt", 3 lines
        :q                        # quit 


2023-4-15 by espilab.

EOF
