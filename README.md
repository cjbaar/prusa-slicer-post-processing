# prusa-slicer-post-processing
Scripts for post processing of generated g-code files

#### mmu-wipe-fix
Removes extra moves at the end of the wipe tower when using PrusaSlicer with MMU models. This prevents small under-extrusions at the beginning of each new filament path.
`./mmu-wipe-fix.py {filename.gcode}`
