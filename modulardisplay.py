import requests 
import json
import os
from math import floor
from flask import Flask, render_template, request, url_for, redirect
import datetime as dt

from static.DynamicComponents.htmlbits import Buttons, Views
from static.DynamicComponents.iconsbits import Bootstrap_SVG_Icons
from static.Configuration.OctoprintDataModels import DataModels

app=Flask(__name__)

activity_state_1 = ["Offline"]
activity_state_2 = ["Inactive"]
activity_state_3 = ["Starting", "Printing", "Operational", "Paused"]
activity_state_4 = ["Complete", "Stopped"]

btn_region_upper_actions_valid = ['pause', 'stop']
btn_region_lower_actions_valid = ['connect', 'start']

endpoint = "127.0.0.1:5000"
X_Api_Key = "593425E324D842BCB2938C7D8E583B76" #only works for local instance

class printer_connection():
    def __init__(self, endpoint, X_Api_Key):
        self._endpoint = endpoint
        self._X_Api_Key = X_Api_Key
        os.environ["NO_PROXY"] = "127.0.0.1"
        
    def printer_btn_post(self, btn_output):
        data_models = DataModels
        printer_btn_data = {}
        operation = btn_output['operation']
        command = btn_output['command']
        action = btn_output['action']
        printer_btn_ready = False
                
        if btn_output != data_models.btn_output():
            printer_btn_ready = True
            if command != '' and action != '':
                printer_btn_data = {
                    "command": command,
                    "action": action
                }
            elif command != '' and action == '':
                printer_btn_data = {
                    "command": command
                }
            else:
                printer_btn_datatransfer = False
                printer_btn_data = {}
        else:
            printer_btn_ready = False
            
        if printer_btn_ready == True:
            printer_btn_data = json.dumps(printer_btn_data, indent=4)
            printer_btn_data = json.loads(printer_btn_data)
            try:
                requests.post(f'http://{self._endpoint}{operation}', json=printer_btn_data, headers={'X-Api-Key': self._X_Api_Key})
            except Exception:
                pass
        else:
            pass 
        
    def printer_btn_press(self, btn_input):
        data_models = DataModels
        btn_region = btn_input['btn_region']
        btn_action = btn_input['btn_action']
        btn_output = {
            'operation': '',
            'command': '',
            'action': ''
        }
        
        if btn_input != data_models.btn_input():
            if btn_region == 'upper' and btn_action in btn_region_upper_actions_valid:
                if btn_action == "pause":
                    btn_output['operation'] = '/api/job'
                    btn_output['command'] = 'pause'
                    btn_output['action'] = 'toggle'
                elif btn_action == 'stop':
                    btn_output['operation'] = '/api/job'
                    btn_output['command'] = 'cancel'
                    btn_output['action'] = ''
            elif btn_region == 'lower' and btn_action in btn_region_lower_actions_valid:
                if btn_action == 'connect':
                    btn_output['operation'] = '/api/connection'
                    btn_output['command'] = 'connect'
                    btn_output['action'] = ''
            else:
                pass
            
        self.printer_btn_post(btn_output=btn_output)
        
    def printer_ext_get(self):
        try:
            printer_ext_get_request = requests.get(f"http://{self._endpoint}/api/printer/tool", headers={"X-Api-Key":self._X_Api_Key}, verify=False)
            printer_ext_get_content = printer_ext_get_request.content
            printer_ext_get_json = json.loads(printer_ext_get_content)
            printer_ext_get_raw = printer_ext_get_json['tool0']
        except Exception:
            printer_ext_get_raw = {}
            
        return printer_ext_get_raw
    
    def printer_bed_get(self):
        try:
            printer_bed_get_request = requests.get(f"http://{self._endpoint}/api/printer/bed", headers={"X-Api-Key":self._X_Api_Key}, verify=False)
            printer_bed_get_content = printer_bed_get_request.content
            printer_bed_get_json = json.loads(printer_bed_get_content)
            printer_bed_get_raw = printer_bed_get_json['bed']
        except Exception:
            printer_bed_get_raw = {}
            
        return printer_bed_get_raw
    
    def printer_job_get(self):
        printer_job_get_raw_job = ''
        printer_job_get_raw_progress = ''
        printer_job_get_raw_state = ''
        
        try:
            printer_job_get_request = requests.get(f"http://{self._endpoint}/api/job", headers={"X-Api-Key":self._X_Api_Key}, verify=False)
            printer_job_get_content = printer_job_get_request.content
            printer_job_get_json = json.loads(printer_job_get_content)
            printer_job_get_raw_job = printer_job_get_json['job']
            printer_job_get_raw_progress = printer_job_get_json['progress']
            printer_job_get_raw_state = printer_job_get_json['state']
            printer_job_get_raw = {
            'printer_job_get_job': printer_job_get_raw_job,
            'printer_job_get_progress': printer_job_get_raw_progress,
            'printer_job_get_state': printer_job_get_raw_state
            }
        except Exception:
            printer_job_get_raw = {}
            
        return printer_job_get_raw
        
    def ext_data(self):
        ext_data_raw = self.printer_ext_get()   
        ext_data_processed = {}
        ext_temp_actual = ''
        ext_temp_target = ''
        ext_temp_status = ''
        ext_temp_state = ''
        
        if ext_data_raw != {}:
            ext_temp_actual = ext_data_raw['actual']
            ext_temp_target = ext_data_raw['target']
            
            if ext_temp_actual < ext_temp_target:
                ext_temp_state = 'heating'
            elif ext_temp_actual == ext_temp_target:
                ext_temp_state = 'stable'
            elif ext_temp_actual > ext_temp_target and ext_temp_target != 0:
                ext_temp_state = 'cooling'
            elif ext_temp_actual > ext_temp_target and ext_temp_target == 0 and ext_temp_actual >= 25:
                ext_temp_state = 'cooling'
            elif ext_temp_actual > ext_temp_target and ext_temp_target == 0 and ext_temp_actual < 25:
                ext_temp_state = 'stable'
                
            if ext_temp_actual >= 50:
                ext_temp_status = 'unsafe'
            elif ext_temp_actual < 50: 
                ext_temp_status = 'safe'
        else:
            pass
                    
        ext_data_processed = {
            'ext_temp_actual': ext_temp_actual,
            'ext_temp_target': ext_temp_target,
            'ext_temp_status': ext_temp_status,
            'ext_temp_state': ext_temp_state
        }
        
        return ext_data_processed
        
    def bed_data(self):
        bed_data_raw = self.printer_bed_get()   
        bed_data_processed = {}
        bed_temp_actual = ''
        bed_temp_target = ''
        bed_temp_status = ''
        bed_temp_state = ''
        
        if bed_data_raw != {}:
            bed_temp_actual = bed_data_raw['actual']
            bed_temp_target = bed_data_raw['target']
            
            if bed_temp_actual < bed_temp_target:
                bed_temp_state = 'heating'
            elif bed_temp_actual == bed_temp_target:
                bed_temp_state = 'stable'
            elif bed_temp_actual > bed_temp_target and bed_temp_target != 0:
                bed_temp_state = 'cooling'
            elif bed_temp_actual > bed_temp_target and bed_temp_target == 0 and bed_temp_actual >= 25:
                bed_temp_state = 'cooling'
            elif bed_temp_actual > bed_temp_target and bed_temp_target == 0 and bed_temp_actual < 25:
                bed_temp_state = 'stable'
                
            if bed_temp_actual >= 50:
                bed_temp_status = 'unsafe'
            elif bed_temp_actual < 50: 
                bed_temp_status = 'safe'
        else:
            pass
                    
        bed_data_processed = {
            'bed_temp_actual': bed_temp_actual,
            'bed_temp_target': bed_temp_target,
            'bed_temp_status': bed_temp_status,
            'bed_temp_state': bed_temp_state
        }
        
        return bed_data_processed
    
    def job_time_proc(self, job_time):
        job_time = job_time

        if floor(job_time/3600) >= 1:
            job_time = f"{floor(float(job_time)/3600)} hr."
        elif job_time/3600 <= 1 and floor(job_time/60) >= 1:
            job_time = f"{floor(float(job_time)/60)} min."  
        elif job_time/3600 <= 1 and job_time/60 < 1:
            job_time = "< 1 min."   
        
        return job_time

    def job_data(self):
        job_data_raw = self.printer_job_get()
        job_data_processed = {}
        
        job_time = ''
        job_progress = ''
        job_state = ''
        
        if job_data_raw != {}:
            job_data_raw_job = job_data_raw['printer_job_get_job'] #12/08/22 -- currently unused (info will be needed with introduction of bed clearing and advanced job operations)
            job_data_raw_progress = job_data_raw['printer_job_get_progress']
            job_data_raw_state = job_data_raw['printer_job_get_state']
            try:
                job_time = self.job_time_proc(float(job_data_raw_progress['printTimeLeft']))
                job_progress = job_data_raw_progress['completion']
                job_state = job_data_raw_state
            except Exception:
                pass
        else:
            pass
        
        job_data_processed = {
            'job_time': job_time,
            'job_progress': job_progress,
            'job_state': job_state
        }
        
        return job_data_processed        
    
    def printer_status(self, ext_data, bed_data, job_data):
        data_models = DataModels
        ext_data = ext_data
        bed_data = bed_data
        job_data = job_data
        
        if ext_data != data_models.ext_data() or bed_data != data_models.bed_data():
            if job_data != data_models.job_data():
                if job_data['job_progress'] is not None:
                    if job_data['job_state'] != 'Paused':
                        if job_data['job_progress'] <= 0.15:
                            return "Starting"
                        elif job_data['job_progress'] > 0.15 and job_data['job_progress'] < 100:
                            return "Printing"
                        elif job_data['job_progress'] == 100:
                            return "Complete"
                    else:
                        return "Paused"
                elif ext_data['ext_temp_actual'] <= 25 or bed_data['bed_temp_actual'] <= 25:
                    return "Inactive"
                else:
                    return "Stopped"
            else:
                return "Inactive"
        else:
            return "Offline"

