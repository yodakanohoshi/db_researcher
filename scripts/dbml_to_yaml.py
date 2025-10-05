#!/usr/bin/env python3
"""
Refactored dbml -> yml extractor.

- Safer attribute access (handles missing notes/defaults/indexes).
- Clearer naming and structure.
- Type hints and minimal validation.
- Uses yaml.safe_dump for output.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import yaml
from pydbml import PyDBML

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dbml2yml")


def safe_text(obj: Any) -> Optional[str]:
    """Return obj.text if present, otherwise None."""
    return getattr(obj, "text", None) if obj is not None else None


def format_fk_refs(refs: Iterable) -> str:
    """
    Convert a DBML reference structure into a newline separated string of "table.column".
    This function is defensive about the shape of `refs` (some pydbml versions nest refs).
    """
    if not refs:
        return ""
    lines: List[str] = []
    for group in refs:
        # group may be an iterable of refs or an object with attribute 'col1'
        candidates = getattr(group, "col1", group)
        try:
            iterator = iter(candidates)
        except TypeError:
            # not iterable, skip
            continue
        for ref in iterator:
            table_name = getattr(getattr(ref, "table", None), "name", None) or getattr(ref, "table_name", None)
            col_name = getattr(ref, "name", None) or getattr(ref, "column", None)
            if table_name and col_name:
                lines.append(f"{table_name}.{col_name}")
    return "\n".join(lines)


def key_to_dict(column: Any) -> Dict[str, Any]:
    """Serialize a column/key object to a plain dict with safe accessors."""
    return {
        "name": getattr(column, "name", None),
        "type": getattr(column, "type", None),
        "pk": bool(getattr(column, "pk", False)),
        "fk": format_fk_refs(getattr(column, "get_refs", lambda: [])()),
        "unique": bool(getattr(column, "unique", False)),
        "not_null": bool(getattr(column, "not_null", False)),
        "default": safe_text(getattr(column, "default", None)),
        "note": safe_text(getattr(column, "note", None)),
    }


def indexes_to_list(indexes: Iterable) -> List[str]:
    """Serialize index objects to "index_name: col1,col2" strings."""
    result: List[str] = []
    for idx in indexes or []:
        name = getattr(idx, "name", None) or ""
        subjects = getattr(idx, "subject_names", []) or []
        cols = ",".join(subjects)
        result.append(f"{name}: {cols}" if name else cols)
    return result


def parse_dbml_text(dbml_text: str) -> List[Dict[str, Any]]:
    """Parse DBML text with pydbml and return a data structure ready to dump to YAML."""
    db = PyDBML(dbml_text)
    tables_serialized: List[Dict[str, Any]] = []

    for table in getattr(db, "tables", []) or []:
        table_name = getattr(table, "name", None)
        table_note = safe_text(getattr(table, "note", None))
        columns = [key_to_dict(col) for col in getattr(table, "columns", []) or []]
        indexes = indexes_to_list(getattr(table, "indexes", []) or [])

        tables_serialized.append(
            {
                "table_name": table_name,
                "table_description": table_note,
                "indexes": indexes,
                "keys": columns,
            }
        )

    return tables_serialized


def read_text_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        logger.error("Input file does not exist: %s", path)
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def write_text_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert DBML to YAML table description.")
    parser.add_argument("-i", "--input-file", type=str, default="data/shema.dbml", help="Path to input DBML")
    parser.add_argument("-o", "--output-file", type=str, default="data.yml", help="Path to output YAML")
    return parser.parse_args()


def main() -> int:
    args = get_args()
    in_path = Path(args.input_file)
    out_path = Path(args.output_file)

    try:
        dbml_text = read_text_file(in_path)
    except FileNotFoundError:
        logger.exception("Failed to read input file.")
        return 2

    try:
        structured = parse_dbml_text(dbml_text)
    except Exception:
        logger.exception("Failed to parse DBML content.")
        return 3

    yaml_text = yaml.safe_dump(structured, allow_unicode=True, sort_keys=False)
    try:
        write_text_file(out_path, yaml_text)
    except Exception:
        logger.exception("Failed to write output file.")
        return 4

    logger.info("Wrote %d tables to %s", len(structured), out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())