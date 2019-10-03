#!/usr/bin/env python3
'''
Usage:
  timespent.py (--wage <wage> | --salary <salary> | --weekly-rate <weekly-rate>) --from <date> [--currency-symbol <symbol>] [--not-continuous]

Options:
  -w | --wage          Hourly rate of pay. Float.
  -r | --weekly-rate   Self explanatory. Float.
  -s | --salary        Annual take home. Float.
  -f | --from          Date job would have started (i.e. time to start counter 
                       from). This is in ISO-8601 format: "YYYY-MM-DD".

  -c | --currency-symbol   Symbol used for currency. Default is '£'
  -n | --not-continuous    Use this flag to only show once, otherwise 
                           recalculates once a second until <C-c> is pressed.'''

import sys
import re
from datetime import datetime
import time

major, minor, patch = [int(s) for s in sys.version.split()[0].split('.')]

if major < 3:
    print("Good god, get python3!")
    exit(1)

if minor < 6:
    print("Upgrade to 3.6 for glorious f-strings")
    exit(1)

arglen = len(sys.argv)
isodate_re = re.compile(r'\d\d\d\d-[01]\d-[0-3]\d')

def error(message):
    print(message, __doc__)
    exit(1)

if arglen < 5:
    error("Syntax error.")

earnings_per_second = None
date_from = None
currency = '£'
continuous = True

RESET = '\033[0m'
RED = '\033[31m'
BOLD = '\033[1m'

for key, value in zip(sys.argv[1::2], sys.argv[2::2]):
    
    if key in ['-w', '--wage', '-s', '--salary', '-r', '--weekly-rate']:
        
        if key in ['-s', '--salary']:
            mult = (60*60*24*365.24)
        elif key in ['-w', '--wage']:
            mult = (60*60)
        else: #key in ['-r', '--weekly-rate']:
            mult = (60*60*24*7)
            
        try:
            earnings_per_second = float(value) / (mult)
        except ValueError:
            error("Earning rate needs to be float.")
            
    elif key in ['-f', '--from']:
        
        if isodate_re.match(value):
            date_from = datetime.fromisoformat(value)
        else:
            error("Date from needs to be in ISO-8601 format (YYY-MM-DD).")
            
    elif key in ['-c', '--currency-symbol']:

        currency = value

    elif key in ['-n', '--not-continuous']:

        continuous = False
            
    else:
        error("Argument not understood: {}".format(key))

def calc_unearned(date_from):
    dt = datetime.now() - date_from
    cash_not_earned = dt.total_seconds() * earnings_per_second
    return '  Cash not earned: {}{}{}{:.2f}{}'.format(RED, BOLD, currency, cash_not_earned, RESET)

if not continuous:
    print(calc_unearned(date_from))
else:
    try:
        while (True):
            print(calc_unearned(date_from), end='\r')
            time.sleep(1)
    except KeyboardInterrupt:
        pass
