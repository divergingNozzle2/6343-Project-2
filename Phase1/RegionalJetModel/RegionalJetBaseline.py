### Regional Jet Baseline with Discontinuous Reserve Mission

import aviary.api as av
import os

# This will assume that the vehicle CSV is in the same folder as this script, but should be adapted to point to the true location as appropriate
file_dir = os.path.dirname(__file__)
aircraft_data = os.path.join(file_dir, "RegionalJet.csv")
optimizer = "IPOPT"
max_iter = 50
objective_setting = "hybrid_objective"

## Define desired mission settings
design_mission_target_range = 2850

# Initial Climb Phase (climb1)
climb1_optimize_mach = False
climb1_optimize_alt = False
climb1_mach_guess = (0.3, 0.78)
climb1_mach_bounds = (0.29, 0.81)
climb1_alt_guess = (0, 35000)
climb1_alt_bounds = (0, 41000)
climb1_duration_bounds = (10, 250)

# Cruise Phase (cruise1)
cruise1_optimize_mach = False
cruise1_optimize_alt = False
cruise1_mach_guess = (0.78, 0.78)
cruise1_mach_bounds = (0.77, 0.79)
cruise1_alt_guess = (35000, 35000)
cruise1_alt_bounds = (35000, 41000)
cruise1_duration_bounds = (100, 1000)

# Descent Phase (descent1)
descent1_optimize_mach = False
descent1_optimize_alt = False
descent1_mach_guess = (0.78, 0.3)
descent1_mach_bounds = (0.29, 0.79)
descent1_alt_guess = (35000, 0)
descent1_alt_bounds = (0, 41000)
descent1_duration_bounds = (20, 100)

# Reserve Cruise Distance Phase (res_cruise)
res_cruise_optimize_mach = False
res_cruise_optimize_alt = False
res_cruise_mach_guess = (0.78, 0.78)
res_cruise_mach_bounds = (0.77, 0.79)
res_cruise_alt_guess = (39000, 39000)
res_cruise_alt_bounds = (35000, 39000)
res_cruise_duration_bounds = (5, 1000)
res_cruise_target_distance = 200

# Reserve Cruise Hold Phase (res_hold)
res_hold_optimize_mach = False
res_hold_optimize_alt = False
res_hold_mach_guess = (0.78, 0.78)
res_hold_mach_bounds = (0.77, 0.79)
res_hold_alt_guess = (39000, 39000)
res_hold_alt_bounds = (35000, 41000)
res_hold_duration_bounds = (25, 35)
res_hold_time_duration = 30

# Generate initial bounds on the initial times for each segment based on the declared segment durations
climb1_time_initial_bounds = (0, 0)
cruise1_time_initial_bounds = (
    climb1_time_initial_bounds[0] + climb1_duration_bounds[0],
    climb1_time_initial_bounds[1] + climb1_duration_bounds[1],
)
descent1_time_initial_bounds = (
    cruise1_time_initial_bounds[0] + cruise1_duration_bounds[0],
    cruise1_time_initial_bounds[1] + cruise1_duration_bounds[1],
)

res_cruise_time_initial_bounds = (
    descent1_time_initial_bounds[0] + descent1_duration_bounds[0],
    descent1_time_initial_bounds[1] + descent1_duration_bounds[1],
)
res_hold_time_initial_bounds = (
    res_cruise_time_initial_bounds[0] + res_cruise_duration_bounds[0],
    res_cruise_time_initial_bounds[1] + res_cruise_duration_bounds[1],
)


