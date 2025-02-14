from odoo import fields, models, api

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    attendance_webcam_image = fields.Boolean(string="Attendances Webcam Image", default=False)