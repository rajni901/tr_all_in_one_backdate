from odoo import _, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    backdate = fields.Datetime(string='Backdate', copy=False)
    backdate_remarks = fields.Char(string='Backdate Remarks', copy=False)

    def _is_backdate_enabled(self):
        return self.env['ir.config_parameter'].sudo().get_param('tr_backdate.sale', False)

    def action_backdate_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Set Backdate'),
            'res_model': 'backdate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': 'sale.order',
                'default_res_ids': self.ids,
            },
        }

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order.backdate and self._is_backdate_enabled():
                order.date_order = order.backdate
                if order.picking_ids:
                    order.picking_ids.write({
                        'scheduled_date': order.backdate,
                    })
                    order.picking_ids.move_ids.write({'date': order.backdate})
        return res
