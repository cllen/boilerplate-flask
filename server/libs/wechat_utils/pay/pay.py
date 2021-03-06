#coding:utf8
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



from ._pay_helper import WeixinPay,build_pay_sign
import time


def pay(
        appid,
        mch_id,
        partner_key,
        
        body,
        openid,
        total_fee,
        notify_url,
        out_trade_no
    ):

    # 创建支付对象
    wxpay = WeixinPay(
        appid=appid,                # 小程序id
        mch_id=mch_id,              # 商户号
        partner_key=partner_key     # 商户支付秘钥
    )

    # 获取支付结果
    unified_order = wxpay.unifiedorder(
        body=body,                  # 支付备注
        openid=openid,              # 支付用户openid
        total_fee=total_fee,        # 支付价格
        notify_url=notify_url,      # 支付结果通知接口
        out_trade_no=out_trade_no   # 支付记录id
    )

    logger.info('>>> wxpay.unifiedorder')
    logger.info(unified_order)

    #
    # 初步处理支付结果
    #

    # 时间戳
    time_stamp = str(int(time.time()))

    """

        unified_order['return_code']的值为：'SUCCESS','PRDERPAID'，根据这个值判断支付结果，然后修改业务数据，如订单状态。
        data_for_frontend: 将这些数据返回给前端。
        参考微信支付文档：https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter3_5_4.shtml

    """
    return {
        'return_code':unified_order.get('return_code'),#SUCCESS,PRDERPAID
        'err_code':unified_order.get('err_code'),#PRDERPAID
        'unified_order':unified_order,
        'data_for_frontend':{
            'time_stamp':time_stamp,
            'nonce_str':unified_order['nonce_str'],
            'prepay_id':unified_order['prepay_id'],
            'sign':build_pay_sign(
                appid,
                unified_order['nonce_str'],
                unified_order['prepay_id'],
                time_stamp,
                partner_key
            ),
        },
    }



import xml.etree.ElementTree as ET
def xml_to_dict(xml_data):
    '''
    xml to dict
    :param xml_data:
    :return:
    '''
    xml_dict = {}
    root = ET.fromstring(xml_data)
    for child in root:
        xml_dict[child.tag] = child.text
    return xml_dict


