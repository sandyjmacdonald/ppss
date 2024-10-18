from lark import Lark, Transformer, exceptions
from dataclasses import dataclass
from typing import List

# ----------------------------
# Data Classes Definitions
# ----------------------------

class ProteinComponent:
    """
    Base class representing a component of a protein structure.
    """
    pass

@dataclass
class Subunit(ProteinComponent):
    """
    Represents a single subunit within a protein.

    Attributes:
        id (str): The identifier of the subunit (e.g., 'B1', 'B36').
    """
    id: str

@dataclass
class Concatenation(ProteinComponent):
    """
    Represents the concatenation of two protein components.

    Attributes:
        left (ProteinComponent): The left component in the concatenation.
        right (ProteinComponent): The right component in the concatenation.
    """
    left: ProteinComponent
    right: ProteinComponent

@dataclass
class Alternation(ProteinComponent):
    """
    Represents an alternation (choice) between multiple protein components.

    Attributes:
        options (List[ProteinComponent]): A list of possible components to choose from.
    """
    options: List[ProteinComponent]

@dataclass
class Multiplicity(ProteinComponent):
    """
    Represents a protein component that is repeated multiple times.

    Attributes:
        component (ProteinComponent): The component to be repeated.
        count (int): The number of times the component is repeated.
    """
    component: ProteinComponent
    count: int

@dataclass
class OptionalComponent(ProteinComponent):
    """
    Represents an optional protein component that can be included or excluded.

    Attributes:
        component (ProteinComponent): The optional component.
    """
    component: ProteinComponent

# ----------------------------
# Transformer Definition
# ----------------------------

class ProteinTransformer(Transformer):
    """
    Transforms the parse tree generated by Lark into a structured ProteinComponent hierarchy.
    """

    def subunit(self, items):
        """
        Transforms a subunit token into a Subunit instance.

        Args:
            items (List[str]): List containing the subunit ID.

        Returns:
            Subunit: An instance representing the subunit.
        """
        return Subunit(id=str(items[0]))

    def concatenation(self, items):
        """
        Transforms concatenated components into a Concatenation instance.

        Args:
            items (List[ProteinComponent]): List of components to concatenate.

        Returns:
            ProteinComponent: The concatenated protein component.
        """
        if len(items) == 1:
            return items[0]
        else:
            left = items[0]
            for right in items[1:]:
                left = Concatenation(left=left, right=right)
            return left

    def alternation(self, items):
        """
        Transforms alternated components into an Alternation instance.

        Args:
            items (List[ProteinComponent]): List of components to alternate between.

        Returns:
            Alternation: An instance representing the alternation.
        """
        return Alternation(options=items)

    def multiplicity(self, items):
        """
        Transforms a multiplicity expression into a Multiplicity instance.

        Args:
            items (List[ProteinComponent, str]): The component to repeat and the count as a string.

        Returns:
            Multiplicity: An instance representing the multiplicity.
        """
        component, count = items
        return Multiplicity(component=component, count=int(count))

    def optional(self, items):
        """
        Transforms an optional expression into an OptionalComponent instance.

        Args:
            items (List[ProteinComponent]): The optional component.

        Returns:
            OptionalComponent: An instance representing the optional component.
        """
        (component,) = items
        return OptionalComponent(component=component)

    def protein(self, items):
        """
        Transforms the root protein component.

        Args:
            items (List[ProteinComponent]): The top-level protein component.

        Returns:
            ProteinComponent: The root protein component.
        """
        return items[0]

    # Pass-through methods for other rules
    def expression(self, items):
        return items[0]

    def term_expr(self, items):
        return items[0]

    def factor(self, items):
        return items[0]

    def term(self, items):
        return items[0]

    def required_term(self, items):
        return items[0]

    def optional_term(self, items):
        return items[0]

# ----------------------------
# Grammar Definition
# ----------------------------

grammar = """
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

    SUBUNIT: "B" DIGIT+

    DIGIT: "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

    %import common.WS
    %ignore WS
"""

# ----------------------------
# ProteinParser Class Definition
# ----------------------------

class ProteinParser:
    """
    A class to parse protein definitions and generate possible protein structures.

    Attributes:
        parser (Lark): An instance of the Lark parser configured with the protein grammar.
    """

    def __init__(self):
        """
        Initializes the ProteinParser with the predefined grammar and transformer.
        """
        self.parser = Lark(grammar, parser='lalr', transformer=ProteinTransformer())

    def parse(self, protein_definition: str) -> List[str]:
        """
        Parses a protein definition string and returns all possible protein structures.

        Args:
            protein_definition (str): The protein definition string to parse.

        Returns:
            List[str]: A list of possible protein structures as strings.

        Raises:
            ValueError: If the protein definition is invalid or cannot be parsed.
        """
        try:
            # Parse the expression using Lark
            parsed_component = self.parser.parse(protein_definition)
            
            # Expand all possible structures
            expanded = self.expand_protein(parsed_component)
            
            # Convert to string representations
            structures = self.structures_to_strings(expanded)
            
            return structures
        except exceptions.LarkError as e:
            raise ValueError(f"Failed to parse protein definition: {e}")
        except ValueError as ve:
            raise ValueError(f"Error during expansion: {ve}")

    @staticmethod
    def expand_protein(component: ProteinComponent) -> List[List[str]]:
        """
        Recursively expands a ProteinComponent into all possible structures based on its type.

        Args:
            component (ProteinComponent): The protein component to expand.

        Returns:
            List[List[str]]: A list of possible protein structures, each represented as a list of subunit IDs.

        Raises:
            ValueError: If an unknown ProteinComponent type is encountered.
        """
        if isinstance(component, Subunit):
            return [[component.id]]
        elif isinstance(component, Concatenation):
            left_expansions = ProteinParser.expand_protein(component.left)
            right_expansions = ProteinParser.expand_protein(component.right)
            # Concatenate each left expansion with each right expansion
            return [left + right for left in left_expansions for right in right_expansions]
        elif isinstance(component, Alternation):
            expansions = []
            for option in component.options:
                expansions.extend(ProteinParser.expand_protein(option))
            return expansions
        elif isinstance(component, Multiplicity):
            base_expansions = ProteinParser.expand_protein(component.component)
            expanded = []
            for expansion in base_expansions:
                # Repeat the expansion 'count' times
                repeated = []
                for _ in range(component.count):
                    repeated += expansion
                expanded.append(repeated)
            return expanded
        elif isinstance(component, OptionalComponent):
            # Two possibilities: include or exclude the optional component
            included = ProteinParser.expand_protein(component.component)
            excluded = [[]]
            return included + excluded
        else:
            raise ValueError(f"Unknown ProteinComponent type: {type(component)}")

    @staticmethod
    def structures_to_strings(structures: List[List[str]]) -> List[str]:
        """
        Converts a list of protein structures from list of subunits to string representations.

        Args:
            structures (List[List[str]]): A list of protein structures, each as a list of subunit IDs.

        Returns:
            List[str]: A list of protein structures represented as strings with subunits concatenated by '+'.
        """
        return [" + ".join(structure) for structure in structures]

# ----------------------------
# Parsing Function to Expose to Users
# ----------------------------

def parse_protein(protein_definition: str) -> List[str]:
    """
    Parses a protein definition string and returns all possible protein structures.

    Args:
        protein_definition (str): The protein definition string to parse.

    Returns:
        List[str]: A list of possible protein structures as strings.

    Raises:
        ValueError: If the protein definition is invalid or cannot be parsed.
    """
    parser = ProteinParser()
    return parser.parse(protein_definition)