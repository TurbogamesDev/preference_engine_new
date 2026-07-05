from utils.entry import Entry
from utils.tag_score import TagScore

def calculate_raw_entry_score(entry: Entry, tag_scores: dict[int, TagScore]) -> float:
    final_score: float = 0.0

    for tag_data in entry.media.tags:
        tag_id = tag_data.tag_id

        if not tag_scores.get(tag_id):
            continue

        final_score += (tag_data.tag_weight * tag_scores[tag_id].total_tag_score)

    return final_score

def normalise_raw_entry_score(raw_entry_score: float, highest_entry_score: float, median_entry_score: float) -> float:
    # y = mx + c
    
    slope: float = 50 / (highest_entry_score - median_entry_score)
    intercept: float = (50 * (highest_entry_score - (2 * median_entry_score) ) ) / (highest_entry_score - median_entry_score)

    normalised_score: float = (slope * raw_entry_score) + intercept

    return normalised_score
    