#!/usr/bin/env python

"""
Automate the following tasks:
1) Copy the LICENSE.md,  CONTRIBUTORS.md and VERSION.txt files at the root of the baltek-the-rules package.
2) Insert or update the license and copyright Markdown text in the files of the project (expected as comments).
3) Insert or update a conversion to HTML of the Markdown in the rules HTML texts.
"""

_COPYRIGHT_AND_LICENSE = """
BALTEK-THE-RULES-LICENSE-MD-BEGIN
# LICENSE

[![Creative Commons License](../packages/creative-commons/pictures/CC-BY-SA.png)](http://creativecommons.org/licenses/by-sa/4.0)

BALTEK (the rules) describes a turn-based board game, inspired from football.

Copyright (C) 2017-2018 Lucas Borboleta ([lucas.borboleta@free.fr](mailto:lucas.borboleta@free.fr)) and Baltekians (see [CONTRIBUTORS.md](./CONTRIBUTORS.md) file).

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License. To view a copy of this license, visit [http://creativecommons.org/licenses/by-sa/4.0](http://creativecommons.org/licenses/by-sa/4.0).

Attribute work to URL [https://github.com/LucasBorboleta/baltek-the-rules](https://github.com/LucasBorboleta/baltek-the-rules).
BALTEK-THE-RULES-LICENSE-MD-END
"""

import os
import re
import shutil
import sys

project_home = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

tmp_path = os.path.join(project_home, "tmp")

log_path = os.path.join(tmp_path, os.path.basename(__file__) + ".log.txt")
sys.stdout = open(log_path, "w")
sys.stderr = open(log_path, "w")

print
print "Hello"

baltek_the_rules_package_path = os.path.join(project_home, "packages", "baltek-the-rules")
baltek_the_rules_package_html_path = os.path.join(baltek_the_rules_package_path, "html")

version_txt_path = os.path.join(project_home, "docs", "VERSION.txt")
contributors_path = os.path.join(project_home, "docs", "CONTRIBUTORS.md")
license_md_path = os.path.join(project_home, "docs", "LICENSE.md")

license_md_begin_rule = re.compile(r"^\W*BALTEK-THE-RULES-LICENSE-MD-BEGIN\W*$")
license_md_end_rule = re.compile(r"^\W*BALTEK-THE-RULES-LICENSE-MD-END\W*$")

license_html_begin_rule = re.compile(r"^\W*BALTEK-THE-RULES-LICENSE-HTML-BEGIN\W*$")
license_html_end_rule = re.compile(r"^\W*BALTEK-THE-RULES-LICENSE-HTML-END\W*$")

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
excluded_file_rules.append(re.compile(r"^.*\.txt$"))

def convert_licence_lines_from_md_to_html(license_md_lines):
    license_html_lines = list()

    empty_line_rule = re.compile(r"^\s*$")
    h1_line_rule = re.compile(r"^#\s+\w*\s*$")

    newline_rule = re.compile(r"\n")
    newline_replacement = r' '

    image_rule = re.compile(r"!\[(?P<image_alt>[^\[\]]*)\]\((?P<image_src>[^\(\)]*)\)")
    image_replacement = r'<img lang="en" alt="\g<image_alt>" src="\g<image_src>">'

    link_rule = re.compile(r"\[(?P<link_text>[^\[\]]*)\]\((?P<link_href>[^\(\)]*)\)")
    link_replacement = r'<a lang="en" target="_blank" href="\g<link_href>">\g<link_text></a>'

    package_path_rule = re.compile(r'"[./]+/packages/(?P<package_name>[^"]+)"')
    package_path_replacement = r'"../../../packages/\g<package_name>"'

    local_path_rule = re.compile(r'"[.]/(?P<file_name>[^"]+)"')
    local_path_replacement = r'"../\g<file_name>"'

    paragraph_begin_found = False
    paragraph_end_found = False
    paragraph_text = ""

    # Add an empty line in order to treat the last paragraph like the previous ones.
    for license_md_line in license_md_lines + ["\n"]:
        if empty_line_rule.match(license_md_line):
            if paragraph_begin_found:
                paragraph_end_found = True
        elif h1_line_rule.match(license_md_line):
            pass
        else:
            paragraph_begin_found = True
            paragraph_text += license_md_line

        if paragraph_begin_found and paragraph_end_found:
            paragraph_text = newline_rule.sub(newline_replacement, paragraph_text)
            paragraph_text = image_rule.sub(image_replacement, paragraph_text)
            paragraph_text = link_rule.sub(link_replacement, paragraph_text)
            paragraph_text = package_path_rule.sub(package_path_replacement, paragraph_text)
            paragraph_text = local_path_rule.sub(local_path_replacement, paragraph_text)

            paragraph_text = '<p lang="en" >' + paragraph_text + '</p>\n'
            license_html_lines.append(paragraph_text)

            paragraph_begin_found = False
            paragraph_end_found = False
            paragraph_text = ""

    return license_html_lines

