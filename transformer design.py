import math
import numpy as np
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import warnings
warnings.filterwarnings("ignore")

class TransformerDesign:
    def __init__(self):
        # Basic parameters
        self.standard = ""
        self.transformer_type = ""
        self.core_material = ""
        self.cooling_type = ""
        self.phase = ""
        self.core_shape = ""
        self.winding_type = ""
        self.connection_type = ""
        
        # Electrical parameters
        self.V1 = 0
        self.V2 = 0
        self.frequency = 50
        self.power = 0
        self.efficiency = 0.95
        self.regulation = 0.05
        self.harmonic_factor = 1.0
        
        # Material properties
        self.Bm = 1.2
        self.J = 3.0
        self.k = 0.9
        self.kw = 0.3
        self.rho_cu = 1.68e-8
        self.rho_fe = 7.65  # g/cm³
        
        # Advanced parameters
        self.max_temp_rise = 65
        self.max_losses = None
        self.max_weight = None
        self.max_cost = None
        self.ambient_temp = 30
        self.altitude = 0
        self.noise_limit = None
        
        # Results storage
        self.results = {}
        self.design_steps = []
        self.optimization_results = {}
        self.thermal_results = {}
        self.mechanical_results = {}
        self.cost_results = {}
        self.optimization_target = "cost"  # Added initialization
        
    def get_user_inputs(self):
        print("=== Advanced Transformer Design Calculator ===")
        
        # Standard selection
        print("\nStandards Available:")
        print("1. IEC 60076")
        print("2. ANSI C57")
        print("3. IS 2026 (Indian Standard)")
        print("4. BS EN 60076 (British Standard)")
        print("5. GOST 11677 (Russian Standard)")
        std_choice = input("Select standard (1-5): ")
        standards = {
            "1": "IEC 60076",
            "2": "ANSI C57",
            "3": "IS 2026",
            "4": "BS EN 60076",
            "5": "GOST 11677"
        }
        self.standard = standards.get(std_choice, "IEC 60076")
        
        # Transformer type
        print("\nTransformer Types:")
        print("1. Distribution Transformer")
        print("2. Power Transformer")
        print("3. Instrument Transformer")
        print("4. Autotransformer")
        print("5. Isolation Transformer")
        print("6. Rectifier Transformer")
        print("7. Phase Shifting Transformer")
        type_choice = input("Select transformer type (1-7): ")
        types = {
            "1": "Distribution Transformer",
            "2": "Power Transformer",
            "3": "Instrument Transformer",
            "4": "Autotransformer",
            "5": "Isolation Transformer",
            "6": "Rectifier Transformer",
            "7": "Phase Shifting Transformer"
        }
        self.transformer_type = types.get(type_choice, "Distribution Transformer")
        
        # Core material
        print("\nCore Materials:")
        print("1. CRGO Steel (Cold Rolled Grain Oriented)")
        print("2. Amorphous Metal (Metglas)")
        print("3. Silicon Steel")
        print("4. Nano-Crystalline")
        print("5. High Permeability Steel")
        core_choice = input("Select core material (1-5): ")
        materials = {
            "1": "CRGO Steel",
            "2": "Amorphous Metal",
            "3": "Silicon Steel",
            "4": "Nano-Crystalline",
            "5": "High Permeability Steel"
        }
        self.core_material = materials.get(core_choice, "CRGO Steel")
        
        # Cooling type
        print("\nCooling Types:")
        print("1. ONAN (Oil Natural Air Natural)")
        print("2. ONAF (Oil Natural Air Forced)")
        print("3. OFAF (Oil Forced Air Forced)")
        print("4. Dry Type (Air Cooled)")
        print("5. AN (Air Natural)")
        print("6. AF (Air Forced)")
        print("7. Water Cooled")
        cool_choice = input("Select cooling type (1-7): ")
        cooling_types = {
            "1": "ONAN",
            "2": "ONAF",
            "3": "OFAF",
            "4": "Dry Type",
            "5": "AN",
            "6": "AF",
            "7": "Water Cooled"
        }
        self.cooling_type = cooling_types.get(cool_choice, "ONAN")
        
        # Phase configuration
        print("\nPhase Configuration:")
        print("1. Single Phase")
        print("2. Three Phase")
        phase_choice = input("Select phase (1 or 2): ")
        self.phase = "Single Phase" if phase_choice == "1" else "Three Phase"
        
        # Core shape
        print("\nCore Shapes:")
        print("1. EI Core")
        print("2. UI Core")
        print("3. C Core")
        print("4. Toroidal")
        print("5. Shell Type")
        print("6. Berry Type")
        core_shape_choice = input("Select core shape (1-6): ")
        core_shapes = {
            "1": "EI Core",
            "2": "UI Core",
            "3": "C Core",
            "4": "Toroidal",
            "5": "Shell Type",
            "6": "Berry Type"
        }
        self.core_shape = core_shapes.get(core_shape_choice, "EI Core")
        
        # Winding type
        print("\nWinding Types:")
        print("1. Layer Winding")
        print("2. Helical Winding")
        print("3. Disc Winding")
        print("4. Foil Winding")
        print("5. Interleaved Winding")
        winding_choice = input("Select winding type (1-5): ")
        winding_types = {
            "1": "Layer Winding",
            "2": "Helical Winding",
            "3": "Disc Winding",
            "4": "Foil Winding",
            "5": "Interleaved Winding"
        }
        self.winding_type = winding_types.get(winding_choice, "Layer Winding")
        
        # Connection type (for three-phase)
        if self.phase == "Three Phase":
            print("\nConnection Types:")
            print("1. Delta-Delta")
            print("2. Delta-Wye")
            print("3. Wye-Delta")
            print("4. Wye-Wye")
            print("5. Zig-Zag")
            connection_choice = input("Select connection type (1-5): ")
            connection_types = {
                "1": "Delta-Delta",
                "2": "Delta-Wye",
                "3": "Wye-Delta",
                "4": "Wye-Wye",
                "5": "Zig-Zag"
            }
            self.connection_type = connection_types.get(connection_choice, "Delta-Wye")
        
        # Basic electrical parameters
        self.V1 = float(input("\nPrimary Voltage (V): "))
        self.V2 = float(input("Secondary Voltage (V): "))
        self.frequency = float(input("Frequency (Hz, default 50): ") or 50)
        self.power = float(input("Power Rating (VA): "))
        self.efficiency = float(input("Efficiency (decimal, default 0.95): ") or 0.95)
        self.regulation = float(input("Regulation (decimal, default 0.05): ") or 0.05)
        
        # Advanced parameters
        print("\nAdvanced Parameters (press Enter for defaults):")
        self.max_temp_rise = float(input("Maximum allowed temperature rise (°C, default 65): ") or 65)
        self.ambient_temp = float(input("Ambient temperature (°C, default 30): ") or 30)
        self.altitude = float(input("Altitude (meters, default 0): ") or 0)
        self.harmonic_factor = float(input("Harmonic factor (K-factor, default 1.0): ") or 1.0)
        self.noise_limit = input("Noise limit (dB, optional): ")
        self.noise_limit = float(self.noise_limit) if self.noise_limit else None
        
        # Optimization constraints
        print("\nOptimization Constraints (optional):")
        max_losses = input("Maximum total losses (W, optional): ")
        self.max_losses = float(max_losses) if max_losses else None
        max_weight = input("Maximum weight (kg, optional): ")
        self.max_weight = float(max_weight) if max_weight else None
        max_cost = input("Maximum cost (USD, optional): ")
        self.max_cost = float(max_cost) if max_cost else None
        
        # Set material-specific parameters
        self.set_material_parameters()
        
    def set_material_parameters(self):
        """Set material-specific design parameters based on selected standard"""
        # Flux density (Bm) in Tesla
        bm_values = {
            "IEC 60076": {
                "CRGO Steel": 1.5,
                "Amorphous Metal": 1.3,
                "Silicon Steel": 1.2,
                "Nano-Crystalline": 1.4,
                "High Permeability Steel": 1.6
            },
            "ANSI C57": {
                "CRGO Steel": 1.4,
                "Amorphous Metal": 1.25,
                "Silicon Steel": 1.1,
                "Nano-Crystalline": 1.35,
                "High Permeability Steel": 1.5
            },
            "IS 2026": {
                "CRGO Steel": 1.45,
                "Amorphous Metal": 1.3,
                "Silicon Steel": 1.15,
                "Nano-Crystalline": 1.4,
                "High Permeability Steel": 1.55
            },
            "BS EN 60076": {
                "CRGO Steel": 1.5,
                "Amorphous Metal": 1.3,
                "Silicon Steel": 1.2,
                "Nano-Crystalline": 1.4,
                "High Permeability Steel": 1.6
            },
            "GOST 11677": {
                "CRGO Steel": 1.35,
                "Amorphous Metal": 1.2,
                "Silicon Steel": 1.05,
                "Nano-Crystalline": 1.3,
                "High Permeability Steel": 1.45
            }
        }
        self.Bm = bm_values.get(self.standard, {}).get(self.core_material, 1.2)
        
        # Current density (J) in A/mm²
        j_values = {
            "IEC 60076": {
                "CRGO Steel": 3.0,
                "Amorphous Metal": 2.8,
                "Silicon Steel": 2.5,
                "Nano-Crystalline": 3.2,
                "High Permeability Steel": 3.5
            },
            "ANSI C57": {
                "CRGO Steel": 3.2,
                "Amorphous Metal": 3.0,
                "Silicon Steel": 2.8,
                "Nano-Crystalline": 3.4,
                "High Permeability Steel": 3.7
            },
            "IS 2026": {
                "CRGO Steel": 2.8,
                "Amorphous Metal": 2.6,
                "Silicon Steel": 2.4,
                "Nano-Crystalline": 3.0,
                "High Permeability Steel": 3.3
            },
            "BS EN 60076": {
                "CRGO Steel": 3.0,
                "Amorphous Metal": 2.8,
                "Silicon Steel": 2.5,
                "Nano-Crystalline": 3.2,
                "High Permeability Steel": 3.5
            },
            "GOST 11677": {
                "CRGO Steel": 2.7,
                "Amorphous Metal": 2.5,
                "Silicon Steel": 2.3,
                "Nano-Crystalline": 2.9,
                "High Permeability Steel": 3.1
            }
        }
        base_J = j_values.get(self.standard, {}).get(self.core_material, 3.0)
        
        # Adjust for cooling type
        cooling_adjustment = {
            "ONAN": 1.0,
            "ONAF": 1.2,
            "OFAF": 1.5,
            "Dry Type": 0.8,
            "AN": 0.9,
            "AF": 1.1,
            "Water Cooled": 1.8
        }
        self.J = base_J * cooling_adjustment.get(self.cooling_type, 1.0)
        
        # Core stacking factor
        self.k = 0.95 if "CRGO" in self.core_material else 0.90
        
        # Winding space factor
        if self.winding_type == "Layer Winding":
            self.kw = 0.3
        elif self.winding_type == "Helical Winding":
            self.kw = 0.35
        elif self.winding_type == "Disc Winding":
            self.kw = 0.4
        elif self.winding_type == "Foil Winding":
            self.kw = 0.45
        else:  # Interleaved
            self.kw = 0.5
    
    def calculate_core_dimensions(self):
        """Calculate core dimensions based on shape and power"""
        # Empirical constant
        K = 0.9 if self.power < 1000 else 1.1
        
        # Core area (cm²)
        Ac = K * math.sqrt(self.power)
        Ag = Ac / self.k  # Gross core area
        
        # Core dimensions based on shape
        if self.core_shape == "EI Core":
            # For EI core, assume square central limb
            core_width = math.sqrt(Ag) * 10  # mm
            core_depth = core_width  # mm
            window_width = core_width * 0.6  # mm
            window_height = core_width * 1.8  # mm
            yoke_height = core_width * 0.7  # mm
            core_building_factor = 1.15
            
        elif self.core_shape == "UI Core":
            # UI core has rectangular central limb
            core_width = math.sqrt(Ag * 1.2) * 10  # mm
            core_depth = core_width * 0.8  # mm
            window_width = core_width * 0.5  # mm
            window_height = core_width * 1.5  # mm
            yoke_height = core_width * 0.6  # mm
            core_building_factor = 1.2
            
        elif self.core_shape == "C Core":
            # C core is similar to UI but with rounded corners
            core_width = math.sqrt(Ag) * 10  # mm
            core_depth = core_width * 0.7  # mm
            window_width = core_width * 0.4  # mm
            window_height = core_width * 1.3  # mm
            yoke_height = core_width * 0.5  # mm
            core_building_factor = 1.25
            
        elif self.core_shape == "Toroidal":
            # Toroidal core - different calculation approach
            mean_diameter = (4 * Ac / math.pi) ** 0.5 * 10  # mm
            core_width = mean_diameter * 0.3  # mm (radial thickness)
            core_depth = mean_diameter * 0.3  # mm (axial height)
            window_width = mean_diameter * 0.7  # mm
            window_height = core_depth  # mm
            yoke_height = 0  # Not applicable
            core_building_factor = 1.0
            
        elif self.core_shape == "Shell Type":
            # Shell type has three limbs
            core_width = math.sqrt(Ag * 1.5) * 10  # mm
            core_depth = core_width * 0.6  # mm
            window_width = core_width * 0.4  # mm
            window_height = core_width * 1.2  # mm
            yoke_height = core_width * 0.5  # mm
            core_building_factor = 1.3
            
        else:  # Berry Type
            # Berry type has distributed core
            core_width = math.sqrt(Ag * 2) * 10  # mm
            core_depth = core_width * 0.5  # mm
            window_width = core_width * 0.3  # mm
            window_height = core_width * 1.0  # mm
            yoke_height = core_width * 0.4  # mm
            core_building_factor = 1.4
            
        return {
            "Core Area (cm²)": Ac,
            "Gross Core Area (cm²)": Ag,
            "Core Width (mm)": core_width,
            "Core Depth (mm)": core_depth,
            "Window Width (mm)": window_width,
            "Window Height (mm)": window_height,
            "Yoke Height (mm)": yoke_height,
            "Core Building Factor": core_building_factor
        }
    
    def calculate_turns(self, Ac):
        """Calculate primary and secondary turns"""
        # For three-phase, divide power by 3 for per-phase calculations
        phase_factor = 3 if self.phase == "Three Phase" else 1
        phase_power = self.power / phase_factor
        
        # Primary turns
        N1 = self.V1 / (4.44 * self.frequency * self.Bm * Ac * 1e-4)
        
        # Secondary turns (accounting for regulation)
        N2 = (self.V2 * (1 + self.regulation)) / (4.44 * self.frequency * self.Bm * Ac * 1e-4)
        
        # Adjust for three-phase connection type
        if self.phase == "Three Phase":
            if "Wye" in self.connection_type:
                N1 /= math.sqrt(3)
                N2 /= math.sqrt(3)
        
        return {
            "Primary Turns": N1,
            "Secondary Turns": N2
        }
    
    def calculate_currents(self):
        """Calculate primary and secondary currents"""
        phase_factor = 3 if self.phase == "Three Phase" else 1
        
        # Primary current
        I1 = self.power / (self.V1 * phase_factor)
        
        # Secondary current
        I2 = self.power / (self.V2 * phase_factor)
        
        # Adjust for three-phase connection type
        if self.phase == "Three Phase":
            if "Wye" in self.connection_type:
                I1 *= math.sqrt(3)
                I2 *= math.sqrt(3)
        
        return {
            "Primary Current (A)": I1,
            "Secondary Current (A)": I2
        }
    
    def calculate_conductor_size(self, I):
        """Calculate conductor size for given current"""
        # Conductor area (mm²)
        Aw = I / self.J
        
        # Find standard wire gauge
        swg = self.calculate_swg(Aw)
        
        # Calculate skin depth and check for eddy current effects
        skin_depth = 66.1 / math.sqrt(self.frequency)  # mm at 20°C
        effective_radius = math.sqrt(Aw / math.pi)
        
        # If conductor is too large for frequency, consider Litz wire
        if effective_radius > skin_depth * 2:
            strands = math.ceil((effective_radius / skin_depth) ** 2)
            strand_area = Aw / strands
            strand_swg = self.calculate_swg(strand_area)
            swg["Strands"] = strands
            swg["Strand SWG"] = strand_swg["SWG"]
            swg["Strand Diameter"] = strand_swg["Diameter"]
        
        return {
            "Conductor Area (mm²)": Aw,
            "SWG": swg,
            "Skin Depth (mm)": skin_depth,
            "Effective Radius (mm)": effective_radius
        }
    
    def calculate_swg(self, area):
        """Find closest standard wire gauge for given area"""
        # Standard wire gauge table (extended)
        swg_table = [
            {"SWG": "4/0", "Diameter": 11.684, "Area": 107.22, "Resistance": 0.160},
            {"SWG": "3/0", "Diameter": 10.404, "Area": 85.01, "Resistance": 0.202},
            {"SWG": "2/0", "Diameter": 9.266, "Area": 67.43, "Resistance": 0.255},
            {"SWG": "1/0", "Diameter": 8.252, "Area": 53.48, "Resistance": 0.322},
            {"SWG": "1", "Diameter": 7.348, "Area": 42.41, "Resistance": 0.406},
            {"SWG": "2", "Diameter": 6.544, "Area": 33.63, "Resistance": 0.512},
            {"SWG": "3", "Diameter": 5.827, "Area": 26.67, "Resistance": 0.646},
            {"SWG": "4", "Diameter": 5.189, "Area": 21.15, "Resistance": 0.815},
            {"SWG": "5", "Diameter": 4.621, "Area": 16.77, "Resistance": 1.028},
            {"SWG": "6", "Diameter": 4.115, "Area": 13.30, "Resistance": 1.296},
            {"SWG": "7", "Diameter": 3.665, "Area": 10.55, "Resistance": 1.634},
            {"SWG": "8", "Diameter": 3.264, "Area": 8.37, "Resistance": 2.060},
            {"SWG": "9", "Diameter": 2.906, "Area": 6.63, "Resistance": 2.599},
            {"SWG": "10", "Diameter": 2.588, "Area": 5.26, "Resistance": 3.277},
            {"SWG": "11", "Diameter": 2.305, "Area": 4.17, "Resistance": 4.132},
            {"SWG": "12", "Diameter": 2.053, "Area": 3.31, "Resistance": 5.211},
            {"SWG": "13", "Diameter": 1.828, "Area": 2.63, "Resistance": 6.571},
            {"SWG": "14", "Diameter": 1.628, "Area": 2.08, "Resistance": 8.286},
            {"SWG": "15", "Diameter": 1.450, "Area": 1.65, "Resistance": 10.45},
            {"SWG": "16", "Diameter": 1.291, "Area": 1.31, "Resistance": 13.18},
            {"SWG": "17", "Diameter": 1.150, "Area": 1.04, "Resistance": 16.62},
            {"SWG": "18", "Diameter": 1.024, "Area": 0.82, "Resistance": 20.96},
            {"SWG": "19", "Diameter": 0.912, "Area": 0.65, "Resistance": 26.43},
            {"SWG": "20", "Diameter": 0.812, "Area": 0.52, "Resistance": 33.33},
            {"SWG": "21", "Diameter": 0.723, "Area": 0.41, "Resistance": 42.03},
            {"SWG": "22", "Diameter": 0.644, "Area": 0.33, "Resistance": 53.00},
            {"SWG": "23", "Diameter": 0.573, "Area": 0.26, "Resistance": 66.84},
            {"SWG": "24", "Diameter": 0.511, "Area": 0.20, "Resistance": 84.29},
            {"SWG": "25", "Diameter": 0.455, "Area": 0.16, "Resistance": 106.3},
            {"SWG": "26", "Diameter": 0.405, "Area": 0.13, "Resistance": 134.0},
            {"SWG": "27", "Diameter": 0.361, "Area": 0.10, "Resistance": 169.0},
            {"SWG": "28", "Diameter": 0.321, "Area": 0.08, "Resistance": 213.1},
            {"SWG": "29", "Diameter": 0.286, "Area": 0.06, "Resistance": 268.7},
            {"SWG": "30", "Diameter": 0.255, "Area": 0.05, "Resistance": 338.8}
        ]
        
        # Find the closest SWG
        closest = min(swg_table, key=lambda x: abs(x["Area"] - area))
        return closest
    
    def calculate_winding(self, N, I, Aw, window_width, window_height):
        """Calculate winding parameters"""
        # Winding height
        turns_per_layer = math.floor((window_height * 0.9) / (Aw ** 0.5))
        layers = math.ceil(N / turns_per_layer)
        winding_height = layers * (Aw ** 0.5) * 1.1  # mm (with insulation)
        
        # Winding thickness
        turns_per_row = math.floor((window_width * 0.9) / (Aw ** 0.5))
        rows = math.ceil(N / turns_per_row)
        winding_thickness = rows * (Aw ** 0.5) * 1.1  # mm (with insulation)
        
        # Choose the configuration with minimum dimensions
        if winding_height <= window_height and winding_thickness <= window_width:
            # Use vertical winding
            winding_config = {
                "Turns per Layer": turns_per_layer,
                "Layers": layers,
                "Winding Height (mm)": winding_height,
                "Winding Thickness (mm)": (Aw ** 0.5) * 1.1
            }
        else:
            # Use horizontal winding
            winding_config = {
                "Turns per Row": turns_per_row,
                "Rows": rows,
                "Winding Height (mm)": (Aw ** 0.5) * 1.1,
                "Winding Thickness (mm)": winding_thickness
            }
        
        # Calculate mean turn length
        if self.core_shape == "EI Core":
            lmt = 2 * (window_width + window_height) / 1000  # meters
        elif self.core_shape == "Toroidal":
            mean_diameter = (window_width + (Aw ** 0.5)) / 1000  # meters
            lmt = math.pi * mean_diameter
        else:
            lmt = 2 * (window_width + window_height) / 1000  # meters
        
        # Calculate resistance
        R = (self.rho_cu * lmt * N) / (Aw * 1e-6)  # ohms
        
        # Calculate copper loss
        Pcu = I ** 2 * R
        
        return {
            "Winding Configuration": winding_config,
            "Mean Turn Length (m)": lmt,
            "Resistance (Ohm)": R,
            "Copper Loss (W)": Pcu
        }
    
    def calculate_core_loss(self, Ac, lmt):
        """Calculate core loss based on material and dimensions"""
        # Core volume (cm³)
        core_volume = Ac * lmt * 100  # lmt in meters to cm
        
        # Core weight (kg)
        core_weight = core_volume * self.rho_fe / 1000
        
        # Core loss factors (W/kg)
        core_loss_factors = {
            "CRGO Steel": 1.2,
            "Amorphous Metal": 0.3,
            "Silicon Steel": 1.5,
            "Nano-Crystalline": 0.5,
            "High Permeability Steel": 1.0
        }
        core_loss_factor = core_loss_factors.get(self.core_material, 1.2)
        
        # Adjust for frequency
        if self.frequency != 50:
            core_loss_factor *= (self.frequency / 50) ** 1.3
        
        # Total core loss
        Pcore = core_weight * core_loss_factor
        
        return {
            "Core Volume (cm³)": core_volume,
            "Core Weight (kg)": core_weight,
            "Core Loss Factor (W/kg)": core_loss_factor,
            "Core Loss (W)": Pcore
        }
    
    def calculate_eddy_losses(self, I, Aw, N, lmt):
        """Calculate eddy current losses in windings"""
        # Conductor diameter equivalent
        d = 2 * math.sqrt(Aw / math.pi) * 1000  # microns
        
        # Skin depth (microns)
        skin_depth = 66.1 / math.sqrt(self.frequency) * 1000
        
        # Eddy loss factor
        if d > skin_depth:
            xi = ((d / skin_depth) ** 4) / (192 + 0.8 * (d / skin_depth) ** 4)
        else:
            xi = 0
        
        # Total eddy loss
        Peddy = xi * I ** 2 * N * lmt * (self.rho_cu / (Aw * 1e-6))
        
        return {
            "Conductor Diameter (μm)": d,
            "Skin Depth (μm)": skin_depth,
            "Eddy Loss Factor": xi,
            "Eddy Loss (W)": Peddy
        }
    
    def calculate_stray_losses(self, total_copper_loss):
        """Estimate stray losses (simplified)"""
        # Stray loss is typically 10-20% of total load loss
        Pstray = 0.15 * total_copper_loss
        
        return {
            "Stray Loss (W)": Pstray
        }
    
    def calculate_harmonic_losses(self, Pcu, Peddy):
        """Calculate additional losses due to harmonics"""
        # Harmonic loss factor multiplies the eddy losses
        Pharmonic = (self.harmonic_factor ** 2) * Peddy
        
        # Also increases copper loss slightly
        Pcu_harmonic = Pcu * (1 + 0.05 * (self.harmonic_factor - 1))
        
        return {
            "Harmonic Copper Loss (W)": Pcu_harmonic - Pcu,
            "Harmonic Eddy Loss (W)": Pharmonic,
            "Total Harmonic Loss (W)": (Pcu_harmonic - Pcu) + Pharmonic
        }
    
    def calculate_temperature_rise(self, total_loss, surface_area):
        """Calculate temperature rise based on cooling method"""
        # Cooling coefficients (W/m²°C)
        cooling_coefficients = {
            "ONAN": 6.0,
            "ONAF": 10.0,
            "OFAF": 15.0,
            "Dry Type": 5.0,
            "AN": 5.5,
            "AF": 8.0,
            "Water Cooled": 20.0
        }
        h = cooling_coefficients.get(self.cooling_type, 6.0)
        
        # Adjust for altitude
        altitude_factor = 1 / (1 - self.altitude / 9000) ** 0.5
        h_adj = h / altitude_factor
        
        # Temperature rise
        temp_rise = total_loss / (h_adj * surface_area)
        
        # Hot spot temperature (simplified)
        hot_spot = self.ambient_temp + temp_rise * 1.2
        
        return {
            "Cooling Coefficient (W/m²°C)": h,
            "Adjusted Coefficient (W/m²°C)": h_adj,
            "Temperature Rise (°C)": temp_rise,
            "Hot Spot Temperature (°C)": hot_spot
        }
    
    def calculate_noise_level(self, core_weight, Bm):
        """Estimate transformer noise level"""
        # Base noise level (dB) at 1.5T and 50Hz
        if "CRGO" in self.core_material:
            base_noise = 30 + 20 * math.log10(core_weight)
        elif "Amorphous" in self.core_material:
            base_noise = 25 + 18 * math.log10(core_weight)
        else:
            base_noise = 32 + 22 * math.log10(core_weight)
        
        # Adjust for flux density
        noise_Bm = base_noise + 15 * math.log10(Bm / 1.5)
        
        # Adjust for frequency
        noise_freq = noise_Bm + 10 * math.log10(self.frequency / 50)
        
        # Cooling system noise addition
        cooling_noise = 0
        if "ONAF" in self.cooling_type or "OFAF" in self.cooling_type:
            cooling_noise = 5 + math.log10(self.power / 1000)
            total_noise = 10 * math.log10(10 ** (noise_freq / 10) + 10 ** (cooling_noise / 10))
        else:
            total_noise = noise_freq
        
        return {
            "Core Noise (dB)": base_noise,
            "Flux Adjusted Noise (dB)": noise_Bm,
            "Frequency Adjusted Noise (dB)": noise_freq,
            "Cooling System Noise (dB)": cooling_noise,
            "Total Noise Level (dB)": total_noise
        }
    
    def calculate_mechanical_parameters(self, core_dims):
        """Calculate tank size, radiator requirements, etc."""
        # Core dimensions
        core_width = core_dims["Core Width (mm)"] / 1000  # meters
        core_depth = core_dims["Core Depth (mm)"] / 1000
        window_height = core_dims["Window Height (mm)"] / 1000
        yoke_height = core_dims.get("Yoke Height (mm)", 0) / 1000
        
        # Calculate approximate tank size
        if self.cooling_type in ["ONAN", "ONAF", "OFAF"]:
            # Oil-immersed transformer
            tank_width = core_width * 1.5
            tank_depth = core_depth * 1.5
            tank_height = window_height * 1.8
            
            # Oil volume (liter)
            oil_volume = (tank_width * tank_depth * tank_height) * 1000 * 0.7  # 70% fill
            
            # Radiator sizing (simplified)
            radiator_area = max(0.5, self.power / 500)  # m² per 500VA
            
            # Tank weight (kg)
            tank_weight = (2 * (tank_width + tank_depth) * tank_height + 
                          tank_width * tank_depth) * 5  # 5kg/m² steel
            
            mech_results = {
                "Tank Width (m)": tank_width,
                "Tank Depth (m)": tank_depth,
                "Tank Height (m)": tank_height,
                "Oil Volume (liter)": oil_volume,
                "Radiator Area (m²)": radiator_area,
                "Tank Weight (kg)": tank_weight
            }
            
            if self.power > 10000:  # Large transformers need conservator
                mech_results["Conservator Size (liter)"] = oil_volume * 0.1
        else:
            # Dry-type transformer
            enclosure_width = core_width * 1.3
            enclosure_depth = core_depth * 1.3
            enclosure_height = window_height * 1.5
            
            # Cooling vents/fans
            if self.cooling_type == "AF":
                fan_flow = max(0.1, self.power / 1000)  # m³/s per kVA
                mech_results = {
                    "Enclosure Width (m)": enclosure_width,
                    "Enclosure Depth (m)": enclosure_depth,
                    "Enclosure Height (m)": enclosure_height,
                    "Required Air Flow (m³/s)": fan_flow,
                    "Number of Fans": math.ceil(fan_flow / 0.05)  # 0.05 m³/s per fan
                }
            else:
                vent_area = max(0.1, self.power / 2000)  # m² per 2kVA
                mech_results = {
                    "Enclosure Width (m)": enclosure_width,
                    "Enclosure Depth (m)": enclosure_depth,
                    "Enclosure Height (m)": enclosure_height,
                    "Ventilation Area (m²)": vent_area
                }
        
        return mech_results
    
    def calculate_short_circuit(self, V1, N1, Ac, lmt):
        """Calculate short-circuit withstand capability"""
        # Calculate reactance
        X = 2 * math.pi * self.frequency * (4 * math.pi * 1e-7) * (N1 ** 2) * Ac * 1e-4 / (lmt)
        
        # Short-circuit current
        Isc = V1 / X
        
        # Mechanical forces
        F = 0.5 * (4 * math.pi * 1e-7) * (N1 * Isc) ** 2 / (lmt / N1)
        
        # Thermal capacity
        t_short = 2  # seconds (typical short-circuit duration)
        Q = Isc ** 2 * t_short
        
        return {
            "Reactance (Ohm)": X,
            "Short-Circuit Current (A)": Isc,
            "Radial Force (N)": F,
            "Thermal Capacity (A²s)": Q
        }
    
    def calculate_inrush_current(self, V1, N1, Ac):
        """Estimate inrush current"""
        # Residual flux (typically 50-80% of Bm)
        Br = 0.7 * self.Bm
        
        # Worst-case inrush occurs when switching at voltage zero
        Iinrush = (self.Bm + Br) * Ac * 1e-4 / (math.sqrt(2) * V1 / (2 * math.pi * self.frequency * N1))
        
        # Duration of inrush (cycles)
        tau = N1 * Ac * 1e-4 * (self.Bm + Br) / V1 * self.frequency
        
        return {
            "Peak Inrush Current (A)": Iinrush,
            "Inrush Duration (cycles)": tau
        }
    
    def calculate_cost(self, core_weight, cu_weight, design_complexity=1.0):
        """Estimate transformer cost"""
        # Material prices (USD/kg)
        material_costs = {
            "CRGO Steel": 3.5,
            "Amorphous Metal": 6.0,
            "Silicon Steel": 2.5,
            "Nano-Crystalline": 8.0,
            "High Permeability Steel": 4.5,
            "Copper": 9.0,
            "Aluminum": 3.0
        }
        
        # Core cost
        core_cost = core_weight * material_costs.get(self.core_material, 3.0)
        
        # Winding cost (assuming copper)
        winding_cost = cu_weight * material_costs["Copper"]
        
        # Labor cost factor
        labor_factors = {
            "Distribution Transformer": 1.0,
            "Power Transformer": 1.5,
            "Instrument Transformer": 2.0,
            "Autotransformer": 0.8,
            "Isolation Transformer": 1.2,
            "Rectifier Transformer": 1.3,
            "Phase Shifting Transformer": 2.5
        }
        labor_factor = labor_factors.get(self.transformer_type, 1.0)
        
        # Cooling system cost
        cooling_costs = {
            "ONAN": 0.1 * self.power,
            "ONAF": 0.15 * self.power,
            "OFAF": 0.2 * self.power,
            "Dry Type": 0.05 * self.power,
            "AN": 0.03 * self.power,
            "AF": 0.08 * self.power,
            "Water Cooled": 0.3 * self.power
        }
        cooling_cost = cooling_costs.get(self.cooling_type, 0.1 * self.power)
        
        # Total cost
        total_cost = (core_cost + winding_cost) * labor_factor * design_complexity + cooling_cost
        
        return {
            "Core Cost (USD)": core_cost,
            "Winding Cost (USD)": winding_cost,
            "Labor Factor": labor_factor,
            "Cooling Cost (USD)": cooling_cost,
            "Total Cost (USD)": total_cost
        }
    
    def optimize_design(self):
        """Optimize the design for cost, weight, or losses"""
        # Define objective function (minimize cost by default)
        def objective(x):
            # x[0] = Bm, x[1] = J
            self.Bm = x[0]
            self.J = x[1]
            self.calculate_design()
            
            # Get the parameter we want to optimize
            if self.optimization_target == "cost":
                return self.cost_results["Total Cost (USD)"]
            elif self.optimization_target == "weight":
                return self.results["Core Weight (kg)"] + self.results["Copper Weight (kg)"]
            else:  # losses
                return self.results["Total Losses (W)"]
        
        # Constraints
        constraints = []
        
        # Temperature rise constraint
        def temp_constraint(x):
            self.Bm = x[0]
            self.J = x[1]
            self.calculate_design()
            return self.max_temp_rise - self.thermal_results["Temperature Rise (°C)"]
        constraints.append({'type': 'ineq', 'fun': temp_constraint})
        
        # Losses constraint if specified
        if self.max_losses:
            def loss_constraint(x):
                self.Bm = x[0]
                self.J = x[1]
                self.calculate_design()
                return self.max_losses - self.results["Total Losses (W)"]
            constraints.append({'type': 'ineq', 'fun': loss_constraint})
        
        # Weight constraint if specified
        if self.max_weight:
            def weight_constraint(x):
                self.Bm = x[0]
                self.J = x[1]
                self.calculate_design()
                return self.max_weight - (self.results["Core Weight (kg)"] + self.results["Copper Weight (kg)"])
            constraints.append({'type': 'ineq', 'fun': weight_constraint})
        
        # Cost constraint if specified
        if self.max_cost:
            def cost_constraint(x):
                self.Bm = x[0]
                self.J = x[1]
                self.calculate_design()
                return self.max_cost - self.cost_results["Total Cost (USD)"]
            constraints.append({'type': 'ineq', 'fun': cost_constraint})
        
        # Noise constraint if specified
        if self.noise_limit:
            def noise_constraint(x):
                self.Bm = x[0]
                self.J = x[1]
                self.calculate_design()
                return self.noise_limit - self.results["Noise Level (dB)"]
            constraints.append({'type': 'ineq', 'fun': noise_constraint})
        
        # Bounds (Bm between 0.8 and 1.8 T, J between 1.5 and 6 A/mm²)
        bounds = [(0.8, 1.8), (1.5, 6.0)]
        
        # Initial guess
        x0 = [self.Bm, self.J]
        
        # Optimization
        print("\nRunning design optimization...")
        result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
        
        # Update with optimized parameters
        self.Bm = result.x[0]
        self.J = result.x[1]
        
        # Store optimization results
        self.optimization_results = {
            "Optimization Target": self.optimization_target,
            "Optimal Flux Density (T)": result.x[0],
            "Optimal Current Density (A/mm²)": result.x[1],
            "Final Objective Value": result.fun,
            "Success": result.success,
            "Message": result.message
        }
    
    def calculate_design(self):
        """Perform all design calculations"""
        self.design_steps = ["=== Design Methodology ==="]
        
        # 1. Core dimensions
        core_dims = self.calculate_core_dimensions()
        Ac = core_dims["Core Area (cm²)"]
        Ag = core_dims["Gross Core Area (cm²)"]
        
        self.design_steps.append(f"\n1. Core Dimensions ({self.core_shape}):")
        self.design_steps.append(f"   Core area: A_c = K*sqrt(P) = 0.9 × sqrt({self.power}) = {Ac:.2f} cm²")
        self.design_steps.append(f"   Gross core area: A_g = A_c/k = {Ac:.2f}/{self.k} = {Ag:.2f} cm²")
        for key, value in core_dims.items():
            if "mm" in key:
                self.design_steps.append(f"   {key}: {value:.1f}")
        
        # 2. Turns calculation
        turns = self.calculate_turns(Ac)
        N1 = turns["Primary Turns"]
        N2 = turns["Secondary Turns"]
        
        self.design_steps.append(f"\n2. Turns Calculation:")
        self.design_steps.append(f"   Primary turns: N1 = V1/(4.44×f×Bm×Ac) = {self.V1}/(4.44×{self.frequency}×{self.Bm}×{Ac:.2f}e-4) = {N1:.0f}")
        self.design_steps.append(f"   Secondary turns: N2 = V2×(1+alpha)/(4.44×f×Bm×Ac) = {self.V2}×1.05/(4.44×{self.frequency}×{self.Bm}×{Ac:.2f}e-4) = {N2:.0f}")
        
        # 3. Current calculation
        currents = self.calculate_currents()
        I1 = currents["Primary Current (A)"]
        I2 = currents["Secondary Current (A)"]
        
        self.design_steps.append(f"\n3. Current Calculation:")
        self.design_steps.append(f"   Primary current: I1 = P/V1 = {self.power}/{self.V1} = {I1:.2f} A")
        self.design_steps.append(f"   Secondary current: I2 = P/V2 = {self.power}/{self.V2} = {I2:.2f} A")
        
        # 4. Conductor sizing
        primary_conductor = self.calculate_conductor_size(I1)
        secondary_conductor = self.calculate_conductor_size(I2)
        Aw1 = primary_conductor["Conductor Area (mm²)"]
        Aw2 = secondary_conductor["Conductor Area (mm²)"]
        
        self.design_steps.append(f"\n4. Conductor Sizing:")
        self.design_steps.append(f"   Primary conductor area: Aw1 = I1/J = {I1:.2f}/{self.J} = {Aw1:.4f} mm²")
        self.design_steps.append(f"   Secondary conductor area: Aw2 = I2/J = {I2:.2f}/{self.J} = {Aw2:.4f} mm²")
        self.design_steps.append(f"   Primary wire: {primary_conductor['SWG']['SWG']} ({primary_conductor['SWG']['Diameter']} mm)")
        self.design_steps.append(f"   Secondary wire: {secondary_conductor['SWG']['SWG']} ({secondary_conductor['SWG']['Diameter']} mm)")
        
        # Check for Litz wire
        if 'Strands' in primary_conductor['SWG']:
            self.design_steps.append(f"   Primary requires Litz wire: {primary_conductor['SWG']['Strands']} strands of {primary_conductor['SWG']['Strand SWG']}")
        if 'Strands' in secondary_conductor['SWG']:
            self.design_steps.append(f"   Secondary requires Litz wire: {secondary_conductor['SWG']['Strands']} strands of {secondary_conductor['SWG']['Strand SWG']}")
        
        # 5. Winding design
        primary_winding = self.calculate_winding(N1, I1, Aw1, core_dims["Window Width (mm)"], core_dims["Window Height (mm)"])
        secondary_winding = self.calculate_winding(N2, I2, Aw2, core_dims["Window Width (mm)"], core_dims["Window Height (mm)"])
        
        self.design_steps.append(f"\n5. Winding Design ({self.winding_type}):")
        self.design_steps.append("   Primary Winding:")
        for key, value in primary_winding["Winding Configuration"].items():
            self.design_steps.append(f"      {key}: {value}")
        self.design_steps.append("   Secondary Winding:")
        for key, value in secondary_winding["Winding Configuration"].items():
            self.design_steps.append(f"      {key}: {value}")
        
        # 6. Loss calculations
        core_loss = self.calculate_core_loss(Ac, core_dims["Core Building Factor"])
        primary_eddy = self.calculate_eddy_losses(I1, Aw1, N1, primary_winding["Mean Turn Length (m)"])
        secondary_eddy = self.calculate_eddy_losses(I2, Aw2, N2, secondary_winding["Mean Turn Length (m)"])
        
        # Calculate total copper loss before stray losses
        total_copper_loss = primary_winding["Copper Loss (W)"] + secondary_winding["Copper Loss (W)"]
        
        # Now calculate stray losses
        stray_loss = self.calculate_stray_losses(total_copper_loss)
        
        harmonic_loss = self.calculate_harmonic_losses(total_copper_loss, 
                                                     primary_eddy["Eddy Loss (W)"] + secondary_eddy["Eddy Loss (W)"])
        
        total_copper_loss += harmonic_loss["Harmonic Copper Loss (W)"]
        total_eddy_loss = primary_eddy["Eddy Loss (W)"] + secondary_eddy["Eddy Loss (W)"] + harmonic_loss["Harmonic Eddy Loss (W)"]
        total_losses = total_copper_loss + core_loss["Core Loss (W)"] + total_eddy_loss + stray_loss["Stray Loss (W)"]
        
        self.design_steps.append(f"\n6. Loss Calculations:")
        self.design_steps.append(f"   Primary copper loss: {primary_winding['Copper Loss (W)']:.2f} W")
        self.design_steps.append(f"   Secondary copper loss: {secondary_winding['Copper Loss (W)']:.2f} W")
        self.design_steps.append(f"   Harmonic copper loss: {harmonic_loss['Harmonic Copper Loss (W)']:.2f} W")
        self.design_steps.append(f"   Primary eddy loss: {primary_eddy['Eddy Loss (W)']:.2f} W")
        self.design_steps.append(f"   Secondary eddy loss: {secondary_eddy['Eddy Loss (W)']:.2f} W")
        self.design_steps.append(f"   Harmonic eddy loss: {harmonic_loss['Harmonic Eddy Loss (W)']:.2f} W")
        self.design_steps.append(f"   Core loss: {core_loss['Core Loss (W)']:.2f} W")
        self.design_steps.append(f"   Stray loss: {stray_loss['Stray Loss (W)']:.2f} W")
        self.design_steps.append(f"   Total losses: {total_losses:.2f} W")
        
        # 7. Temperature rise
        # Calculate surface area (simplified)
        surface_area = 2 * ((core_dims["Core Width (mm)"]/1000 * core_dims["Core Depth (mm)"]/1000) +
                           (core_dims["Core Width (mm)"]/1000 * core_dims["Window Height (mm)"]/1000) +
                           (core_dims["Core Depth (mm)"]/1000 * core_dims["Window Height (mm)"]/1000))
        
        thermal = self.calculate_temperature_rise(total_losses, surface_area)
        
        self.design_steps.append(f"\n7. Thermal Analysis:")
        self.design_steps.append(f"   Surface area: {surface_area:.2f} m²")
        self.design_steps.append(f"   Cooling coefficient: {thermal['Cooling Coefficient (W/m²°C)']:.1f} W/m²°C")
        self.design_steps.append(f"   Temperature rise: {thermal['Temperature Rise (°C)']:.1f} °C")
        self.design_steps.append(f"   Hot spot temperature: {thermal['Hot Spot Temperature (°C)']:.1f} °C")
        
        # 8. Noise calculation
        if self.noise_limit:
            noise = self.calculate_noise_level(core_loss["Core Weight (kg)"], self.Bm)
            self.design_steps.append(f"\n8. Noise Calculation:")
            self.design_steps.append(f"   Core noise: {noise['Core Noise (dB)']:.1f} dB")
            self.design_steps.append(f"   Flux adjusted noise: {noise['Flux Adjusted Noise (dB)']:.1f} dB")
            self.design_steps.append(f"   Frequency adjusted noise: {noise['Frequency Adjusted Noise (dB)']:.1f} dB")
            if noise['Cooling System Noise (dB)'] > 0:
                self.design_steps.append(f"   Cooling system noise: {noise['Cooling System Noise (dB)']:.1f} dB")
            self.design_steps.append(f"   Total noise level: {noise['Total Noise Level (dB)']:.1f} dB")
        
        # 9. Mechanical design
        mech = self.calculate_mechanical_parameters(core_dims)
        
        self.design_steps.append(f"\n9. Mechanical Design:")
        for key, value in mech.items():
            self.design_steps.append(f"   {key}: {value:.2f}")
        
        # 10. Short-circuit and inrush
        short_circuit = self.calculate_short_circuit(self.V1, N1, Ac, primary_winding["Mean Turn Length (m)"])
        inrush = self.calculate_inrush_current(self.V1, N1, Ac)
        
        self.design_steps.append(f"\n10. Dynamic Performance:")
        self.design_steps.append(f"   Reactance: {short_circuit['Reactance (Ohm)']:.4f} Ohm")
        self.design_steps.append(f"   Short-circuit current: {short_circuit['Short-Circuit Current (A)']:.1f} A")
        self.design_steps.append(f"   Radial force: {short_circuit['Radial Force (N)']:.1f} N")
        self.design_steps.append(f"   Thermal capacity: {short_circuit['Thermal Capacity (A²s)']:.1f} A²s")
        self.design_steps.append(f"   Peak inrush current: {inrush['Peak Inrush Current (A)']:.1f} A")
        self.design_steps.append(f"   Inrush duration: {inrush['Inrush Duration (cycles)']:.1f} cycles")
        
        # 11. Cost estimation
        # Calculate copper weight
        cu_volume = (primary_winding["Mean Turn Length (m)"] * N1 * Aw1 * 1e-6 +
                    secondary_winding["Mean Turn Length (m)"] * N2 * Aw2 * 1e-6)  # m³
        cu_weight = cu_volume * 8960  # kg (density of copper)
        
        cost = self.calculate_cost(core_loss["Core Weight (kg)"], cu_weight)
        
        self.design_steps.append(f"\n11. Cost Estimation:")
        self.design_steps.append(f"   Core weight: {core_loss['Core Weight (kg)']:.1f} kg")
        self.design_steps.append(f"   Copper weight: {cu_weight:.1f} kg")
        self.design_steps.append(f"   Core cost: ${cost['Core Cost (USD)']:.2f}")
        self.design_steps.append(f"   Winding cost: ${cost['Winding Cost (USD)']:.2f}")
        self.design_steps.append(f"   Cooling cost: ${cost['Cooling Cost (USD)']:.2f}")
        self.design_steps.append(f"   Total cost: ${cost['Total Cost (USD)']:.2f}")
        
        # Store all results
        self.results = {
            **core_dims,
            **turns,
            **currents,
            "Primary Conductor": primary_conductor,
            "Secondary Conductor": secondary_conductor,
            "Primary Winding": primary_winding,
            "Secondary Winding": secondary_winding,
            "Core Loss": core_loss,
            "Primary Eddy Loss": primary_eddy,
            "Secondary Eddy Loss": secondary_eddy,
            "Stray Loss": stray_loss,
            "Harmonic Loss": harmonic_loss,
            "Total Copper Loss (W)": total_copper_loss,
            "Total Eddy Loss (W)": total_eddy_loss,
            "Total Losses (W)": total_losses,
            "Thermal Analysis": thermal,
            "Mechanical Design": mech,
            "Short-Circuit Analysis": short_circuit,
            "Inrush Current": inrush,
            "Copper Weight (kg)": cu_weight,
            "Surface Area (m²)": surface_area
        }
        
        if self.noise_limit:
            self.results["Noise Level (dB)"] = noise["Total Noise Level (dB)"]
        
        self.cost_results = cost
        self.thermal_results = thermal
        
        # Calculate efficiency
        input_power = self.power + total_losses
        calculated_efficiency = self.power / input_power
        self.results["Efficiency (%)"] = calculated_efficiency * 100
    
    def generate_pdf_report(self, filename="transformer_design_report.pdf"):
        """Generate a comprehensive PDF report with all design details"""
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Use standard fonts instead of trying to load custom ones
        pdf.set_font('Arial', 'B', 16)
        
        # Title
        pdf.cell(0, 10, "Advanced Transformer Design Report", 0, 1, 'C')
        pdf.ln(5)
        
        # Date and standard
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
        pdf.cell(0, 6, f"Design Standard: {self.standard}", 0, 1)
        pdf.ln(5)
        
        # Project information
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, "Project Information", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        info_data = [
            ["Transformer Type:", self.transformer_type],
            ["Core Material:", self.core_material],
            ["Cooling Type:", self.cooling_type],
            ["Phase Configuration:", self.phase],
            ["Core Shape:", self.core_shape],
            ["Winding Type:", self.winding_type]
        ]
        
        if self.phase == "Three Phase":
            info_data.append(["Connection Type:", self.connection_type])
        
        for item in info_data:
            pdf.cell(60, 6, item[0], 0, 0)
            pdf.cell(0, 6, item[1], 0, 1)
        
        pdf.ln(3)
        
        # Electrical parameters
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, "Electrical Parameters:", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        elec_data = [
            ["Primary Voltage:", f"{self.V1} V"],
            ["Secondary Voltage:", f"{self.V2} V"],
            ["Frequency:", f"{self.frequency} Hz"],
            ["Power Rating:", f"{self.power} VA"],
            ["Target Efficiency:", f"{self.efficiency*100:.1f}%"],
            ["Regulation:", f"{self.regulation*100:.1f}%"],
            ["Flux Density:", f"{self.Bm:.2f} T"],
            ["Current Density:", f"{self.J:.2f} A/mm²"]
        ]
        
        for item in elec_data:
            pdf.cell(60, 6, item[0], 0, 0)
            pdf.cell(0, 6, item[1], 0, 1)
        
        pdf.ln(3)
        
        # Environmental parameters
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, "Environmental Parameters:", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        env_data = [
            ["Ambient Temperature:", f"{self.ambient_temp} °C"],
            ["Maximum Temperature Rise:", f"{self.max_temp_rise} °C"],
            ["Altitude:", f"{self.altitude} m"],
            ["Harmonic Factor:", f"{self.harmonic_factor}"]
        ]
        
        if self.noise_limit:
            env_data.append(["Noise Limit:", f"{self.noise_limit} dB"])
        
        for item in env_data:
            pdf.cell(60, 6, item[0], 0, 0)
            pdf.cell(0, 6, item[1], 0, 1)
        
        pdf.ln(5)
        
        # Design Summary
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, "Design Summary", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        summary_data = [
            ["Core Area:", f"{self.results['Core Area (cm²)']:.2f} cm²"],
            ["Core Dimensions:", f"{self.results['Core Width (mm)']:.1f} × {self.results['Core Depth (mm)']:.1f} mm"],
            ["Window Dimensions:", f"{self.results['Window Width (mm)']:.1f} × {self.results['Window Height (mm)']:.1f} mm"],
            ["Primary Turns:", f"{self.results['Primary Turns']:.0f}"],
            ["Secondary Turns:", f"{self.results['Secondary Turns']:.0f}"],
            ["Primary Current:", f"{self.results['Primary Current (A)']:.2f} A"],
            ["Secondary Current:", f"{self.results['Secondary Current (A)']:.2f} A"],
            ["Primary Conductor:", f"{self.results['Primary Conductor']['SWG']['SWG']} ({self.results['Primary Conductor']['Conductor Area (mm²)']:.2f} mm²)"],
            ["Secondary Conductor:", f"{self.results['Secondary Conductor']['SWG']['SWG']} ({self.results['Secondary Conductor']['Conductor Area (mm²)']:.2f} mm²)"],
            ["Calculated Efficiency:", f"{self.results['Efficiency (%)']:.2f}%"],
            ["Total Losses:", f"{self.results['Total Losses (W)']:.2f} W"],
            ["Temperature Rise:", f"{self.results['Thermal Analysis']['Temperature Rise (°C)']:.1f} °C"],
            ["Hot Spot Temp:", f"{self.results['Thermal Analysis']['Hot Spot Temperature (°C)']:.1f} °C"],
            ["Core Weight:", f"{self.results['Core Loss']['Core Weight (kg)']:.1f} kg"],
            ["Copper Weight:", f"{self.results['Copper Weight (kg)']:.1f} kg"],
            ["Total Cost:", f"${self.cost_results['Total Cost (USD)']:.2f}"]
        ]
        
        if 'Noise Level (dB)' in self.results:
            summary_data.insert(12, ["Noise Level:", f"{self.results['Noise Level (dB)']:.1f} dB"])
        
        for item in summary_data:
            pdf.cell(60, 6, item[0], 0, 0)
            pdf.cell(0, 6, item[1], 0, 1)
        
        # Add detailed sections
        self.add_detailed_sections(pdf)
        
        # Save PDF
        pdf.output(filename)
        print(f"\nReport generated successfully: {filename}")
    
    def add_detailed_sections(self, pdf):
        """Add detailed design sections to the PDF"""
        # Core Design Details
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, "Core Design Details", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        core_data = [
            ["Core Shape:", self.core_shape],
            ["Material:", self.core_material],
            ["Stacking Factor:", f"{self.k:.3f}"],
            ["Building Factor:", f"{self.results['Core Building Factor']:.3f}"],
            ["Net Core Area:", f"{self.results['Core Area (cm²)']:.2f} cm²"],
            ["Gross Core Area:", f"{self.results['Gross Core Area (cm²)']:.2f} cm²"],
            ["Core Width:", f"{self.results['Core Width (mm)']:.1f} mm"],
            ["Core Depth:", f"{self.results['Core Depth (mm)']:.1f} mm"],
            ["Window Width:", f"{self.results['Window Width (mm)']:.1f} mm"],
            ["Window Height:", f"{self.results['Window Height (mm)']:.1f} mm"],
            ["Core Volume:", f"{self.results['Core Loss']['Core Volume (cm³)']:.1f} cm³"],
            ["Core Weight:", f"{self.results['Core Loss']['Core Weight (kg)']:.1f} kg"],
            ["Flux Density:", f"{self.Bm:.3f} T"],
            ["Core Loss:", f"{self.results['Core Loss']['Core Loss (W)']:.2f} W"]
        ]
        
        if 'Yoke Height (mm)' in self.results:
            core_data.insert(9, ["Yoke Height:", f"{self.results['Yoke Height (mm)']:.1f} mm"])
        
        for item in core_data:
            pdf.cell(70, 6, item[0], 0, 0)
            pdf.cell(0, 6, item[1], 0, 1)
        
        # Winding Design Details
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, "Winding Design Details", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        pdf.cell(0, 6, f"Winding Type: {self.winding_type}", 0, 1)
        pdf.ln(2)
        
        # Primary Winding
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, "Primary Winding:", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        primary_data = [
            ["Turns:", f"{self.results['Primary Turns']:.0f}"],
            ["Current:", f"{self.results['Primary Current (A)']:.2f} A"],
            ["Conductor Area:", f"{self.results['Primary Conductor']['Conductor Area (mm²)']:.4f} mm²"],
            ["Conductor Type:", f"{self.results['Primary Conductor']['SWG']['SWG']} ({self.results['Primary Conductor']['SWG']['Diameter']} mm)"],
            ["Mean Turn Length:", f"{self.results['Primary Winding']['Mean Turn Length (m)']:.3f} m"],
            ["Resistance:", f"{self.results['Primary Winding']['Resistance (Ohm)']:.4f} Ohm"],
            ["Copper Loss:", f"{self.results['Primary Winding']['Copper Loss (W)']:.2f} W"],
            ["Eddy Loss:", f"{self.results['Primary Eddy Loss']['Eddy Loss (W)']:.2f} W"],
            ["Skin Depth:", f"{self.results['Primary Conductor']['Skin Depth (mm)']:.3f} mm"]
        ]
        
        if 'Strands' in self.results['Primary Conductor']['SWG']:
            primary_data.append(["Litz Wire:", f"{self.results['Primary Conductor']['SWG']['Strands']} strands of {self.results['Primary Conductor']['SWG']['Strand SWG']}"])
        
        for item in primary_data:
            pdf.cell(70, 6, item[0], 0, 0)
            pdf.cell(0, 6, item[1], 0, 1)
        
        # Winding configuration
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, "Winding Configuration:", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        for key, value in self.results['Primary Winding']['Winding Configuration'].items():
            pdf.cell(70, 6, key, 0, 0)
            pdf.cell(0, 6, str(value), 0, 1)
        
        # Secondary Winding
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, "Secondary Winding:", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        secondary_data = [
            ["Turns:", f"{self.results['Secondary Turns']:.0f}"],
            ["Current:", f"{self.results['Secondary Current (A)']:.2f} A"],
            ["Conductor Area:", f"{self.results['Secondary Conductor']['Conductor Area (mm²)']:.4f} mm²"],
            ["Conductor Type:", f"{self.results['Secondary Conductor']['SWG']['SWG']} ({self.results['Secondary Conductor']['SWG']['Diameter']} mm)"],
            ["Mean Turn Length:", f"{self.results['Secondary Winding']['Mean Turn Length (m)']:.3f} m"],
            ["Resistance:", f"{self.results['Secondary Winding']['Resistance (Ohm)']:.4f} Ohm"],
            ["Copper Loss:", f"{self.results['Secondary Winding']['Copper Loss (W)']:.2f} W"],
            ["Eddy Loss:", f"{self.results['Secondary Eddy Loss']['Eddy Loss (W)']:.2f} W"],
            ["Skin Depth:", f"{self.results['Secondary Conductor']['Skin Depth (mm)']:.3f} mm"]
        ]
        
        if 'Strands' in self.results['Secondary Conductor']['SWG']:
            secondary_data.append(["Litz Wire:", f"{self.results['Secondary Conductor']['SWG']['Strands']} strands of {self.results['Secondary Conductor']['SWG']['Strand SWG']}"])
        
        for item in secondary_data:
            pdf.cell(70, 6, item[0], 0, 0)
            pdf.cell(0, 6, item[1], 0, 1)
        
        # Winding configuration
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, "Winding Configuration:", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        for key, value in self.results['Secondary Winding']['Winding Configuration'].items():
            pdf.cell(70, 6, key, 0, 0)
            pdf.cell(0, 6, str(value), 0, 1)
        
        # Loss Analysis
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, "Loss Analysis", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        loss_data = [
            ["Primary Copper Loss:", f"{self.results['Primary Winding']['Copper Loss (W)']:.2f} W"],
            ["Secondary Copper Loss:", f"{self.results['Secondary Winding']['Copper Loss (W)']:.2f} W"],
            ["Harmonic Copper Loss:", f"{self.results['Harmonic Loss']['Harmonic Copper Loss (W)']:.2f} W"],
            ["Total Copper Loss:", f"{self.results['Total Copper Loss (W)']:.2f} W"],
            ["Primary Eddy Loss:", f"{self.results['Primary Eddy Loss']['Eddy Loss (W)']:.2f} W"],
            ["Secondary Eddy Loss:", f"{self.results['Secondary Eddy Loss']['Eddy Loss (W)']:.2f} W"],
            ["Harmonic Eddy Loss:", f"{self.results['Harmonic Loss']['Harmonic Eddy Loss (W)']:.2f} W"],
            ["Total Eddy Loss:", f"{self.results['Total Eddy Loss (W)']:.2f} W"],
            ["Core Loss:", f"{self.results['Core Loss']['Core Loss (W)']:.2f} W"],
            ["Stray Loss:", f"{self.results['Stray Loss']['Stray Loss (W)']:.2f} W"],
            ["Total Losses:", f"{self.results['Total Losses (W)']:.2f} W"]
        ]
        
        for item in loss_data:
            pdf.cell(80, 6, item[0], 0, 0)
            pdf.cell(0, 6, item[1], 0, 1)
        
        # Thermal Analysis
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, "Thermal Analysis", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        thermal_data = [
            ["Cooling Type:", self.cooling_type],
            ["Surface Area:", f"{self.results['Surface Area (m²)']:.3f} m²"],
            ["Cooling Coefficient:", f"{self.results['Thermal Analysis']['Cooling Coefficient (W/m²°C)']:.1f} W/m²°C"],
            ["Adjusted Coefficient:", f"{self.results['Thermal Analysis']['Adjusted Coefficient (W/m²°C)']:.1f} W/m²°C"],
            ["Temperature Rise:", f"{self.results['Thermal Analysis']['Temperature Rise (°C)']:.1f} °C"],
            ["Hot Spot Temperature:", f"{self.results['Thermal Analysis']['Hot Spot Temperature (°C)']:.1f} °C"],
            ["Ambient Temperature:", f"{self.ambient_temp} °C"],
            ["Maximum Allowed Rise:", f"{self.max_temp_rise} °C"]
        ]
        
        for item in thermal_data:
            pdf.cell(80, 6, item[0], 0, 0)
            pdf.cell(0, 6, item[1], 0, 1)
        
        # Mechanical Design
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, "Mechanical Design", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        for key, value in self.results['Mechanical Design'].items():
            pdf.cell(80, 6, key, 0, 0)
            if isinstance(value, float):
                pdf.cell(0, 6, f"{value:.2f}", 0, 1)
            else:
                pdf.cell(0, 6, str(value), 0, 1)
        
        # Dynamic Performance
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, "Dynamic Performance", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        dynamic_data = [
            ["Reactance:", f"{self.results['Short-Circuit Analysis']['Reactance (Ohm)']:.4f} Ohm"],
            ["Short-Circuit Current:", f"{self.results['Short-Circuit Analysis']['Short-Circuit Current (A)']:.1f} A"],
            ["Radial Force:", f"{self.results['Short-Circuit Analysis']['Radial Force (N)']:.1f} N"],
            ["Thermal Capacity:", f"{self.results['Short-Circuit Analysis']['Thermal Capacity (A²s)']:.1f} A²s"],
            ["Peak Inrush Current:", f"{self.results['Inrush Current']['Peak Inrush Current (A)']:.1f} A"],
            ["Inrush Duration:", f"{self.results['Inrush Current']['Inrush Duration (cycles)']:.1f} cycles"]
        ]
        
        for item in dynamic_data:
            pdf.cell(80, 6, item[0], 0, 0)
            pdf.cell(0, 6, item[1], 0, 1)
        
        # Cost Analysis
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, "Cost Analysis", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        cost_data = [
            ["Core Weight:", f"{self.results['Core Loss']['Core Weight (kg)']:.1f} kg"],
            ["Copper Weight:", f"{self.results['Copper Weight (kg)']:.1f} kg"],
            ["Core Cost:", f"${self.cost_results['Core Cost (USD)']:.2f}"],
            ["Winding Cost:", f"${self.cost_results['Winding Cost (USD)']:.2f}"],
            ["Cooling Cost:", f"${self.cost_results['Cooling Cost (USD)']:.2f}"],
            ["Labor Factor:", f"{self.cost_results['Labor Factor']:.1f}"],
            ["Total Cost:", f"${self.cost_results['Total Cost (USD)']:.2f}"]
        ]
        
        for item in cost_data:
            pdf.cell(80, 6, item[0], 0, 0)
            pdf.cell(0, 6, item[1], 0, 1)
        
        # Add design methodology
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, "Design Methodology", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        for step in self.design_steps:
            pdf.multi_cell(0, 5, step)
            pdf.ln(2)
    
    def add_core_diagram(self, pdf):
        """Add a diagram of the core structure to the PDF"""
        # Create a simple diagram using matplotlib
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Get dimensions in cm for drawing
        core_width = self.results['Core Width (mm)'] / 10
        core_depth = self.results['Core Depth (mm)'] / 10
        window_width = self.results['Window Width (mm)'] / 10
        window_height = self.results['Window Height (mm)'] / 10
        
        if self.core_shape == "EI Core":
            # Draw EI core
            # Center limb
            ax.add_patch(plt.Rectangle((window_width/2, window_height/2), 
                                     core_width - window_width, 
                                     core_depth - window_height, 
                                     fill=False, edgecolor='blue', linewidth=2))
            
            # Outer limbs
            ax.add_patch(plt.Rectangle((0, window_height/2), 
                                     window_width/2, 
                                     core_depth - window_height, 
                                     fill=False, edgecolor='blue', linewidth=2))
            ax.add_patch(plt.Rectangle((core_width - window_width/2, window_height/2), 
                                     window_width/2, 
                                     core_depth - window_height, 
                                     fill=False, edgecolor='blue', linewidth=2))
            
            # Yokes
            ax.add_patch(plt.Rectangle((0, 0), 
                                     core_width, 
                                     window_height/2, 
                                     fill=False, edgecolor='blue', linewidth=2))
            ax.add_patch(plt.Rectangle((0, core_depth - window_height/2), 
                                     core_width, 
                                     window_height/2, 
                                     fill=False, edgecolor='blue', linewidth=2))
            
            # Window
            ax.add_patch(plt.Rectangle((window_width/2, window_height/2), 
                                     core_width - window_width, 
                                     core_depth - window_height, 
                                     fill=False, edgecolor='red', linestyle='--', linewidth=1))
            
            # Labels
            ax.text(core_width/2, -0.5, f"EI Core: {core_width:.1f}cm × {core_depth:.1f}cm", ha='center')
            ax.text(core_width/2, window_height/2, f"Window: {window_width:.1f}cm × {window_height:.1f}cm", ha='center', va='center')
        
        elif self.core_shape == "Toroidal":
            # Draw toroidal core
            mean_radius = (window_width + core_width) / 4
            torus = plt.Circle((mean_radius, mean_radius), mean_radius, 
                             fill=False, edgecolor='blue', linewidth=2)
            ax.add_patch(torus)
            
            # Window representation
            inner_radius = window_width / 2
            ax.add_patch(plt.Circle((mean_radius, mean_radius), inner_radius,
                                   fill=False, edgecolor='red', linestyle='--', linewidth=1))
            
            # Labels
            ax.text(mean_radius, -0.5, f"Toroidal Core: Ø{2*mean_radius:.1f}cm", ha='center')
            ax.text(mean_radius, mean_radius, f"Window: Ø{window_width:.1f}cm", ha='center', va='center')
        
        # Common settings
        ax.set_xlim(-1, core_width + 1)
        ax.set_ylim(-1, core_depth + 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Save the plot to a temporary file and add to PDF
        temp_img = "temp_core_diagram.png"
        plt.savefig(temp_img, dpi=300, bbox_inches='tight')
        plt.close()
        
        pdf.image(temp_img, x=50, y=None, w=100)

# Main program execution
if __name__ == "__main__":
    print("=== Advanced Transformer Design Software ===")
    print("This program designs transformers with comprehensive features")
    
    designer = TransformerDesign()
    designer.get_user_inputs()
    
    # Ask for optimization
    optimize = input("\nDo you want to optimize the design? (y/n): ").lower()
    if optimize == 'y':
        print("\nOptimization Targets:")
        print("1. Minimize Cost")
        print("2. Minimize Weight")
        print("3. Minimize Losses")
        target = input("Select optimization target (1-3): ")
        targets = {
            "1": "cost",
            "2": "weight",
            "3": "losses"
        }
        designer.optimization_target = targets.get(target, "cost")
        designer.optimize_design()
    
    designer.calculate_design()
    
    report_name = input("\nEnter report filename (default: transformer_design_report.pdf): ") or "transformer_design_report.pdf"
    designer.generate_pdf_report(report_name)
    
    print("\nDesign process completed successfully!")
