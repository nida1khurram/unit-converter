import streamlit as st
import pandas as pd

# Conversion functions for each category
def length_conversion(value, from_unit, to_unit):
    units = {
        'Kilometer': 1000, 'Meter': 1, 'Centimeter': 0.01,
        'Millimeter': 0.001, 'Mile': 1609.34, 'Yard': 0.9144,
        'Foot': 0.3048, 'Inch': 0.0254
    }
    return value * units[from_unit] / units[to_unit]

def area_conversion(value, from_unit, to_unit):
    units = {
        'Square Kilometer': 1000000, 'Square Meter': 1,
        'Square Mile': 2589988.11, 'Square Yard': 0.836127,
        'Square Foot': 0.092903, 'Square Inch': 0.00064516,
        'Hectare': 10000, 'Acre': 4046.86
    }
    return value * units[from_unit] / units[to_unit]

def data_transfer_rate_conversion(value, from_unit, to_unit):
    units = {
        'Bit per second': 1, 'Kilobit per second': 1000,
        'Megabit per second': 1000000, 'Gigabit per second': 1000000000,
        'Byte per second': 8, 'Kilobyte per second': 8000,
        'Megabyte per second': 8000000, 'Gigabyte per second': 8000000000
    }
    return value * units[from_unit] / units[to_unit]

def digital_storage_conversion(value, from_unit, to_unit):
    units = {
        'Bit': 1, 'Byte': 8,
        'Kilobyte': 8*1024, 'Megabyte': 8*1024**2,
        'Gigabyte': 8*1024**3, 'Terabyte': 8*1024**4,
        'Petabyte': 8*1024**5
    }
    return value * units[from_unit] / units[to_unit]

def energy_conversion(value, from_unit, to_unit):
    units = {
        'Joule': 1, 'Kilojoule': 1000,
        'Calorie': 4.184, 'Kilocalorie': 4184,
        'Watt-hour': 3600, 'Kilowatt-hour': 3600000,
        'Electron volt': 1.602176634e-19
    }
    return value * units[from_unit] / units[to_unit]

def frequency_conversion(value, from_unit, to_unit):
    units = {
        'Hertz': 1, 'Kilohertz': 1000,
        'Megahertz': 1000000, 'Gigahertz': 1000000000
    }
    return value * units[from_unit] / units[to_unit]

def fuel_economy_conversion(value, from_unit, to_unit):
    # Base unit: kilometers per liter
    units = {
        'Miles per gallon': 0.425144, 'Kilometers per liter': 1,
        'Liters per 100 kilometers': lambda x: 100/x,
        'Miles per liter': 1.609344
    }
    if callable(units[from_unit]):
        base_value = units[from_unit](value)
    else:
        base_value = value * units[from_unit]
    
    if callable(units[to_unit]):
        return units[to_unit](base_value)
    return base_value / units[to_unit]

def mass_conversion(value, from_unit, to_unit):
    units = {
        'Tonne': 1000000, 'Kilogram': 1000,
        'Gram': 1, 'Milligram': 0.001,
        'Pound': 453.592, 'Ounce': 28.3495
    }
    return value * units[from_unit] / units[to_unit]

def plane_angle_conversion(value, from_unit, to_unit):
    units = {
        'Degree': 1, 'Radian': 57.2958,
        'Gradian': 0.9, 'Milliradian': 0.057296
    }
    return value * units[from_unit] / units[to_unit]

def pressure_conversion(value, from_unit, to_unit):
    units = {
        'Pascal': 1, 'Kilopascal': 1000,
        'Bar': 100000, 'PSI': 6894.76,
        'Atmosphere': 101325, 'Millimeter of mercury': 133.322
    }
    return value * units[from_unit] / units[to_unit]

def speed_conversion(value, from_unit, to_unit):
    units = {
        'Meter per second': 1, 'Kilometer per hour': 0.277778,
        'Mile per hour': 0.44704, 'Knot': 0.514444,
        'Foot per second': 0.3048
    }
    return value * units[from_unit] / units[to_unit]

def temperature_conversion(value, from_unit, to_unit):
    if from_unit == 'Celsius':
        if to_unit == 'Fahrenheit': return (value * 9/5) + 32
        if to_unit == 'Kelvin': return value + 273.15
    elif from_unit == 'Fahrenheit':
        if to_unit == 'Celsius': return (value - 32) * 5/9
        if to_unit == 'Kelvin': return (value - 32) * 5/9 + 273.15
    elif from_unit == 'Kelvin':
        if to_unit == 'Celsius': return value - 273.15
        if to_unit == 'Fahrenheit': return (value - 273.15) * 9/5 + 32
    return value

