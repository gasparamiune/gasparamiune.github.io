# -*- coding: utf-8 -*-
"""Single source of content for the portfolio. Every fact here was checked against
the project repos, reports or verified CV facts (Nov 2026). Edit here, then run build.py."""

PERSON = dict(
    name="Gaspar Amiune",
    role="Mechatronics engineer · AI-native builder",
    tagline="I build real systems across mechanics, electronics and software, and I use AI agents every day to ship them.",
    intro=("Final-year BSc Mechatronics Engineering student at SDU Sønderborg (June 2027), founder of PourStock, "
           "and working at Danfoss in compressor failure analysis. Argentine and Italian, based in Denmark."),
    github="https://github.com/gasparamiune",
    location="Sønderborg, Denmark",
)

# Skill catalogue: id -> (label, group). Projects reference these ids, so the home page
# can count and filter by skill.
SKILLS = {
    "agents":   ("Claude Code & multi-agent workflows", "AI engineering"),
    "llmapi":   ("Claude API & LLM routing", "AI engineering"),
    "aigov":    ("AI rules, quality gates & review", "AI engineering"),
    "cv":       ("Computer vision (OpenCV, MediaPipe)", "AI engineering"),
    "python":   ("Python", "Software"),
    "ts":       ("TypeScript / React", "Software"),
    "sql":      ("PostgreSQL / Supabase", "Software"),
    "cicd":     ("CI, Docker & Linux deployment", "Software"),
    "web3d":    ("three.js & interactive web", "Software"),
    "cpp":      ("C / C++ on microcontrollers", "Embedded & control"),
    "control":  ("Control (PID, LQR)", "Embedded & control"),
    "fusion":   ("Sensor fusion & estimation", "Embedded & control"),
    "algo":     ("Path planning & algorithms", "Embedded & control"),
    "sil":      ("Software-in-the-loop testing", "Embedded & control"),
    "simulink": ("MATLAB / Simulink", "Embedded & control"),
    "cad":      ("Parametric CAD & rendering", "Mechanical & simulation"),
    "fea":      ("FEA (Ansys & scripted)", "Mechanical & simulation"),
    "cfd":      ("CFD", "Mechanical & simulation"),
    "pcb":      ("PCB design & bench testing", "Electronics"),
    "sysmeth":  ("Requirements, budgets & single source of truth", "Engineering method"),
    "lead":     ("Team leadership & integration", "Engineering method"),
    "product":  ("Product & go-to-market", "Engineering method"),
}

CATS = {
    "product": "Products & AI",
    "engineering": "Engineering",
    "university": "University",
}

