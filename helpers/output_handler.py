from datetime import datetime
from zoneinfo import ZoneInfo
from tabulate import tabulate

from utils.media import Media
from utils.tag_score import TagScore
from utils.parsed_entries_response import ParsedEntriesResponse

import helpers.table_to_svg_converter as TableToSVGConverter

def generate_output_svg(media_to_normalised_score: dict[int, float], not_started_medias: dict[int, Media]):
    table_data = [
        [f"#{i}", media.title, f"{media_to_normalised_score[media.id]:.2f}%", "PLANNING"]
        for i, media in enumerate(sorted(list(not_started_medias.values()), key = lambda media: media_to_normalised_score[media.id], reverse = True), 1)
    ]

    with open("output.svg", "w", encoding="utf-8") as file:
        file.write(TableToSVGConverter.convert_table_to_svg(table_data))

def append_log_file(media_to_normalised_score: dict[int, float], parsed_entries_response: ParsedEntriesResponse):
    started_entries = parsed_entries_response.started_entries
    not_started_medias = parsed_entries_response.not_started_media
    media_to_watch_status = parsed_entries_response.media_to_watch_status

    table_headers = ["Rank", "Anime ID", "Anime Title", "Prediction", "Status"]

    table_data = [
        [f"#{i}", f"{media.id}", media.title, f"{media_to_normalised_score[media.id]}", media_to_watch_status[media.id]]
        for i, media in enumerate(sorted( [entry.media for entry in list(started_entries.values())] + list(not_started_medias.values()) , key = lambda media: media_to_normalised_score[media.id], reverse = True) , 1)
    ]

    with open("log_file.txt", "a", encoding="utf-8") as file:
        file.write(f"Log file for {datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%H:%M:%S %d/%m/%y")}:\n")

        file.write(
            tabulate(table_data, table_headers)
        )

        file.write("\n" + ("*" * 120) + "\n")

def append_tag_score_log_file(tag_scores: dict[int, TagScore]):
    table_headers = ["Rank", "Tag ID", "Tag Name", "Total Tag Score"]

    table_data = [
        [f"#{i}", tag_score.tag_id, tag_score.tag_name, tag_score.total_tag_score]
        for i, tag_score in enumerate(sorted(tag_scores.values(), key = lambda x: x.total_tag_score, reverse = True), 1)
    ]

    with open("tag_score_log_file.txt", "a", encoding="utf-8") as file:
        file.write(f"Tag Score Log file for {datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%H:%M:%S %d/%m/%y")}:\n")

        file.write(
            tabulate(table_data, table_headers)
        )

        file.write("\n" + ("*" * 120) + "\n")