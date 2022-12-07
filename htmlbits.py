class Buttons:
    def job_operations(printer_status):
        return rf'<div class="btn-group" role="group" aria-label="Basic checkbox toggle button group" style="height: 80px; width: 100%;"><input type="checkbox" onclick='"location.href='/action?btnregion=upper&btnaction=play';"' class="btn-check" id="menu-upper-button-play" autocomplete="off" checked> <label class="btn btn-outline-danger" for="menu-upper-button-play"><svg xmlns="http://www.w3.org/2000/svg" width="65" height="65" fill="currentColor" class="bi bi-play-circle" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M6.271 5.055a.5.5 0 0 1 .52.038l3.5 2.5a.5.5 0 0 1 0 .814l-3.5 2.5A.5.5 0 0 1 6 10.5v-5a.5.5 0 0 1 .271-.445z"/></svg></label><input type="checkbox" onclick='"location.href='/action?btnregion=upper&btnaction=pause';"' class="btn-check" id="menu-upper-button-pause" autocomplete="off"><label class="btn btn-outline-danger" for="menu-upper-button-pause"><svg xmlns="http://www.w3.org/2000/svg" width="65" height="65" fill="currentColor" class="bi bi-pause-circle" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M5 6.25a1.25 1.25 0 1 1 2.5 0v3.5a1.25 1.25 0 1 1-2.5 0v-3.5zm3.5 0a1.25 1.25 0 1 1 2.5 0v3.5a1.25 1.25 0 1 1-2.5 0v-3.5z"/></svg></label><input type="checkbox" onclick='"location.href='/action?btnregion=upper&btnaction=stop';"' class="btn-check" id="menu-upper-button-stop" autocomplete="off"><label class="btn btn-outline-danger" for="menu-upper-button-stop"><svg xmlns="http://www.w3.org/2000/svg" width="65" height="65" fill="currentColor" class="bi bi-stop-circle" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M5 6.5A1.5 1.5 0 0 1 6.5 5h3A1.5 1.5 0 0 1 11 6.5v3A1.5 1.5 0 0 1 9.5 11h-3A1.5 1.5 0 0 1 5 9.5v-3z"/></svg></label></div>'

    def bed_clear():
        return '<label class="switch"><input type="checkbox"><span class="slider round"></span></label>'
    
class Views:    
    def status_display_upper_emphasis(printer_status):
        return f'<h2 class="display-1" style="font-weight:bold; font-size: 6rem;">{printer_status}</h2>'

    def status_display_upper(printer_status):
        return f'<h2 class="display-2" style="font-weight:bold; font-size: 3rem;">{printer_status}</h2>'
    
    def status_display_lower_ext_emphasis(ext_temp_actual, ext_temp_target, ext_temp_status, ext_temp_state):
        return f'<h3 class="display-1" style="font-size: 300%;">Extruder<br /><span style="font-weight:bold; font-size: 200%;">{ext_temp_actual}</span><span>/{ext_temp_target}</span></h3><h3 style="font-size: 250%;"><span class="badge rounded-pill text-bg-dark">{ext_temp_status}</span>&nbsp;<span class="badge rounded-pill text-bg-dark">{ext_temp_state}</span></h3><br />'
    
    def status_display_lower_ext(ext_temp_actual, ext_temp_status, ext_temp_state):
        return f'<h3 class="display-1" style="font-size: 200%;">Extruder<br /><span style="font-weight:bold; font-size: 200%;">{ext_temp_actual}</span></h3><h3><span class="badge rounded-pill text-bg-dark">{ext_temp_status}</span>&nbsp;<span class="badge rounded-pill text-bg-dark">{ext_temp_state}</span></h3><br />'
    
    def status_display_lower_bed_emphasis(bed_temp_actual, bed_temp_target, bed_temp_status, bed_temp_state):
        return f'<h3 class="display-1" style="font-size: 300%;">Bed<br /><span style="font-weight:bold; font-size: 200%;">{bed_temp_actual}</span><span>/{bed_temp_target}</span></h3><h3 style="font-size: 250%;"><span class="badge rounded-pill text-bg-dark">{bed_temp_status}</span>&nbsp;<span class="badge rounded-pill text-bg-dark">{bed_temp_state}</span></h3><br />'
    
    def status_display_lower_bed(bed_temp_actual, bed_temp_status, bed_temp_state):
        return f'<h3 class="display-1" style="font-size: 200%;">Bed<br /><span style="font-weight:bold; font-size: 200%;">{bed_temp_actual}</span></h3><h3><span class="badge rounded-pill text-bg-dark">{bed_temp_status}</span>&nbsp;<span class="badge rounded-pill text-bg-dark">{bed_temp_state}</span></h3><br />'