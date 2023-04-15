#
# cpufreq.py --- set/get cpu clock frequency
#
import machine

args = COMMAND_LINE.split(' ')

if len(args) < 2:
    freq = machine.freq()
    print('current frequency = ', freq, 'Hz', sep="", end="")
    print(' (', freq / 1e6, 'MHz)', sep="")
else:
    set_freq = int(args[1])
    try:
        machine.freq(set_freq)
    except OSError as exc:
        print('error no=',exc.errno)

