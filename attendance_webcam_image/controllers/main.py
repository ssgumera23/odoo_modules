from odoo import http, _
from odoo.http import request
import datetime
from odoo.addons.hr_attendance.controllers.main import HrAttendance as HrAttendance

class HrAttendance(HrAttendance):

    @staticmethod
    def _get_user_attendance_data(employee):
        rslt = super(HrAttendance, HrAttendance)._get_user_attendance_data(employee)
        rslt['attendance_webcam_image'] = employee.company_id and employee.company_id.attendance_webcam_image,
        return rslt
    
    @staticmethod
    def _get_employee_info_response(employee):
        rslt = super(HrAttendance, HrAttendance)._get_employee_info_response(employee)
        rslt['attendance']['id'] = employee.last_attendance_id.id or False
        return rslt
    
    @http.route('/hr_attendance/update_checkin_image', type="json", auth="public")
    def update_checkin_image(self, token, attendance_id, image):
        company = self._get_company(token)
        if company:
            attendance = request.env['hr.attendance'].sudo().browse(attendance_id)
            if attendance:
                attendance.sudo().write({
                    'check_in_image': image
                })
        return {}
    
    @http.route('/hr_attendance/update_checkout_image', type="json", auth="public")
    def update_checkout_image(self, token, attendance_id, image):
        company = self._get_company(token)
        if company:
            attendance = request.env['hr.attendance'].sudo().browse(attendance_id)
            if attendance:
                attendance.sudo().write({
                    'check_out_image': image
                })
        return {}
    
    @http.route('/hr_attendance/attendance_res_config', type="json", auth="public")
    def attendance_res_config(self, token):
        company = self._get_company(token)
        conf = {}
        if company:
            conf['attendance_webcam_image'] = company.attendance_webcam_image
        return conf