PROJECTS = [
# ---------------------------------------------------------------- PourStock
dict(
    slug="pourstock", title="PourStock", cat="product", year="2026", featured=True,
    short="My startup: one operations app for restaurants, hotels and cafés, built from scratch with Claude Code.",
    status=("Live", "live"), role="Founder", team="Solo founder, AI coding agents",
    links=[("Live site", "https://www.pourstock.com", "live")],
    cover="pourstock/cover.webp", hero="pourstock/floor-merge.webp",
    intro=[
        "After 11 years working in restaurants and hotels, I built the tool I always wanted: floor plan and orders, "
        "kitchen screens, the bar, reception and housekeeping, stock, shift planning, forecasts and reports in one app. "
        "It is live at pourstock.com and in pilot use at a hotel in Denmark.",
        "I used Claude to build it from scratch. My work is the product, the architecture and the rules that keep "
        "AI-written code safe to ship to real staff on a real service night.",
    ],
    did=[
        "<b>AI constitution:</b> a written rulebook every coding agent must follow (tenant isolation, additive-only database changes, banned actions), with its key rules checked automatically on every change.",
        "<b>Quality gate:</b> unit tests, end-to-end browser tests and rule checks run on Linux CI before anything reaches a customer.",
        "<b>24/7 support agent:</b> staff report a problem on Telegram or in the app, Claude triages and answers on the same channel, and fixable bugs go to a coding agent whose fix must pass the tests.",
        "<b>Forecast-driven planning:</b> a Python demand-forecasting service (Docker) feeds the AI shift planner and a stock agent that drafts supplier orders for a manager to approve.",
        "<b>Load tests with 10 simulated venues:</b> completed steps rose from 58 % to 96 % after the fixes they pointed to.",
    ],
    how=[
        ("TypeScript + React", "the web app every role uses: floor, kitchen, bar, reception, stock and shifts."),
        ("PostgreSQL (Supabase)", "the data model, with row-level security so each venue only ever sees its own data."),
        ("Deno edge functions", "server-side logic and the calls to Claude, kept behind one shared helper."),
        ("Python", "the demand-forecasting service, packaged as a Docker container."),
        ("Playwright", "end-to-end tests that click through the app like a waiter would."),
    ],
    diagram="pourstock",
    videos=[
        ("pourstock/floor-merge.mp4", "Floor plan: merging tables during live service.", "pourstock/floor-merge.webp"),
        ("pourstock/forecasting.mp4", "Forecasting: expected covers per day and how sure the model is.", "pourstock/forecasting.webp"),
        ("pourstock/shifts.mp4", "AI shift planner: a full week generated, then tuned by the manager.", "pourstock/shifts.webp"),
        ("pourstock/kitchen.mp4", "Kitchen screen: courses fired and timed per table.", "pourstock/kitchen.webp"),
        ("pourstock/stock-payment.mp4", "Stock: sold drinks come off the stock count at payment.", "pourstock/stock-payment.webp"),
        ("pourstock/menu-editor.mp4", "Menu editor with ingredients and availability.", "pourstock/menu-editor.webp"),
    ],
    gallery=[
        ("pourstock/hotel-peek.webp", "Housekeeping: arrivals readiness and room status for the day."),
        ("pourstock/wine-pairing.webp", "Wine pairing suggestions shown with each course."),
        ("pourstock/pet-league.webp", "A small game layer: each venue's mascot climbs a league as the team uses the app."),
    ],
    skills=["agents", "aigov", "llmapi", "ts", "sql", "cicd", "python", "product"],
),
# ---------------------------------------------------------------- ARGUS
dict(
    slug="argus", title="ARGUS lunar rover", cat="university", year="2026", featured=True,
    short="A 20 kg lunar rover designed end to end by a team of nine students I led, with a drivable 3D test on the web.",
    status=("Live 3D test", "live"), role="Team lead and integrator", team="Nine engineering students, SDU",
    links=[("Drive it on the Moon", "https://gasparamiune.github.io/ARGus/surface-test/", "play"),
           ("Project site", "https://gasparamiune.github.io/ARGus/", "live")],
    cover="argus/01_deployed_driving.webp", hero="argus/03_at_station_APXS_down.webp",
    intro=[
        "ARGUS is the Space Systems Engineering project of SDU's fifth semester: a 20 kg rover that spends one "
        "equatorial lunar day studying how the soil would behave under a lander's plume, so future landing pads can be built from it. I led and coordinated a team of nine engineering "
        "students through the full design, and integrated the mechanical, thermal, power and software work.",
        "Every number in the project lives in one synchronized, well-architected source of truth. Mass, power and thermal "
        "budgets, tables, figures and the report are rebuilt from it, so a design change propagates everywhere at once. "
        "I used Claude agents to build the CAD generators, the checks and the documents under that system.",
    ],
    did=[
        "<b>Led the team of nine</b> from requirements to a reviewed design, and ran integration across all subsystems.",
        "<b>Single source of truth:</b> one Python model computes every budget; the report, tables and web pages are generated from it.",
        "<b>Revision system:</b> every design change gets a dated revision and is checked against the mass limit and margins.",
        "<b>Four-wheel rocker-differential</b> chassis, a lid-mounted solar array over a zenith radiator, stereo cameras and an APXS instrument.",
        "<b>Surface Test:</b> a browser game where you drive the current design on the Moon, switch revisions and inspect every part down to each screw.",
    ],
    how=[
        ("Python", "the budget model (mass, power, thermal, illumination) that every document reads from."),
        ("CadQuery + Blender scripts", "generate each part, the assembly and the renders from code."),
        ("JavaScript + three.js", "the Surface Test: real CAD meshes, a soil and slope model and live power figures."),
        ("XeLaTeX", "the report, rebuilt with numbers injected from the model."),
    ],
    code=("python", "budgets.py: the single source of truth (excerpt)", """# Single source of truth for every number quoted in the A1 report.
S_SOL   = 1361.0          # W/m^2  solar flux at the Moon
SIGMA   = 5.67e-8         # W/m^2K^4 Stefan-Boltzmann
G_MOON  = 1.62            # m/s^2
FLUX_VAR = 0.035          # +-3.5 % over the year
S_MAX   = S_SOL*(1+FLUX_VAR)   # thermal worst case  -> 1408.6 W/m2
S_MIN   = S_SOL*(1-FLUX_VAR)   # power worst case    -> 1313.4 W/m2
T_REG_HOT = (S_MAX/SIGMA)**0.25   # design hot case of the regolith""",
          "Design worst cases are derived, not typed in: the hot case drives thermal, the cold case drives power."),
    embed=("https://gasparamiune.github.io/ARGus/surface-test/", "ARGUS Surface Test: WASD to drive, switch design revisions, open any part."),
    gallery=[
        ("argus/01_deployed_driving.webp", "Deployed and driving, mast raised."),
        ("argus/02_stowed_in_0.5m_cube.webp", "Stowed inside its 0.5 m launch envelope."),
        ("argus/04_leg_closeup.webp", "Wheel and rocker close-up."),
        ("argus/05_internal_layout_cutaway.webp", "Internal layout cutaway."),
        ("argus/06_exploded_view.webp", "Exploded view of the assembly."),
        ("argus/inside_lower.webp", "Lower tier: battery, warm box, differential and drives, each labelled."),
        ("argus/inside_upper.webp", "Upper tier: compute, radio, cameras and the APXS head."),
        ("argus/wheel_before_after.webp", "A design revision: the wheel's spoke-to-hub joint before and after."),
    ],
    skills=["lead", "sysmeth", "cad", "python", "web3d", "agents"],
),
# ---------------------------------------------------------------- Micromouse
dict(
    slug="micromouse", title="Micromouse maze robot", cat="university", year="2025", featured=True,
    short="An autonomous maze-solving robot on an STM32H743. I wrote the firmware by hand in C/C++.",
    status=("Firmware + interactive demo", "built"), role="Firmware author", team="Semester project 3, team of seven",
    links=[("Play the floodfill demo", "../play/micromouse.html", "play")],
    cover="micromouse/m_060.webp", hero="micromouse/m_058.webp",
    intro=[
        "Micromouse is the classic robotics contest: a small robot must explore an unknown 16 × 16 maze, find the centre "
        "and then race there on the shortest path. Our team designed the mechanics, sensors and PCB; I wrote the firmware.",
        "The robot runs on an STM32H743 (480 MHz Cortex-M7) with N20 motors and magnetic encoders, two custom infrared "
        "side sensors and three ultrasonic sensors. The code is about 650 lines of my own C/C++ on the STM32 HAL.",
    ],
    did=[
        "<b>Classic floodfill solver:</b> every cell holds its step distance to the goal; one recomputation updates the whole map when a new wall is seen.",
        "<b>Dual PID control</b> of speed and heading, on top of a motion core with acceleration profiles.",
        "<b>Sensor fusion</b> of infrared and ultrasonic readings to detect walls reliably.",
        "<b>Speed run</b> with smooth diagonal-cut 90° turns and smooth 180° U-turns instead of stop-turn-go.",
    ],
    how=[
        ("C/C++ (STM32 HAL)", "motor control, encoders, PID loops and the maze logic, all on the microcontroller."),
        ("Breadth-first floodfill", "a queue-based distance map, which is optimal in cell steps and runs well under 1 ms."),
    ],
    code=("cpp", "Flood(): my floodfill implementation", """void Flood() {
  std::queue<pii> q;
  for (int i = 0; i < MAZE_SIZE; i++)
    for (int j = 0; j < MAZE_SIZE; j++) dist[i][j] = 65535;

  int goals[4][2] = {{7,7},{7,8},{8,7},{8,8}};
  for (int i = 0; i < 4; i++) {
    int x = goals[i][0], y = goals[i][1];
    dist[x][y] = 0;
    q.push({x, y});
  }

  while (!q.empty()) {
    auto [x, y] = q.front(); q.pop();
    for (int d = 0; d < 4; d++) {
      int nx = x + dx[d], ny = y + dy[d];
      if (nx < 0 || nx >= MAZE_SIZE || ny < 0 || ny >= MAZE_SIZE) continue;
      if (wall[x][y][d] == 1) continue;          // known wall
      if (dist[nx][ny] > dist[x][y] + 1) {
        dist[nx][ny] = dist[x][y] + 1;
        q.push({nx, ny});
      }
    }
  }
}""", "The mouse always moves to the open neighbour with the lowest distance, preferring straight, then sides, then back."),
    play=("../play/micromouse.html", "Watch this algorithm explore a random maze, step by step, in your browser."),
    gallery=[
        ("micromouse/m_060.webp", "Team CAD of the robot body and sensor mounts."),
        ("micromouse/m_058.webp", "Chassis and drive layout."),
        ("micromouse/m_004.webp", "Gear train between the N20 motors and the wheels."),
        ("micromouse/m_027.webp", "Team PCB layout around the STM32."),
        ("micromouse/m_024.webp", "Bench testing the infrared sensor circuit."),
        ("micromouse/m_048.webp", "Maze simulation used to test the solver before hardware."),
    ],
    skills=["cpp", "algo", "control", "fusion"],
),
# ---------------------------------------------------------------- Hedge agents
dict(
    slug="hedge-agents", title="Hedge agents", cat="product", year="2026", featured=True,
    short="Always-on trading agents in Python: ten agents score stocks and crypto, and only broad agreement raises a signal.",
    status=("Private code", "private"), role="Builder", team="Personal project",
    links=[],
    cover=None, hero=None,
    intro=[
        "A personal research system that watches markets on a schedule: a deep cycle once a day and an intraday cycle "
        "every 30 minutes on weekdays, both running on Linux in the cloud. Each agent looks at one angle "
        "(fundamentals, valuation, catalysts, institutional flow, moat, macro) and returns a normalised score.",
        "The idea is that no single signal is enough. A weighted engine merges the scores, and the top conviction tier "
        "needs several agents to agree plus a fresh written thesis from an LLM. Everything sits behind a safety layer.",
    ],
    did=[
        "<b>Ten agent modules</b> feeding one scoring engine; only two of them call an LLM.",
        "<b>Conviction tiers</b> (HIGH, MEDIUM, LOW, Watch) with explicit rules, so every decision can be traced.",
        "<b>Safety layer:</b> kill switch, maximum actions per day, heartbeat and a token-protected halt endpoint.",
        "<b>One LLM router</b> with budget caps and retry, so model costs and outages cannot run away.",
        "<b>Telegram alerts</b> and scheduled runs on GitHub Actions; the code stays private.",
    ],
    how=[
        ("Python", "agents, scoring engine, portfolio planner and the risk layer."),
        ("GitHub Actions (Linux cron)", "runs the daily and 30-minute cycles without a laptop."),
        ("LLM router", "one choke point for every model call, with budget caps."),
    ],
    diagram="hedge",
    code=("python", "conviction.py: how a tier is decided (excerpt)", """def _tier_for(agg, agreement, llm_conviction, has_required,
              llm_outage=False, llm_fresh_long=False) -> Tier:
    if not has_required:
        return Tier.WATCH
    for tier in (Tier.HIGH, Tier.MEDIUM, Tier.LOW):
        min_agg, min_agree, min_llm_conv = TIER_RULES[tier]
        if tier is Tier.HIGH and not llm_fresh_long:
            continue
        if llm_outage:
            # a HIGH position is never granted without a fresh LLM read
            if tier is Tier.HIGH:
                continue
            llm_ok = True
        else:
            llm_ok = (llm_conviction or 0.0) >= min_llm_conv
        if agg >= min_agg and agreement >= min_agree and llm_ok:
            return tier
    return Tier.WATCH""", "Graceful degradation: if the LLM is down, lower tiers still work, but the top tier is withheld."),
    gallery=[],
    skills=["python", "agents", "llmapi", "cicd", "sysmeth"],
),
# ---------------------------------------------------------------- ARGOS-H1
dict(
    slug="argos-h1", title="ARGOS-H1 engine", cat="engineering", year="2026", featured=True,
    short="A 500 N self-landing hybrid rocket engine and its C++ controller, designed with AI agents. Design and simulation only.",
    status=("Design & simulation only", "sim"), role="Designer", team="Personal project (the rocket airframe is my brother's)",
    links=[("Engineering package", "https://github.com/gasparamiune/p1-propulsion/tree/main/argos-engine", "code")],
    cover="engine/engine_section_labelled.webp", hero="engine/plume_artistic_side.webp",
    intro=[
        "The engine for my brother's ARGOS H1 rocket: a 500 N nitrous-oxide / ABS hybrid that must lift the rocket, "
        "throttle down and bring it back to an upright landing, steering with a two-axis gimbal.",
        "I did this interdisciplinary work on my own with AI agents: requirements, combustion, CAD, assembled-engine FEA, "
        "plume CFD and the controller firmware. Nothing has been built or fired; every number carries an evidence tag "
        "that says where it comes from.",
    ],
    did=[
        "<b>Requirements first:</b> engine requirements turned into firmware interfaces, and each release checked against them.",
        "<b>C++ controller firmware</b> for a Teensy 4.1 (ARM Cortex-M7): ignition, throttle, shutdown and relight lockout.",
        "<b>Software-in-the-loop:</b> every release tested against a simulated engine and reviewed independently.",
        "<b>Assembled-engine 3D FEA</b> with a margin for every part under every load case, plus plume CFD and landing Monte Carlo.",
        "<b>Found and fixed a real hazard:</b> a faulty seat-temperature sensor could fake the \"lit\" signal; the fix freezes and checks it through ignition.",
    ],
    how=[
        ("C++ (Teensy 4.1)", "the engine control unit: sequencing, sensor checks and fault handling."),
        ("C++ simulation (SIL)", "a model of the engine the firmware runs against before any hardware exists."),
        ("Python", "combustion sizing, FEA post-processing, Monte Carlo and the 161-page datasheet build."),
        ("CAD via SolidWorks MCP", "the engine part set, driven by agents and checked by the FEA."),
    ],
    videos=[("engine/plume_startup.mp4", "CFD of the exhaust plume during start-up.", "engine/plume_T_full.webp")],
    gallery=[
        ("engine/engine_iso.webp", "Engine assembly."),
        ("engine/engine_section_labelled.webp", "Labelled section: injector, combustion chamber, fuel grain and nozzle."),
            ("engine/plume_artistic_side.webp", "Artistic render (Blender) built from the CFD fields, with its own label: appearance only, not a measurement."),
        ("engine/plume_mach_near.webp", "Plume CFD: Mach number near the nozzle."),
        ("engine/plume_schlieren_near.webp", "Plume CFD: synthetic schlieren image of the shock structure."),
        ("engine/fea_max_thrust_vm.webp", "3D FEA at maximum thrust (von Mises stress)."),
        ("engine/fea_min_margins.webp", "Lowest margin of safety for every part across all load cases."),
        ("engine/landing_scatter.webp", "Landing Monte Carlo: touchdown speed and tilt over 500 dispersed runs."),
    ],
    skills=["cpp", "sil", "control", "cad", "fea", "cfd", "sysmeth", "agents"],
),
# ---------------------------------------------------------------- Waterjet
dict(
    slug="waterjet", title="P1-J electric waterjet", cat="engineering", year="2026",
    short="An inboard electric waterjet for a 2.3 m jet boat: sizing, parametric CAD, FEA and a 3D viewer. Designed, not yet built.",
    status=("Design in review", "sim"), role="Designer", team="Personal project for a private client",
    links=[("Live project site + 3D viewer", "https://gasparamiune.github.io/p1-propulsion/", "live"),
           ("Source", "https://github.com/gasparamiune/p1-propulsion", "code")],
    cover="waterjet/vista_perspectiva.webp", hero="waterjet/corte_lateral.webp",
    intro=[
        "A boat owner wanted an electric waterjet for his small jet boat. I redesigned his sketch so it can actually work: "
        "a flush intake fully ahead of the impeller, a stainless impeller driven directly by a water-cooled motor, a "
        "steerable nozzle and a mandatory reverse bucket, all under 50 V.",
        "The whole engineering package (calculations, parametric CAD, drawings, bill of materials, FEA and test plan) "
        "regenerates from one input file. The site is in Spanish and says honestly what the model shows and what only a water test can decide.",
    ],
    did=[
        "<b>Sizing model</b> for thrust against hull resistance, cavitation and battery endurance.",
        "<b>Parametric CAD</b> with automatic interference checks, drawings and a bill of materials.",
        "<b>FEA</b> of the intake, steering and reverse parts, with the weak point stated openly.",
        "<b>Honest recommendation:</b> the model shows the hull, not the propulsion, is the main risk, and that buying an off-the-shelf pump is cheaper.",
    ],
    how=[
        ("Python", "sizing, comparison of architectures (Monte Carlo), BOM and the site build."),
        ("CadQuery + Blender", "parametric parts, interference checks and renders."),
        ("JavaScript", "the 3D viewer on the project site: assembled, exploded and part by part."),
    ],
    embed=("https://gasparamiune.github.io/p1-propulsion/", "The live project site (Spanish), with the 3D viewer."),
    gallery=[
        ("waterjet/vista_perspectiva.webp", "Drive train in the hull: battery, motor, pump and nozzle."),
        ("waterjet/vista_lateral_marcha.webp", "Side view, nozzle straight, bucket up."),
        ("waterjet/vista_lateral_reversa.webp", "Reverse: bucket down."),
        ("waterjet/corte_lateral.png".replace(".png", ".webp"), "Centre-line section of the boat with the intake ahead of the impeller."),
        ("waterjet/fea_intake.webp", "FEA of the intake under load."),
        ("waterjet/fea_reverse.webp", "FEA of the reverse bucket."),
        ("waterjet/thrust_drag.webp", "Thrust against resistance: where the boat can and cannot plane."),
        ("waterjet/power_cavitation.webp", "Power and cavitation margin of the impeller."),
    ],
    skills=["cad", "fea", "python", "sysmeth", "web3d"],
),
# ---------------------------------------------------------------- Quantum book
dict(
    slug="quantum-book", title="Quantum Book", cat="product", year="2026",
    short="An interactive companion to my Quantum Physics course: explanations, simulations, 873 exercises and four exam bosses.",
    status=("Live", "live"), role="Builder", team="Personal study project",
    links=[("Open the book", "https://gasparamiune.github.io/quantum-physics-book/", "live"),
           ("Source", "https://github.com/gasparamiune/quantum-physics-book", "code")],
    cover="quantum/home.webp", hero="quantum/home.webp",
    intro=[
        "I turned a whole semester of Quantum Physics into a book I actually wanted to study from. Every course file was "
        "read page by page and turned into explanations, interactive explorations and practice with step-by-step hints.",
        "It ends with four \"final bosses\", one per exam topic: the infinite well, the oscillator, hydrogen and solids. "
        "It is an unofficial study aid, built with AI agents and checked by an independent computation of the answers.",
    ],
    did=[
        "<b>Coverage tracking:</b> every teaching item in the course is linked to an explanation, an exercise or a figure.",
        "<b>Answer checks:</b> final answers are verified by a second, independent computation.",
        "<b>Runs fully in the browser</b>: maths rendering, a calculator, notes and pen drawings saved locally.",
    ],
    how=[
        ("JavaScript", "the reader, exercises, simulations and progress tracking."),
        ("KaTeX + math.js", "maths typesetting and the built-in calculator."),
        ("Node build + Python (numpy, scipy, sympy)", "turns Markdown/YAML content into the site and checks the answers."),
    ],
    embed=("https://gasparamiune.github.io/quantum-physics-book/", "The live book."),
    gallery=[("quantum/home.webp", "Home: start here, follow the lectures, practise, or face the final bosses.")],
    skills=["agents", "web3d", "python", "sysmeth"],
),
# ---------------------------------------------------------------- AI bubble
dict(
    slug="ai-bubble", title="AI Bubble monitor", cat="product", year="2026",
    short="A phone-friendly dashboard that tracks the signals that would pop the AI boom, refreshed by a cron job in the cloud.",
    status=("Live", "live"), role="Builder", team="Personal project",
    links=[("Open the dashboard", "https://gasparamiune.github.io/ai-buble/", "live"),
           ("Source", "https://github.com/gasparamiune/ai-buble", "code")],
    cover="aibubble/home.webp", hero="aibubble/home.webp",
    intro=[
        "A free, always-on monitor for one question: is the AI investment boom still healthy? It compares hyperscaler "
        "capex growth with AI revenue growth, tracks a scoreboard of eight triggers, and shows live prices.",
        "GitHub Pages hosts it and GitHub Actions refreshes the data after every US market close, so it works with my laptop off.",
    ],
    did=[
        "<b>Serverless by design:</b> a scheduled workflow fetches prices and commits a data file; the page just renders it.",
        "<b>Trigger scoreboard</b> with clear thresholds for each risk, from capex cuts to credit stress.",
        "<b>Optional headlines and AI analysis</b> wired in through repository secrets.",
    ],
    how=[
        ("JavaScript (Node)", "the refresh script that pulls prices and headlines."),
        ("GitHub Actions", "the weekday cron that keeps the data fresh."),
        ("HTML + CSS", "a single static dashboard that reads one JSON file."),
    ],
    embed=("https://gasparamiune.github.io/ai-buble/", "The live dashboard."),
    gallery=[("aibubble/home.webp", "The dashboard: the money-in vs money-out signal, the next check and live prices.")],
    skills=["cicd", "python", "product"],
),
# ---------------------------------------------------------------- COOL-BENCH
dict(
    slug="cool-bench", title="COOL-BENCH", cat="university", year="2026",
    short="A physical test and validation bench for refrigeration controller applications, with Danfoss as company partner.",
    status=("In progress", "wip"), role="Team member", team="Experts in Teams, eleven students, SDU with Danfoss",
    links=[],
    cover=None, hero=None,
    intro=[
        "An interdisciplinary SDU project running until December 2026. Instead of a real refrigeration circuit, the bench "
        "uses adjustable sensor-simulation circuits and switches to represent temperature, pressure, defrost demand and a sensor fault.",
        "A controller application calculates superheat, commands a valve, runs a timed defrost and manages alarms, while a "
        "stepper-driven pointer shows the valve position. A validation tool guides an operator through test scenarios and saves traceable results.",
    ],
    did=[
        "Working in a team of eleven from many disciplines and countries, with a company partner.",
        "Deliverables: an integrated demonstrator, calibrated interfaces, controller and validation software, and test evidence.",
    ],
    how=[("Embedded controller + validation software", "scenario-based acceptance tests with saved, traceable results.")],
    diagram="coolbench",
    gallery=[],
    skills=["sysmeth", "control", "pcb"],
),
# ---------------------------------------------------------------- IFEM
dict(
    slug="robotic-arm-fea", title="Robotic arm link FEA", cat="university", year="2026",
    short="Finite element analysis of a self-designed robotic arm link under a 100 N bending load, with a mesh convergence study.",
    status=("Individual report", "built"), role="Author", team="Introduction to FEM, individual",
    links=[],
    cover="ifem/fea_000.webp", hero="ifem/fea_026.webp",
    intro=[
        "I designed the last link of a robotic arm in Ansys Discovery and analysed it in Ansys Mechanical: a fixed mounting "
        "face and a 100 N load at the hand, to create realistic bending.",
        "Three meshes (4, 2 and 1 mm) were compared to check that the result does not depend on the mesh, and two stress "
        "probes away from the concentrations gave a consistent comparison between them.",
    ],
    did=[
        "Derived the strong and weak forms of linear elasticity and a bending sanity-check model before trusting the solver.",
        "Ran the mesh convergence study for deformation and von Mises stress.",
        "Found the highest stresses at the mounting region and the largest deflection at the loaded end, as the beam model predicts.",
    ],
    how=[("Ansys Discovery + Mechanical", "geometry, meshing, static structural solution and probes."),
         ("Python", "convergence plots.")],
    gallery=[
        ("ifem/fea_026.webp", "Total deformation along the link."),
        ("ifem/fea_000.webp", "Stress concentration around the mounting bore."),
        ("ifem/fea_043.webp", "Von Mises stress."),
        ("ifem/fea_006.webp", "The link geometry."),
        ("ifem/fea_016.webp", "Refined mesh at the mounting hole."),
        ("ifem/fea_020.webp", "Convergence of maximum deformation with mesh size."),
        ("ifem/fea_045.webp", "Stress probes compared across the three meshes."),
    ],
    skills=["fea", "cad", "python"],
),
# ---------------------------------------------------------------- AquaGate
dict(
    slug="aquagate", title="AquaGate underwater vehicle", cat="university", year="2026",
    short="A tethered underwater vehicle with three thrusters and an axial jet: modelling, sensor fusion and LQR control.",
    status=("Built prototype", "built"), role="Team member", team="Semester project 4, team of seven",
    links=[],
    cover="aquagate/jet_photo.webp", hero="aquagate/r_006.webp",
    intro=[
        "AquaGate is a submersible that has to hold its attitude and depth on its own. Three vertical thrusters control "
        "roll, pitch and depth, and an axial jet impeller drives it forward.",
        "The team modelled the 6-degree-of-freedom dynamics in water, fused IMU data for attitude, designed LQR gains and "
        "auto-generated the controller from Simulink onto a dual-core STM32H755.",
    ],
    did=[
        "Thruster allocation that maps roll, pitch and depth commands to three thrusters.",
        "LQR gain synthesis, tuned over several iterations of closed-loop responses.",
        "Impeller design checked with CFD for pressure and velocity.",
    ],
    how=[("MATLAB / Simulink", "dynamics model, LQR design and auto-generated embedded code."),
         ("STM32H755 + BNO055 IMU", "on-board control and attitude estimation."),
         ("CFD", "pressure and velocity around the jet impeller.")],
    gallery=[
        ("aquagate/jet_photo.webp", "The built axial jet unit."),
        ("aquagate/r_006.webp", "Impeller render."),
        ("aquagate/cfd_pressure.webp", "CFD: static pressure on the impeller."),
        ("aquagate/cfd_velocity.webp", "CFD: velocity field."),
        ("aquagate/frame_iso.webp", "Vehicle frame CAD."),
        ("aquagate/jet_drawing.webp", "Jet unit drawing and section."),
        ("aquagate/r_014.webp", "LQR closed-loop responses for roll, pitch, heave and surge."),
    ],
    skills=["control", "simulink", "fusion", "cfd", "cad"],
),
# ---------------------------------------------------------------- Drone
dict(
    slug="flood-drone", title="Flood surveillance drone", cat="university", year="2024",
    short="A quadcopter for flood surveillance: dynamics model, PID control in Simulink, a custom PCB and a built prototype.",
    status=("Built & tested", "built"), role="Electronics and testing lead", team="Semester project, team of six",
    links=[],
    cover="drone/d_155.webp", hero="drone/d_000.webp",
    intro=[
        "A quadcopter concept for spotting people in flood zones. The team modelled the quadrotor dynamics, designed PID "
        "controllers in Simulink and built the drone around its frame and a custom PCB.",
        "I was in charge of electronics and testing: the PCB, wiring and the bench tests that validated the motors, "
        "ESCs and sensors before flight.",
    ],
    did=[
        "Designed the electronics and PCB, and assembled the drone.",
        "Characterised the BLDC motors and ESCs on the bench against the manufacturer's data.",
        "Integrated the sensors with the control model and tested the full system.",
    ],
    how=[("MATLAB / Simulink", "quadrotor dynamics and PID attitude control with motor mixing."),
         ("KiCad", "the PCB that carries power distribution and the sensors."),
         ("Ansys", "static check of the frame arms.")],
    gallery=[
        ("drone/d_000.webp", "The assembled drone."),
        ("drone/d_155.webp", "Full system on the bench."),
        ("drone/d_128.webp", "Frame with the PCB mounted."),
        ("drone/d_129.webp", "Wiring and motor tests."),
        ("drone/d_070.webp", "CAD of the drone with the PCB."),
        ("drone/d_066.webp", "PCB layout."),
        ("drone/d_028.webp", "Simulink: PID loops and motor mixing."),
        ("drone/d_093.webp", "FEA of the frame."),
        ("drone/proto.webp", "First prototype of the concept."),
    ],
    skills=["pcb", "control", "simulink", "fea"],
),
# ---------------------------------------------------------------- Robot dog
dict(
    slug="robot-dog", title="SAP robot dog", cat="university", year="2024",
    short="A companion robot dog with a camera and gas, smoke and flame sensors to keep a home safe.",
    status=("Built prototype", "built"), role="Electronics and programming", team="Semester project, team of five",
    links=[],
    cover="robotdog/g_090.webp", hero="robotdog/g_001.webp",
    intro=[
        "Our first big build: a robot dog that is a companion and a home-safety device at once. It recognises poses with a "
        "camera and watches for CO, CO₂, alcohol vapour and fire.",
        "I worked in the electronics and programming pair: circuit and PCB design, soldering and testing, and the code for "
        "its modes (explorer, police, pose detector, fire detection and companion).",
    ],
    did=[
        "Designed the sensor, motor-controller, ADC and power modules and the PCB.",
        "Soldered and tested the boards, then integrated them into the 3D-printed body.",
        "Wrote the Python behaviours on the Raspberry Pi, including alerts when a gas leak or fire is detected.",
    ],
    how=[("Python (Raspberry Pi)", "behaviour modes, camera pose detection and sensor alerts."),
         ("KiCad", "the custom PCB."),
         ("3D printing", "the body, head and legs.")],
    gallery=[
        ("robotdog/g_090.webp", "The finished prototype."),
        ("robotdog/g_001.webp", "Design render."),
        ("robotdog/g_060.webp", "Our assembled PCB."),
        ("robotdog/g_059.webp", "The board before mounting."),
        ("robotdog/g_106.webp", "PCB layout."),
        ("robotdog/g_088.webp", "Assembly in the workshop."),
        ("robotdog/g_084.webp", "Leg kinematics: hip, knee and side bone."),
        ("robotdog/g_076.webp", "Head design."),
    ],
    skills=["pcb", "python", "cv", "cad"],
),
# ---------------------------------------------------------------- Interstellar
dict(
    slug="interstellar-game", title="AI Interstellar game", cat="university", year="2024",
    short="A space game you play with your bare hand: real-time hand tracking turns gestures into controls.",
    status=("Course project", "built"), role="Developer", team="Course project",
    links=[],
    cover=None, hero=None,
    intro=[
        "A project to learn computer vision by building something fun. You steer a spaceship with your hand in front of a "
        "webcam, close your fist to catch floating astronauts for points, and avoid black holes that take points away.",
        "MediaPipe finds the hand's landmarks in every frame; an open hand moves the cursor and a closed fist acts as a click.",
    ],
    did=["Built the camera pipeline, the gesture logic and the game loop.",
         "Structured the code as menu, hand tracker, game classes, settings and assets."],
    how=[("Python + OpenCV", "camera capture and image handling."),
         ("MediaPipe", "hand landmark detection in real time."),
         ("Pygame", "the game, menus and graphics.")],
    diagram="interstellar",
    gallery=[],
    skills=["cv", "python"],
),
]


