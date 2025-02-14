from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    attendance_webcam_image = fields.Boolean(related="company_id.attendance_webcam_image", string="Attendances Webcam Image", readonly=False)