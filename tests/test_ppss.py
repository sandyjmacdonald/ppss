import pytest
from ppss import ProteinParser, parse_protein

def test_simple_concatenation():
    protein_definition = "B1 + B1"
    expected = ["B1 + B1"]
    assert parse_protein(protein_definition) == expected

def test_alternation():
    protein_definition = "(B1 + B2) | (B3 + B4)"
    expected = ["B1 + B2", "B3 + B4"]
    assert parse_protein(protein_definition) == expected

def test_multiplicity():
    protein_definition = "B2{3}"
    expected = ["B2 + B2 + B2"]
    assert parse_protein(protein_definition) == expected

def test_optional_component():
    protein_definition = "B1 + [B2] + B3"
    expected = ["B1 + B2 + B3", "B1 + B3"]
    assert parse_protein(protein_definition) == expected

def test_optional_component_with_complex_structure():
    protein_definition = "B1 + [B2 + B3] + B4"
    expected = ["B1 + B2 + B3 + B4", "B1 + B4"]
    assert parse_protein(protein_definition) == expected

def test_nested_alternation():
    protein_definition = "(B1 | B2){2} + [B3]"
    expected = [
        "B1 + B1 + B3",
        "B1 + B1",
        "B1 + B2 + B3",
        "B1 + B2",
        "B2 + B1 + B3",
        "B2 + B1",
        "B2 + B2 + B3",
        "B2 + B2"
    ]
    assert parse_protein(protein_definition) == expected

def test_invalid_input():
    protein_definition = "[B3]"
    with pytest.raises(ValueError):
        parse_protein(protein_definition)

def test_class_usage():
    parser = ProteinParser()
    protein_definition = "B1 + (B2 | B3) + B4"
    expected = ["B1 + B2 + B4", "B1 + B3 + B4"]
    assert parser.parse(protein_definition) == expected

def test_multiple_optional_components():
    protein_definition = "B1 + [B2] + [B3] + B4"
    expected = [
        "B1 + B2 + B3 + B4",
        "B1 + B2 + B4",
        "B1 + B3 + B4",
        "B1 + B4"
    ]
    assert parse_protein(protein_definition) == expected