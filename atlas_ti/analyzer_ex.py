# !/usr/bin/env python
# -*-coding: utf-8-*-


if __name__ == '__main__':

    p = __import__('atlas_ti_quotation_preprocess')
    a = __import__('analyzer')

    root = 'D:/work\JYS/data'

    quotation_path = '%s/quotations_20180209.txt' % root
    quotations, primary_docs, codes = p.load_data(quotation_path)

    print(len(quotations))

    a.code_error_check(quotations)

    disciplines = ['eco', 'law', 'pol', 'soc', 'psy']

    quotation_count, code_count, skipped = a.table_1(quotations, disciplines, ['Wrong Data', 'I-NA'])
    '''
    # 표 1
    for discipline in disciplines:
        print('%s\t%d\t%d\t' % (discipline, len(quotation_count[discipline]), sum(quotation_count[discipline].values())))


    skip_code_count = {}
    for discipline in skipped:
        skip_code_count[discipline] = defaultdict(lambda: 0)
        for p_name, q_id, code in skipped[discipline]:
            skip_code_count[discipline][code] += 1

    for discipline in sorted(skip_code_count):
        for code in sorted(skip_code_count[discipline]):
            print('%s\t%s\t%d' % (discipline, code, skip_code_count[discipline][code]))
    

    # 표 2
    table_2_position(quotation_count, '../data/person.txt', 7, ['조교수', '부교수', '교수'], disciplines)
    print()
    table_2_age(quotation_count, '../data/person.txt', 3, [30, 40, 50, 60], disciplines)
    print()
    table_2_gender(quotation_count, '../data/person.txt', 5, ['남', '여'], disciplines)

    
    
    # 표 3
    
    top10 = sorted(quotation_count[dp].items(), key=lambda x: (-x[1], x[0]))[:10]
    for idx in range(0, 10):
        row_items = []
        for dp in disciplines:
            p_name, value = top10[idx]
            p_id = p_name.replace('_', '').rstrip('.txt')
            row_items.append(p_id)
            row_items.append(value)
        print('\t'.join(row_items))
    
    # 표 4
    count = {}
    for dp in disciplines:
        count[dp] = {}
        for p_id in quotation_count[dp]:
            for q_id in quotations[p_id]:
                count[dp][(p_id, q_id)] = len(quotations[p_id][q_id].codes)
    top10 = sorted(count[dp].items(), key=lambda x: (-x[1], x[0][0], int(x[0][1])))[:10]
    for i in range(0, 10):
        row = ''
        for dp in disciplines:
            (p_name, q_id), value = top10[i]
            row += '\t%s-%s\t%d' % (p_name.replace('_', '').rstrip('.txt'), q_id, value)
        print(row.strip())
    
    
    
    # tweet count list
    for dp in sorted(quotation_count):
        for p_id, value in sorted(quotation_count[dp].items(), key=lambda x: -x[1]):
            print('%s\t%d' % (p_id.replace('_', '').rstrip('.txt'), value))
    '''

    '''
    # code count list
    for dp in sorted(code_count):
        for p_id, value in sorted(code_count[dp].items(), key=lambda x: -x[1]):
            print('%s\t%d' % (p_id.replace('_', '').rstrip('.txt'), value))
    '''
