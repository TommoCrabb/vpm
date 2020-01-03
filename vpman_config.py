''' DESCRIPTION
Pull information from config files and generate
a dictionary type object.
'''
from pathlib import Path
import configparser
from re import compile as reco
from vpman_common import fatal as fatal

def parse_cfg(cf, data):
    cfg = configparser.ConfigParser()
    cfg.read(cf)
    vpn = {
        "name" : cfg["general"]["name"],
        "locales" : {}
    }
    cap = reco(cfg["capture"]["regex"])
    af = [x for x in cf.parent.rglob("*") if x.is_file()]
    for f in af:
        m = cap.search(f.name)
        if m != None:
            ml = m.group( cfg["capture"].getint("location") )
            mp = m.group( cfg["capture"].getint("protocol") )
            if not ml in vpn["locales"].keys():
                vpn["locales"][ml] = {
                    "name" : cfg["locales"][ml],
                    "files" : []
                }
            vf = {
                "path" : str(f),
                "protocol" : mp,
            }
            vpn["locales"][ml]["files"].append(vf)
    data.append(vpn)

def main():
    data = []
    xdir = Path(__file__).resolve()
    cdir = xdir.parent / "conf"
    cfgs = cdir.rglob("vpm.cfg")
    for f in cfgs:
        parse_cfg(cf=f, data=data)
    return(data)