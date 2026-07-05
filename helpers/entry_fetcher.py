import utils.graphql_interface as graphql_interface

from utils.entry import Entry
from utils.tag_score import TagScore

test_query_file_path = "queries/test_query.graphql"

test_query = graphql_interface.get_query_from_file_path(test_query_file_path)

def get_started_and_not_started_entries(username: str) -> tuple[list[Entry], list[Entry]]:
    response = graphql_interface.run_anilist_query(
        test_query,
        {
            "type": "ANIME",
            "userName": username
        }
    )

    started_entries: list[Entry] = []
    not_started_entries: list[Entry] = []

    for watch_list in response["MediaListCollection"]["lists"]: #[0]["entries"]:
        for raw_entry in watch_list["entries"]:
            entry: Entry = Entry(raw_entry)

            if entry.status == "PLANNING":
                not_started_entries.append(entry)
            else:
                started_entries.append(entry)

    return (started_entries, not_started_entries)