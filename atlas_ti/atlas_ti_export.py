# !/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from scipy.stats.stats import pearsonr


# prefix_code_by_primary_doc(quotations, primary_docs, 'result/book_PD.txt', 'M-PB-Book-')
def prefix_code_by_primary_doc(data, primary_doc_names, output, prefix):
    """frequency matrix : prefix_codes X primary_doc"""
    matrix = {}
    for primary_doc_name in data:
        for quotation_id in data[primary_doc_name]:
            for code in data[primary_doc_name][quotation_id].codes:
                if code.startswith(prefix):
                    try:
                        matrix[code][primary_doc_name] += 1
                    except KeyError:
                        matrix[code] = defaultdict(lambda: 0)
                        matrix[code][primary_doc_name] += 1

    with open(output, 'w', encoding='utf8') as out:
        out.write('\t%s\n' % '\t'.join(primary_doc_names))
        for code in sorted(matrix):
            row = code
            for primary_doc_name in primary_doc_names:
                row += '\t%d' % matrix[code][primary_doc_name]
            out.write(row + '\n')
    return matrix


# prefix_code_by_discipline(quotations, 'result/book_DP.txt', ['ECO', 'LAW', 'POL', 'PSY', 'SOC'], 'M-PB-Book-')
def prefix_code_by_discipline(data, output_path, primary_doc_prefixes, code_prefix):
    """frequency matrix : prefix_codes X prefix_primary_document"""
    matrix = {}
    for primary_doc_name in data:
        for primary_doc_prefix in primary_doc_prefixes:
            if primary_doc_name.upper().startswith(primary_doc_prefix):
                for quotation_id in data[primary_doc_name]:
                    for code in data[primary_doc_name][quotation_id].codes:
                        if code.startswith(code_prefix):
                            try:
                                matrix[code][primary_doc_prefix] += 1
                            except KeyError:
                                matrix[code] = defaultdict(lambda: 0)
                                matrix[code][primary_doc_prefix] += 1
    with open(output_path, 'w', encoding='utf8') as out:
        out.write('CODE NAME\tTOTAL\t%s\n' % '\t'.join(primary_doc_prefixes).upper())
        for code in sorted(matrix):
            row = '%s\t%d' % (code, sum(matrix[code].values()))
            for primary_doc_prefix in primary_doc_prefixes:
                row += '\t%d' % matrix[code][primary_doc_prefix]
            out.write(row + '\n')
    return matrix


# pearson_from_frequency_matrix({'code1':{'ECO':1, 'LAW':2}...},...}, 'result/pearson_result.txt', 3)
def pearson_from_frequency_matrix(data, output_path, threshold=0):
    selected_code = []
    for code in data:
        if sum(data[code].values()) >= threshold:
            selected_code.append(code)
    selected_code.sort()
    with open(output_path, 'w', encoding='utf8') as out:
        for idx, left_code in enumerate(selected_code):
            for right_code in selected_code[idx + 1:]:
                r_score, p_value = pearsonr(data[left_code].values(), data[right_code].values())
                out.write('%s\t%s\t%.4f\n' % (left_code, right_code, r_score))


# sub_discipline_by_others(quotations, unique_codes, 'data/person.txt', 'result/sub_discipline_by_codes_ECO.txt', 'ECO')
def sub_discipline_by_others(data, unique_codes, input_path, output_path, prefix):
    count = {}
    subjects = set()
    subject_info = {}
    with open(input_path, 'r') as fr:
        for line in fr:
            line = map(str.strip, line.split('\t'))
            subject_info[line[0]] = line[2]
    for primary_doc_name in data:
        pid = primary_doc_name.replace('_', '').upper()
        if pid.startswith(prefix):
            subject = subject_info[pid]
            subjects.add(subject)
            for quotation_id in data[primary_doc_name]:
                for code in data[primary_doc_name][quotation_id].codes:
                    try:
                        count[subject][code] += 1
                    except KeyError:
                        count[subject] = defaultdict(lambda: 0)
                        count[subject][code] += 1
    subjects = sorted(subjects)
    with open(output_path, 'w', encoding='utf8') as out:
        out.write('SUBJECT\tTOTAL\t%s\n' % '\t'.join(unique_codes))
        for subject in subjects:
            row = '%s\t%d' % (subject, sum(count[subject].values()))
            for code in unique_codes:
                row += '\t%d' % count[subject][code]
            out.write(row + '\n')


