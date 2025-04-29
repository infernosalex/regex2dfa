# Regex to DFA Converter

A Python implementation of Thompson's construction algorithm to convert regular expressions to deterministic finite automata (DFA).

## Overview

This project implements a complete pipeline for converting regular expressions to deterministic finite automata:

1. Regular expression parsing
2. Conversion to postfix notation (using Shunting Yard algorithm)
3. NFA construction (using Thompson's algorithm)
4. DFA conversion (using subset construction)
5. DFA simulation

## Features

- Supports basic regex operations: concatenation, alternation (`|`), Kleene star (`*`), plus (`+`), and optional (`?`)
- Handles character escaping with backslash
- Supports direct testing of regex patterns against input strings
- Includes a test framework for validating regex pattern matching

## Components

- `regex_to_postfix.py`: Converts infix regex notation to postfix (Polish) notation
- `nfa_builder.py`: Implements Thompson's construction algorithm to build NFAs
- `nfa_to_dfa.py`: Converts NFAs to DFAs using subset construction
- `main.py`: CLI interface for testing regex patterns

## Usage

Run the main script with a test file:

```bash
python main.py [test_file.json]
```

If no test file is provided, it will use the default test file.

### Test File Format

The test file should be a JSON array of objects with the following structure:

```json
[
  {
    "name": "Test Case 1",
    "regex": "a(b|c)*",
    "test_strings": [
      {"input": "abcbc", "expected": true},
      {"input": "ad", "expected": false}
    ]
  }
]
```

## Implementation Details

### Regex to Postfix

The infix regex is first converted to postfix notation using the Shunting Yard algorithm, with explicit concatenation symbols added. Operator precedence is:
* `*, +, ?` (highest)
* `.` (concatenation)
* `|` (alternation) (lowest)

### Thompson's Construction

The postfix regex is converted to an NFA using Thompson's construction algorithm. Each regex operator is handled by specific NFA constructions with ε-transitions used to combine sub-NFAs.

### Subset Construction

The NFA is converted to a DFA using the subset construction algorithm. This involves computing ε-closures and creating DFA states that represent sets of NFA states.



