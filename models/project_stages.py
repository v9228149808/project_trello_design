# -*- coding: utf-8 -*-

from odoo import api, fields, models



class ProjectStage(models.Model):
    
    _name = "project.stage"
    _description = "Project Stages"
    _rec_name = 'name'
    _order = "sequence, name, id"


    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    fold = fields.Boolean('Folded in Pipeline',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')
    project_stage_type = fields.Selection([
        ('take_requirement', "Take Requirement"),
        ('default_doc', "Default Documentation"),
        ('doc_sent_to_client', "Document Sent to Client"), 
        ('doc_approval', "Document APPROVED / DISAPPROVED"), 
        ('server_setup_test', "Setup Test Server"), 
        ('upload_odoo_apps', "Upload Odoo Apps"),
        ('demo_to_client', "Demo Client with Existing Apps"), 
        ('development_customization_doc', "Development/Customization Document"), 
        ('setup_network_requirements', "Setup Network Requirements"), 
        ('setup_server_live', "Setup Live Server"), 
        ('start_customization', "Start Customization"), 
        ('code_on_live', "Setup Code On Live Server"),
        ('review_verify_req', "Review/Verify the Requirements On Live Server"),
        ('fix_bugs', "Fix Bugs"),
        ('recheck_software', "Recheck Software"),
        ('provide_final_demo', "Provide Final Demo"),
        ('erp_finished', "Erp Finished"),
    ])

    # # This field for interface only
    # team_count = fields.Integer('team_count', compute='_compute_team_count')

    # def _compute_team_count(self):
    #     for stage in self:
    #         stage.team_count = self.env['crm.team'].search_count([])