def time_conversion(value, from_unit, to_unit):
    units = {
        'Second': 1, 'Minute': 60,
        'Hour': 3600, 'Day': 86400,
        'Week': 604800, 'Month': 2592000,
        'Year': 31536000
    }
    return value * units[from_unit] / units[to_unit]

def volume_conversion(value, from_unit, to_unit):
    units = {
        'Cubic meter': 1000, 'Liter': 1,
        'Milliliter': 0.001, 'Gallon': 3.78541,
        'Quart': 0.946353, 'Pint': 0.473176,
        'Cup': 0.236588, 'Fluid ounce': 0.0295735,
        'Cubic foot': 28.3168, 'Cubic inch': 0.0163871
    }
    return value * units[from_unit] / units[to_unit]

# Categories and their units
categories = {
    'Length': ['Kilometer', 'Meter', 'Centimeter', 'Millimeter', 'Mile', 'Yard', 'Foot', 'Inch'],
    'Area': ['Square Kilometer', 'Square Meter', 'Square Mile', 'Square Yard', 'Square Foot', 'Square Inch', 'Hectare', 'Acre'],
    'Data Transfer Rate': ['Bit per second', 'Kilobit per second', 'Megabit per second', 'Gigabit per second', 
                          'Byte per second', 'Kilobyte per second', 'Megabyte per second', 'Gigabyte per second'],
    'Digital Storage': ['Bit', 'Byte', 'Kilobyte', 'Megabyte', 'Gigabyte', 'Terabyte', 'Petabyte'],
    'Energy': ['Joule', 'Kilojoule', 'Calorie', 'Kilocalorie', 'Watt-hour', 'Kilowatt-hour', 'Electron volt'],
    'Frequency': ['Hertz', 'Kilohertz', 'Megahertz', 'Gigahertz'],
    'Fuel Economy': ['Miles per gallon', 'Kilometers per liter', 'Liters per 100 kilometers', 'Miles per liter'],
    'Mass': ['Tonne', 'Kilogram', 'Gram', 'Milligram', 'Pound', 'Ounce'],
    'Plane Angle': ['Degree', 'Radian', 'Gradian', 'Milliradian'],
    'Pressure': ['Pascal', 'Kilopascal', 'Bar', 'PSI', 'Atmosphere', 'Millimeter of mercury'],
    'Speed': ['Meter per second', 'Kilometer per hour', 'Mile per hour', 'Knot', 'Foot per second'],
    'Temperature': ['Celsius', 'Fahrenheit', 'Kelvin'],
    'Time': ['Second', 'Minute', 'Hour', 'Day', 'Week', 'Month', 'Year'],
    'Volume': ['Cubic meter', 'Liter', 'Milliliter', 'Gallon', 'Quart', 'Pint', 'Cup', 'Fluid ounce', 'Cubic foot', 'Cubic inch']
}

# Mapping categories to conversion functions
conversion_functions = {
    'Length': length_conversion,
    'Area': area_conversion,
    'Data Transfer Rate': data_transfer_rate_conversion,
    'Digital Storage': digital_storage_conversion,
    'Energy': energy_conversion,
    'Frequency': frequency_conversion,
    'Fuel Economy': fuel_economy_conversion,
    'Mass': mass_conversion,
    'Plane Angle': plane_angle_conversion,
    'Pressure': pressure_conversion,
    'Speed': speed_conversion,
    'Temperature': temperature_conversion,
    'Time': time_conversion,
    'Volume': volume_conversion
}

# Set page config
st.set_page_config(page_title="Advanced Unit Converter", layout="centered")

# Title and description
st.title("🔄 Unit Converter")
st.write("Convert between different units of measurement across multiple categories")

# Category selection
category = st.selectbox("Select Category", list(categories.keys()))

# Create columns for better layout
col1, col2 = st.columns(2)

# Input value
value = st.number_input("Enter Value", value=1.0)

# Unit selection
with col1:
    from_unit = st.selectbox("From", categories[category])
with col2:
    to_unit = st.selectbox("To", categories[category])

# Perform conversion
try:
    result = conversion_functions[category](value, from_unit, to_unit)
    # Display result
    st.markdown("### Result")
    st.write(f"{value} {from_unit} = {result:.6g} {to_unit}")
except Exception as e:
    st.error(f"Error in conversion: {str(e)}")

# Add some styling
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    .stSelectbox {
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Additional information
with st.expander("About"):
    st.write("""
    This advanced unit converter supports multiple categories:
    - Length
    - Area
    - Data Transfer Rate
    - Digital Storage
    - Energy
    - Frequency
    - Fuel Economy
    - Mass
    - Plane Angle
    - Pressure
    - Speed
    - Temperature
    - Time
    - Volume
    
    All conversions are based on standard conversion factors.
    """)