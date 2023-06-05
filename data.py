import csv
import pydantic
import decimal
import tempfile
import subprocess
import shutil
import os
import solid2
from typing import Optional


class LayoutConfig(pydantic.BaseModel):
    ru: decimal.Decimal
    rl: decimal.Decimal
    ht: decimal.Decimal
    gap: decimal.Decimal


class TagConfig(LayoutConfig):
    label: str


class BottleType(LayoutConfig):
    type_name: str


_openscad_binary = None


def get_openscad_binary() -> Optional[str]:
    global _openscad_binary
    if (
        _openscad_binary is not None
        and subprocess.call(["which", _openscad_binary]) == 0
    ):
        return _openscad_binary
    possible_cmds = [
        "openscad",
        "OpenSCAD",
        "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD",
    ]
    for cmd in possible_cmds:
        result = subprocess.call(["which", cmd])
        if result == 0:
            _openscad_binary = cmd
            return cmd


decimal_fields = ["ru", "rl", "ht", "gap"]


def load_bottle_types():
    bottle_types = {}
    with open("bottle-types.csv") as f:
        for row in csv.DictReader(f, delimiter=";"):
            print(row)
            for k in decimal_fields:
                row[k] = decimal.Decimal(row[k])
            bt = BottleType.parse_obj(row)
            bottle_types[bt.type_name] = bt
    return bottle_types


def generate_stl(config: TagConfig):
    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copytree("scad-files/", os.path.join(tmpdir, "scad-files"))
        scad_file = solid2.import_scad(
            os.path.join(tmpdir, "scad-files", "bottle-clip.scad")
        )
        clip = scad_file.bottle_clip(
            config.ru,
            config.rl,
            config.ht,
            2.5,
            config.label,
            logo="thing-logos/jh_alpaka.dxf",
        )
        scad_path = os.path.join(tmpdir, "tmp.scad")
        solid2.scad_render_to_file(clip, scad_path)
        out_stl = os.path.join(tmpdir, "out.stl")
        subprocess.call([get_openscad_binary(), "-o", out_stl, scad_path])
        with open(out_stl) as f:
            return f.read()
