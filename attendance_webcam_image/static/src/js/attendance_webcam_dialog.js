/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";
import { onMounted, useState, useRef, Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class AttendanceWebcamDialog extends Component {
    setup() {
        this.title = _t("Capture Snapshot");

        this.videoRef = useRef("video");
        this.imageRef = useRef("image");
        this.selectRef = useRef("select");

        this.notificationService = useService('notification');

        this.state = useState({
            videoEl: false,
            imageEl: false,
            videoElwidth: 0,
            videoElheight: 0,
        })

        onMounted(async () => {
            await this.loadWebcam();            
        });        
    }
    loadWebcam(){
        var self = this;
        if (navigator.mediaDevices) {
            
            var videoElement = this.videoRef.el;
            var imageElement = this.imageRef.el;
            var videoSelect = this.selectRef.el;
            
            videoSelect.onchange = getStream;

            getStream().then(getDevices).then(gotDevices);

            async function getStream() {
                if (window.stream) {
                    window.stream.getTracks().forEach(track => {
                        track.stop();
                    });
                }
                const videoSource = videoSelect.value;
                const constraints = {
                    video: { deviceId: videoSource ? { exact: videoSource } : undefined }
                };
                return await navigator.mediaDevices.getUserMedia(constraints).then(gotStream).catch(handleError);
            }

            async function getDevices() {
                return await navigator.mediaDevices.enumerateDevices();
            }

            function gotDevices(deviceInfos) {
                window.deviceInfos = deviceInfos;
                
                for (const deviceInfo of deviceInfos) {
                    const option = document.createElement('option');
                    option.selected = deviceInfo.label;
                    option.value = deviceInfo.deviceId;
                    if (deviceInfo.kind === 'videoinput') {
                        option.text = deviceInfo.label || "Camera" + (videoSelect.length + 1) + "";
                        videoSelect.appendChild(option);
                    }
                }
                
            }

            function gotStream(stream) {
                window.stream = stream;
                videoSelect.selectedIndex = [...videoSelect.options].
                    findIndex(option => option.text === stream.getVideoTracks()[0].label);
                videoElement.srcObject = stream;
                videoElement.onloadedmetadata = function(e) {
                    videoElement.play();
                    self.state.videoEl = videoElement;
                    self.state.imageEl = imageElement;
                    self.state.videoElwidth = videoElement.offsetWidth;
                    self.state.videoElheight = videoElement.offsetHeight;
                };
            }

            function handleError(error) {
                console.error('Error: ', error);
            }              
        }
        else{
            this.notificationService.add(_t("https Failed: Warning! WEBCAM MAY ONLY WORKS WITH HTTPS CONNECTIONS. So your Odoo instance must be configured in https mode."), { type: "danger" });
        }
    }
    close() {
        this.props.close && this.props.close();
    }
    async onClickConfirm(){
        var video = this.state.videoEl;
        var image = this.state.imageEl;

        image.width = this.state.videoElwidth;
        image.height = this.state.videoElheight;

        image.getContext('2d').drawImage(video, 0, 0, image.width, image.height);
        var image_data = image.toDataURL("image/jpeg");
        await this.props.uploadWebcamImage({
            image: image_data,
        });

        if (window.stream) {
            window.stream.getTracks().forEach(track => {
                track.stop();
            });
        }

        this.props.close();
    }
}
AttendanceWebcamDialog.components = { Dialog };
AttendanceWebcamDialog.template = "attendance_webcam_image.AttendanceWebcamDialog";
AttendanceWebcamDialog.defaultProps = {};