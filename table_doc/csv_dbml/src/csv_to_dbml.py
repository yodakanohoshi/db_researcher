#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
import pandas as pd
from jinja2 import Environment, FileSystemLoader, StrictUndefined

def excel_to_dbml(xlsx_path: Path, tmpl_dir: Path, tmpl_name: str, out_path: Path):
    loader=FileSystemLoader(str(tmpl_dir))
    undefined=StrictUndefined
    env = Environment(
        loader=loader,
        undefined=undefined,
        trim_blocks=True, lstrip_blocks=True,
    )
    tmpl = env.get_template(tmpl_name)

    xl = pd.ExcelFile(xlsx_path)
    
    """
    [
        {table_name: "table_name",
            table_note: "",
            columns: [
                {name: "col1", type: "int", other: "[pk, null, unique, note: 'note']",
                {name: "col2", type: "varchar(255)", "[null, unique]"},
            ]
        },
        ...
    ] 
    という辞書を作ることから始める(pkは後から手入力する、teble_note:も手入力する)
    """
    
    # シート一覧を取得
    sheets = xl.sheet_names
    # シートごとに処理
    tables = []
    for sheet in sheets:
        df = xl.parse(sheet)
        table_name = sheet
        
        columns = []
        for _, row in df.iterrows():
            col = {
                "name": row["name"],
                "type": row["type"],
            }
            other_attrs = []

            if row["null"] == "yes":
                other_attrs.append("null")
            elif row["null"] == "no":
                other_attrs.append("not null")
            
            if row["unique"] == "yes":
                other_attrs.append("unique")
            
            if pd.notna(row.get("note")) and row["note"]:
                other_attrs.append(f"note: '{row["note"]}'")
            
            other_attrs_str = ", ".join(other_attrs)
            
            col["other"] = f"[{other_attrs_str}]" if other_attrs_str else None
            
            columns.append(col)
        
        tables.append({
            "table_name": table_name,
            "columns": columns,
        })
        
    dbml = tmpl.render(tables=tables)
    out_path.write_text(dbml, encoding="utf-8")
    return out_path

def main():
    parser = argparse.ArgumentParser(description="Convert Excel schema to DBML format.")
    parser.add_argument("--xlsx", type=Path, help="Path to the input Excel file.")
    parser.add_argument("--template-dir", type=Path, default=Path("./data"), help="Directory containing Jinja2 templates.")
    parser.add_argument("--template-name", type=str, default="template.jinja", help="Name of the Jinja2 template file.")
    parser.add_argument("--output", type=Path, default=Path("./output.dbml"), help="Path to the output DBML file.")
    
    args = parser.parse_args()
    
    out_path = excel_to_dbml(args.xlsx, args.template_dir, args.template_name, args.output)
    print(f"DBML file generated at: {out_path}")

if __name__ == "__main__":
    main()
