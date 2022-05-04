import argparse
import os
import re


def readfile(name):
    print("Reading file " + name + "...")
    try:
        file_exists = os.path.exists(name)
        if not file_exists and re.match(".*_l_russian.yml", name):
            # Create ru template translate if not exists
            with open(name, 'w') as f:
                f.write("l_russian:")
        with open(name, "r", encoding='utf-8-sig') as f:
            lines = f.read().splitlines()
    except Exception as e:
        print("Could not read file " + name + "!")
        print(e)

    iter_lines = iter(lines)
    modified_lines = []
    for line in iter_lines:
        if re.match('.*l_english:', line) or re.match('.*l_russian:', line):
            continue
        line = re.sub('#.*', "", line)
        modified_lines.append(line)

    non_empty_lines = [line for line in modified_lines if line.strip() != ""]

    prepared_kv_lines = {}
    for line in non_empty_lines:
        sp_l = re.split(' "|0"', line, maxsplit=1)
        prepared_kv_lines[sp_l[0].strip()] = sp_l[1].strip('"')

    return prepared_kv_lines


def build_kv_line(key, value):
    line = '\n{0} "{1}"'.format(key, value)
    return line


def add_non_existing_keys(orig, target):
    orig_parced = readfile(orig)
    target_parced = readfile(target)
    keys_to_add = []
    for key in orig_parced.keys():
        if key not in target_parced.keys():
            keys_to_add.append(key)

    print(keys_to_add)
    lines_to_be_added = []
    for key in keys_to_add:
        li = build_kv_line(key, orig_parced[key])
        lines_to_be_added.append(li)

    with open(target, "a", encoding='utf-8-sig') as f:
        f.writelines(lines_to_be_added)
        f.close()


def show_gone_or_changed_keys(orig, target):
    orig_parced = readfile(orig)
    target_parced = readfile(target)
    keys_gone = []
    for key in target_parced.keys():
        if key not in orig_parced.keys():
            keys_gone.append(key)
    if len(keys_gone) == 0:
        print("Lucky you, no changed/gone keys")
    else:
        print("{0} file have keys that does not exist in original".format(target))
        print(keys_gone)


parser = argparse.ArgumentParser(
    description='Given an event, national_focus, decisions, decision_categories or ideas file, add missing localisation entries to a specified localisation file. Note: custom tooltips are not supported. In case of events, title, description and option names will be added (triggered titles and descriptions are supported). For national_focus and ideas, names and descriptions will be added. For decisions and decision_categories, names and category names will be added. WARNING: The script defaults to a decisions file if it cannot determine the type of file.')
parser.add_argument('input', metavar='input',
                    help='Event, national_focus, decisions, decision_categories or ideas file to parse')
parser.add_argument('output', metavar='output',
                    help='Localisation file to write to (if empty/non-existing, a new English localisation file will be created)')
parser.add_argument('-t', '--todo', action='store_true',
                    help='Add "#TODO" to every added line instead of just once (Default: False)')

args = parser.parse_args()
origin = args.input
target = args.output

add_non_existing_keys(origin, target)
show_gone_or_changed_keys(origin, target)
