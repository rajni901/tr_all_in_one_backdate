from odoo import _, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

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
                'default_model': 'stock.picking',
                'default_res_ids': self.ids,
                'default_current_date': self.scheduled_date,
            },
        }

    def button_validate(self):
        for picking in self:
            if picking.backdate:
                picking.write({
                    'scheduled_date': picking.backdate,
                    'date_done': picking.backdate,
                })
                picking.move_ids.write({'date': picking.backdate})
                picking.move_ids.move_line_ids.write({'date': picking.backdate})
        return super().button_validate()
