from utils.tag_score import TagScore
from utils.entry import Entry

def calculate_tag_scores(started_entries_dict: dict[int, Entry]) -> dict[int, TagScore]:
    tag_scores: dict[int, TagScore] = {}

    for entry in list(started_entries_dict.values()):
        print(f"[{entry.status}] {entry.media.title} ({entry.progress}/{entry.media.total_episodes})")

        for tag_data in entry.media.tags:
            if not tag_scores.get(tag_data.tag_id):
                tag_scores[tag_data.tag_id] = TagScore(tag_data.tag_id, tag_data.tag_name)

            tag_scores[tag_data.tag_id].add_entry(entry, tag_data)

    return tag_scores