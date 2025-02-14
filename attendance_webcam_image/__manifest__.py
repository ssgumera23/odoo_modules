# -*- coding: utf-8 -*-
#################################################################################
# Author      : CFIS (<https://www.cfis.store/>)
# Copyright(c): 2017-Present CFIS.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.cfis.store/>
#################################################################################

{
    "name": "Attendance Webcam Image -  Attendance Photo",
    "summary": """
        This module helps you to capture the employees photo while check in / check and 
        kiosk mode from Employee Attendance.
    """,
    "version": "17.1",
    "description": """
        This module helps you to capture the employees photo while check in / check and 
        kiosk mode from Employee Attendance.
        Attendance Webcam.
        Attendance Webcam Photo.
        Attendance Employee Photo.
        Attendance Webcam Image.
        check in / check out Employee Picture.
        HR Attendance Employee Photo.
        check in / check out Employee Photo.
        Webcam and Employee Photo.
        Attendance check in / check out Employee Photo.               
        Attendance Capure Webcam Employee Photo.
        HR Attendance Webcam Image.
        Attendance Image.
        Photo.                   
    """,    
    "author": "CFIS",
    "maintainer": "CFIS",
    "license" :  "Other proprietary",
    "website": "https://www.cfis.store",
    "images": ["images/attendance_webcam_image.png"],
    "category": "eCommerce",
    "depends": [
        "base",
        "hr_attendance",
    ],
    "data": [
        "views/hr_attendance_views.xml",
        "views/res_config_settings.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/attendance_webcam_image/static/src/css/style.css",
            "/attendance_webcam_image/static/src/js/attendance_menu.js",
            "/attendance_webcam_image/static/src/js/attendance_webcam_dialog.js",
            "/attendance_webcam_image/static/src/xml/attendance_webcam_dialog.xml",
        ],
        "hr_attendance.assets_public_attendance":[
            "/attendance_webcam_image/static/src/css/style.css",
            "/attendance_webcam_image/static/src/js/public_kiosk_app.js",
            "/attendance_webcam_image/static/src/js/attendance_webcam_dialog.js",
            "/attendance_webcam_image/static/src/xml/attendance_webcam_dialog.xml",
        ]
    },
    "installable": True,
    "application": True,
    "price"                 :  20.00,
    "currency"              :  "EUR",
    "pre_init_hook"         :  "pre_init_check",
}