How to to run a4.py

First when the code is run, the program will ask for an input:
    kb>

1. Enter "load a4_q2_kb.txt" to load the rules for the KB

    swerve <-- cut_off & close_distance & lane_empty
    slow_down <-- over_speed_limit
    apply_brake <-- car_ahead_stops
    apply_gas <-- car_moves_ahead & light_green
    honk <-- stupid_action_detected
    record <-- motion_detected_parked

2. tell the commands that are available - please double check the spelling

    ex) "tell cut_off"
        "tell car_ahead_stops"


3. After some tell commands, you can now "infer_all"

4. If new file is loaded, all previous tell commands and infers will be forgotten



Errors & Exceptions Applied:

1. load "file_name" - only loads file names that are available
2. tell _____ - will require a rule for the input after tell
3. infer_all will only work if rules are loaded and tell commands have been completed
4. Will let the user know if the atom has already been saved

