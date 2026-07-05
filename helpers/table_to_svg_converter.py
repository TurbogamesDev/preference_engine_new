from datetime import datetime
from zoneinfo import ZoneInfo

svg_format_path = "svg_templates/main_svg_template.txt"

svg_rows_non_end_path = "svg_templates/row_non_end_svg_template.txt"

svg_rows_end_path = "svg_templates/row_end_svg_template.txt"

with open(svg_format_path, "r") as file:
    svg_format = file.read()

with open(svg_rows_non_end_path, "r") as file:
    svg_rows_non_end_format = file.read()

with open(svg_rows_end_path, "r") as file:
    svg_rows_end_format = file.read()

def convert_table_to_svg(input_table) -> str:
    return_svg = svg_format

    rows_svg = ""

    for i, row in enumerate(input_table, 0):
        if i == 5:
            break

        if i == len(input_table) - 1:
            rows_svg += svg_rows_end_format.format(
                Y_OFFSET = i * 65,
                FIELD_1 = row[0],
                FIELD_2 = row[1] if len(row[1]) <= 40 else row[1][:37] + "...",
                FIELD_3 = row[2],
            )
        else:
            rows_svg += svg_rows_non_end_format.format(
                Y_OFFSET = i * 65,
                FIELD_1 = row[0],
                FIELD_2 = row[1] if len(row[1]) <= 40 else row[1][:37] + "...",
                FIELD_3 = row[2],
            )

    return return_svg.format(ROWS = rows_svg, TIMESTAMP = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%H:%M %d/%m/%y"))
