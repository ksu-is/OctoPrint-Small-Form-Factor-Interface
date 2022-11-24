# OctoPrint Small Form Factor Interface (SFFI)
A small form factor touchscreen interface for 3D printers, enabling users to more easily view, start, stop, and pause 3D print jobs.

## Sprints

### Sprint 1 (11/10/2022; <em>as submitted, 11/15/2022</em>)
1. ~~Develop a project topic~~
2. ~~Create a project README~~
3. ~~Establish a project timeline~~

### Sprint 2
1. Assess viability of Flask server connected to OctoPrint running on Ubuntu Frame
2. ~~Initial view-only functionality of interface (working through quirks of OctoPrint API, Flask routes, and Jinja templating)~~
3. Initial test of job commands to printer (with a jupyter notebook)

### Sprint 3
1. Adding job start commands to interface
2. Adding input functionality to job command buttons (play, pause, stop)
3. Test integration on Ubuntu Frame (with remote OctoPrint and localhost OPSFFI Flask instance)
4. 3D printing hardware prototypes of touchscreen & Pi mounting hardware

### Final Product (hopefully)
A proof-of-concept test integration (read: demo) running on a printer that can start, track, and manage a print job.
