from odoo import _, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    backdate = fields.Date(string='Backdate', copy=False)
    backdate_remarks = fields.Char(string='Backdate Remarks', copy=False)

    def _is_backdate_enabled(self):
        return self.env['ir.config_parameter'].sudo().get_param('tr_backdate.invoice', False)

    def action_backdate_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Set Backdate'),
            'res_model': 'backdate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': 'account.move',
                'default_res_ids': self.ids,
                'default_is_date': True,
            },
        }

    def action_post(self):
        for move in self:
            if move.backdate and self._is_backdate_enabled():
                move.write({
                    'invoice_date': move.backdate,
                    'date': move.backdate,
                })
        return super().action_post()
