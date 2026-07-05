import utils.graphql_interface as graphql_interface

from utils.entry import Entry
from utils.media import Media
from utils.parsed_entries_response import ParsedEntriesResponse

entry_fetch_query_file_path = "queries/entry_fetch_query.graphql"

entry_fetch_query = graphql_interface.get_query_from_file_path(entry_fetch_query_file_path)

def fetch_parsed_entries_response(username: str) -> ParsedEntriesResponse:
    response = graphql_interface.run_anilist_query(
        entry_fetch_query,
        {
            "type": "ANIME",
            "userName": username
        }
    )

    started_entries: dict[int, Entry] = {}
    not_started_medias: dict[int, Media] = {}
    media_to_watch_status: dict[int, str] = {}

    for watch_list in response["MediaListCollection"]["lists"]: #[0]["entries"]:
        for raw_entry in watch_list["entries"]:
            media: Media = Media(raw_entry["media"])

            if len(media.tags) == 0:
                continue
            
            watch_status: str = raw_entry["status"]

            media_to_watch_status[media.id] = watch_status

            if watch_status == "PLANNING":
                if not_started_medias.get(media.id):
                    continue
                
                not_started_medias[media.id] = media

            else:
                entry: Entry = Entry(raw_entry, media)

                if started_entries.get(entry.media.id):
                    continue
                
                started_entries[entry.media.id] = entry

    return ParsedEntriesResponse(started_entries, not_started_medias, media_to_watch_status)