from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class BackdateWizard(models.TransientModel):
    _name = 'backdate.wizard'
    _description = 'Assign Backdate'

    model = fields.Char(string='Model', readonly=True)
    res_ids = fields.Json(string='Record IDs')
    backdate = fields.Date(string='Backdate', required=True, default=fields.Date.today)
    backdate_datetime = fields.Datetime(string='Backdate', default=fields.Datetime.now)
    remarks = fields.Char(string='Remarks')
    remarks_required = fields.Boolean(
        compute='_compute_remarks_required',
    )
    use_datetime = fields.Boolean(compute='_compute_use_datetime')

    @api.depends('model')
    def _compute_use_datetime(self):
        datetime_models = ['sale.order', 'purchase.order', 'stock.picking']
        for rec in self:
            rec.use_datetime = rec.model in datetime_models

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

    def action_assign(self):
        self.ensure_one()
        if not self.res_ids:
            return
        records = self.env[self.model].browse(self.res_ids)
        date_val = self.backdate_datetime if self.use_datetime else self.backdate
        records.write({
            'backdate': date_val,
            'backdate_remarks': self.remarks or '',
        })
        return {'type': 'ir.actions.act_window_close'}
