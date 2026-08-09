from src.data.labels import derive_label

def test_background():
    assert derive_label(0.1,0.2,0.3) == "background_dominant"

def test_enhancement_dominant():
    assert derive_label(10.0,2.0,4.0) == "enhancement_dominant"

def test_oedema():
    assert derive_label(1.0,2.0,8.0) == "oedema"
