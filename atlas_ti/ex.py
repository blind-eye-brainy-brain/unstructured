# !/usr/bin/env python
# -*- coding: utf-8 -*-

import glob


if __name__ == '__main__':

    p = __import__('atlas_ti_quotation_preprocess')
    e = __import__('atlas_ti_export')

    root = 'D:/work\JYS/data'

    quotation_path = '%s/quotations_20180131.txt' % root
    quotations, primary_docs, codes = p.load_data(quotation_path)

    print(len(quotations))

    discipline_prefixes = ['ECO', 'LAW', 'POL', 'PSY', 'SOC']

    # 지정한 코드와 주제분야 사이의 빈도 테이블
    code_prefixes = ['M-', 'M-MM-', 'M-PB-Book-', 'C-', 'P-', 'I-', 'I-GO-']
    for code_prefix in code_prefixes:
        table_output_path = '%s/table/%s_by_DP_result.txt' % (root, code_prefix)
        table = e.prefix_code_by_discipline(quotations, table_output_path, discipline_prefixes, code_prefix)

    # table 에서 SPSS 형식으로 변환
    for table_path in glob.glob('%s/table/*' % root):
        fname = table_path.split('\\')[-1]
        spss_path = '%s/spss/%s' % (root, fname)
        if fname.startswith('M-PB-Book-'):
            prefix = 'M-PB-Book-'
        else:
            prefix = None
        e.convert_matrix_to_spss(table_path, spss_path, delimiter='\t', start_idx=2, header=True, prefix=prefix)

    '''
    # 소주제분야와 나머지 코드 사이의 빈도 테이블
    person_path = '%s/persons.txt' % root
    for discipline_prefix in discipline_prefixes:
        table_output_path = 'table/sub_discipline_by_codes_%s.txt' % discipline_prefix
        e.sub_discipline_by_others(quotations, codes, person_path, table_output_path, discipline_prefix)
    '''




    # 기타 함수
    '''
    # 지정한 코드와 P_document 사이의 빈도 테이블
    code_prefix = 'M-PB-Book-'
    table_output_path = '../table/%s_by_PD_result.txt' % code_prefix
    e.prefix_code_by_primary_doc(quotations, primary_docs, table_output_path, code_prefix)
    '''
