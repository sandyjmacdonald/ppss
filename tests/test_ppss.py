import pytest
from protein_parser import ProteinParser, parse_protein

def test_simple_concatenation():
    protein_definition = "B1 + B1"
    expected = ["B1 + B1"]
    assert parse_protein(protein_definition) == expected

def test_complex_prefix_concatenation():
    protein_definition = "AA23 + XYZ789"
    expected = ["AA23 + XYZ789"]
    assert parse_protein(protein_definition) == expected

def test_alternation():
    protein_definition = "(B1 + C2) | (AA23 + XYZ789)"
    expected = ["B1 + C2", "AA23 + XYZ789"]
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

def test_multiple_complex_prefixes():
    protein_definition = "AA23 + (XYZ789 | BB12) + [CC34]"
    expected = [
        "AA23 + XYZ789 + CC34",
        "AA23 + XYZ789",
        "AA23 + BB12 + CC34",
        "AA23 + BB12"
    ]
    assert parse_protein(protein_definition) == expected

def test_multiplicity_with_complex_prefix():
    protein_definition = "AA + BB{2} + CC"
    expected = ["AA + BB + BB + CC"]
    assert parse_protein(protein_definition) == expected

def test_mixed_case_subunits():
    protein_definition = "aA1 + Bb2 + cC3"
    expected = ["aA1 + Bb2 + cC3"]
    assert parse_protein(protein_definition) == expected

def test_subunits_with_digits_only():
    protein_definition = "123 + 456"
    expected = ["123 + 456"]
    assert parse_protein(protein_definition) == expected

def test_subunits_with_letters_only():
    protein_definition = "ABC + xyz"
    expected = ["ABC + xyz"]
    assert parse_protein(protein_definition) == expected

def test_subunits_with_alphanumerics():
    protein_definition = "A1B2 + c3D4"
    expected = ["A1B2 + c3D4"]
    assert parse_protein(protein_definition) == expected

def test_subunits_with_no_separator():
    protein_definition = "A1B2c3D4"
    expected = ["A1B2c3D4"]
    assert parse_protein(protein_definition) == expected

def test_subunits_with_invalid_characters():
    protein_definition = "A1B2 + C#3"
    with pytest.raises(ValueError):
        parse_protein(protein_definition)