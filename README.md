# PPSS - Python Protein Subunit Syntax

A simple Python package for defining protein subunit structures.

## Installation

The simplest way to install this is to do as follows:

```
pip install ppss
```

You can also install the Poetry packaging and dependency tool and then clone this repository and install with poetry, as follows:

```
pipx install poetry
git clone https://github.com/sandyjmacdonald/ppss
cd ppss
poetry install
```

## Usage

The simple example below defines a protein comprised of either an S1 *plus* S1 subunit, or just an S3 subunit. The bar (|) symbol here represents an OR condition or "alternation", while the + represents an AND condition or "concatenation". Subunit IDs can be any combination of upper and/or lowercase alphabetical and numerical characters.

```
from ppss import ProteinParser

# Instantiate the parser
parser = ProteinParser()

# Define a protein structure
protein_definition = "(S1 + S2) | S3"

# Parse the protein structure
structures = parser.parse(protein_definition)

# Display the structures
for structure in structures:
    print(structure)
```

The two possible structures are printed:

```
S1 + S2
S3
```

The full grammar of the Lark parser is as follows:

```
?start: protein

protein: alternation

alternation: concatenation ("|" concatenation)*

concatenation: required_term ("+" term)*

?term: required_term
        | optional_term

required_term: multiplicity
                | subunit
                | "(" alternation ")"

optional_term: optional

multiplicity: subunit "{" DIGIT+ "}"
            | "(" alternation ")" "{" DIGIT+ "}"

optional: "[" alternation "]"

subunit: SUBUNIT

SUBUNIT: /[A-Za-z0-9]+/

DIGIT: "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

%import common.WS
%ignore WS
```