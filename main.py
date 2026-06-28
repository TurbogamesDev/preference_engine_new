import utils.graphql_interface as graphql_interface
from utils.entry import Entry
# from utils.media import Media
# from utils.tag_data import TagData
from utils.tag_score import TagScore
import utils.entry_score_calculator as entry_score_calc
import statistics
from tabulate import tabulate
import utils.table_to_svg as table_to_svg
from datetime import datetime
from zoneinfo import ZoneInfo

test_query_file_path = "queries/test_query.graphql"

test_query = graphql_interface.get_query_from_file_path(test_query_file_path)

response = graphql_interface.run_anilist_query(
    test_query,
    {
        "type": "ANIME",
        "userName": "turbogames"
    }
)

started_entries: list[Entry] = []
not_started_entries: list[Entry] = []

tag_scores: dict[str, TagScore] = {}
started_entry_score_values: list[float] = []

for watch_list in response["MediaListCollection"]["lists"]: #[0]["entries"]:
    for raw_entry in watch_list["entries"]:
        entry: Entry = Entry(raw_entry)

        if entry.status == "PLANNING":
            not_started_entries.append(entry)
        else:
            started_entries.append(entry)

for entry in started_entries:
    print(f"[{entry.status}] {entry.media.title} ({entry.progress}/{entry.media.total_episodes})")

    for tag_data in entry.media.tags:
        if tag_data.tag_name not in tag_scores:
            tag_scores[tag_data.tag_name] = TagScore(tag_data.tag_name)

        tag_scores[tag_data.tag_name].add_entry(entry, tag_data)
    
for entry in started_entries:
    started_entry_score_values.append(entry_score_calc.calculate_raw_entry_score(entry, tag_scores))

for entry in started_entries:
    raw_entry_score = entry_score_calc.calculate_raw_entry_score(entry, tag_scores)
    normalised_entry_score = entry_score_calc.normalise_raw_entry_score(
        raw_entry_score,
        max(started_entry_score_values),
        statistics.median(started_entry_score_values)
    )

    entry.normalised_score = normalised_entry_score

    # table_data.append([entry.media.title, f"{normalised_entry_score}%"])

    # print(f"This should be 100%: {entry_score_calc.normalise_raw_entry_score(max(started_entry_score_values), max(tag_score_values), statistics.median(tag_score_values))}%")
    # print(f"This should be 50%: {entry_score_calc.normalise_raw_entry_score(max(tag_score_values), max(tag_score_values), statistics.median(tag_score_values))}%")
    print(f"{entry.media.title} is predicted to have a score of {normalised_entry_score:.2f}%") 

print("-"*80)

for entry in not_started_entries:
    raw_entry_score = entry_score_calc.calculate_raw_entry_score(entry, tag_scores)
    normalised_entry_score = entry_score_calc.normalise_raw_entry_score(
        raw_entry_score,
        max(started_entry_score_values),
        statistics.median(started_entry_score_values)
    )

    entry.normalised_score = normalised_entry_score

    # table_data.append([entry.media.title, f"{normalised_entry_score:.2f}%"])

    # print(f"This should be 100%: {entry_score_calc.normalise_raw_entry_score(max(started_entry_score_values), max(tag_score_values), statistics.median(tag_score_values))}%")
    # print(f"This should be 50%: {entry_score_calc.normalise_raw_entry_score(max(tag_score_values), max(tag_score_values), statistics.median(tag_score_values))}%")
    print(f"{entry.media.title} is predicted to have a score of {normalised_entry_score:.2f}%") 

table_data = [
    [f"#{i}", entry.media.title, f"{entry.normalised_score:.2f}%", entry.status]
    for i, entry in enumerate(sorted(not_started_entries, key = lambda x: x.normalised_score, reverse = True), 1)
]

table_headers = ["Rank", "Anime Title", "Prediction", "Status"]

with open("output.svg", "w", encoding="utf-8") as file:
    file.write(table_to_svg.convert_table_to_svg(table_data))

# table_data.extend([
#     [f"#{i}", entry.media.title, f"{entry.normalised_score:.2f}%", entry.status]
#     for i, entry in enumerate(sorted(started_entries, key = lambda x: x.normalised_score, reverse = True), 1)
# ])

table_data = [
    [f"#{i}", entry.media.title, f"{entry.normalised_score}", entry.status]
    for i, entry in enumerate(sorted(started_entries + not_started_entries, key = lambda x: x.normalised_score, reverse = True), 1)
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





