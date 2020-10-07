"""Part of odoo. See LICENSE file for full copyright and licensing details."""
import functools
import logging
from datetime import timedelta
import pytz
from odoo import http,fields, _
from ..common import (invalid_response,valid_response)
from odoo.http import request

_logger = logging.getLogger(__name__)


def validate_token(func):
    """."""
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        """."""
        access_token = request.httprequest.headers.get("access_token")
        if not access_token:
            return invalid_response("Access Token Not Found","Missing access token in request header",401)
        access_token_data = (
            request.env["api.access.token"]
            .sudo()
            .search([("token", "=", access_token)], order="id DESC", limit=1)
        )

        if (access_token_data.find_one_or_create_token(user_id=access_token_data.user_id.id)!= access_token):
            return invalid_response("Access Token", "Token seems to have expired or invalid", 401)
        request.session.uid = access_token_data.user_id.id
        request.uid = access_token_data.user_id.id
        return func(self, *args, **kwargs)
    return wrap


_routes = ["/api/<model>", "/api/<model>/<id>", "/api/<model>/<id>/<action>"]
store_mapping_1 = "restful.store_mapping_1"
store_mapping_2 = "restful.store_mapping_2"

class APIController(http.Controller):
    """."""
    status_name_to_id = {'draft': 1, 'cancel': 2, 'paid': 3, 'done': 4, 'invoiced': 5, 'partial_payment': 6}

    def __init__(self):
        self._model = "ir.model"
    def format_date(self,date):
        date=fields.Date.from_string(date).strftime("%Y-%m-%d")
        return date

    def get_sale_details(self, date_start=False, date_stop=False,model='pos.order', configs_id=0):
        try:
            user_tz = pytz.timezone(request.env.context.get('tz') or request.env.user.tz or 'UTC')
            today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(request)))
            today = today.astimezone(pytz.timezone('UTC'))
            if date_start:
                date_start = fields.Datetime.from_string(date_start)
            else:
                # start by default today 00:00:00
                date_start = today

            if date_stop:
                # set time to 23:59:59
                date_stop = fields.Datetime.from_string(date_stop)
            else:
                # stop by default today 23:59:59
                date_stop = today + timedelta(days=1, seconds=-1)

            date_start = fields.Datetime.to_string(date_start)
            date_stop = fields.Datetime.to_string(date_stop)
            # avoid a date_stop smaller than date_start
            date_stop = max(date_stop, date_start)
            user_currency = request.env.user.company_id.currency_id
            orders = request.env[model].sudo().search([
                ('date_order', '>=', date_start),
                ('date_order', '<=', date_stop),
                ('config_id', '=', configs_id)])
            data = []
            for order in orders:
                st_line_ids = request.env["account.bank.statement.line"].search(
                    [('pos_statement_id', '=', order.id)]).ids
                if st_line_ids:
                    request.env.cr.execute("""
                                                SELECT aj.id as "PaymentMethodId",sum(amount) as "Dollar", 0.00 as "Riel"
                                                FROM account_bank_statement_line AS absl,
                                                     account_bank_statement AS abs,
                                                     account_journal AS aj
                                                WHERE absl.statement_id = abs.id
                                                    AND abs.journal_id = aj.id
                                                    AND absl.id IN %s
                                                GROUP BY aj.name,aj.id
                                            """, (tuple(st_line_ids),))
                    payments = request.env.cr.dictfetchall()
                else:
                    payments = []

                sub_total = order.amount_total - order.amount_tax
                # convert pricelist to discount amount
                discount_dollar = 0.00
                pricelist_items = order.pricelist_id.item_ids
                if len(pricelist_items) == 1:
                    if pricelist_items[0].compute_price == 'percentage':
                        percentage = pricelist_items[0].percent_price
                        if percentage == 100:
                            discount_dollar = order.amount_total
                        else:
                            discount_dollar = (order.amount_total / ((100 - percentage) / 100)) - order.amount_total
                if discount_dollar != 0:
                    discount_details = [{
                        "DiscountDollar": discount_dollar,
                        "DiscountRiel": 0.00,
                        "DiscountTypeID": 1
                    }]
                else:
                    discount_details = []
                data.append({
                    "TransactionID": order.display_name,
                    "InvoiceID": order.pos_reference,
                    "ReceiptID": order.pos_reference,
                    "Date": self.format_date(order.date_order),
                    "StartTime": order.create_date,
                    "EndTime": order.write_date,
                    "NumberOfCustomer": order.customer_count,
                    "SubTotal": sub_total,
                    "ReturnAmount": 0.00,
                    "RefundAmount": 0.00,
                    "Vat": order.amount_tax,
                    "Net": sub_total,
                    "GrandTotal": order.amount_total,
                    "PaymentDollar": order.amount_paid,
                    "PaymentRiel": 0.00,
                    "DiscountDetails": discount_details,
                    "ChangeDollar": 0.00,
                    "ChangeRiel": 0.00,
                    "PaymentDetails": payments,
                    "Cashier": order.user_id.name,
                    "StatusId": self.status_name_to_id[order.state],
                    "Comment": '' if order.note == False else order.note,
                    "Currency": "%s %s" % (all([order.currency_id.name, order.currency_id.currency_unit_label]) and (
                    order.currency_id.name, order.currency_id.currency_unit_label) or (
                                           user_currency.name, user_currency.currency_unit_label)),
                    "ExchangeRate": ("exchange_rate" in order and order.exchange_rate) or 0.00,
                    "PLT": 0.00,
                })
            if data:
                return valid_response(data, 200)
            else:
                return invalid_response(
                    "Not Found",
                    "Record not found!",
                    404,
                )
        except Exception as e:
            info = e
            error = "ERROR"
            _logger.error(info)
            return invalid_response(error, info,400)
    @http.route('/api/get_pos_data', type="http", auth="none", methods=["GET"], csrf=False)
    @validate_token
    def get_pos_data_v1(self, model=None, **payload):
        ioc_name = model
        session = {
                    '90ec4424-5209-11ea-8d77-2e728ce88125': request.env.ref(store_mapping_1, raise_if_not_found=False) and int(request.env.ref(store_mapping_1, raise_if_not_found=False).sudo().value),
                    '0c20a123-cb03-445d-8521-2d320ce3305d': request.env.ref(store_mapping_2, raise_if_not_found=False) and int(request.env.ref(store_mapping_2, raise_if_not_found=False).sudo().value)
                }
        params = ["store_code", "StartTime", "EndTime"]
        params = {key: payload.get(key) for key in params if payload.get(key)}
        store_code, start_time, end_time = (params.get("store_code"), params.get("StartTime"), params.get("EndTime"))
        if not store_code:
            return invalid_response(
                "Missing error",
                "Parameter 'store_code' parameter is missing store code is uuid!",
                400,
            )
        elif not store_code in session:
            return invalid_response(
                "Missing error",
                "Store=%s is not exist!"%store_code,
                400,
            )
        if not all([store_code, start_time, end_time]):
            return invalid_response(
                "Missing error",
                "Either of the following are missing [store_code,StartTime,EndTime]",
                400,
            )

        model = request.env[self._model].sudo().search([("model", "=", 'pos.order')], limit=1)
        if model:
            return self.get_sale_details(start_time,end_time,configs_id=session[store_code])
        return invalid_response(
            "Invalid object model",
            "The model %s is not available in the registry." % ioc_name,
        )