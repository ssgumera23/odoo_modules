/** @odoo-module **/

import public_kiosk_app from "@hr_attendance/public_kiosk/public_kiosk_app";
const kioskAttendanceApp = public_kiosk_app.kioskAttendanceApp;

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { AttendanceWebcamDialog } from "./attendance_webcam_dialog"
import { session } from "@web/session";

patch(kioskAttendanceApp.prototype, {
setup() {
        super.setup();
        this.rpc = useService("rpc");
        this.dialog = useService("dialog");
        this.loadResConfig();
    },
    async loadResConfig(){
        const result = await this.rpc("/hr_attendance/attendance_res_config" ,{
            'token': this.props.token,
        });
        this.res_config = result;
        if (this.res_config && this.res_config.attendance_webcam_image) {
            const attendance_webcam_image = this.res_config.attendance_webcam_image;
            this.state.attendance_webcam_image = attendance_webcam_image ? attendance_webcam_image : false;  
        }
    },
    async uploadWebcamImage(data) {
        var self = this;

        var employeeId= data.employeeId;
        var enteredPin = data.enteredPin;

        if (data && data.image){   
            var image = data.image.split(',')[1];         
            const result = await this.rpc('manual_selection',
            {
                'token': this.props.token,
                'employee_id': employeeId,
                'pin_code': enteredPin,
            })
            if (result && result.attendance) {
                if (result.attendance.id && result.attendance_state == "checked_in"){
                    await this.rpc('update_checkin_image',{
                        'token': this.props.token,
                        'attendance_id':parseInt(result.attendance.id),
                        'image': image,
                    })
                }
                else if(result.attendance.id && result.attendance_state == "checked_out"){
                    await this.rpc('update_checkout_image',{
                        'token': this.props.token,
                        'attendance_id':parseInt(result.attendance.id),
                        'image': image,
                    })
                }
                this.employeeData = result
                this.switchDisplay('greet')
            }else{
                if (enteredPin){
                    this.displayNotification(_t("Wrong Pin"))
                }
            }
        }
    },
    async onManualSelection(employeeId, enteredPin){
        if (this.state.attendance_webcam_image) {
            this.dialog.add(AttendanceWebcamDialog, {
                employeeId : employeeId, 
                enteredPin : enteredPin,
                uploadWebcamImage: (image) => {
                    var input = {
                        'employeeId' : employeeId, 
                        'enteredPin' : enteredPin,
                    }
                    var data = Object.assign({}, input, image);
                    this.uploadWebcamImage(data);
                },
            });
        }else{
            const result = await this.rpc('manual_selection',
            {
                'token': this.props.token,
                'employee_id': employeeId,
                'pin_code': enteredPin
            })
            if (result && result.attendance) {
                this.employeeData = result
                this.switchDisplay('greet')
            }else{
                if (enteredPin){
                    this.displayNotification(_t("Wrong Pin"))
                }
            }
        }        
    },
});

