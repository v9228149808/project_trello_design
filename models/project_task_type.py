# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    is_default_design_stage = fields.Boolean("Is Default Design Stage ?")
    is_default_printing_stage = fields.Boolean("Is Default Printing Stage ?")
    send_notification = fields.Boolean("Send Notification")
    stage_type = fields.Selection([('new', "NEW TASK"), ('start', "WORK STARTED"), ('req_approval', "REQUESTING WORK APPROVE"), 
        ('approved', "WORK APPROVED"), ('revision', "CUSTOMER ISSUE"),
        ('new_print', "NEW PRINT"), ('in_print', "IN PRINT"), ('printing', "PRINTING"), ('job_issue', "JOB ISSUE"), 
        ('job_done', "DONE"), ('shipped', "SHIPPED")])

    is_erp_stage = fields.Boolean("Is ERP Stage ?")
    is_web_stage = fields.Boolean("Is Web Stage ?")