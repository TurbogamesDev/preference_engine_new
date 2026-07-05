from utils.entry import Entry
from utils.media import Media

class ParsedEntriesResponse:
    def __init__(self, started_entries: dict[int, Entry], not_started_media: dict[int, Media], media_to_watch_status: dict[int, str]) -> None:
        self.started_entries: dict[int, Entry] = started_entries

        self.not_started_media: dict[int, Media] = not_started_media
        
        self.media_to_watch_status: dict[int, str] = media_to_watch_status