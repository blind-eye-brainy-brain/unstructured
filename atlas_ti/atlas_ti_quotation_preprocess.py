# !/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from collections import namedtuple

QUOTATION = namedtuple('quotation', 'codes text')


def load_data(path):
    """load data file that was exported all quotations into .rft format by atlas.ti"""
    id_regex = '^P\s*\d+?: (.*?) - \d+:(\d+)'
    codes_regex = '^Codes:\t(.*?)$'
    code_regex = '\[(.*?)\]'

    data = {}
    primary_doc_names = set()
    unique_codes = set()
    primary_doc_name = quotation_id = code_list = None

    fr = open(path, 'r', encoding='utf8')
    for line in fr:
        line = line.strip()
        if any(line):
            id_obj = re.match(id_regex, line)
            codes_obj = re.match(codes_regex, line)
            if id_obj is not None:
                primary_doc_name = id_obj.group(1).rstrip('.txt')
                primary_doc_names.add(primary_doc_name)
                quotation_id = id_obj.group(2)
            elif codes_obj is not None:
                code_list = re.findall(code_regex, codes_obj.group(1))
                unique_codes.update(code_list)
            elif line is not 'No memos':
                try:
                    data[primary_doc_name][quotation_id] = QUOTATION(codes=code_list, text=line)
                except KeyError:
                    data[primary_doc_name] = {}
                    data[primary_doc_name][quotation_id] = QUOTATION(codes=code_list, text=line)
    fr.close()
    primary_doc_names = sorted(primary_doc_names, key=lambda x: (x.split('_')[0], int(x.split('_')[1])))
    unique_codes = sorted(unique_codes)
    return data, primary_doc_names, unique_codes


def annotate_according_to_primary_doc(path, data, skip_list):
    """edit data according to primary document"""
    subjects = {}
    fr = open(path, 'r')
    for line in fr:
        line = map(str.strip, line.split('\t'))
        subjects[line[0].lower()] = line[1]
    fr.close()
    for primary_doc_name in data:
        for quotation_id in data[primary_doc_name]:
            if not any(x in data[primary_doc_name][quotation_id].codes for x in skip_list):
                data[primary_doc_name][quotation_id].codes.append(subjects[primary_doc_name.lower().replace('_', '')])
    return data
