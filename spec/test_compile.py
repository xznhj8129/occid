"""
Usage:
    python3 occid/spec/test_compile.py
    python3 occid/spec/test_compile.py --out-typology occid/spec/test_typology.yaml --out-ontology occid/spec/test_ontology.md
"""

from argparse import ArgumentParser
from pathlib import Path

import yaml


HERE = Path(__file__).resolve().parent
DEFAULT_ONTOLOGY = HERE / "ontology.yaml"
DEFAULT_AXIS = HERE / "axis.yaml"
DEFAULT_OUT_TYPOLOGY = HERE / "test_typology.yaml"
DEFAULT_OUT_ONTOLOGY = HERE / "test_ontology.md"


def load_yaml(path: Path):
    with path.open() as handle:
        return yaml.safe_load(handle)


class Dumper(yaml.SafeDumper):
    pass


def add_spacing(text: str):
    lines = text.splitlines()
    spaced = []
    children_indents = []

    def in_children_entry(indent: int):
        return bool(children_indents) and indent == children_indents[-1] + 2

    for line in lines:
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))
        is_entry = ":" in stripped and not stripped.startswith("- ")

        while children_indents and stripped and indent <= children_indents[-1]:
            children_indents.pop()

        if stripped == "children:":
            spaced.append(line)
            children_indents.append(indent)
            continue

        if spaced and is_entry and in_children_entry(indent):
            spaced.append("")

        spaced.append(line)

    return "\n".join(spaced) + "\n"


def type_name(axis_value: str, base_name: str):
    parts = []
    token = []
    for char in axis_value:
        if char.isalnum():
            token.append(char)
            continue
        if token:
            parts.append("".join(token))
            token = []
    if token:
        parts.append("".join(token))
    return "".join(part[:1].upper() + part[1:] for part in parts) + base_name


def expand_axis_names(base_name: str, axis_names: tuple[str, ...], axes: dict):
    names = [base_name]
    for axis_name in reversed(axis_names):
        next_names = []
        for name in names:
            for axis_value in axes[axis_name]:
                next_names.append(type_name(axis_value, name))
        names = next_names
    return names


def expand_typology_node(node_name: str, node_data: dict, axes: dict, inherited_axes: tuple[str, ...] = ()):
    compiled = {}
    axis_name = node_data.get("axis")
    current_axes = inherited_axes + ((axis_name,) if axis_name else ())
    children = node_data.get("children")

    if not children:
        if current_axes:
            compiled["children"] = {}
            for child_name in expand_axis_names(node_name, current_axes, axes):
                compiled["children"][child_name] = {}
        return compiled

    compiled_children = {}
    for child_name, child_data in children.items():
        compiled_children[child_name] = expand_typology_node(child_name, child_data, axes, current_axes)

    if compiled_children:
        compiled["children"] = compiled_children
    return compiled


def render_markdown_children(children: dict, indent: int, spaced: bool):
    lines = []

    for index, (name, node_data) in enumerate(children.items()):
        if spaced and index:
            lines.append("")
        lines.extend(render_markdown_node(name, node_data, indent))

    return lines


def render_markdown_node(name: str, node_data: dict, indent: int):
    description = node_data["description"] or ""
    children = node_data.get("children")
    axis_name = node_data.get("axis")
    pad = " " * indent
    lines = [f"{pad}- **{name}**: {description}"]

    if axis_name:
        return lines

    if children:
        child_names = list(children)
        spaced = name != "Definition" and any(children[child].get("children") for child in child_names)
        lines.extend(render_markdown_children(children, indent + 4, spaced))

    return lines


def write_typology(path: Path, ontology: dict, axes: dict):
    class_node = ontology["Class"]
    rendered = {"Class": expand_typology_node("Class", class_node, axes)}
    text = yaml.dump({"types": rendered}, Dumper=Dumper, sort_keys=False, width=1000)
    body = add_spacing(text)
    path.write_text(
        "\n".join(
            [
                "includes:",
                "- ontology.yaml",
                "- axis.yaml",
                "",
                "# Only one discriminator key? ",
                "# ie: Vehicle * PhysicalDomain = LandVehicle, AirVehicle, etc",
                "# Multiple discriminator keys?",
                "# ie: Polygon * LLA = GeoArea",
                "",
                body.rstrip("\n"),
                "",
            ]
        )
    )


def write_ontology(path: Path, ontology: dict):
    class_node = ontology["Class"]
    children = class_node["children"]
    lines = ["", "### Classes", ""]
    spaced = any(node.get("children") for node in children.values())
    lines.extend(render_markdown_children(children, 0, spaced))
    path.write_text("\n".join(lines) + "\n")


parser = ArgumentParser()
parser.add_argument("--ontology", type=Path, default=DEFAULT_ONTOLOGY)
parser.add_argument("--axis", type=Path, default=DEFAULT_AXIS)
parser.add_argument("--out-typology", type=Path, default=DEFAULT_OUT_TYPOLOGY)
parser.add_argument("--out-ontology", type=Path, default=DEFAULT_OUT_ONTOLOGY)
args = parser.parse_args()

ontology = load_yaml(args.ontology)
axes = load_yaml(args.axis)

write_typology(args.out_typology, ontology, axes)
write_ontology(args.out_ontology, ontology)

print(f"wrote={args.out_typology}")
print(f"wrote={args.out_ontology}")