# ====================================================================== REV 2 presentation data
# Short names for the skills matrix header.
SHORT = {
    "pourstock": "PourStock", "argus": "ARGUS rover", "micromouse": "Micromouse", "hedge-agents": "Hedge agents",
    "argos-h1": "ARGOS-H1 engine", "waterjet": "P1-J waterjet", "quantum-book": "Quantum Book",
    "ai-bubble": "AI Bubble monitor", "cool-bench": "COOL-BENCH", "robotic-arm-fea": "Arm link FEA",
    "aquagate": "AquaGate", "flood-drone": "Flood drone", "robot-dog": "Robot dog", "interstellar-game": "Interstellar game",
}

# Featured plates on the home page: media, caption and three key facts (all taken from the project text above).
FEATURE = {
    "pourstock": {"media": ("video", "pourstock/floor-merge.mp4", "pourstock/floor-merge.webp"),
                  "cap": "Floor plan: merging tables during live service. Screen recording.",
                  "keys": ["Live at pourstock.com", "AI constitution and a quality gate on every change", "24/7 Claude support agent for staff"]},
    "argus": {"media": ("img", "argus/06_exploded_view.webp"),
              "cap": "Exploded view of the assembly. CAD render.",
              "keys": ["I led the team of nine and ran integration", "One Python model computes every budget", "A drivable 3D test in the browser"]},
    "micromouse": {"media": ("maze",),
                   "cap": "Running now: my floodfill algorithm solving a random maze.",
                   "keys": ["Firmware written by hand in C/C++", "Floodfill solver with dual PID control", "STM32H743 microcontroller"]},
    "hedge-agents": {"media": ("diagram",),
                     "cap": "System map: data, agents, scoring and the safety layer.",
                     "keys": ["Ten agent modules, one scoring engine", "Kill switch, daily action limit, heartbeat", "One LLM router with budget caps"]},
    "argos-h1": {"media": ("img", "engine/plume_render.webp", "fit"),
                 "cap": "Artistic render built from the CFD fields. Appearance only.",
                 "keys": ["C++ controller for a Teensy 4.1", "Software-in-the-loop test on every release", "3D FEA, plume CFD and landing Monte Carlo"]},
}

