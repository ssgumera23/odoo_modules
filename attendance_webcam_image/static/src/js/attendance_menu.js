/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ActivityMenu } from "@hr_attendance/components/attendance_menu/attendance_menu";
import { AttendanceWebcamDialog } from "./attendance_webcam_dialog"
import { useService } from "@web/core/utils/hooks";
import { isIosApp } from "@web/core/browser/feature_detection";

patch(ActivityMenu.prototype, {
    setup() {
        super.setup();
        this.rpc = useService("rpc");
        this.dialog = useService("dialog");
    },
    async searchReadEmployee(){
        await super.searchReadEmployee();
        const attendance_webcam_image = this.employee.attendance_webcam_image;
        this.state.attendance_webcam_image = attendance_webcam_image ? attendance_webcam_image : false;        
    },
    async uploadWebcamImage({ image }) {
        var self = this;
        if (image){
            image = image.split(',')[1];
            navigator.geolocation.getCurrentPosition(
                async ({coords: {latitude, longitude}}) => {
                    await self.rpc("/hr_attendance/systray_check_in_out", {
                        latitude,
                        longitude
                    }).then(async function(data){
                        if (data.attendance.id && data.attendance_state == "checked_in"){
                            await self.rpc("/web/dataset/call_kw/hr.attendance/write", {
                                model: "hr.attendance",
                                method: "write",
                                args: [parseInt(data.attendance.id), {
                                    'check_in_image': image,
                                }],
                                kwargs: {},
                            })
                        }
                        else if(data.attendance.id && data.attendance_state == "checked_out"){
                            await self.rpc("/web/dataset/call_kw/hr.attendance/write", {
                                model: "hr.attendance",
                                method: "write",
                                args: [parseInt(data.attendance.id), {
                                    'check_out_image': image,
                                }],
                                kwargs: {},
                            })
                        }
                    })
                    await self.searchReadEmployee()
                },
                async err => {
                    await self.rpc("/hr_attendance/systray_check_in_out")
                    await self.searchReadEmployee()
                }
            )
        }
    },
    async signInOut() {
        if (this.state.attendance_webcam_image) {
            this.dialog.add(AttendanceWebcamDialog, {
                uploadWebcamImage: (image) => this.uploadWebcamImage(image),
            });
        } else {
            if (!isIosApp()) {
                navigator.geolocation.getCurrentPosition(
                    async ({coords: {latitude, longitude}}) => {
                        await this.rpc("/hr_attendance/systray_check_in_out", {
                            latitude,
                            longitude
                        })
                        await this.searchReadEmployee()
                    },
                    async err => {
                        await this.rpc("/hr_attendance/systray_check_in_out")
                        await this.searchReadEmployee()
                    },
                    {
                        enableHighAccuracy: true,
                    }
                )
            } else {
                await this.rpc("/hr_attendance/systray_check_in_out")
                await this.searchReadEmployee()
            }
        }
    }
});
export default ActivityMenu;
