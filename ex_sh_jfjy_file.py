from xml.dom.minidom import parseString

import pandas as pd

from tools import to_excel_autowidth_and_border


def main():
    content = open('./上交所数据文件/jfjy20230708.xml', encoding='gbk').read()
    dom = parseString(content)
    root = dom.documentElement

    element_list = []
    child_ele = {}
    for child in root.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            if child.tagName == 'Non_Trd_Rec':
                child_ele = {}
            for subchild in child.childNodes:
                if subchild.nodeType == subchild.ELEMENT_NODE:
                    child_ele[subchild.tagName] = subchild.firstChild.nodeValue
        if child_ele:
            element_list.append(child_ele)
            child_ele = {}
    valid_data_lines(element_list)


def valid_data_lines(data_lines):
    # ETF实物/黄金申赎
    etf_goods_gold_list = []
    # ETF现金申赎
    etf_cash_list = []
    for line in data_lines:
        inst_id = line['Inst_ID']
        assert len(inst_id) == 6
        inst_name = line['Inst_Nam']
        assert len(inst_name.encode('gbk')) == 8
        busi_typ = line['Busi_Typ']
        assert busi_typ in ['IEC', 'IER', 'GEC', 'GER', 'EEC', 'EER']

        if busi_typ in ['IEC', 'IER', 'GEC', 'GER']:
            item = [inst_id, inst_name, busi_typ]
            etf_goods_gold_list.append(item)
        elif busi_typ in ['EEC', 'EER']:
            crea_rtgs_tag = line['Crea_Rtgs_Tag']
            if busi_typ == 'EEC':
                assert crea_rtgs_tag in ['0', '1']
            else:
                assert len(crea_rtgs_tag) == 1
            item = [inst_id, inst_name, busi_typ, crea_rtgs_tag]
            etf_cash_list.append(item)

    dump_data_to_excel(etf_goods_gold_list, etf_cash_list)


def dump_data_to_excel(etf_goods_gold_list, etf_cash_list):
    writer = pd.ExcelWriter(FILE_NAME, engine='xlsxwriter')
    df = pd.DataFrame(etf_goods_gold_list, columns=[
        '证券代码',
        '证券简称',
        '业务类型',
    ])
    to_excel_autowidth_and_border(writer, df, sheetname='ETF实物黄金申赎', startrow=0, startcol=0)
    df = pd.DataFrame(etf_cash_list, columns=[
        '证券代码',
        '证券简称',
        '业务类型',
        'RTGS申购标志',
    ])
    to_excel_autowidth_and_border(writer, df, sheetname='ETF现金申赎', startrow=0, startcol=0)

    writer.close()


FILE_NAME = 'jfjy20230708.xlsx'

if __name__ == '__main__':
    main()