# Rotating plate in the home hero: (image, project slug, caption, fit)
HERO_SLIDES = [
    ("argus/02_stowed_in_0.5m_cube.webp", "argus", "ARGUS lunar rover, stowed in its 0.5 m launch envelope. CAD render.", ""),
    ("pourstock/floor-merge.webp", "pourstock", "PourStock, the floor plan during service. Screenshot.", "top"),
    ("engine/plume_render.webp", "argos-h1", "ARGOS-H1 engine plume. Artistic render from the CFD fields, appearance only.", "fit"),
    ("drone/d_000.webp", "flood-drone", "Flood surveillance drone, assembled. Photo.", ""),
    ("aquagate/jet_photo.webp", "aquagate", "AquaGate, the built axial jet unit. Photo.", ""),
]

# How the big figure at the top of each project page is shown.
#   cover (default) | top (screenshots, anchored to the top) | fit (whole image on dark) | sheet (small image on the grid)
#   maze (live simulator) | pair (two images) | diagram (no image: the system map)
PAGE_HERO = {
    "pourstock": ("top", "pourstock/floor-merge.webp"),
    "argus": ("cover", "argus/03_at_station_APXS_down.webp"),
    "micromouse": ("maze",),
    "hedge-agents": ("diagram",),
    "argos-h1": ("fit", "engine/plume_render.webp"),
    "waterjet": ("sheet", "waterjet/corte_lateral.webp"),
    "quantum-book": ("top", "quantum/home.webp"),
    "ai-bubble": ("top", "aibubble/home.webp"),
    "cool-bench": ("diagram",),
    "robotic-arm-fea": ("cover", "ifem/fea_016.webp"),
    "aquagate": ("cover", "aquagate/jet_photo.webp"),
    "flood-drone": ("cover", "drone/d_000.webp"),
    "robot-dog": ("pair", "robotdog/g_090.webp", "robotdog/g_001.webp"),
    "interstellar-game": ("diagram",),
}
PAGE_HERO_CAP = {
    "pourstock": "The floor plan during service. Screenshot of the live product.",
    "argus": "At a science station with the APXS instrument lowered. CAD render.",
    "micromouse": "Running now: the floodfill algorithm from my firmware solving a random maze.",
    "hedge-agents": "System map: data, agents, scoring and the safety layer.",
    "argos-h1": "Artistic render built from the CFD fields. Appearance only, not a measurement.",
    "waterjet": "Centreline section through the CAD: intake, impeller, nozzle and reverse bucket.",
    "quantum-book": "Home of the book. Screenshot.",
    "ai-bubble": "The dashboard. Screenshot.",
    "cool-bench": "System map of the bench.",
    "robotic-arm-fea": "Mesh around the mounting bore. Ansys.",
    "aquagate": "The built axial jet unit. Photo.",
    "flood-drone": "The assembled drone. Photo.",
    "robot-dog": "Left: the finished prototype. Right: the design render.",
    "interstellar-game": "From webcam frame to game input.",
}

