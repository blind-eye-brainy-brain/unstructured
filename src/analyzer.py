# !/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import atlas_ti_quotation_preprocess as quotation_count
import atlas_ti_export as e


def table_1(data, items, skip_codes):
    quotation_counter = {}
    code_counter = {}
    skip_info = {}
    for item in items:
        quotation_counter[item] = defaultdict(lambda: 0)
        code_counter[item] = defaultdict(lambda: 0)
        skip_info[item] = []
    for p_id in sorted(data):
        p_prefix = p_id[:3]
        for q_id in sorted(data[p_id], key=int):
            is_skip = False
            for code in sorted(data[p_id][q_id].codes):
                if code in skip_codes:
                    skip_info[p_prefix].append((p_id, q_id, code))
                    is_skip = True
                else:
                    code_counter[p_prefix][code] += 1
            if not is_skip:
                quotation_counter[p_prefix][p_id] += 1
    return quotation_counter, code_counter, skip_info


def table_2_position(data, input_path, idx, row_labels, col_labels):
    persons = {}
    with open(input_path, 'r', encoding='utf8') as fr:
        for line in fr:
            line = line.strip().split('\t')
            persons[line[0]] = line[1:]

    counter = {}
    for discipline in data:
        for p_name in data[discipline]:
            p_id = p_name.replace('_', '').rstrip('.txt').upper()
            try:
                counter[discipline][persons[p_id][idx]] += 1
            except KeyError:
                counter[discipline] = defaultdict(lambda: 0)
                counter[discipline][persons[p_id][idx]] += 1

    for row_label in row_labels:
        row_txt = ''
        for col_label in col_labels:
            count = counter[col_label][row_label]
            ratio = float(counter[col_label][row_label]) / sum(counter[discipline].values()) * 100
            row_txt += '%d\t(%.1f)\t' % (count, ratio)
        print(row_txt.strip())


def table_2_age(data, input_path, idx, row_labels, col_labels):
    persons = {}
    with open(input_path, 'r', encoding='utf8') as fr:
        for line in fr:
            line = line.strip().split('\t')
            persons[line[0]] = line[1:]

    counter = {}
    for discipline in data:
        for p_name in data[discipline]:
            p_id = p_name.replace('_', '').rstrip('.txt').upper()
            age = (118 - int(persons[p_id][idx])) // 10 * 10
            try:
                counter[discipline][age] += 1
            except KeyError:
                counter[discipline] = defaultdict(lambda: 0)
                counter[discipline][age] += 1

    for row_label in row_labels:
        row = ''
        for col_label in col_labels:
            count = counter[col_label][row_label]
            ratio = float(counter[col_label][row_label]) / sum(counter[col_label].values()) * 100
            row += '%d\t(%.1f)\t' % (count, ratio)
        print(row.strip())


def table_2_gender(p_list, input_path, idx, row_labels, col_labels):
    persons = {}
    with open(input_path, 'r', encoding='utf8') as fr:
        for line in fr:
            line = line.strip().split('\t')
            persons[line[0]] = line[1:]

    counter = {}
    for discipline in p_list:
        for p_name in p_list[discipline]:
            p_id = p_name.replace('_', '').rstrip('.txt').upper()
            try:
                if persons[p_id][idx] == '':
                    counter[discipline]['남'] += 1
                else:
                    counter[discipline][persons[p_id][idx]] += 1
            except KeyError:
                counter[discipline] = defaultdict(lambda: 0)
                if persons[p_id][idx] == '':
                    counter[discipline]['남'] += 1
                else:
                    counter[discipline][persons[p_id][idx]] += 1

    for row_label in row_labels:
        row_txt = ''
        for col_label in col_labels:
            count = counter[col_label][row_label]
            ratio = float(counter[col_label][row_label]) / sum(counter[col_label].values()) * 100
            row_txt += '%d\t(%.1f)\t' % (count, ratio)
        print(row_txt.strip())


def code_error_check(data):
    points = ['M', 'C', 'P', 'I']
    skips = ['Wrong Data', 'I-NA']
    for p_id in sorted(data):
        for q_id in sorted(data[p_id], key=int):
            count = {}
            for code in data[p_id][q_id].codes:
                point = code.split('-')[0].strip()
                count[point] = code
            if sorted(count.keys()) != sorted(points):
                if (len(count) != 1) or (list(count.values())[0] not in skips):
                    print('%s\t%s\t%s' % (p_id, q_id, data[p_id][q_id].codes))


