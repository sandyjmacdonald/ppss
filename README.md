PPSS - Python Protein Subunit Syntax

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

```
from ppss import ProteinParser

# Instantiate the parser
parser = ProteinParser()

# Define a protein structure
protein_definition = "(B1 + B2) | B3"

# Parse the protein structure
structures = parser.parse(protein_definition)

# Display the structures
for structure in structures:
    print(structure)
```
