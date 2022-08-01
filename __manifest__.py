# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Project Kanban Design',
    'category': 'Project',
    'sequence': 150,
    'summary': 'Change the project task kanban view',
    'depends': ['project', 'project_team'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_data.xml',
        'view/assets.xml',
        'view/project_task_view.xml',
        'view/project_portal_template_view.xml',
        'view/project_stage_view.xml',
        'view/project_view.xml',
    ],
    'application': True,
}
