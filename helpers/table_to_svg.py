# from utils.entry import Entry
from datetime import datetime
from zoneinfo import ZoneInfo

svg_format = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 448" preserveAspectRatio="xMidYMid meet" style="width: 100%; height: auto; max-width: 720px;">
  <defs>
    <linearGradient id="boxGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b1622" />
      <stop offset="100%" stop-color="#112233" />
    </linearGradient>

    <clipPath id="titleClip">
      <rect x="90" y="0" width="510" height="100%" />
    </clipPath>
  </defs>

  <style>
    .bg {{ fill: url(#boxGrad); rx: 20px; }}
    .header {{ font-family: 'Overpass', 'Inter', system-ui, sans-serif; font-weight: 800; font-size: 28px; fill: #edf1f5; }}
    .rank {{ font-family: 'Overpass', 'Inter', system-ui, sans-serif; font-weight: 700; font-size: 22px; fill: #e5933a; }}
    .title {{ font-family: 'Overpass', 'Inter', system-ui, sans-serif; font-weight: 600; font-size: 22px; fill: #9fadbd; }}
    .score {{ font-family: 'Overpass', 'Inter', system-ui, sans-serif; font-weight: 700; font-size: 22px; fill: #3db4f2; }}
    .line {{ stroke: #152232; stroke-width: 2; stroke-linecap: round; }}
  </style>

  <rect class="bg" width="720" height="448" />

  <text x="35" y="65" class="header">Anime Preference Predictor {TIMESTAMP}</text>
  <line x1="35" y1="85" x2="685" y2="85" class="line" />

  {ROWS}
</svg>
"""

svg_rows_format_not_end = """
  <g transform="translate(0, {Y_OFFSET})">
    <text x="35" y="140" class="rank">{FIELD_1}</text>
    <text x="90" y="140" class="title">{FIELD_2}</text>
    <text x="685" y="140" class="score" text-anchor="end">{FIELD_3}</text>
    <line x1="35" y1="160" x2="685" y2="160" class="line" />
  </g>

"""

svg_rows_format_end = """
  <g transform="translate(0, {Y_OFFSET})">
    <text x="35" y="140" class="rank">{FIELD_1}</text>
    <text x="90" y="140" class="title">{FIELD_2}</text>
    <text x="685" y="140" class="score" text-anchor="end">{FIELD_3}</text>
  </g>

"""

def convert_table_to_svg(input_table) -> str:
    return_svg = svg_format

    rows_svg = ""

    for i, row in enumerate(input_table, 0):
        if i == 5:
            break

        if i == len(input_table) - 1:
            rows_svg += svg_rows_format_end.format(
                Y_OFFSET = i * 65,
                FIELD_1 = row[0],
                FIELD_2 = row[1] if len(row[1]) <= 40 else row[1][:37] + "...",
                FIELD_3 = row[2],
            )
        else:
            rows_svg += svg_rows_format_not_end.format(
                Y_OFFSET = i * 65,
                FIELD_1 = row[0],
                FIELD_2 = row[1] if len(row[1]) <= 40 else row[1][:37] + "...",
                FIELD_3 = row[2],
            )

    return return_svg.format(ROWS = rows_svg, TIMESTAMP = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%H:%M %d/%m/%y"))
