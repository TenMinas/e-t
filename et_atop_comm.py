# Common functions used across the app

def yaml_to_dict(ffp):
    import yaml

    my_dict = {}
    with open(ffp, 'r') as f:
        my_dict = yaml.safe_load(f)
    return my_dict


def get_config():
    ffp = "/data/code/et_app/et_sto/et_config/et_config_top.yaml"
    config_dict = yaml_to_dict(ffp)
    return config_dict


def get_config_val(config_dict, c_key):
    # base_path = config_dict["store_loc"]["root_path"]
    ca_config_val = config_dict[c_key]
    return ca_config_val


def load_et_lod(cd):
    root_path = cd['et_sto']['root_path']
    et_lod_path = cd['et_sto']['et_lod']
    ffp = root_path + et_lod_path
    return yaml_to_dict(ffp)


"""
    # non-async version of dict-to-yaml
    # ffp = full file path
"""


def dict_to_yaml(my_dict, ffp):
    import yaml

    with open(ffp, 'w') as f:
        yaml.dump(my_dict, f)


# ffp = full file path
# This code writes the event item dict to storage
async def a_dict_to_yaml(my_dict, ffp):
    import yaml

    with open(ffp, 'w') as f:
        yaml.dump(my_dict, f)


# This code loads an event item from storage into a dict
async def a_yaml_to_dict(ffp):
    import yaml

    my_dict = {}
    with open(ffp, 'r') as f:
        my_dict = yaml.safe_load(f)
    return my_dict


def get_ca_id(user):
    import time

    ca_tm = str(int(time.time()))
    ca_id = ca_tm + user

    print(34, ca_id)
    return ca_id


"""
strtm2ts
- Function created for the event/task app
- Converts a date/time string into a UNIX timestamp
- Assumes the tz is UTC
- Sets the all-day-flag (adf) depending upon the length of the dt-string

"""


def strtm2ts(stm):

    from datetime import datetime, timezone

    if len(stm) == 16:
        date_format = datetime.strptime(stm,
                                        "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        ts = int(datetime.timestamp(date_format))
        adf = False
    elif (len(stm) == 8):
        date_format = datetime.strptime(stm, "%Y%m%d").replace(tzinfo=timezone.utc)
        ts = int(datetime.timestamp(date_format))
        adf = True

    return ts, adf
