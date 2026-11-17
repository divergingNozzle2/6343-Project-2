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

# First Cruise Phase (cruise1)
cruise1_optimize_mach = False
cruise1_optimize_alt = False
cruise1_mach_guess = (0.78, 0.78)
cruise1_mach_bounds = (0.77, 0.79)
cruise1_alt_guess = (35000, 35000)
cruise1_alt_bounds = (35000, 41000)
cruise1_duration_bounds = (100, 1000)

# Second Climb Phase (climb2)
climb2_optimize_mach = False
climb2_optimize_alt = False
climb2_mach_guess = (0.78, 0.78)
climb2_mach_bounds = (0.77, 0.79)
climb2_alt_guess = (35000, 37000)
climb2_alt_bounds = (35000, 41000)
climb2_duration_bounds = (10, 250) # how did they choose these bounds

# Second Cruise Phase (cruise2)
cruise2_optimize_mach = False
cruise2_optimize_alt = False
cruise2_mach_guess = (0.78, 0.78)
cruise2_mach_bounds = (0.77, 0.79)
cruise2_alt_guess = (37000, 37000)
cruise2_alt_bounds = (35000, 41000)
cruise2_duration_bounds = (100, 1000)

# Descent Phase (descent1)
descent1_optimize_mach = False
descent1_optimize_alt = False
descent1_mach_guess = (0.78, 0.3)
descent1_mach_bounds = (0.29, 0.79)
descent1_alt_guess = (37000, 0)
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
# Generate initial time bounds for each phase
climb1_time_initial_bounds = (0, 0)

cruise1_time_initial_bounds = (
    climb1_time_initial_bounds[0] + climb1_duration_bounds[0],
    climb1_time_initial_bounds[1] + climb1_duration_bounds[1],
)

climb2_time_initial_bounds = (
    cruise1_time_initial_bounds[0] + cruise1_duration_bounds[0],
    cruise1_time_initial_bounds[1] + cruise1_duration_bounds[1],
)

cruise2_time_initial_bounds = (
    climb2_time_initial_bounds[0] + climb2_duration_bounds[0],
    climb2_time_initial_bounds[1] + climb2_duration_bounds[1],
)

