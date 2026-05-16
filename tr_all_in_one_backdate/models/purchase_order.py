from odoo import _, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    backdate = fields.Datetime(string='Backdate', copy=False)
    backdate_remarks = fields.Char(string='Backdate Remarks', copy=False)

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
                'default_current_date': self.date_order,
            },
        }

    def button_confirm(self):
        res = super().button_confirm()
        for order in self:
            if order.backdate:
                order.write({
                    'date_order': order.backdate,
                    'date_approve': order.backdate,
                })
                order.picking_ids.write({
                    'scheduled_date': order.backdate,
                    'date_done': order.backdate,
                })
                order.picking_ids.move_ids.write({'date': order.backdate})
        return res