PLAYS = [
    ("https://gasparamiune.github.io/ARGus/surface-test/", ("img", "argus/04_leg_closeup.webp"), "Game · 3D",
     "Drive ARGUS on the Moon", "The real rover CAD in three.js: drive it, switch design revisions, open every part."),
    ("play/micromouse.html", ("maze",), "Simulation",
     "Micromouse floodfill", "My maze-solving algorithm exploring a random maze, step by step."),
    ("https://gasparamiune.github.io/quantum-physics-book/", ("img", "quantum/home.webp"), "Interactive book",
     "Beat the quantum bosses", "Simulations, hint ladders and four final bosses for the exam."),
]

TIMELINE = [
    ("Now", "Compressor failure analysis, Danfoss", "Disassembling compressors and tracing mechanical, electrical and electronic faults."),
    ("Now", "Founder, PourStock", "Operations software for restaurants and hotels, live at pourstock.com."),
    ("2027", "BSc Mechatronics Engineering, SDU Sønderborg", "Final year. Graduating June 2027."),
    ("11 yrs", "Restaurants and hotels", "Eleven years on the floor. It is where PourStock comes from."),
    ("2017", "Programming Technician (Java)", "Technical secondary school diploma, Argentina."),
]
# CEFR level on a six-step scale (A1 = 1 ... C2 / native = 6)
LANGS = [("Spanish", 6, "Native"), ("English", 5, "C1"), ("Italian", 5, "C1"), ("Danish", 3, "B1"), ("Russian", 1, "A1")]