license_md_stream = file(license_md_path, "rU")
license_md_lines = license_md_stream.readlines()
license_md_stream.close()

license_html_lines = convert_licence_lines_from_md_to_html(license_md_lines)

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

    license_md_begin_found = False
    license_md_end_found = False
    license_md_error = False

    license_html_begin_found = False
    license_html_end_found = False
    license_html_error = False

    for line in file_lines:
        license_md_begin_match = license_md_begin_rule.match(line)
        license_md_end_match = license_md_end_rule.match(line)

        license_html_begin_match = license_html_begin_rule.match(line)
        license_html_end_match = license_html_end_rule.match(line)

        if license_md_begin_match:
            if license_md_begin_found:
                license_md_error = True
                print "error: license_md_begin_match matched more than one time"
            elif license_md_end_found:
                license_md_error = True
                print "error: license_md_begin_match matched after license_md_end_match"
            else:
                license_md_begin_found = True
                udpated_lines.append(line)
                udpated_lines.extend(license_md_lines)

        if license_html_begin_match:
            # the relative path of license_html_lines have been prepared for the HTML rules only !
            assert os.path.dirname(file_path) == baltek_the_rules_package_html_path

            if license_html_begin_found:
                license_html_error = True
                print "error: license_html_begin_match matched more than one time"
            elif license_html_end_found:
                license_html_error = True
                print "error: license_html_begin_match matched after license_html_end_match"
            else:
                license_html_begin_found = True
                udpated_lines.append(line)
                udpated_lines.extend(license_html_lines)

        if license_md_end_match:
            if license_md_end_found:
                license_md_error = True
                print "error: license_md_end_match matched more than one time"
            elif not license_md_begin_found:
                license_md_error = True
                print "error: license_md_end_match matched before license_md_begin_match"
            else:
                license_md_end_found = True
                udpated_lines.append(line)

        if license_html_end_match:
            if license_html_end_found:
                license_html_error = True
                print "error: license_html_end_match matched more than one time"
            elif not license_html_begin_found:
                license_html_error = True
                print "error: license_html_end_match matched before license_html_begin_match"
            else:
                license_html_end_found = True
                udpated_lines.append(line)

        if not (license_md_begin_match or license_md_end_match or license_html_begin_match or license_html_end_match):
            if not( (license_md_begin_found != license_md_end_found) or (license_html_begin_found != license_html_end_found) ):
                udpated_lines.append(line)

    if not (license_md_begin_found and license_md_end_found):
        license_md_error = True
        print "error: not both license_md_begin_match and license_md_end_match"

    if not (license_html_begin_found == license_html_end_found):
        # HTML licences tags are not mandatory
        license_html_error = True
        print "error: not both license_html_begin_match and license_html_end_match"

    if not (license_md_error or license_html_error):
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

for file_path in [license_md_path, contributors_path, version_txt_path]:
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
