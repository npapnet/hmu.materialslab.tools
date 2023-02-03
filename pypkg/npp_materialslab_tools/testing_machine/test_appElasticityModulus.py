import pytest
from .appElasticityCalculator import SpecimenDimensions

def test_one():
    pass

def test_SpecimenDimensions():
    sd = SpecimenDimensions(width_mm=10, thickness_mm=3, gauge_length_mm=100)
    assert sd.width_mm ==10
    assert sd.thickness_mm==3
    assert sd.gauge_length_mm==100
    assert sd.csArea_mm2==30