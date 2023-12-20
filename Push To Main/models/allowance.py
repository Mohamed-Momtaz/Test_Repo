""" Initialize Allowance Deduction """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class AllowanceDeduction(models.Model):
    """
        Initialize Allowance Deduction:
         -
    """
    _name = 'allowance.allowance'
    _description = 'Bonus'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(
        tracking=True
    )
    employee_id = fields.Many2one(
        'hr.employee',
        default=lambda self:self.env['hr.employee'].search(
        [('user_id', '=', self.env.uid)], limit=1),
        tracking=True
    )
    amount = fields.Float(compute='_compute_amount')
    type = fields.Selection(
        [('hour', 'Hour'),
         ('day', 'day'),
         ('fixed', 'fixed'),
         ],
        default='hour',
        tracking=True
    )
    contract_id = fields.Many2one(
        'hr.contract',
        related='employee_id.contract_id'
    )
    notes = fields.Html(
        'Reason',
        tracking=True
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('done', 'Done'),
         ('cancel', 'Cancelled')
         ],
        default='draft',
        string='Status',
        tracking=True
    )
    value = fields.Float(
        tracking=1
    )

    def action_draft(self):
        """ Action Draft """
        for rec in self:
            rec.write({
                'state': 'draft'
            })

    def action_cancel(self):
        """ Action Draft """
        for rec in self:
            rec.write({
                'state': 'cancel'
            })

    def action_done(self):
        """ Action Draft """
        for rec in self:
            rec.write({
                'state': 'done'
            })

    @api.depends('contract_id', 'type', 'value')
    def _compute_amount(self):
        """ Compute amount value """
        for rec in self:
            if rec.contract_id and rec.type:
                if rec.type == 'hour':
                    rec.amount = rec.value * rec.contract_id.hour_value
                elif rec.type == 'day':
                    rec.amount = rec.value * rec.contract_id.day_value
                else:
                    rec.amount = rec.value
            else:
                rec.amount = 0

