activity_state_1 = ["Offline"]
activity_state_2 = ["Inactive"]
activity_state_3 = ["Starting", "Printing", "Operational", "Paused"]
activity_state_4 = ["Complete", "Stopped"]

class Buttons:
    def job_operations(menu_context_upper_btn_left = '', menu_context_upper_btn_right = ''):
        return '<div class="btn-group" role="group" aria-label="Basic checkbox toggle button group" style="height: 80px; width: 100%;"><input type="checkbox" onclick='"location.href='/action?btnregion=upper&btnaction=pause';"' class="btn-check" id="menu-upper-button-pause" autocomplete="off"><label class="btn btn-outline-danger" for="menu-upper-button-pause">' + f'{menu_context_upper_btn_left}' + '</label><input type="checkbox" onclick='"location.href='/action?btnregion=upper&btnaction=stop';"' class="btn-check" id="menu-upper-button-stop" autocomplete="off"><label class="btn btn-outline-danger" for="menu-upper-button-stop">' + f'{menu_context_upper_btn_right}'+'</label></div>'

    def bed_clear():
        return '<label class="switch"><input type="checkbox"><span class="slider round"></span></label>'
    
    def printer_connect():
        return '<button type="button" class="btn btn-warning" onclick='"location.href='/action?btnregion=lower&btnaction=connect';"' style="height: 80px; width: 100%;"><a href="/action?btnregion=lower&btnaction=connect" style="text-decoration: none; color: black;"><h4>Connect to OctoPrint</h4></a></button>'
    
class Views:    
    def status_display_upper(printer_status):
        return f'<h2 class="display-2"><span style="font-weight:bold; font-size: 3rem;">{printer_status}</span></h2>'

    def status_display_upper_hybrid(printer_status, job_time):
        return f'<h2 class="display-2" style="font-weight:bold; font-size: 3rem;">{printer_status}; {job_time}</h2>'
    
    def status_display_upper_emphasis(printer_status):
        return f'<h2 class="display-1" style="font-weight:bold; font-size: 6rem;">{printer_status}</h2>'

    def status_display_upper_progress(job_progress):
        return f'<progress id="file" max="100" value={job_progress} style="height: 100px; width: 100%; text-align: center;">{job_progress}</progress>'
    
    def status_display_lower_msg():
        return f'<h2 class="display-2" style="font-weight:bold; font-size: 3rem;">Please reconnect to OctoPrint.</h2>'
    
    def status_display_lower_ext(ext_temp_actual, ext_temp_status, ext_temp_state):
        return f'<h3 class="display-1" style="font-size: 200%;">Extruder<br /><span style="font-weight:bold; font-size: 200%;">{ext_temp_actual}</span></h3><h3><span class="badge rounded-pill text-bg-dark">{ext_temp_status}</span>&nbsp;<span class="badge rounded-pill text-bg-dark">{ext_temp_state}</span></h3><br />'
    
    def status_display_lower_ext_emphasis(ext_temp_actual, ext_temp_target, ext_temp_status, ext_temp_state):
        return f'<h3 class="display-1" style="font-size: 300%;">Extruder<br /><span style="font-weight:bold; font-size: 200%;">{ext_temp_actual}</span><span>/{ext_temp_target}</span></h3><h3 style="font-size: 250%;"><span class="badge rounded-pill text-bg-dark">{ext_temp_status}</span>&nbsp;<span class="badge rounded-pill text-bg-dark">{ext_temp_state}</span></h3><br />'
    
    def status_display_lower_bed(bed_temp_actual, bed_temp_status, bed_temp_state):
        return f'<h3 class="display-1" style="font-size: 200%;">Bed<br /><span style="font-weight:bold; font-size: 200%;">{bed_temp_actual}</span></h3><h3><span class="badge rounded-pill text-bg-dark">{bed_temp_status}</span>&nbsp;<span class="badge rounded-pill text-bg-dark">{bed_temp_state}</span></h3><br />'
    
    def status_display_lower_bed_emphasis(bed_temp_actual, bed_temp_target, bed_temp_status, bed_temp_state):
        return f'<h3 class="display-1" style="font-size: 300%;">Bed<br /><span style="font-weight:bold; font-size: 200%;">{bed_temp_actual}</span><span>/{bed_temp_target}</span></h3><h3 style="font-size: 250%;"><span class="badge rounded-pill text-bg-dark">{bed_temp_status}</span>&nbsp;<span class="badge rounded-pill text-bg-dark">{bed_temp_state}</span></h3><br />'