''' DESCRIPTION
Open a curses interface which allows the user to select
an openvpn configuration file.
'''
''' Example layout of data
data.0.name = Nord VPN
data.0.locales.au.name = Australia
data.0.locales.au.files.0.path = {path to file}
data.0.locales.au.files.0.protocol = {udp|tcp}
'''
import curses
from vpman_common import fatal as fatal

def main(data):
    curses.wrapper(conf_select, data)

def conf_select(stdscr, data):
    y = curses.LINES - 1
    x = curses.COLS - 1
    pad = curses.newpad(len(data), x)
    for i, v in enumerate(data):
        pad.addstr(i, 0, v["name"])
    pad.refresh(0,0, 0,0, y,x)
    c = pad.getkey()
    
