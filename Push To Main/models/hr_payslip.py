""" Initialize Hr Payslip """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class HrPayslip(models.Model):
    """
        Inherit Hr Payslip:
         - 
    """
    _inherit = 'hr.payslip'

    allowance_ids = fields.Many2many(
        'allowance.allowance',
        string='Bonus'
    )
    bonus_amount = fields.Float(
        compute='_compute_bonus_amount'
    )
    penalty_amount = fields.Float(
        compute='_compute_penalty_amount'
    )
    penalty_ids = fields.Many2many(
        'penalty.penalty'
    )

    @api.depends('allowance_ids')
    def _compute_bonus_amount(self):
        """ Compute bonus_amount value """
        for rec in self:
            if rec.allowance_ids:
                rec.bonus_amount = sum(rec.allowance_ids.mapped('amount'))
            else:
                rec.bonus_amount = 0

    @api.depends('penalty_ids')
    def _compute_penalty_amount(self):
        """ Compute bonus_amount value """
        for rec in self:
            if rec.penalty_ids:
                rec.penalty_amount = sum(rec.penalty_ids.mapped('amount'))
            else:
                rec.penalty_amount = 0

    def compute_sheet(self):
        """ Override compute_sheet """
        res = super(HrPayslip, self).compute_sheet()
        for rec in self:
            all_ded = self.env['allowance.allowance'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('date', '>=', rec.date_from),
                ('date', '<=', rec.date_to),
                ('state', '=', 'done'),
            ])
            if all_ded:
                rec.allowance_ids = all_ded.ids
            ded = self.env['penalty.penalty'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('date', '>=', rec.date_from),
                ('date', '<=', rec.date_to),
                ('state', '=', 'done'),
            ])
            if ded:
                rec.allowance_ids = ded.ids
        return res
