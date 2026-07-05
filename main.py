from utils.tag_score import TagScore

from tabulate import tabulate
import utils.table_to_svg as table_to_svg
from datetime import datetime
from zoneinfo import ZoneInfo

import helpers.entry_fetcher as EntryFetcher
import helpers.tag_scores_calculator as TagScoresCalculator
import helpers.normalised_score_assigner as NormalisedScoreAssigner

parsed_entries_response = EntryFetcher.fetch_parsed_entries_response("turbogames")

started_entries = parsed_entries_response.started_entries
not_started_medias = parsed_entries_response.not_started_media
media_to_watch_status = parsed_entries_response.media_to_watch_status

tag_scores: dict[int, TagScore] = TagScoresCalculator.calculate_tag_scores(started_entries)

media_to_normalised_score: dict[int, float] = NormalisedScoreAssigner.calculate_media_to_normalised_score_dict(started_entries, not_started_medias, tag_scores)
    
# for entry in list(started_entries.values()):
#     started_entries_raw_scores.append(entry_score_calc.calculate_raw_media_score(entry.media, tag_scores))

# for entry in list(started_entries.values()):
#     raw_entry_score = entry_score_calc.calculate_raw_media_score(entry.media, tag_scores)
#     normalised_entry_score = entry_score_calc.normalise_raw_media_score(
#         raw_entry_score,
#         max(started_entries_raw_scores),
#         statistics.median(started_entries_raw_scores)
#     )

#     entry.normalised_score = normalised_entry_score

#     print(f"{entry.media.title} is predicted to have a score of {normalised_entry_score:.2f}%") 

# print("-"*80)

# for media in list(not_started_medias.values()):
#     raw_entry_score = entry_score_calc.calculate_raw_media_score(media, tag_scores)
#     normalised_entry_score = entry_score_calc.normalise_raw_media_score(
#         raw_entry_score,
#         max(started_entries_raw_scores),
#         statistics.median(started_entries_raw_scores)
#     )

#     media_to_normalised_score[media.id] = normalised_entry_score

#     print(f"{media.title} is predicted to have a score of {normalised_entry_score:.2f}%") 

table_data = [
    [f"#{i}", media.title, f"{media_to_normalised_score[media.id]:.2f}%", "PLANNING"]
    for i, media in enumerate(sorted(list(not_started_medias.values()), key = lambda media: media_to_normalised_score[media.id], reverse = True), 1)
]

table_headers = ["Rank", "Anime Title", "Prediction", "Status"]

with open("output.svg", "w", encoding="utf-8") as file:
    file.write(table_to_svg.convert_table_to_svg(table_data))

# table_data.extend([
#     [f"#{i}", entry.media.title, f"{entry.normalised_score:.2f}%", entry.status]
#     for i, entry in enumerate(sorted(started_entries, key = lambda x: x.normalised_score, reverse = True), 1)
# ])

table_data = [
    [f"#{i}", media.title, f"{media_to_normalised_score[media.id]}", media_to_watch_status[media.id]]
    for i, media in enumerate(sorted([entry.media for entry in list(started_entries.values())] + list(not_started_medias.values()), key = lambda media: media_to_normalised_score[media.id], reverse = True), 1)
]

with open("log_file.txt", "a", encoding="utf-8") as file:
    file.write(f"Log file for {datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%H:%M:%S %d/%m/%y")}:\n")

    file.write(
        tabulate(table_data, table_headers)
    )

    file.write("\n")

    file.write("*" * 120)

    file.write("\n")

with open("tag_score_log_file.txt", "a", encoding="utf-8") as file:
    file.write(f"Log file for {datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%H:%M:%S %d/%m/%y")}:\n")

    file.write(
        tabulate(
            [
                [f"#{i}", tag_score.tag_name, tag_score.total_tag_score]
                for i, tag_score in enumerate(sorted(tag_scores.values(), key = lambda x: x.total_tag_score, reverse = True), 1)
            ],
        )
    )

    file.write("\n")

    file.write("*" * 120)

    file.write("\n")



# table_data = [
#     [i, entry.media.title, f"{}"]
#     for i, entry in enumerate(not_started_entries, 1)
# ]

# for tag_score in tag_scores.values():
#     print(f"Tag {tag_score.tag_name} has a score of {round(tag_score.total_tag_score, 2)}")





