#!/usr/bin/env python2.7
#by azazhel

from sys import modules

import readline
import atexit

modules.clear()
del modules

saved_raw_input = raw_input
saved_exception = Exception

__builtins__.__dict__.clear()
__builtins__ = None


black_list = ['os', 'sh', 'bash', 'system', 'import']

print "                    ____"
print "                 _.' :  `._"
print "             .-.'`.  ;   .'`.-."
print "    __      / : ___\\ ;  /___ ; \\      __"
print "  ,'_ \"\"--.:__;\".-.\";: :\".-.\":__;.--\"\" _`,"
print "  :' `.t\"\"--.. '<@.`;_  ',@>` ..--\"\"j.' `;"
print "       `:-.._J '-.-'L__ `-- ' L_..-;'"
print "         \"-.__ ;  .-\"  \"-.  : __.-\""
print "             L ' /.------.\\ ' J"
print "              \"-.   \"--\"   .-\""
print "             __.l\"-:_JL_;-\";.__"
print "          .-j/'.;  ;\"\"\"\"  / .';\"-."
print "        .' /:`. \"-.:     .-\" .';  `."
print "     .-\"  / ;  \"-. \"-..-\" .-\"  :    \"-."
print "  .+\"-.  : :      \"-.__.-\"      ;-._   \\"
print "  ; \\  `.; ;                    : : \"+. ;"
print "  :  ;   ; ;                    : ;  : \\:"
print " : `.\"-; ;  ;                  :  ;   ,/;"
print "  ;    -: ;  :                ;  : .-\"'  :"
print "  :\\     \\  : ;             : \\.-\"      :"
print "   ;`.    \\  ; :            ;.'_..--  / ;"
print "   :  \"-.  \"-:  ;          :/.\"      .'  :"
print "     \\       .-`.\\        /t-\"\"  \":-+.   :"
print "      `.  .-\"    `l    __/ /`. :  ; ; \\  ;"
print "        \\   .-\" .-\"-.-\"  .' .'j \\  /   ;/"
print "         \\ / .-\"   /.     .'.' ;_:'    ;"
print "          :-\"\"-.`./-.'     /    `.___.'"
print "                \\ `t  ._  /  bug :F_P:"
print "                 \"-.t-._:'"



print 'Type "exit" to exit.'

while 1:
    try:
        print '>>>',
        vars = {'result':0}
        user_input = saved_raw_input()

        if user_input == 'exit':
            break
        found = 0
        for bad_word in black_list:
            if bad_word in user_input:
                found = 1
                break
        
        if found:
            print 'Nope'
        else:
            exec 'result = ' + user_input in vars
            print vars['result']
    except saved_exception as e:
        print "Error:", e