class component_sort():
    def status_display_upper(self, printer_status, job_progress, job_time):
        status_upper = ""
        status_upper_status = ""
        status_upper_progress = ""
        views = Views
        
        if printer_status in activity_state_1 or printer_status in activity_state_2:
            status_upper_status = views.status_display_upper_emphasis(printer_status)
            status_upper_progress = ""
        elif printer_status in activity_state_3:
            status_upper_status = views.status_display_upper_hybrid(printer_status, job_time)
            status_upper_progress = views.status_display_upper_progress(job_progress)
        elif printer_status in activity_state_4:
            status_upper_status = views.status_display_upper(printer_status)
            status_upper_progress = views.status_display_upper_progress(job_progress)

        status_upper = status_upper_status + status_upper_progress + "<hr>"
        return status_upper

    def menu_context_upper(self, printer_status):
        menu_upper = ""
        printer_status=printer_status
        buttons = Buttons
        icons = Bootstrap_SVG_Icons

        if printer_status in activity_state_1:
            menu_upper = "" #10-22-22: remains empty, devoid of light
        elif printer_status in activity_state_2 or printer_status in activity_state_4:
            menu_upper = buttons.bed_clear() #10-22-22: change to bed clear toggle
        elif printer_status in activity_state_3:
            if printer_status == "Paused":
                menu_upper = buttons.job_operations(menu_context_upper_btn_left=icons.icon_svg_play(), menu_context_upper_btn_right=icons.icon_svg_stop()) #10-22-22: change to job operations shortcuts   
            else: 
                menu_upper = buttons.job_operations(menu_context_upper_btn_left=icons.icon_svg_pause(), menu_context_upper_btn_right=icons.icon_svg_stop())
        return menu_upper + "<hr>"

    def status_display_lower(self, printer_status, 
                            ext_temp_actual, 
                            ext_temp_target, 
                            ext_temp_status, 
                            ext_temp_state, 
                            bed_temp_actual, 
                            bed_temp_target, 
                            bed_temp_status,
                            bed_temp_state):
        status_lower = ""
        ext_display = ""
        bed_display = ""
        status_msg = ""
        views = Views
        
        if printer_status in activity_state_1:
            ext_display = "" 
            bed_display = ""
            status_msg = views.status_display_lower_msg()
        elif printer_status in activity_state_2 or printer_status in activity_state_4:
            ext_display = views.status_display_lower_ext(ext_temp_actual=ext_temp_actual, 
                                                        ext_temp_status=ext_temp_status, 
                                                        ext_temp_state= ext_temp_state)
            bed_display = views.status_display_lower_bed(bed_temp_actual=bed_temp_actual,
                                                        bed_temp_status=bed_temp_status, 
                                                        bed_temp_state=bed_temp_state) #10-22-22: change to bed clear toggle
            status_msg = ""
        elif printer_status in activity_state_3:
            ext_display = views.status_display_lower_ext_emphasis(ext_temp_actual=ext_temp_actual, 
                                                                ext_temp_target=ext_temp_target, 
                                                                ext_temp_status=ext_temp_status, 
                                                                ext_temp_state= ext_temp_state)
            bed_display = views.status_display_lower_bed_emphasis(bed_temp_actual=bed_temp_actual, 
                                                                bed_temp_target=bed_temp_target, 
                                                                bed_temp_status=bed_temp_status, 
                                                                bed_temp_state=bed_temp_state)
            status_msg = ""
            
        status_lower = ext_display + bed_display + status_msg
        return status_lower

    def menu_context_lower(self, printer_status):
        menu_lower = ""
        buttons = Buttons
        
        if printer_status in activity_state_1:
            menu_lower = buttons.printer_connect()
        elif printer_status in activity_state_2 or printer_status in activity_state_4:
            menu_lower = "" #10-22-22: change to bed clear toggle
        elif printer_status in activity_state_3:
            menu_lower = "" #11-23-22: remain empty, devoid of light
        return menu_lower

