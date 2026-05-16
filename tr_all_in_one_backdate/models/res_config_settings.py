from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    backdate_sale = fields.Boolean(
        string='Sale Order Backdate',
        config_parameter='tr_backdate.sale',
    )
    backdate_purchase = fields.Boolean(
        string='Purchase Order Backdate',
        config_parameter='tr_backdate.purchase',
    )
    backdate_invoice = fields.Boolean(
        string='Invoice / Bill Backdate',
        config_parameter='tr_backdate.invoice',
    )
    backdate_payment = fields.Boolean(
        string='Payment Backdate',
        config_parameter='tr_backdate.payment',
    )
    backdate_inventory = fields.Boolean(
        string='Inventory / Picking Backdate',
        config_parameter='tr_backdate.inventory',
    )
    backdate_remarks_required = fields.Boolean(
        string='Remarks Mandatory',
        config_parameter='tr_backdate.remarks_required',
        help='If enabled, users must enter remarks when assigning a backdate.',
    )
