import unittest
from dataclasses import dataclass, field
from typing import Optional

from Programs.Utilities.ProgramUtilities import dataclass_to_json_schema, get_all_program_classes


class TestProgramUtilities(unittest.TestCase):
    @dataclass
    class TestInputs:
        int_field: int
        float_field: float
        bool_field: bool = False
        optional_field: str = "default value"

    def test_dataclass_to_json_schema(self):
        schema = dataclass_to_json_schema(TestProgramUtilities.TestInputs)
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
        self.assertTrue(schema == expected_schema, "Schema does not match expected output.")

    def test_get_all_subclasses(self):
        all_classes = get_all_program_classes(MockProgram)
        expected_classes = [SubProgram1, SubProgram2, SubSubProgram1]
        self.assertTrue(all(cls in all_classes for cls in expected_classes), "Not all subclasses were found.")
        self.assertTrue(len(all_classes) == len(expected_classes), "Unexpected subclasses found.")

    def test_get_all_program_classes(self):
        all_classes = get_all_program_classes()

        from Programs.ManualControlProgram import ManualControlProgram
        from Programs.PanProgram import PanProgram
        from Programs.StarTrackProgram import StarTrackProgram

        expected_classes = [ManualControlProgram, PanProgram, StarTrackProgram]
        self.assertTrue(all(cls in all_classes for cls in expected_classes), "Not all subclasses were found.")
        self.assertTrue(len(all_classes) == len(expected_classes), "Unexpected subclasses found.")


class MockProgram:
    pass


class SubProgram1(MockProgram):
    pass


class SubProgram2(MockProgram):
    pass


class SubSubProgram1(SubProgram1):
    pass
