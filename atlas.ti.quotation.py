# !/usr/bin/env python
# -*- coding: utf-8 -*-


import re

RE_ID = '^P.*?: (.*?) - \d+:(\d+)'
RE_CODES = '^Codes:\t(.*?)$'
RE_CODE = '\[(.*?)\]'

quotation_txt = {}
code_info = {}
p_file = quotation_id = codes = None

fr = open('data/quotations.txt', 'r')
for line in fr:
    line = line.strip()
    if any(line):
        id_obj = re.match(RE_ID, line)
        codes_obj = re.match(RE_CODES, line)
        if id_obj is not None:
            p_file = id_obj.group(1).rstrip('.txt').replace('_', '')
            quotation_id = id_obj.group(2)
        elif codes_obj is not None:
            codes = re.findall(RE_CODE, codes_obj.group(1))
            try:
                code_info[p_file][quotation_id] = codes
            except KeyError:
                code_info[p_file] = {}
                code_info[p_file][quotation_id] = codes
        elif line is not 'No memos':
            quotation_txt[p_file] = line
fr.close()

subjects = {}
fr = open('data/subject_list.txt', 'r')
for line in fr:
    line = map(str.strip, line.split('\t'))
    subjects[line[0].lower()] = line[1]
fr.close()

print len(sorted(code_info.keys()))
print len(quotation_txt)
for p_file in code_info:
    for quotation_id in code_info[p_file]:
        if 'NA' not in code_info[p_file][quotation_id] and 'NO DATA' not in code_info[p_file][quotation_id]:
            code_info[p_file][quotation_id].append(subjects[p_file])
