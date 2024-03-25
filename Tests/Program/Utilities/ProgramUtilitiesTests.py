from dataclasses import dataclass, field
from typing import Optional

import pytest

from Programs.Utilities.ProgramUtilities import dataclass_to_json_schema, get_all_program_classes


@dataclass
class TestInputs:
    int_field: int
    float_field: float
    bool_field: bool = False
    optional_field: str ="default value"

def test_dataclass_to_json_schema():
    schema = dataclass_to_json_schema(TestInputs)
    expected_schema = {
        'type': 'object',
        'properties': {
            'int_field': {'type': 'integer'},
            'float_field': {'type': 'number'},
            'bool_field': {'type': 'boolean'},
            'optional_field': {'type': 'string'}
        },
        'required': ['int_field', 'float_field']
    }
    assert schema == expected_schema, "Schema does not match expected output."
class MockProgram:
    pass

class SubProgram1(MockProgram):
    pass

class SubProgram2(MockProgram):
    pass

class SubSubProgram1(SubProgram1):
    pass

def test_get_all_program_classes():
    all_classes = get_all_program_classes(MockProgram)
    expected_classes = [SubProgram1, SubProgram2, SubSubProgram1]
    assert all(cls in all_classes for cls in expected_classes), "Not all subclasses were found."
    assert len(all_classes) == len(expected_classes), "Unexpected subclasses found."
