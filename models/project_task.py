# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class LogoCheck(models.Model):
    _name = 'logo.check'

    done_logo = fields.Binary("Revision Image")
    logo_name = fields.Char("Logo name")
    task_id = fields.Many2one('project.task')


class Attachment(models.Model):
    
    _inherit = 'ir.attachment'

    @api.model
    def create(self, vals):
        print('============= vals =========== ', vals)
        record = super(Attachment,self).create(vals)
        if record.res_model=='project.task' and record.res_id:
            task_id = self.env['project.task'].browse(record.res_id)
            if task_id:
                task_id.displayed_image_id = record.id
                print("-------- test------- ")
        print("revision_image ========== ", record)
        return record


class ProjectTaks(models.Model):
    _inherit = 'project.task'
    
    task_image_atc = fields.Binary(string='Attachment')
    revision_image = fields.Binary("Revision Image")
    task_image_name = fields.Char('Attachment')
    # attachment_ids2 = fields.One2many(
    #     'ir.attachment', 'res_id')
    print_manager_id = fields.Many2one("res.partner", "Print Manager")
    revision_note = fields.Text()
    stage_type = fields.Selection([('new', "NEW TASK"), ('start', "WORK STARTED"), ('req_approval', "REQUESTING WORK APPROVE"), 
        ('approved', "WORK APPROVED"), ('revision', "CUSTOMER ISSUE"),
        ('new_print', "NEW PRINT"), ('in_print', "IN PRINT"), ('printing', "PRINTING"), ('job_issue', "JOB ISSUE"), 
        ('job_done', "DONE"), ('shipped', "SHIPPED")], compute="get_stage_type", store=True)
    final_image = fields.Binary("Image")
    logo_ids = fields.One2many('logo.check', 'task_id')
    approved_logo = fields.Binary(string='Approved Logo')
    project_stage_id = fields.Many2one('project.stage')

    front_image = fields.Binary()
    back_image = fields.Binary()
    design_product_id = fields.Many2one("product.template", "Apply On Product")
    quantity = fields.Integer()
    is_web_design = fields.Boolean()

    @api.model
    def create_design_tasks(self, vals):
        project_obj = self.env['project.project']
        project = project_obj.sudo().search([('partner_id', '=', self.env.user.partner_id.id), ('project_type', '=', 'graphic')], limit=1)
        if not project:
            project_vals = {
                'name': self.env.user.name + " Design",
                'partner_id': self.env.user.partner_id.id,
                'privacy_visibility': 'portal',
            }
            project = project_obj.sudo().with_context(gv=True).create(project_vals)

        if 'front_image' in vals and vals['front_image']:
            front_design = self.env['user.design'].search([('name', '=', 'Front Design'), ('user_id', '=', self.env.user.id)], limit=1)
            vals.update({
                'front_image': front_design.save_design,
            })

        if 'back_image' in vals and vals['back_image']:
            back_design = self.env['user.design'].search([('name', '=', 'Back Design'), ('user_id', '=', self.env.user.id)], limit=1)
            vals.update({
                'back_image': back_design.save_design,
            })
        vals.update({
            'is_web_design': True, 
            'project_id': project.id, 
            'name': self.env.user.name + " Tshirt Printing Design"
        })
        print("-------------- vals ------------ ", vals)
        task = self.create(vals)
        save_design_vals = {
            'save_front_design': task.front_image,
            'save_back_design': task.back_image,
            'user_id': self.env.user.id
        }
        print('=========== save_design_vals ====== ', save_design_vals)
        design = self.env['save.user.design'].create(save_design_vals)
        task.name = task.name + " " + str(task.id)
        return task


    @api.model
    def create(self, vals):
        task_id = super(ProjectTaks, self).create(vals)
        if task_id.approved_logo:
            self.env['ir.attachment'].create({
                    'res_id': task_id.id,
                    'res_model': 'project.task',
                    'type': 'binary',
                    'datas': task_id.approved_logo,
                    'name': "Approved Logo",
            })
        if task_id.project_id and task_id.project_id.is_development_project:
            task_id.project_stage_id = task_id.project_id.stage_id.id
        return task_id

    @api.depends('stage_id')
    def get_stage_type(self):
        for task in self:
            task.stage_type = task.stage_id.stage_type

    def write(self,vals):
        if 'logo' in vals and vals['logo']:
            logo_id = vals['logo']
            logo = self.env['logo.check'].browse(logo_id)
            del vals['logo']
            vals.update({'approved_logo': logo.done_logo})
            self.env['ir.attachment'].create({
                    'res_id': self.id,
                    'res_model': 'project.task',
                    'type': 'binary',
                    'datas': logo.done_logo,
                    'name': logo.logo_name,
            })
        if 'logo' in vals:
            del vals['logo']
        if 'stage_id' in vals:
            stage_id = self.env['project.task.type'].browse(vals['stage_id'])

            # Word started by developer mail goes to customer
            if stage_id.send_notification and stage_id.stage_type == 'start':
                print("------- mail need to send ---- ")
                self.ensure_one()
                template_id = self.env['ir.model.data'].xmlid_to_res_id('project_trello_design.email_template_work_started', raise_if_not_found=False)
                lang = self.env.context.get('lang')
                template = self.env['mail.template'].sudo().browse(template_id)
                if template.lang:
                    lang = template.sudo()._render_template(template.lang, 'project.task', self.ids[0])
                ctx = {
                    'default_model': 'project.task',
                    'default_res_id': self.ids[0],
                    'default_use_template': bool(template_id),
                    'default_template_id': template_id,
                    'default_composition_mode': 'comment',
                    'force_email': True,
                    # 'model_description': self.with_context(lang=lang).type_name,
                }

                self.with_context(force_send=True).sudo().message_post_with_template(template_id, composition_mode='comment', email_layout_xmlid="mail.mail_notification_paynow")

            if stage_id.send_notification and stage_id.stage_type == 'req_approval':
                print("------- mail need to send ---- ")
                self.ensure_one()
                template_id = self.env['ir.model.data'].xmlid_to_res_id('project_trello_design.email_template_request_design_approve', raise_if_not_found=False)
                lang = self.env.context.get('lang')
                template = self.env['mail.template'].sudo().browse(template_id)
                if template.lang:
                    lang = template.sudo()._render_template(template.lang, 'project.task', self.ids[0])
                ctx = {
                    'default_model': 'project.task',
                    'default_res_id': self.ids[0],
                    'default_use_template': bool(template_id),
                    'default_template_id': template_id,
                    'default_composition_mode': 'comment',
                    'force_email': True,
                    # 'model_description': self.with_context(lang=lang).type_name,
                }

                self.with_context(force_send=True).sudo().message_post_with_template(template_id, composition_mode='comment', email_layout_xmlid="mail.mail_notification_paynow")

            if stage_id.send_notification and stage_id.stage_type == 'revision':
                print("------- mail need to send ---- a")
                self.ensure_one()
                template_id = self.env['ir.model.data'].xmlid_to_res_id('project_trello_design.email_template_design_customer_issue', raise_if_not_found=False)
                lang = self.env.context.get('lang')
                template = self.env['mail.template'].sudo().browse(template_id)
                if template.lang:
                    lang = template.sudo()._render_template(template.lang, 'project.task', self.ids[0])
                ctx = {
                    'default_model': 'project.task',
                    'default_res_id': self.ids[0],
                    'default_use_template': bool(template_id),
                    'default_template_id': template_id,
                    'default_composition_mode': 'comment',
                    'force_email': True,
                    # 'model_description': self.with_context(lang=lang).type_name,
                }
                self.with_context(force_send=True).sudo().message_post_with_template(template_id, composition_mode='comment', email_layout_xmlid="mail.mail_notification_paynow")


            if stage_id.send_notification and stage_id.stage_type == 'job_done':
                print("------- mail need to send ---- p ")
                self.ensure_one()
                template_id = self.env['ir.model.data'].xmlid_to_res_id('project_trello_design.email_template_design_done', raise_if_not_found=False)
                lang = self.env.context.get('lang')
                template = self.env['mail.template'].sudo().browse(template_id)
                if template.lang:
                    lang = template.sudo()._render_template(template.lang, 'project.task', self.ids[0])
                ctx = {
                    'default_model': 'project.task',
                    'default_res_id': self.ids[0],
                    'default_use_template': bool(template_id),
                    'default_template_id': template_id,
                    'default_composition_mode': 'comment',
                    'force_email': True,
                    # 'model_description': self.with_context(lang=lang).type_name,
                }
                self.with_context(force_send=True).sudo().message_post_with_template(template_id, composition_mode='comment', email_layout_xmlid="mail.mail_notification_paynow")

        record = super(ProjectTaks,self).write(vals)

        if 'user_id' in vals and vals['user_id']:
            template_id = self.env['ir.model.data'].xmlid_to_res_id('project_trello_design.email_template_assign_task', raise_if_not_found=False)
            lang = self.env.context.get('lang')
            template = self.env['mail.template'].sudo().browse(template_id)
            if template.lang:
                lang = template.sudo()._render_template(template.lang, 'project.task', self.ids[0])
            ctx = {
                'default_model': 'project.task',
                'default_res_id': self.ids[0],
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_composition_mode': 'comment',
                'force_email': True,
                # 'model_description': self.with_context(lang=lang).type_name,
            }
            self.with_context(force_send=True).sudo().message_post_with_template(template_id, composition_mode='comment', email_layout_xmlid="mail.mail_notification_paynow")

        # if vals.get('final_image',False):
        #     for res in self:
        #         print("========= ", res.attachment_ids)
        #         partner_ids = []
        #         for follower in res.message_follower_ids:
        #             partner_ids.append(follower.partner_id.id)
        #         atc_create = self.env['ir.attachment'].create({'datas':res.final_image,'name':"Final image to approve",'type':'binary','res_model':'project.task','res_id':res.id})
        #         res.message_post(body='Please find attached document', 
        #             partner_ids=partner_ids, type="comment", attachment_ids=[atc_create.id])
        #         res.attachment_ids = (4, atc_create.id)


        return record

    def _find_mail_template(self, force_confirmation_template=False):
        template_id = False
        if not template_id:
            template_id = self.env['ir.model.data'].xmlid_to_res_id('project_trello_design.email_template_request_design_approve', raise_if_not_found=False)
        return template_id

    def open_record(self):
        view_id = self.env.ref('project_trello_design.project_task_inherit_trello').id
        return {
        'type': 'ir.actions.act_window', 
        'res_model': 'project.task', 
        'name': 'Task', 
        'view_type': 'form', 
        'view_mode': 'form', 
        'res_id': self.id, 
        'target': 'self',
        'views': [[view_id, 'form']], 
    }