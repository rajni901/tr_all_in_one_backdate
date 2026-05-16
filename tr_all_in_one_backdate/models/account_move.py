from odoo import _, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    backdate = fields.Date(string='Backdate', copy=False)
    backdate_remarks = fields.Char(string='Backdate Remarks', copy=False)

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
                'default_current_date': self.invoice_date or self.date,
            },
        }

    def action_post(self):
        for move in self:
            if move.backdate:
                move.write({
                    'invoice_date': move.backdate,
                    'date': move.backdate,
                })
        return super().action_post()


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    backdate = fields.Date(string='Backdate', copy=False)
    backdate_remarks = fields.Char(string='Backdate Remarks', copy=False)

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
                'default_current_date': self.date,
            },
        }

    def action_post(self):
        for payment in self:
            if payment.backdate:
                payment.date = payment.backdate
        return super().action_post()
