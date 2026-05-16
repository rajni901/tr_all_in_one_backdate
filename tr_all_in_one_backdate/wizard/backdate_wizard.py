import ast

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class BackdateWizard(models.TransientModel):
    _name = 'backdate.wizard'
    _description = 'Assign Backdate'

    model = fields.Char(string='Model', readonly=True)
    res_ids = fields.Char(string='Record IDs', readonly=True)
    is_date = fields.Boolean(default=False)
    backdate = fields.Date(string='Backdate', default=fields.Date.today)
    backdate_datetime = fields.Datetime(string='Backdate', default=fields.Datetime.now)
    remarks = fields.Char(string='Remarks', placeholder='Reason for backdate...')
    remarks_required = fields.Boolean(compute='_compute_remarks_required')

    @api.depends()
    def _compute_remarks_required(self):
        required = self.env['ir.config_parameter'].sudo().get_param(
            'tr_backdate.remarks_required', False
        )
        for rec in self:
            rec.remarks_required = bool(required)

    @api.constrains('remarks')
    def _check_remarks(self):
        for rec in self:
            if rec.remarks_required and not rec.remarks:
                raise ValidationError(_('Remarks are mandatory when assigning a backdate.'))

    def _get_records(self):
        raw = self.res_ids or ''
        try:
            parsed = ast.literal_eval(raw)
            if isinstance(parsed, (list, tuple)):
                ids = [int(i) for i in parsed]
            else:
                ids = [int(parsed)]
        except (ValueError, SyntaxError):
            ids = [int(i.strip()) for i in raw.split(',') if i.strip()]
        return self.env[self.model].browse(ids)

    def action_assign(self):
        self.ensure_one()
        records = self._get_records()
        if not records:
            return {'type': 'ir.actions.act_window_close'}

        date_val = self.backdate if self.is_date else self.backdate_datetime
        records.write({
            'backdate': date_val,
            'backdate_remarks': self.remarks or '',
        })
        if self.remarks:
            for rec in records:
                rec.message_post(
                    body=_('Backdate set to %s. Remarks: %s', date_val, self.remarks),
                    subtype_xmlid='mail.mt_note',
                )
        return {'type': 'ir.actions.act_window_close'}
