import re
from typing import List, Tuple
from proof_helper.core.proof import Proof, Statement, Subproof, StepID, Step
from proof_helper.core.formula import Formula
from proof_helper.io.deserialize import parse_formula

def parse_named_proof(text: str) -> Tuple[str, Proof]:
    # Get the first line of the proof
    title_line, proof = text.split("\n", 1)

    # Remove any comments from the title line
    title_line = title_line.split(";", 1)[0]

    return title_line.strip(), parse_proof(proof.strip())

def parse_proof(text: str) -> Proof:
    # Separate the lines of the proof and remove comments
    lines = [line.split(";", 1)[0].rstrip() for line in text.strip().splitlines()]

    # Remove any empty lines
    lines = [line for line in lines if lines]

    # Create holding structure for organized lines
    structure = []
    current_block = []
    current_indent = 1

    for line in lines:
        # Split the line into <indentation> <step>: <formula> '<rule>' [<support>]
        #                  or <indentation>-
        #                  or <indentation>>

        # Look for a step number to find indentation
        match = re.search(r'\d', line)
        if match:
            indent, rest = line[:match.start()].strip(), line[match.start():]
        else:
            indent, rest = line.strip(), ""
        
        # Count '|' appearances to find current indentation
        indent_level = indent.count("|")
        if indent_level == current_indent:
            structure.append(rest)


        