descent1_time_initial_bounds = (
    cruise2_time_initial_bounds[0] + cruise2_duration_bounds[0],
    cruise2_time_initial_bounds[1] + cruise2_duration_bounds[1],
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
    "climb2": {
            "subsystem_options": {"core_aerodynamics": {"method": "computed"}},
            "user_options": {
                "num_segments": 5,
                "order": 3,
                "mach_optimize": climb2_optimize_mach,
                "mach_initial": (climb2_mach_guess[0], "unitless"),
                "mach_final": (climb2_mach_guess[1], "unitless"),
                "mach_bounds": (climb2_mach_bounds, "unitless"),
                "mach_polynomial_order": 3,
                "altitude_optimize": climb2_optimize_alt,
                "altitude_initial": (climb2_alt_guess[0], "ft"),
                "altitude_final": (climb2_alt_guess[1], "ft"),
                "altitude_bounds": (climb2_alt_bounds, "ft"),
                "altitude_polynomial_order": 3,
                "throttle_enforcement": "path_constraint",
                "time_initial_bounds": (climb2_time_initial_bounds, "min"),
                "time_duration_bounds": (climb2_duration_bounds, "min"),
            },
        },
     "cruise2": {
            "subsystem_options": {"core_aerodynamics": {"method": "computed"}},
            "user_options": {
                "num_segments": 5,
                "order": 3,
                "mach_optimize": cruise2_optimize_mach,
                "mach_initial": (cruise2_mach_guess[0], "unitless"),
                "mach_final": (cruise2_mach_guess[1], "unitless"),
                "mach_bounds": (cruise2_mach_bounds, "unitless"),
                "mach_polynomial_order": 3,
                "altitude_optimize": cruise2_optimize_alt,
                "altitude_initial": (cruise2_alt_guess[0], "ft"),
                "altitude_final": (cruise2_alt_guess[1], "ft"),
                "altitude_bounds": (cruise2_alt_bounds, "ft"),
                "altitude_polynomial_order": 3,
                "throttle_enforcement": "boundary_constraint",
                "time_initial_bounds": (cruise2_time_initial_bounds, "min"),
                "time_duration_bounds": (cruise2_duration_bounds, "min"),
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

print("\n--- FINAL AIRCRAFT SIZING RESULTS ---")

variables = {
    "Gross Mass": ("aircraft:design:gross_mass", "lbm"),
    "Wing Area": ("aircraft:wing:area", "ft**2"),
    "Total Thrust": ("aircraft:propulsion:total_scaled_sls_thrust", "lbf"),
    "Wing Aspect Ratio": ("aircraft:wing:aspect_ratio", "unitless"),
    "Design Range": ("mission:range", "nmi"),
    "Mission Fuel Mass": ("mission:fuel_mass", "lbm"),
}

for label, (variable, units) in variables.items():
    try:
        value = prob.get_val(variable, units=units)
        print(f"{label}: {value.item():,.4f} {units}")
    except (KeyError, RuntimeError, ValueError) as error:
        print(f"{label}: Not found ({error})")
print("\n--- MISSION PHASE DISTANCES ---")

phases = [
    "climb1",
    "cruise1",
    "climb2",
    "cruise2",
    "descent1",
    "res_cruise",
    "res_hold",
]

for phase in phases:
    try:
        distance = prob.get_val(
            f"traj.{phase}.timeseries.distance",
            units="nmi"
        )

        segment_distance = distance[-1].item() - distance[0].item()

        print(f"{phase:<15}: {segment_distance:,.2f} nmi")

    except (KeyError, RuntimeError, ValueError) as error:
        print(f"{phase}: Not found ({error})")

# masses of individual components
print("\n--- MASS BREAKDOWN (% of gross mass) ---")

def mass(name):
    """Get a mass from the model in lbm, summed over engine types if it's an array."""
    return prob.get_val(name, units="lbm").sum()

gross = mass("aircraft:design:gross_mass")

# Nacelle mass in Aviary is per nacelle, so multiply by the number of engines
try:
    n_eng = prob.aviary_inputs.get_val("aircraft:engine:num_engines")
    nacelle_total = float((prob.get_val("aircraft:nacelle:mass", units="lbm") * n_eng).sum())
except Exception:
    nacelle_total = mass("aircraft:nacelle:mass")
    print("(Warning: couldn't read engine count; nacelle shown per nacelle)")

# (label, mass in lbm, reference %) -- reference % taken from the assignment table
groups = [
    ("STRUCTURE", [
        ("Wing",             mass("aircraft:wing:mass"),                 9.51),
        ("Horizontal Tail",  mass("aircraft:horizontal_tail:mass"),      0.94),
        ("Vertical Tail",    mass("aircraft:vertical_tail:mass"),        0.58),
        ("Fuselage",         mass("aircraft:fuselage:mass"),            10.62),
        ("Landing Gear",     mass("aircraft:landing_gear:total_mass"),   4.09),
        ("Nacelle",          nacelle_total,                              0.88),
    ], ("Structure Total", mass("aircraft:design:structure_mass"), 26.62)),

    ("PROPULSION", [
        ("Engines",          mass("aircraft:propulsion:total_engine_mass"),          9.26),
        ("Thrust Reversers", mass("aircraft:propulsion:total_thrust_reversers_mass"), 0.00),
        ("Misc. Systems",    mass("aircraft:propulsion:total_misc_mass"),            0.00),
        ("Fuel System",      mass("aircraft:fuel:fuel_system_mass"),                 0.54),
    ], ("Propulsion Total", mass("aircraft:propulsion:mass"), 9.80)),

    ("SYSTEMS AND EQUIPMENT", [
        ("Surface Controls", mass("aircraft:wing:surface_control_mass"), 1.02),
        ("Auxiliary Power",  mass("aircraft:apu:mass"),                  0.51),
        ("Instruments",      mass("aircraft:instruments:mass"),          0.00),
        ("Hydraulics",       mass("aircraft:hydraulics:mass"),           0.68),
        ("Electrical",       mass("aircraft:electrical:mass"),           1.16),
        ("Avionics",         mass("aircraft:avionics:mass"),             0.71),
        ("Furnishings",      mass("aircraft:furnishings:mass"),         10.89),
        ("Air Conditioning", mass("aircraft:air_conditioning:mass"),     0.74),
        ("Anti-Icing",       mass("aircraft:anti_icing:mass"),           0.00),
    ], ("Systems and Equipment Total", mass("aircraft:design:systems_and_equipment_mass"), 15.71)),
]

header = f"{'Component':<30}{'Mass [lbm]':>14}{'% Gross':>10}{'Ref %':>9}{'Diff':>8}"
line = "-" * len(header)

def row(label, m, ref):
    pct = 100 * m / gross
    return f"{label:<30}{m:>14,.2f}{pct:>10.2f}{ref:>9.2f}{pct - ref:>+8.2f}"

print(f"Gross mass: {gross:,.2f} lbm\n")
print(header)
print(line)
for group_name, items, (total_label, total_mass, total_ref) in groups:
    for label, m, ref in items:
        print(row(label, m, ref))
    print(row(total_label, total_mass, total_ref))
    # Sanity check: components should add up to Aviary's own total
    comp_sum = sum(m for _, m, _ in items)
    if abs(comp_sum - total_mass) > 1.0:
        print(f"  (note: listed components sum to {comp_sum:,.2f} lbm; "
              f"difference {total_mass - comp_sum:,.2f} lbm is from items not listed)")
    print(line)

print(row("Empty Mass", mass("aircraft:design:empty_mass"), 52.13))
print(line)
