from random import choice, random
TEMP_PRE = "Glaci Frigi Medi Calori Incendi"\
    .replace('-','').split()
WET_POST = "aris siccus humus aquosus marinus"\
    .replace('-','').split()

TEMP_POST = "glacus frigis medis caloris scendis"\
    .replace('-','').split()
WET_PRE = "Ari Sicci Humi Aqua Marina"\
    .replace('-','').split()
USED_NAMES = []


def list_float_idx(list_: list, idx: float):
    return list_[int((len(list_))*idx)]


def name_planet(wet, temp):
    global USED_NAMES
    # wet is a humidity value between 0.0 and 1.0
    # temp is a temperature value
    if random() > 0.5:
        name = list_float_idx(TEMP_PRE, temp) \
            + ("" if True else choice(MID)) \
            + list_float_idx(WET_POST, wet)
    else:
        name = list_float_idx(WET_PRE, wet) \
            + ("" if True else choice(MID)) \
            + list_float_idx(TEMP_POST, temp)
    while name in USED_NAMES:
        name += 'I'
        for target, replacement in (("IIII",  "IV"),
                                    ("IVI",   "V"),
                                    ("VIIII", "IX"),
                                    ("IXI",   "X")):
            replaced = name.replace(target, replacement)
            if replaced != name:
                name = replaced
                break
    USED_NAMES.append(name)
    return name