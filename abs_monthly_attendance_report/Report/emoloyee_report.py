# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2023-Today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
import time
import datetime
import calendar
from odoo import api, models, fields
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import date, datetime, time ,timedelta
from pytz import timezone

class RepairReport(models.AbstractModel):
    _name = 'report.abs_monthly_attendance_report.emoloyee_report'
    _description = "Maintenance summary"

    #Get employee report value function
    def _get_report_values(self, docids, data=None):
        employee_ids = False
        attendance_ids = False
        manager_ids = False
        doc_model = False
        docs = False
        month = False
        active_model = self.env['hr.employee']
        
        if docids:
            active_id = docids
            docs = self.env['employe.order'].browse(docids)
            
            if docs:
                employee_ids = self.env['hr.employee'].search([])
                if employee_ids:
                    manager_ids = []
                    for employee in employee_ids:
                        presented = 0
                        attendance_ids = self.env['hr.attendance'].search([('employee_id', '=', employee.id)])
                        count = 0.0
                        difference = 0
                        tz = timezone(employee.resource_calendar_id.tz)
                        month_date=date(int(docs.year),int(docs.month),1)
                        docs.date_from=month_date.replace(day=1)
                        docs.date_to=month_date.replace(day=calendar.monthrange(month_date.year,month_date.month)[1])
                        date_from = tz.localize(datetime.combine(fields.Datetime.from_string(str(docs.date_from)), time.min))
                        date_to = tz.localize(datetime.combine(fields.Datetime.from_string(str(docs.date_to)), time.max))
                        intervals = employee.list_work_time_per_day(date_from, date_to, calendar=employee.resource_calendar_id)
                        
                        for rec in intervals:
                            attendances = self.env["hr.attendance"].search(
                                    [('employee_id', '=', employee.id), ('check_in', '>=', str(docs.date_from)),
                                    ('check_in', '<=', str(docs.date_to))])
                            if attendances:
                                count = 0.0
                                presented = 0
                                for attendance in attendances:
                                    if docs.year and docs.month:
                                        presented += 1
                                        check_in = attendance.check_in
                                        check_out = attendance.check_out
                                        difference = check_out - check_in
                                        count = attendance.worked_hours + count                                        
                        total_hour = 0
                        month_date=date(int(docs.year),int(docs.month),1)
                        docs.date_from=month_date.replace(day=1)
                        docs.date_to=month_date.replace(day=calendar.monthrange(month_date.year,month_date.month)[1])
                        today = docs.date_from
                        wizard_month = int(docs.month)
                        day=date(int(docs.year), int(docs.month) ,1)
                        single_day = timedelta(days=1)
                        weekday = docs.month
                        days = 0
                        while day.month == today.month:
                            if day.isoweekday() == 5:
                                days += 1
                            day += single_day
                        today = docs.date_from
                        wizard_month = int(docs.month)
                        day=date(int(docs.year), int(docs.month) ,1)
                        single_day = timedelta(days=1)
                        weekday = docs.month
                        dayss = 0
                        while day.month == today.month:
                            if day.isoweekday() == 7:
                                dayss += 1
                            day += single_day 
                        week_day = dayss + days
                        monthday =  docs.date_to - docs.date_from
                        monthday += timedelta(days=1)
                        total_day = (monthday.days) - week_day
                        total_hour = total_day * employee.resource_calendar_id.hours_per_day                        
                        employee.total_day = total_day
                        employee.total_hour = total_hour
                        employee.present_day = presented
                        employee.present_hour = '%.2f' % count
                            
                        if employee.parent_id and employee.parent_id not in manager_ids :
                            manager_ids.append(employee.parent_id)
                            month = calendar.month_name[int(docs.month)]
       
        return {
                   'manager_ids':manager_ids,
                   'employee_ids':employee_ids,
                   'doc_model': active_model,
                   'docks': docs,
                   'month':month,
                   }
