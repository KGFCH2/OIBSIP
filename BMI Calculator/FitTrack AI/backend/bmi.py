"""
BMI logic helpers

Contains calculate_bmi and categorize_bmi functions which are easy to test.
"""
from typing import Tuple


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI and return rounded value to 2 decimals.

    Raises ValueError for invalid inputs (<= 0 or non-numeric handled by caller).
    """
    if height_m <= 0 or weight_kg <= 0:
        raise ValueError("Weight and height must be positive numbers")
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def categorize_bmi(bmi: float) -> Tuple[str, str]:
    """Return (category_name, color_hex) for a BMI value.

    Colors are chosen to match the UI spec.
    """
    if bmi < 18.5:
        return "Underweight", "#FF8C00"  # Orange
    if 18.5 <= bmi <= 24.9:
        return "Normal", "#2ECC71"  # Green
    if 25 <= bmi <= 29.9:
        return "Overweight", "#3498DB"  # Blue
    return "Obese", "#E74C3C"  # Red
