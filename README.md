====================================================================
         TRANSFORMER DESIGN CALCULATOR - TECHNICAL DOCUMENTATION
====================================================================

1. INTRODUCTION
---------------
This Python program automates the design of electrical transformers by calculating:
- Core dimensions
- Winding parameters
- Power losses
- Thermal performance
- Mechanical requirements
- Cost estimation

WHY USE THIS TOOL?
Manual transformer design requires complex iterative calculations. This program:
- Saves engineering time
- Reduces human error
- Allows quick design optimization
- Generates professional reports

2. CORE DESIGN CALCULATIONS
--------------------------
2.1 Core Area Calculation
Purpose: Determine the minimum core size to avoid magnetic saturation.

Formula:
Core Area (A_c) = K × √Power
Where:
- K = Empirical constant (0.9-1.1 based on core type)
- Power = Transformer rating in VA

Why Important:
- Too small core → Magnetic saturation → Excessive heating
- Too large core → Wasted material → Increased cost

2.2 Flux Density (B_m)
Purpose: Measure magnetic flux per unit area.

Typical Values:
- CRGO Steel: 1.2-1.5 Tesla
- Amorphous Metal: 1.1-1.3 Tesla

Impact:
- Higher B_m → Smaller core but more losses
- Lower B_m → Larger core but better efficiency

3. WINDING CALCULATIONS
----------------------
3.1 Turns Calculation
Purpose: Determine proper voltage transformation ratio.

Formula:
Primary Turns (N1) = V1 / (4.44 × f × B_m × A_c)
Where:
- f = Frequency (Hz)
- V1 = Primary voltage

Why Critical:
- Too few turns → Core saturation
- Too many turns → Increased copper losses

3.2 Conductor Sizing
Purpose: Ensure proper current carrying capacity.

Formula:
Conductor Area (A_w) = Current (I) / Current Density (J)
Where:
- J = 2-4 A/mm² (depends on cooling)

Impact:
- Undersized → Overheating
- Oversized → Wasted copper

4. LOSS CALCULATIONS
-------------------
4.1 Copper Loss (I²R Loss)
Purpose: Calculate resistive heating in windings.

Formula:
P_cu = I² × R
Where R = ρ × (MLT × N) / A_w
- ρ = Copper resistivity
- MLT = Mean length per turn

4.2 Core Loss
Purpose: Estimate hysteresis and eddy current losses.

Formula (Modified Steinmetz):
P_core = K × f^α × B_m^β × Weight

Why Important:
Losses directly affect:
- Efficiency
- Temperature rise
- Operating costs

5. THERMAL DESIGN
----------------
5.1 Temperature Rise
Purpose: Ensure safe operating temperatures.

Formula:
ΔT = Total Losses / (h × Surface Area)
Where h = Cooling coefficient

Critical Limits:
- Oil-immersed: 65°C rise
- Dry-type: 150°C hotspot

6. MECHANICAL DESIGN
-------------------
6.1 Short-Circuit Forces
Purpose: Ensure structural integrity during faults.

Formula:
Radial Force = 0.5 × μ₀ × (N × I_sc)² / l_mt

Design Impact:
- Determines winding bracing requirements
- Affects tank strength design

7. OPTIMIZATION TRADEOFFS
------------------------
Parameter       Increase Effect           Decrease Effect
--------------------------------------------------------
Flux Density    Higher losses, smaller    Larger core, lower
(B_m)           size                      losses
Current         Higher copper loss,       Larger conductors,
Density (J)     compact design            higher cost
Efficiency      Larger core & windings,   More losses,
Target          higher cost               cheaper design

8. HOW TO USE THE PROGRAM
------------------------
1) Run transformer_design.py
2) Enter electrical parameters:
   - Power rating
   - Primary/secondary voltages
   - Frequency
3) Select materials and cooling type
4) Choose optimization target:
   - Minimum cost
   - Minimum weight
   - Maximum efficiency
5) Review generated PDF report

9. EXAMPLE DESIGN CASE
---------------------
Input:
- 25 kVA distribution transformer
- 11kV/415V
- CRGO core
- ONAN cooling

Output:
- Core: 28.5 cm² area
- Primary turns: 1,840
- Secondary turns: 68
- Efficiency: 98.4%
- Total losses: 400W
- Temperature rise: 58°C

10. COMMON DESIGN MISTAKES
-------------------------
Mistake                Consequences              Solution
---------------------------------------------------------
Too high flux density  Excessive core losses     Reduce B_m or
                       and overheating          use larger core
Insufficient cooling   Insulation breakdown      Improve cooling
surface area                                     or reduce losses
Undersized conductors  Overheating, reduced      Increase conductor
                       lifespan                 size or improve
                                                cooling


11. FUTURE IMPROVEMENTS
----------------------
- Add 3D visualization of core/windings
- Include harmonic loss calculations
- Add impedance calculation
- Develop GUI interface
