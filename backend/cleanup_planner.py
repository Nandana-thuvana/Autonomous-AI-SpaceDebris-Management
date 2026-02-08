def generate_cleanup_plan(orbital_params):
    sma, ecc, inc, raan, argp, ma = orbital_params
    plan = []
    orbit_type = ""

    if sma < 20000:
        orbit_type = "LEO (Low Earth Orbit)"
    elif sma < 35786:
        orbit_type = "MEO (Medium Earth Orbit)"
    else:
        orbit_type = "GEO (Geostationary Orbit)"

    if orbit_type.startswith("LEO"):
        plan.extend([
            "Track debris using ground radar and AI-based motion prediction.",
            "Deploy debris-removal microsatellite with drag sail and capture net.",
            "Perform autonomous rendezvous using vision-based navigation.",
            "Capture debris using net or robotic arm.",
            "Stabilize tumbling debris using onboard thrusters.",
            "Deploy drag sail to increase atmospheric drag.",
            "Allow controlled orbital decay and burn-up in Earth's atmosphere.",
            "Monitor re-entry to ensure safe disintegration."
        ])
    elif orbit_type.startswith("MEO"):
        plan.extend([
            "Catalog debris using optical telescopes and AI orbit analysis.",
            "Launch robotic servicer spacecraft with ion propulsion.",
            "Perform autonomous rendezvous and proximity operations.",
            "Capture debris using robotic manipulator or docking system.",
            "Stabilize and align debris center of mass.",
            "Execute controlled de-orbit burn toward Earth’s atmosphere.",
            "Guide debris into safe atmospheric re-entry corridor.",
            "Return servicer for multi-debris mission reuse."
        ])
    else:
        plan.extend([
            "Track GEO debris using ground optical systems and AI risk prioritization.",
            "Deploy space tug with high-efficiency ion thrusters.",
            "Perform long-distance autonomous rendezvous.",
            "Identify grappling points using AI vision system.",
            "Capture debris using robotic arm or tentacle gripper.",
            "Dampen rotational motion of debris.",
            "Transfer debris ~300 km above GEO into graveyard orbit.",
            "Release debris safely and return tug for next mission."
        ])

    if ecc > 0.2:
        plan.append("High eccentricity detected: perform preliminary orbit stabilization before capture.")
    if inc > 30:
        plan.append("High inclination: allocate additional fuel for plane-change maneuvers.")

    mission = f"ORBIT TYPE: {orbit_type}\n\nDETAILED CLEAN-UP MISSION PLAN:\n"
    for i, step in enumerate(plan, start=1):
        mission += f"{i}. {step}\n"

    return mission
