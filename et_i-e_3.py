#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 13:09:27 2025.

@author: gary
"""


from et_atop_comm import strtm2ts, dict_to_yaml


"""
Various static constants
lat / long == Alamo in satx
"""

# Input full file path
ie_i_ffp = "/data/code/et_app/et_test_data/Events_20250308_102157.ics"

# Output full file path
ie_o_ffp = "/data/code/et_app/et_sto/et_i-e_files/ie_converted.yaml"

fpr = "/data/code/et_app/et_sto/et_db/et_db_files/"

idn = 0
user = 'ei'
ei_type = "event"
ltz = "CDT"
lat = 29.4259
long = -98.4861

"""
et_schema >> template dict >> schema for ALL of the NEW et entries
et_lod >> is the final product of this import
each event will be enclosed in a dict
the lod is a list of these event dicts

t_lod >> temp dict used during the build cycle

lok >> list of key-words to parce out of the ics file

build_flag >> Set "True" between Begin and End Vevent

ln >> line in the ics file >> helps with debug
"""


ref_lod = {
    "new_uid": "!#!",
    "sort": "!#!",
    "ei_type": ei_type,
    "ei_tags": [],
    "title": "!#!",
    "start_ts": "!#!",
    "start_tz": "!#!",
    "end_ts": "!#!",
    "end_tz": "!#!",
    "create_ts": "!#!",
    "last_mod": "!#!",
    "all_day": False,
    "description": "!#!",
    "location": "!#!",
    "lat-long": {'lat': "!#!", 'long': "!#!"},
    "url":  "!#!",
    "status": "!#!",
    "rrule": "!#!",
    "old_uid": "!#!",
    "exdate": [],
    "attendees": [],
    "trash": False
}

"""
The straight forward way of getting a clean t_lod isn't working

"""


def make_t_lod(ref_lod):
    t_lod = {}
    for d in ref_lod:
        t_lod.update({d: ref_lod[d]})

    return t_lod


# fpr = file path root
def dict_to_yaml_files(my_dict, fpr):
    import yaml

    fn = my_dict["new_uid"]
    ffp = fpr + fn

    with open(ffp, 'w') as f:
        yaml.dump(my_dict, f)


lok = ['SUMMARY',
       'DTSTART',
       'DTEND',
       'CATEGORIES',
       'LAST-MODIFIED',
       'DTSTAMP',
       'RRULE',
       'UID',
       'STATUS'
       ]

sub_lok = ['DESCRIPTION', 'LOCATION', 'EXDATE']

ml_list = ['d', 'l', 'e']

build_flag = False
ln = 0
et_lod = []
ml = "z"


"""
pns >> parse & store
  - parses the line
  - cleans the result
  - saves it in the applicable dict
line
  - a line in the ics determined to be part of a given event
t_lod
  - For def see above.
  - This func modifies the input t_lod and returns the modified t_lod
"""


def pns(t_lod, line):
    tl = line.partition(':')
    if line.startswith('SUMMARY'):
        t_lod['title'] = tl[2].strip()
    elif line.startswith('DTSTART'):
        t_lod['start_tz'] = ltz
        tsadf = strtm2ts(tl[2].strip())
        t_lod['start_ts'] = tsadf[0]
        t_lod['all_day'] = tsadf[1]
    elif line.startswith('DTEND'):
        t_lod['end_tz'] = ltz
        tsadf = strtm2ts(tl[2].strip())
        t_lod['end_ts'] = tsadf[0]
    elif line.startswith('CATEGORIES'):
        temp_tag = tl[2].strip()
        t_lod['ei_tags'] = [temp_tag]
    elif line.startswith('LAST-MODIFIED'):
        tsadf = strtm2ts(tl[2].strip())
        t_lod['last_mod'] = tsadf[0]
    elif line.startswith('DTSTAMP'):
        tsadf = strtm2ts(tl[2].strip())
        t_lod['create_ts'] = tsadf[0]
    elif line.startswith('RRULE'):
        t_lod['rrule'] = tl[2].strip()
    elif line.startswith('UID'):
        t_lod['old_uid'] = tl[2].strip()
    elif line.startswith('STATUS'):
        t_lod['status'] = tl[2].strip().lower()

    return t_lod


def pns_sub(t_lod, line):
    ml = 'z'
    tl = line.partition(':')
    if line.startswith('DESCRIPTION'):
        if tl[2].strip() == "Reminder":
            t_lod['description'] = "!#!"
        else:
            t_lod['description'] = tl[2].strip()
            ml = 'd'
    elif line.startswith('LOCATION'):
        t_lod['location'] = tl[2].strip()
        ml = 'l'
    elif line.startswith('EXDATE:'):
        exts = strtm2ts((tl[2].strip()))
        t_lod['exdate'] = [exts[0]]
        ml = 'e'

    return t_lod, ml


def pns_d(t_lod, line):
    if line.startswith("\t"):
        tv = line.lstrip("\t")
        t_lod['description'] = t_lod['description'] + tv
    return t_lod


def pns_l(t_lod, line):
    if line.startswith("\t"):
        tv = line.lstrip("\t")
        t_lod['location'] = t_lod['description'] + tv
    return t_lod


def pns_e(t_lod, line):

    if line.startswith('EXDATE:'):
        ed = line.lstrip('EXDATE:').strip()
        edts = strtm2ts(ed)
        t_lod['exdate'].append(edts[0])

        return t_lod


with open(ie_i_ffp, 'r') as file:
    # file = open(ics_path, 'r')
    while True:
        ln += 1
        line = file.readline()
        if not line:  # identifies the end of the file
            break  # ends the loop when the eof is reached
        if line.startswith("BEGIN:VEVENT"):
            build_flag = True
            t_lod = make_t_lod(ref_lod)
            idn += 1
            t_lod['new_uid'] = user + str(idn)

        else:
            if line.startswith("END:VEVENT"):
                build_flag = False
                # et_lod.append(t_lod)
                dict_to_yaml_files(t_lod, fpr)

            else:
                if build_flag:
                    if line.startswith(tuple(lok)):
                        t_lod = pns(t_lod, line)
                        ml = "z"
                    elif ml == 'd':
                        t_lod = pns_d(t_lod, line)
                    elif ml == 'l':
                        t_lod = pns_l(t_lod, line)
                    elif ml == 'e':
                        t_lod = pns_e(t_lod, line)

                    elif line.startswith(tuple(sub_lok)):

                        ps = pns_sub(t_lod, line)

                        t_lod = ps[0]
                        ml = ps[1]

# dict_to_yaml(et_lod, ie_o_ffp)
