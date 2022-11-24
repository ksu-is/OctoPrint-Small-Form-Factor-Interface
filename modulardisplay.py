from math import floor
import requests 
import json
import os
import time
from flask import Flask, render_template, request, url_for, redirect
import concurrent.futures as cf
import datetime as dt
from htmlbits import Buttons, Views
from datamodels import DataModels

app=Flask(__name__)

activity_state_1 = ["Offline"]
activity_state_2 = ["Inactive"]
activity_state_3 = ["Printing", "Operational", "Paused"]
activity_state_4 = ["Complete", "Stopped"]

endpoint = "127.0.0.1:5000"
X_Api_Key = "60F9D39D7BED47E793A89BA01156B141" #only works for local instance

class printer_connection():
    def __init__(self, endpoint, X_Api_Key):
        self._endpoint = endpoint
        self._X_Api_Key = X_Api_Key
        os.environ["NO_PROXY"] = "127.0.0.1"
        
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
    
    def job_data(self):
        job_data_raw = self.printer_job_get()
        job_data_processed = {}
        
        job_time = ''
        job_progress = ''
        job_state = ''
        
        if job_data_raw != {}:
            job_data_raw_job = job_data_raw['printer_job_get_job']
            job_data_raw_progress = job_data_raw['printer_job_get_progress']
            job_data_raw_state = job_data_raw['printer_job_get_state']
            
            job_time = job_data_raw_job['estimatedPrintTime']
            job_progress = job_data_raw_progress['completion']
            job_state = job_data_raw_state
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
                        if job_data['job_progress'] <= 0.5 and job_data['job_state'] != 'Paused':
                            return "Starting"
                        elif job_data['job_progress'] > 0.5 and job_data['job_progress'] < 100 and job_data['job_state'] != 'Paused':
                            return "Printing"
                        elif job_data['job_progress'] == 100 and job_data['job_state'] != 'Paused':
                            return "Complete"
                    else:
                        return "Paused"
                else:
                    return "Stopped"
            else:
                return "Inactive"
        else:
            return "Offline"

class component_sort():
    def status_display_upper(self, printer_status):
        status_upper = ""
        views = Views
        
        if printer_status in activity_state_1 or printer_status in activity_state_2:
            status_upper = views.status_display_upper_emphasis(printer_status)
        elif printer_status in activity_state_3 or printer_status in activity_state_4:
            status_upper = views.status_display_upper(printer_status)
        return status_upper

    def menu_context_upper(self, printer_status):
        menu_upper = ""
        buttons = Buttons

        if printer_status in activity_state_1:
            menu_upper = "" #10-22-22: remains empty, devoid of light
        elif printer_status in activity_state_2 or printer_status in activity_state_4:
            menu_upper = buttons.bed_clear() #10-22-22: change to bed clear toggle
        elif printer_status in activity_state_3:
            menu_upper = buttons.job_operations() #10-22-22: change to job operations shortcuts    
        return menu_upper

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
        views = Views
        
        if printer_status in activity_state_1:
            ext_display = "" 
            bed_display = ""
        elif printer_status in activity_state_2 or printer_status in activity_state_4:
            ext_display = views.status_display_lower_ext(ext_temp_actual=ext_temp_actual, 
                                                        ext_temp_status=ext_temp_status, 
                                                        ext_temp_state= ext_temp_state)
            bed_display = views.status_display_lower_bed(bed_temp_actual=bed_temp_actual,
                                                        bed_temp_status=bed_temp_status, 
                                                        bed_temp_state=bed_temp_state) #10-22-22: change to bed clear toggle
        elif printer_status in activity_state_3:
            ext_display = views.status_display_lower_ext_emphasis(ext_temp_actual=ext_temp_actual, 
                                                                ext_temp_target=ext_temp_target, 
                                                                ext_temp_status=ext_temp_status, 
                                                                ext_temp_state= ext_temp_state)
            bed_display = views.status_display_lower_bed_emphasis(bed_temp_actual=bed_temp_actual, 
                                                                bed_temp_target=bed_temp_target, 
                                                                bed_temp_status=bed_temp_status, 
                                                                bed_temp_state=bed_temp_state)
            
        status_lower = ext_display + bed_display
        return status_lower

    def menu_context_lower(self, printer_status):
        menu_lower = ""
        
        if printer_status in activity_state_1:
            menu_lower = "" 
        elif printer_status in activity_state_2 or printer_status in activity_state_4:
            menu_lower = "" #10-22-22: change to bed clear toggle
        elif printer_status in activity_state_3:
            menu_lower = "" #11-23-22: remain empty, devoid of light
        return menu_lower

endpoint = "127.0.0.1:5000"
X_Api_Key = "60F9D39D7BED47E793A89BA01156B141"

@app.route('/octoprint/display', methods=['GET', 'POST'])
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
    status_display_upper_data = components.status_display_upper(printer_status=printer_status)
    menu_context_upper_data = components.menu_context_upper(printer_status=printer_status)
    status_display_lower_data = components.status_display_lower(printer_status=printer_status, 
                                                    ext_temp_actual= ext_data["ext_temp_actual"],
                                                    ext_temp_target= ext_data["ext_temp_target"],
                                                    ext_temp_status= ext_data["ext_temp_status"],
                                                    ext_temp_state= ext_data["ext_temp_state"],
                                                    bed_temp_actual=bed_data["bed_temp_actual"],
                                                    bed_temp_target=bed_data["bed_temp_target"],
                                                    bed_temp_status=bed_data["bed_temp_status"],
                                                    bed_temp_state=bed_data["bed_temp_state"])
    menu_context_lower_data = components.menu_context_lower(printer_status=printer_status)

    return render_template("test_display.html", 
                           status_display_upper=status_display_upper_data, 
                           menu_context_upper=menu_context_upper_data, 
                           status_display_lower=status_display_lower_data,
                           menu_context_lower=menu_context_lower_data)

@app.route('/octoprint/<button_region>/<button_id>', methods=['GET'])
def button_action():
    return redirect("http://127.0.0.1:5002/octoprint/display")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002, debug=True)
