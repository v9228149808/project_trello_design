# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    project_type = fields.Selection([('graphic', 'Graphic'), ('production', 'Production')], "Project Type")
    functional_person_id = fields.Many2one("res.users", "Functional Person")
    server_manager_id = fields.Many2one("res.users", "Server Manager")
    sale_person_id = fields.Many2one("res.users", "Sale Person")
    developer_id = fields.Many2one("res.users", "Developer")
    final_report_id = fields.Many2one("res.users", "Update Done")
    stage_id = fields.Many2one('project.stage', string='Stage', ondelete='restrict', tracking=True, index=True, copy=False)
    is_development_project = fields.Boolean("Is ERP?")
    is_web_development_project = fields.Boolean("Is Web Development?")
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
    ], related="stage_id.project_stage_type")

    document_id = fields.Many2one('documents.document')

    def move_erp_finished(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'erp_finished')])
            project.stage_id = next_stage.id

            template_id = self.env['ir.model.data'].xmlid_to_res_id('project_trello_design.email_template_erp_done', raise_if_not_found=False)
            lang = self.env.context.get('lang')
            template = self.env['mail.template'].sudo().browse(template_id)
            if template.lang:
                lang = template.sudo()._render_template(template.lang, 'project.project', self.ids[0])
            ctx = {
                'default_model': 'project.project',
                'default_res_id': self.ids[0],
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_composition_mode': 'comment',
                'force_email': True,
            }
            self.with_context(force_send=True).sudo().message_post_with_template(template_id, composition_mode='comment', email_layout_xmlid="mail.mail_notification_paynow")

    def move_provide_final_demo(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'provide_final_demo')])
            project.stage_id = next_stage.id

            template_id = self.env['ir.model.data'].xmlid_to_res_id('project_trello_design.email_template_provide_demo', raise_if_not_found=False)
            lang = self.env.context.get('lang')
            template = self.env['mail.template'].sudo().browse(template_id)
            if template.lang:
                lang = template.sudo()._render_template(template.lang, 'project.project', self.ids[0])
            ctx = {
                'default_model': 'project.project',
                'default_res_id': self.ids[0],
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_composition_mode': 'comment',
                'force_email': True,
            }
            self.with_context(force_send=True).sudo().message_post_with_template(template_id, composition_mode='comment', email_layout_xmlid="mail.mail_notification_paynow")

    def move_recheck_software(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'recheck_software')])
            project.stage_id = next_stage.id

            template_id = self.env['ir.model.data'].xmlid_to_res_id('project_trello_design.email_template_provide_demo', raise_if_not_found=False)
            lang = self.env.context.get('lang')
            template = self.env['mail.template'].sudo().browse(template_id)
            if template.lang:
                lang = template.sudo()._render_template(template.lang, 'project.project', self.ids[0])
            ctx = {
                'default_model': 'project.project',
                'default_res_id': self.ids[0],
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_composition_mode': 'comment',
                'force_email': True,
            }
            self.with_context(force_send=True).sudo().message_post_with_template(template_id, composition_mode='comment', email_layout_xmlid="mail.mail_notification_paynow")

    def move_fix_bugs(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'fix_bugs')])
            project.stage_id = next_stage.id

            template_id = self.env['ir.model.data'].xmlid_to_res_id('project_trello_design.email_template_fix_bugs', raise_if_not_found=False)
            lang = self.env.context.get('lang')
            template = self.env['mail.template'].sudo().browse(template_id)
            if template.lang:
                lang = template.sudo()._render_template(template.lang, 'project.project', self.ids[0])
            ctx = {
                'default_model': 'project.project',
                'default_res_id': self.ids[0],
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_composition_mode': 'comment',
                'force_email': True,
            }
            self.with_context(force_send=True).sudo().message_post_with_template(template_id, composition_mode='comment', email_layout_xmlid="mail.mail_notification_paynow")


    def move_review_verify_req(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'review_verify_req')])
            project.stage_id = next_stage.id

            template_id = self.env['ir.model.data'].xmlid_to_res_id('project_trello_design.email_template_review_requirement', raise_if_not_found=False)
            lang = self.env.context.get('lang')
            template = self.env['mail.template'].sudo().browse(template_id)
            if template.lang:
                lang = template.sudo()._render_template(template.lang, 'project.project', self.ids[0])
            ctx = {
                'default_model': 'project.project',
                'default_res_id': self.ids[0],
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_composition_mode': 'comment',
                'force_email': True,
            }
            self.with_context(force_send=True).sudo().message_post_with_template(template_id, composition_mode='comment', email_layout_xmlid="mail.mail_notification_paynow")


    def move_code_on_live(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'code_on_live')])
            project.stage_id = next_stage.id

    def move_start_customization(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'start_customization')])
            project.stage_id = next_stage.id

    def move_setup_server_live(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'setup_server_live')])
            project.stage_id = next_stage.id

    def move_setup_network_requirements(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'setup_network_requirements')])
            project.stage_id = next_stage.id

    def move_development_customization_doc(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'development_customization_doc')])
            project.stage_id = next_stage.id

    def move_demo_to_client(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'demo_to_client')])
            project.stage_id = next_stage.id

    def move_upload_odoo_apps(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'upload_odoo_apps')])
            project.stage_id = next_stage.id

    def move_server_setup_test(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'server_setup_test')])
            project.stage_id = next_stage.id

    def move_doc_approval(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'doc_approval')])
            project.stage_id = next_stage.id

    def move_doc_sent_to_client(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'doc_sent_to_client')])
            project.stage_id = next_stage.id
            template_id = self.env['ir.model.data'].xmlid_to_res_id('project_trello_design.email_template_doc_sent_to_client', raise_if_not_found=False)
            lang = self.env.context.get('lang')
            template = self.env['mail.template'].sudo().browse(template_id)
            if template.lang:
                lang = template.sudo()._render_template(template.lang, 'project.project', self.ids[0])
            ctx = {
                'default_model': 'project.project',
                'default_res_id': self.ids[0],
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_composition_mode': 'comment',
                'force_email': True,
            }
            self.with_context(force_send=True).sudo().message_post_with_template(template_id, composition_mode='comment', email_layout_xmlid="mail.mail_notification_paynow")

    def move_default_doc(self):
        for project in self:
            next_stage = self.env['project.stage'].search([('project_stage_type', '=', 'default_doc')])
            project.stage_id = next_stage.id
            template_id = self.env['ir.model.data'].xmlid_to_res_id('project_trello_design.email_template_default_doc', raise_if_not_found=False)
            lang = self.env.context.get('lang')
            template = self.env['mail.template'].sudo().browse(template_id)
            if template.lang:
                lang = template.sudo()._render_template(template.lang, 'project.project', self.ids[0])
            ctx = {
                'default_model': 'project.project',
                'default_res_id': self.ids[0],
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_composition_mode': 'comment',
                'force_email': True,
            }
            self.with_context(force_send=True).sudo().message_post_with_template(template_id, composition_mode='comment', email_layout_xmlid="mail.mail_notification_paynow")


    @api.model
    def create(self, vals):
        if 'default_is_development_project' in self.env.context and self.env.context['default_is_development_project']:
            default_stage_id = self.env['project.stage'].search([('project_stage_type', '=', 'take_requirement')])
            vals.update({'stage_id': default_stage_id.id})

        if 'default_is_web_development_project' in self.env.context and self.env.context['default_is_web_development_project']:
            default_stage_id = self.env['project.stage'].search([('project_stage_type', '=', 'take_requirement')])
            vals.update({'stage_id': default_stage_id.id})

        project = super(ProjectProject, self).create(vals)
        if 'gv' in self.env.context and self.env.context['gv'] or project.project_type and project.project_type == 'graphic':
            project.project_type = 'graphic'

            project_stage_ids = self.env['project.task.type'].search([('is_default_design_stage', '=', True)])
            project_stage_ids.write({'project_ids': [(4, project.id)]})
            project_team_ids = self.env['crm.team'].search([('type_team', '=', 'project')])
            if project_team_ids:
                project.team_id = project_team_ids[0].id
                project.user_id = project_team_ids[0].user_id.id

        if 'production' in self.env.context and self.env.context['production'] or project.project_type and project.project_type == 'production':
            project.project_type = 'production'

            project_stage_ids = self.env['project.task.type'].search([('is_default_printing_stage', '=', True)])
            project_stage_ids.write({'project_ids': [(4, project.id)]})
            production_team_ids = self.env['crm.team'].search([('type_team', '=', 'production')])
            if project_stage_ids:
                project.production_team_id = production_team_ids[0].id
                project.user_id = production_team_ids[0].user_id.id

        if project.is_development_project:
            erp_stages_ids = self.env['project.task.type'].search([('is_erp_stage', '=', True)])
            erp_stages_ids.write({'project_ids': [(4, project.id)]})

        if project.is_web_development_project:
            web_stages_ids = self.env['project.task.type'].search([('is_web_stage', '=', True)])
            web_stages_ids.write({'project_ids': [(4, project.id)]})

        # if project.is_development_project or project.is_web_development_project:
        #     template_id = self.env['ir.model.data'].xmlid_to_res_id('project_trello_design.email_template_take_requirement', raise_if_not_found=False)
        #     lang = self.env.context.get('lang')
        #     template = self.env['mail.template'].sudo().browse(template_id)
        #     if template.lang:
        #         lang = template.sudo()._render_template(template.lang, 'project.project', project.id)
        #     ctx = {
        #         'default_model': 'project.project',
        #         'default_res_id': project.id,
        #         'default_use_template': bool(template_id),
        #         'default_template_id': template_id,
        #         'default_composition_mode': 'comment',
        #         'force_email': True,
        #     }
        #     self.with_context(force_send=True).sudo().message_post_with_template(template_id, composition_mode='comment', email_layout_xmlid="mail.mail_notification_paynow")

        project.get_project_team_members()
        return project