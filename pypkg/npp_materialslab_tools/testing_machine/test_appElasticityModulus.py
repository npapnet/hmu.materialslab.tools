import pytest
from .app_ElasticModGUI_v1 import TensileSpecimenDimensions

def test_one():
    pass

def test_SpecimenDimensions():
    sd = TensileSpecimenDimensions(width_mm=10, thickness_mm=3, gauge_length_mm=100)
    assert sd.width_mm ==10
    assert sd.thickness_mm==3
    assert sd.gauge_length_mm==100
    assert sd.csArea_mm2==30