def convert_matrix_to_spss(input_path, output_path, delimiter, start_idx, header=True, prefix=None):
    lines = [line.strip() for line in open(input_path, 'r', encoding='utf8').readlines()]
    sps = open(output_path.rsplit('.')[0] + '_sps.sps', 'w')
    sps.write('*Encoding: UTF - 8.\n'
              '/* CSV 파일 불러오기 */\n'
              'GET DATA / TYPE = TXT\n'
              '/ FILE = "%s"\n'
              '/ DELCASE = LINE\n'
              '/ DELIMITERS = "\\t"\n'
              '/ ARRANGEMENT = DELIMITED\n'
              '/ FIRSTCASE = 2\n'
              '/ VARIABLES =\n'
              'row_label A50\n'
              'row_idx F4.0\n'
              'col_idx F4.0\n' % output_path)
    col_lst_idx = 0
    if header:
        sps.write('/* 열 인덱스에 대한 레이블 적용 */\n')
        sps.write('VAL LAB col_idx\n')
        for i, label in enumerate([item.strip() for item in lines[0].split(delimiter)][start_idx:]):
            col_lst_idx = i
            sps.write('%d\'%s\'\n' % (i, label))
        sps.write('.\n')
        lines = lines[1:]
    csv = open(output_path, 'w', encoding='utf8')
    csv.write('%s\t%s\t%s\n' % ('row_label', 'row_idx', 'col_idx'))
    row_idx = row_lst_idx = 0
    sps.write('/* 행 인덱스에 대한 레이블 적용 */\n')
    sps.write('VAL LAB row_idx\n')
    for line in lines:
        if line.strip():
            line = line.split(delimiter)
            row_lst_idx = row_idx
            sps.write('%d\'%s\'\n' % (row_idx, line[0].lstrip(prefix)))
            for col_idx, freq in enumerate(line[start_idx:]):
                for i in range(int(freq)):
                    csv.write('%s\t%d\t%d\n' % (line[0], row_idx, col_idx))
        row_idx += 1
    csv.close()
    sps.write('.\n')
    sps.write('/* 대응일치 명령문 */\n')
    sps.write('CORRESPONDENCE TABLE=row_idx(0 %d) BY col_idx(0 %d)\n' % (row_lst_idx, col_lst_idx))
    sps.write('/DIMENSIONS=2\n')
    sps.write('/MEASURE=CHISQ\n')
    sps.write('/STANDARDIZE=RCMEAN\n')
    sps.write('/NORMALIZATION=SYMMETRICAL\n')
    sps.write('/PRINT=TABLE RPOINTS CPOINTS RPROFILES CPROFILES\n')
    sps.write('/PLOT=NDIM(1,MAX) BIPLOT(20) RPOINTS(20) CPOINTS(20)\n')
    sps.write('.\n')
    sps.close()


def write_primary_doc_by_code(data, primary_doc_names, unique_codes, output):
    """write count matrix : primary document X code"""
    with open(output, 'w', encoding='utf8') as fw:
        fw.write('\t%s\n' % '\t'.join(unique_codes))
        for primary_doc_name in primary_doc_names:
            counter = defaultdict(lambda: 0)
            row = primary_doc_name
            for quotation_id in data[primary_doc_name]:
                for code in data[primary_doc_name][quotation_id].codes:
                    counter[code] += 1
            for code in unique_codes:
                row += '\t%d' % counter[code]
            fw.write(row + '\n')


# private function #1
def write_count_quotation_of_selected_codes(data, codes, output):
    counter = defaultdict(lambda: 0)
    for primary_doc_name in data:
        for quotation_id in data[primary_doc_name]:
            for code in data[primary_doc_name][quotation_id].codes:
                for selected_code in codes:
                    if code.startswith(selected_code):
                        counter[selected_code] += 1
    with open(output, 'w', encoding='utf8') as out:
        for code in codes:
            out.write('%s\t%d\n' % (code, counter[code]))


def write_count_subject(data, output):
    p_counter = defaultdict(lambda: 0)
    for primary_doc_name in data:
        p_counter[primary_doc_name.split('_')[0]] += 1
    with open(output, 'w', encoding='utf8') as out:
        for subject in sorted(p_counter):
            out.write('%s\t%d\n' % (subject, p_counter[subject]))


def write_count_code(data, output, r):
    counter = defaultdict(lambda: 0)
    for primary_doc_name in data:
        for quotation_id in data[primary_doc_name]:
            for code in data[primary_doc_name][quotation_id].codes:
                counter[code] += 1
    order = map(lambda x: x.strip(), open(r, 'r').readlines())
    with open(output, 'w', encoding='utf8') as out:
        for code in order:
            if any(code):
                re = code.split(';')[0].strip()
            out.write('%s\t%d\n' % (re, counter[re]))
