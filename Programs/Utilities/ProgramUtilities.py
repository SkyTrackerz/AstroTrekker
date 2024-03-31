import importlib
import pkgutil
import re
from dataclasses import fields, MISSING
import typing

from Programs.Program import Program

def dataclass_to_json_schema(dataclass):

    properties = {}
    required = []

    for field in fields(dataclass):
        # Determine the JSON schema type based on the field's type
        field_type = field.type

        # Add additional type mappings as necessary

        # Check if the field is optional (either by Optional[type] or by having a default value)
        is_optional = False
        if typing.get_origin(field_type) is typing.Optional:
            is_optional = True
            # Unwrap Optional[type] to get the actual type
            field_type = typing.get_args(field_type)[0]
        if field.default is not MISSING or field.default_factory is not MISSING:
            is_optional = True

        json_type = 'string'  # Default type

        if field_type == int:
            json_type = 'integer'
        elif field_type == float:
            json_type = 'number'
        elif field_type == bool:
            json_type = 'boolean'

        # Construct the property schema
        field_schema = {'type': json_type}

        # Update the properties dictionary
        properties[field.name] = field_schema

        # If the field is not optional, add it to the required list
        if not is_optional:
            required.append(field.name)
    """   properties['button'] = {
        "propertyOrder": 1,
        "format": "button",
        "options": {
            "button": {
                "text": "Search",
                "icon": "search",
                "action": "myAction",
            }
        }
    }"""
    derived_name = camel_case_to_spaced(dataclass.__name__)
    # Construct and return the JSON schema
    schema = {
        'type': 'object',
        'properties': {
            # Extra nesting is required so the name is returned by JSON-Editor
            dataclass.__name__: {
                'title': derived_name,
                'type': 'object',
                'properties': properties,
            }
        },
        #'required': required
    }
    print(schema)

    return schema
def get_all_program_classes(class_to_check=None):
    _import_subclasses("Programs")
    """Recursively get all subclasses of Program."""
    all_subclasses = []
    if class_to_check is None:
        class_to_check = Program
    for subclass in class_to_check.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_program_classes(subclass))

    return all_subclasses

def camel_case_to_spaced(camel_case_string):
    # Step 1: Add space before uppercase letters to separate words
    spaced_string = re.sub(r"([A-Z])", r" \1", camel_case_string)

    # Step 2: Strip leading space if it exists
    spaced_string = spaced_string.strip()

    # Step 3: Check and remove "Input" at the end
    if spaced_string.endswith("Input"):
        spaced_string = spaced_string[:-5].strip()

    return spaced_string

def _import_subclasses(package, recursive=True):
    """Import all submodules of a module, recursively, including subpackages"""
    if isinstance(package, str):
        package = importlib.import_module(package)
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        importlib.import_module(full_name)
        if recursive and is_pkg:
            _import_subclasses(full_name)