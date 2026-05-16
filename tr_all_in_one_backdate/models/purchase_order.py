from odoo import _, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    backdate = fields.Datetime(string='Backdate', copy=False)
    backdate_remarks = fields.Char(string='Backdate Remarks', copy=False)

    def _is_backdate_enabled(self):
        return self.env['ir.config_parameter'].sudo().get_param('tr_backdate.purchase', False)

    def action_backdate_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Set Backdate'),
            'res_model': 'backdate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': 'purchase.order',
                'default_res_ids': self.ids,
            },
        }

    def button_confirm(self):
        res = super().button_confirm()
        for order in self:
            if order.backdate and self._is_backdate_enabled():
                order.write({
                    'date_order': order.backdate,
                    'date_approve': order.backdate,
                })
                if order.picking_ids:
                    order.picking_ids.write({'scheduled_date': order.backdate})
                    order.picking_ids.move_ids.write({'date': order.backdate})
        return res
