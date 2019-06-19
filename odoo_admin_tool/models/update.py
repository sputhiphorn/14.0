# -*- coding: utf-8 -*-
import datetime

from ast import literal_eval
from odoo import api, fields, models, _
from odoo.tools import misc



class PublisherWarrantyContract(models.AbstractModel):
    _inherit = "publisher_warranty.contract"

    @api.model
    def _get_sys_logs(self):
        defult_experire=datetime.datetime.now()+ datetime.timedelta(days=365) # format:'2019-02-28 03:13:27'
        text = "{'messages': [], 'contracts': [], 'enterprise_info': {'enterprise_code': False, 'expiration_date':'"+defult_experire.strftime("%Y-%m-%d %H:%M:%S")+"'}}"
        return literal_eval(text)
