import statistics

from utils.entry import Entry
from utils.media import Media
from utils.tag_score import TagScore

import utils.entry_score_calculator as EntryScoreCalculator

def calculate_normalised_score_for_media(media: Media, tag_scores: dict[int, TagScore], started_entries_raw_scores: list[float]) -> float:
    raw_entry_score: float = EntryScoreCalculator.calculate_raw_media_score(media, tag_scores)

    normalised_entry_score = EntryScoreCalculator.normalise_raw_media_score(
        raw_entry_score,
        max(started_entries_raw_scores),
        statistics.median(started_entries_raw_scores)
    )

    return normalised_entry_score

def calculate_media_to_normalised_score_dict(started_entries: dict[int, Entry], not_started_medias: dict[int, Media], tag_scores: dict[int, TagScore]) -> dict[int, float]:
    started_entries_raw_scores: list[float] = []

    media_to_normalised_score: dict[int, float] = {}
        
    for entry in list(started_entries.values()):
        started_entries_raw_scores.append(EntryScoreCalculator.calculate_raw_media_score(entry.media, tag_scores))

    for entry in list(started_entries.values()): 
        normalised_score = calculate_normalised_score_for_media(entry.media, tag_scores, started_entries_raw_scores)

        media_to_normalised_score[entry.media.id] = normalised_score

    for media in list(not_started_medias.values()):
        normalised_score = calculate_normalised_score_for_media(media, tag_scores, started_entries_raw_scores)

        media_to_normalised_score[media.id] = normalised_score

    return media_to_normalised_score
