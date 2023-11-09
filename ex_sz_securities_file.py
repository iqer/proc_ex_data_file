import re
import xml.etree.ElementTree as ET

from file import File
from log import logger

file_name = 'securities_20230708.xml'


class SZEXSecurityFile(File):
    def __init__(self, file_name):
        super().__init__(file_name)

    def _load_data_lines(self):
        tree = ET.parse(self.file_path)

        root = tree.getroot()
        element_list = []
        for child in root:

            security_id = child.find('SecurityID').text
            security_id_source = child.find('SecurityIDSource').text
            symbol = child.find('Symbol').text
            symbol_ex = child.find('SymbolEx').text
            english_name = child.find('EnglishName').text
            isin = child.find('ISIN').text
            udl_security_id = child.find('UnderlyingSecurityID').text
            udl_security_id_source = child.find('UnderlyingSecurityIDSource').text
            list_date = child.find('ListDate').text
            security_type = child.find('SecurityType').text
            currency = child.find('Currency').text
            qty_unit = child.find('QtyUnit').text
            day_trading = child.find('DayTrading').text
            prev_close_px = child.find('PrevClosePx').text
            security_status = child.find('SecurityStatus').text
            outstanding_share = child.find('OutstandingShare').text
            public_float_share_qty = child.find('PublicFloatShareQuantity').text
            par_value = child.find('ParValue').text
            gage_flag = child.find('GageFlag').text
            gage_ratio = child.find('GageRatio').text
            crd_buy_underlying = child.find('CrdBuyUnderlying').text
            crd_sell_underlying = child.find('CrdSellUnderlying').text
            price_check_mode = child.find('PriceCheckMode').text
            pledge_flag = child.find('PledgeFlag').text
            contract_multiplier = child.find('ContractMultiplier').text
            regular_share = child.find('RegularShare').text
            qualification_flag = child.find('QualificationFlag').text
            qualification_class = child.find('QualificationClass').text

            child_ele = {
                'SecurityID': security_id,
                'SecurityIDSource': security_id_source,
                'Symbol': symbol,
                'SymbolEx': symbol_ex,
                'EnglishName': english_name,
                'ISIN': isin,
                'UnderlyingSecurityID': udl_security_id,
                'UnderlyingSecurityIDSource': udl_security_id_source,
                'ListDate': list_date,
                'SecurityType': security_type,
                'Currency': currency,
                'QtyUnit': qty_unit,
                'DayTrading': day_trading,
                'PrevClosePx': prev_close_px,
                'SecurityStatus': security_status,
                'OutstandingShare': outstanding_share,
                'PublicFloatShareQuantity': public_float_share_qty,
                'ParValue': par_value,
                'GageFlag': gage_flag,
                'GageRatio': gage_ratio,
                'CrdBuyUnderlying': crd_buy_underlying,
                'CrdSellUnderlying': crd_sell_underlying,
                'PriceCheckMode': price_check_mode,
                'PledgeFlag': pledge_flag,
                'ContractMultiplier': contract_multiplier,
                'RegularShare': regular_share,
                'QualificationFlag': qualification_flag,
                'QualificationClass': qualification_class,
            }

            stock_param = child.find('StockParams')
            stock_param_ele = {}
            if stock_param:
                indus_classification = stock_param.find('IndustryClassification').text
                prev_year_profit_per_share = stock_param.find('PreviousYearProfitPerShare').text
                cur_year_profit_per_share = stock_param.find('CurrentYearProfitPerShare').text
                offering_flag = stock_param.find('OfferingFlag').text
                attribute = stock_param.find('Attribute').text
                no_profit = stock_param.find('NoProfit').text
                weighted_voting_rights = stock_param.find('WeightedVotingRights').text
                is_registration = stock_param.find('IsRegistration').text
                is_vie = stock_param.find('IsVIE').text
                stock_param_ele.update({
                    'IndustryClassification': indus_classification,
                    'PreviousYearProfitPerShare': prev_year_profit_per_share,
                    'CurrentYearProfitPerShare': cur_year_profit_per_share,
                    'OfferingFlag': offering_flag,
                    'Attribute': attribute,
                    'NoProfit': no_profit,
                    'WeightedVotingRights': weighted_voting_rights,
                    'IsRegistration': is_registration,
                    'IsVIE': is_vie,
                })

                tenderer = stock_param.find('TendererList')
                tenderer_ele = {}
                if tenderer:
                    tenderer_id = tenderer.find('TendererID').text
                    tenderer_name = tenderer.find('TendererName').text
                    offering_price = tenderer.find('OfferingPrice').text
                    begin_date = tenderer.find('BeginDate').text
                    end_date = tenderer.find('EndDate').text
                    tenderer_ele.update({
                        'TendererID': tenderer_id,
                        'TendererName': tenderer_name,
                        'OfferingPrice': offering_price,
                        'BeginDate': begin_date,
                        'EndDate': end_date,
                    })
                    stock_param_ele['TendererList'] = tenderer_ele
                child_ele['StockParams'] = stock_param_ele

            fund_param = child.find('FundParams')
            fund_param_ele = {}
            if fund_param:
                nav = fund_param.find('NAV').text
                fund_param_ele.update({
                    'NAV': nav,
                })
                child_ele['FundParams'] = fund_param_ele

            bond_param = child.find('BondParams')
            bond_param_ele = {}
            if bond_param:
                coupon_rate = bond_param.find('CouponRate').text
                issue_price = bond_param.find('IssuePrice').text
                interest = bond_param.find('Interest').text
                interest_accrual_date = bond_param.find('InterestAccrualDate').text
                maturity_date = bond_param.find('MaturityDate').text
                offering_flag = bond_param.find('OfferingFlag').text
                swap_flag = bond_param.find('SwapFlag').text
                putback_flag = bond_param.find('PutbackFlag').text
                putback_resell_flag = bond_param.find('PutbackResellFlag').text
                purpose_type = bond_param.find('PurposeType').text
                pricing_method = bond_param.find('PricingMethod').text
                bond_param_ele.update({
                    'CouponRate': coupon_rate,
                    'IssuePrice': issue_price,
                    'Interest': interest,
                    'InterestAccrualDate': interest_accrual_date,
                    'MaturityDate': maturity_date,
                    'OfferingFlag': offering_flag,
                    'SwapFlag': swap_flag,
                    'PutbackFlag': putback_flag,
                    'PutbackResellFlag': putback_resell_flag,
                    'PurposeType': purpose_type,
                    'PricingMethod': pricing_method,
                })
                child_ele['BondParams'] = bond_param_ele
            element_list.append(child_ele)
        self.data_lines = element_list

    def _check_data_lines(self):
        for line in self.data_lines:
            try:
                assert len(line['SecurityID']) <= 8

                assert line['SecurityIDSource'] == '102'
                assert len(line['SymbolEx']) <= 40
                assert len(line['EnglishName']) <= 40
                assert len(line['ISIN']) <= 12
                assert len(line['UnderlyingSecurityID']) <= 8
                assert len(line['UnderlyingSecurityIDSource']) <= 4
                assert len(line['ListDate']) == 8
                assert len(line['SecurityType']) <= 4
                assert len(line['Currency']) <= 4
                assert len(line['QtyUnit'].split('.')[-1]) == 2
                assert len(line['QtyUnit'].split('.')[0]) <= 12
                assert line['DayTrading'] in ['Y', 'N']
                assert len(line['PrevClosePx'].split('.')[0]) <= 8
                assert len(line['PrevClosePx'].split('.')[1]) == 4
                assert len(line['OutstandingShare'].split('.')[-1]) == 2
                assert len(line['OutstandingShare'].split('.')[0]) <= 15
                assert len(line['PublicFloatShareQuantity'].split('.')[-1]) == 2
                assert len(line['PublicFloatShareQuantity'].split('.')[0]) <= 15
                assert len(line['ParValue'].split('.')[-1]) == 4
                assert len(line['ParValue'].split('.')[0]) <= 8
                assert line['GageFlag'] in ['Y', 'N']
                assert len(line['GageRatio'].split('.')[-1]) == 2
                assert len(line['GageRatio'].split('.')[0]) <= 2
                assert line['CrdBuyUnderlying'] in ['Y', 'N']
                assert line['CrdSellUnderlying'] in ['Y', 'N']
                assert line['PriceCheckMode'] in ['0', '1', '2', '3', '4']
                assert line['PledgeFlag'] in ['Y', 'N']
                # if line['ContractMultiplier']:
                assert len(line['ContractMultiplier'].split('.')[-1]) == 4
                assert len(line['ContractMultiplier'].split('.')[0]) <= 1
                # if line['RegularShare']:
                assert len(line['RegularShare']) <= 8
                assert line['QualificationFlag'] in ['Y', 'N']
                assert line['QualificationClass'] in ['0', '1', '2']
            except Exception as e:
                import traceback
                error_message = traceback.format_exc()
                assert_pattern = r'assert .*\n'
                assert_message = re.search(assert_pattern, error_message).group().strip('\n')
                logger.warning(f"出错证券代码: {line['SecurityID']}, 错误表达式: {assert_message}")
                # raise

    def _proc_data_lines(self):
        pass

if __name__ == '__main__':
    file = SZEXSecurityFile(file_name)
    file.to_excel()