@app.route('/display', methods=['GET'])
def display_final():
    #process_duration_init = time.process_time()
    #timed_operations(floor(process_duration_init))
    printer = printer_connection(endpoint=endpoint, X_Api_Key=X_Api_Key)
    ext_data = printer.ext_data() 
    bed_data = printer.bed_data()
    job_data = printer.job_data()
    printer_status = printer.printer_status(ext_data=ext_data, 
                                            bed_data=bed_data,
                                            job_data=job_data)

    components = component_sort()
    status_display_upper_data = components.status_display_upper(printer_status=printer_status, job_progress=job_data['job_progress'], job_time=job_data['job_time'])
    menu_context_upper_data = components.menu_context_upper(printer_status=printer_status)
    status_display_lower_data = components.status_display_lower(printer_status=printer_status, 
                                                    ext_temp_actual=ext_data["ext_temp_actual"],
                                                    ext_temp_target=ext_data["ext_temp_target"],
                                                    ext_temp_status=ext_data["ext_temp_status"],
                                                    ext_temp_state=ext_data["ext_temp_state"],
                                                    bed_temp_actual=bed_data["bed_temp_actual"],
                                                    bed_temp_target=bed_data["bed_temp_target"],
                                                    bed_temp_status=bed_data["bed_temp_status"],
                                                    bed_temp_state=bed_data["bed_temp_state"])
    menu_context_lower_data = components.menu_context_lower(printer_status=printer_status)

    return render_template("test_display.html",
                           raw_data_diagnostic=(ext_data,bed_data,job_data,printer_status),
                           status_display_upper=status_display_upper_data, 
                           menu_context_upper=menu_context_upper_data, 
                           status_display_lower=status_display_lower_data,
                           menu_context_lower=menu_context_lower_data)

@app.route('/action', methods=['GET']) #/action?printerstatus={printer_status}&btnregion={btn_region}&btnaction={btn_action}
def event_button():
    printer = printer_connection(endpoint=endpoint, X_Api_Key=X_Api_Key)
    printer_status = str(request.args.get('printerstatus'))
    btn_region = str(request.args.get('btnregion'))
    btn_action = str(request.args.get('btnaction'))
    btn_input = {
        'printer_status': printer_status,
        'btn_region': btn_region,
        'btn_action': btn_action
    }

    print(btn_input)
    printer.printer_btn_press(btn_input=btn_input)        
    return redirect("http://127.0.0.1:5002/display")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002, debug=True)