#!/usr/bin/env python

"""
Automate the following tasks:
1) Insert or update the license and copyright text in the files of the project.
2) Copy the LICENSE and CONTRIBUTORS files at the root of the baltek-the-rules packages.
"""

COPYRIGHT_AND_LICENSE = """
BALTEK-THE-RULES-LICENSE-BEGIN
# LICENSE

[![Creative Commons License](../packages/creative-commons/pictures/CC-BY-SA.png)](http://creativecommons.org/licenses/by-sa/4.0)

BALTEK (the rules) describes a turn-based board game, inspired from football. 

Copyright (C) 2017-2018 Lucas Borboleta ([lucas.borboleta@free.fr](mailto:lucas.borboleta@free.fr)) and Baltekians (see [CONTRIBUTORS.md](./CONTRIBUTORS.md) file at attributed URL).

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License. To view a copy of this license, visit [http://creativecommons.org/licenses/by-sa/4.0](http://creativecommons.org/licenses/by-sa/4.0).

Attribute work to URL [https://github.com/LucasBorboleta/baltek-the-rules](https://github.com/LucasBorboleta/baltek-the-rules).
BALTEK-THE-RULES-LICENSE-END
"""

import os
import re
import shutil
import sys

print
print "Hello"

project_home = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

baltek_the_rules_package_path = os.path.join(project_home, "packages", "baltek-the-rules")

contributors_path = os.path.join(project_home, "docs", "CONTRIBUTORS.md")

license_path = os.path.join(project_home, "docs", "LICENSE.md")
license_stream = file(license_path, "rU")
license_lines = license_stream.readlines()
license_stream.close()

license_begin_rule = re.compile(r"^\W*BALTEK-THE-RULES-LICENSE-BEGIN\W*$")
license_end_rule = re.compile(r"^\W*BALTEK-THE-RULES-LICENSE-END\W*$")

excluded_dir_paths = list()
excluded_dir_paths.append(os.path.join(project_home, ".git"))
excluded_dir_paths.append(os.path.join(project_home, "docs"))
excluded_dir_paths.append(os.path.join(project_home, "packages", "creative-commons"))
excluded_dir_paths.append(os.path.join(project_home, "packages", "w3.css"))
excluded_dir_paths.append(os.path.join(project_home, "tmp"))

excluded_file_paths = list()
excluded_file_paths.append(os.path.join(project_home, ".gitattributes"))
excluded_file_paths.append(os.path.join(project_home, ".gitignore"))

excluded_file_rules = list()
excluded_file_rules.append(re.compile(r"^.*\.md$"))
excluded_file_rules.append(re.compile(r"^.*\.png$"))
excluded_file_rules.append(re.compile(r"^.*\.tmp$"))

file_paths = list()

for (dir_path, dir_names, file_names) in os.walk(project_home):
    dont_walk_items = list()
    for item in dir_names:
        if os.path.join(dir_path, item) in excluded_dir_paths:
            dont_walk_items.append(item)
    for item in dont_walk_items:
        dir_names.remove(item)

    if not dir_path in excluded_dir_paths:
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            if not file_path in excluded_file_paths:
                file_rule_is_matched = False
                for file_rule in excluded_file_rules:
                    if file_rule.match(file_path):
                        file_rule_is_matched = True
                        break
                if not file_rule_is_matched:
                    file_paths.append(file_path)

failed_file_paths = list()

for file_path in file_paths:
    print
    print "updating file '%s' ..." % file_path
    file_stream = file(file_path, "rU")
    file_lines = file_stream.readlines()
    file_stream.close()

    udpated_lines = list()

    license_begin_found = False
    license_end_found = False
    license_error = False

    for line in file_lines:
        license_begin_match = license_begin_rule.match(line)
        license_end_match = license_end_rule.match(line)

        if license_begin_match:
            if license_begin_found:
                license_error = True
                print "error: license_begin_match matched more than one time"
            elif license_end_found:
                license_error = True
                print "error: license_begin_match matched after license_end_match"
            else:
                license_begin_found = True
                udpated_lines.append(line)
                for new_line in license_lines:
                    udpated_lines.append(new_line)

        if license_end_match:
            if license_end_found:
                license_error = True
                print "error: license_end_match matched more than one time"
            elif not license_begin_found:
                license_error = True
                print "error: license_end_match matched before license_begin_match"
            else:
                license_end_found = True

        if not license_begin_found:
            udpated_lines.append(line)
        elif license_end_found:
            udpated_lines.append(line)

    if not (license_begin_found and license_end_found):
        license_error = True
        print "error: not both license_begin_match and license_end_match"

    if not license_error:
        file_stream = file(file_path, "w")
        file_stream.writelines(udpated_lines)
        file_stream.close()
        print "updating file '%s' done" % file_path
    else:
        failed_file_paths.append(file_path)
        print "updating file '%s' failed !!!" % file_path

if len(failed_file_paths) != 0:
    print
    print "Update failed for the following files:"
    for file_path in failed_file_paths:
        print file_path

for file_path in [license_path, contributors_path]:
    shutil.copyfile(file_path, os.path.join(baltek_the_rules_package_path, os.path.basename(file_path)))
    print
    print "copying file '%s' in '%s' ..." % (file_path, baltek_the_rules_package_path)
    print "copying file done"

print
print "Bye"

if len(failed_file_paths) == 0:
    sys.exit(0)
else:
    sys.exit(1)
