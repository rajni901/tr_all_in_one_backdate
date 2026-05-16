from odoo import _, fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    backdate = fields.Date(string='Backdate', copy=False, tracking=True)
    backdate_remarks = fields.Char(string='Backdate Remarks', copy=False)

    def _is_backdate_enabled(self):
        return self.env['ir.config_parameter'].sudo().get_param('tr_backdate.payment', False)

    def action_backdate_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Set Backdate'),
            'res_model': 'backdate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': 'account.payment',
                'default_res_ids': self.ids,
                'default_is_date': True,
            },
        }

    def action_post(self):
        for payment in self:
            if payment.backdate and self._is_backdate_enabled():
                payment.date = payment.backdate
        return super().action_post()