## Pack mission settings into phase info for Aviary problem
phase_info = {
    "pre_mission": {"include_takeoff": True, "optimize_mass": True},
    "climb1": {
        "subsystem_options": {"core_aerodynamics": {"method": "computed"}},
        "user_options": {
            "num_segments": 5,
            "order": 3,
            "mach_optimize": climb1_optimize_mach,
            "mach_initial": (climb1_mach_guess[0], "unitless"),
            "mach_final": (climb1_mach_guess[1], "unitless"),
            "mach_bounds": (climb1_mach_bounds, "unitless"),
            "mach_polynomial_order": 3,
            "altitude_optimize": climb1_optimize_alt,
            "altitude_initial": (climb1_alt_guess[0], "ft"),
            "altitude_final": (climb1_alt_guess[1], "ft"),
            "altitude_bounds": (climb1_alt_bounds, "ft"),
            "altitude_polynomial_order": 3,
            "throttle_enforcement": "path_constraint",
            "time_initial_bounds": (climb1_time_initial_bounds, "min"),
            "time_duration_bounds": (climb1_duration_bounds, "min"),
        },
    },
    "cruise1": {
        "subsystem_options": {"core_aerodynamics": {"method": "computed"}},
        "user_options": {
            "num_segments": 5,
            "order": 3,
            "mach_optimize": cruise1_optimize_mach,
            "mach_initial": (cruise1_mach_guess[0], "unitless"),
            "mach_final": (cruise1_mach_guess[1], "unitless"),
            "mach_bounds": (cruise1_mach_bounds, "unitless"),
            "mach_polynomial_order": 3,
            "altitude_optimize": cruise1_optimize_alt,
            "altitude_initial": (cruise1_alt_guess[0], "ft"),
            "altitude_final": (cruise1_alt_guess[1], "ft"),
            "altitude_bounds": (cruise1_alt_bounds, "ft"),
            "altitude_polynomial_order": 3,
            "throttle_enforcement": "boundary_constraint",
            "time_initial_bounds": (cruise1_time_initial_bounds, "min"),
            "time_duration_bounds": (cruise1_duration_bounds, "min"),
        },
    },
    "descent1": {
        "subsystem_options": {"core_aerodynamics": {"method": "computed"}},
        "user_options": {
            "num_segments": 5,
            "order": 3,
            "mach_optimize": descent1_optimize_mach,
            "mach_initial": (descent1_mach_guess[0], "unitless"),
            "mach_final": (descent1_mach_guess[1], "unitless"),
            "mach_bounds": (descent1_mach_bounds, "unitless"),
            "mach_polynomial_order": 3,
            "altitude_optimize": descent1_optimize_alt,
            "altitude_initial": (descent1_alt_guess[0], "ft"),
            "altitude_final": (descent1_alt_guess[1], "ft"),
            "altitude_bounds": (descent1_alt_bounds, "ft"),
            "altitude_polynomial_order": 3,
            "time_initial_bounds": (descent1_time_initial_bounds, "min"),
            "time_duration_bounds": (descent1_duration_bounds, "min"),
        },
    },
    "res_cruise": {
        "subsystem_options": {"core_aerodynamics": {"method": "computed"}},
        "user_options": {
            "reserve": True,
            "num_segments": 5,
            "order": 3,
            "mach_optimize": res_cruise_optimize_mach,
            "mach_initial": (res_cruise_mach_guess[0], "unitless"),
            "mach_final": (res_cruise_mach_guess[1], "unitless"),
            "mach_bounds": (res_cruise_mach_bounds, "unitless"),
            "mach_polynomial_order": 3,
            "altitude_optimize": res_cruise_optimize_alt,
            "altitude_initial": (res_cruise_alt_guess[0], "ft"),
            "altitude_final": (res_cruise_alt_guess[1], "ft"),
            "altitude_bounds": (res_cruise_alt_bounds, "ft"),
            "altitude_polynomial_order": 3,
            "throttle_enforcement": "boundary_constraint",
            "time_initial_bounds": (res_cruise_time_initial_bounds, "min"),
            "time_duration_bounds": (res_cruise_duration_bounds, "min"),
            "target_distance": (res_cruise_target_distance, "nmi"),
        },
    },
    "res_hold": {
        "subsystem_options": {"core_aerodynamics": {"method": "computed"}},
        "user_options": {
            "reserve": True,
            "num_segments": 5,
            "order": 3,
            "mach_optimize": res_hold_optimize_mach,
            "mach_initial": (res_hold_mach_guess[0], "unitless"),
            "mach_final": (res_hold_mach_guess[1], "unitless"),
            "mach_bounds": (res_hold_mach_bounds, "unitless"),
            "mach_polynomial_order": 3,
            "altitude_optimize": res_hold_optimize_alt,
            "altitude_initial": (res_hold_alt_guess[0], "ft"),
            "altitude_final": (res_hold_alt_guess[1], "ft"),
            "altitude_bounds": (res_hold_alt_bounds, "ft"),
            "altitude_polynomial_order": 3,
            "throttle_enforcement": "boundary_constraint",
            "time_initial_bounds": (res_hold_time_initial_bounds, "min"),
            "time_duration_bounds": (res_hold_duration_bounds, "min"),
            "time_duration": (res_hold_time_duration, "min"),
        },
    },
    "post_mission": {
        "include_landing": True,
        "constrain_range": True,
        "target_range": (design_mission_target_range, "nmi"),
    },
}

## Begin construction of Aviary Problem
prob = av.AviaryProblem()

# Add and check problem inputs
prob.load_inputs(aircraft_data, phase_info)
prob.check_and_preprocess_inputs(verbosity=2)

# Add mission definition to the problem
prob.add_pre_mission_systems(verbosity=2)
prob.add_phases(verbosity=3)
prob.add_post_mission_systems(verbosity=2)

# Link phases and variables
prob.link_phases(verbosity=2)

# Add driver to problem
prob.add_driver(optimizer=optimizer, max_iter=max_iter)

# Configure the OpenMDAO problem
prob.add_design_variables(verbosity=2)
prob.add_objective(objective_type=objective_setting)

# Finalize model configuration and setup
prob.setup()
prob.set_initial_guesses(verbosity=2)

# Run the configured problem
prob.run_aviary_problem(
    simulate=False,
    run_driver=True,
    suppress_solver_print=True,
    verbosity=3,
    make_plots=True,
)

#print output


# label, [variable names to try: new (1.0+) first, then older], units
results = [
    ("Gross Mass",         ["aircraft:design:gross_mass", "mission:design:gross_mass"], "lbm"),
    ("Wing Area",          ["aircraft:wing:area"],                                      "ft**2"),
    ("Total Thrust",       ["aircraft:propulsion:total_scaled_sls_thrust"],             "lbf"),
    ("Wing Aspect Ratio",  ["aircraft:wing:aspect_ratio"],                              "unitless"),
    ("Design Range",       ["aircraft:design:range", "mission:design:range"],           "NM"),
    ("Mission Fuel Mass",  ["mission:fuel_mass", "mission:summary:fuel_mass"],          "lbm"),
]

print("--- FINAL AIRCRAFT SIZING RESULTS ---")
for label, names, units in results:
    for name in names:
        try:
            val = prob.get_val(name, units=units).item()
            print(f"{label}: {val:,.4f} {units}")
            break
        except KeyError:
            continue
    else:
        print(f"{label}: not found")
