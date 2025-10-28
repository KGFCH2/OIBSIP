import pytest

from backend.bmi import calculate_bmi, categorize_bmi


def test_bmi_normal():
    assert calculate_bmi(70, 1.75) == 22.86
    cat, color = categorize_bmi(22.86)
    assert cat == "Normal"


def test_bmi_underweight():
    val = calculate_bmi(50, 1.8)
    assert val < 18.5
    cat, _ = categorize_bmi(val)
    assert cat == "Underweight"


def test_invalid_inputs():
    with pytest.raises(ValueError):
        calculate_bmi(0, 1.7)
    with pytest.raises(ValueError):
        calculate_bmi(60, 0)
