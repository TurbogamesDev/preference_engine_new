from utils.entry import Entry
from utils.tag_data import TagData

from datetime import datetime, timezone

tag_weight_exponent = 1.5

class TagScore:
    def __init__(self, tag_name: str) -> None:
        self.tag_name: str = tag_name

        self.total_tag_score: float = 0.0

    def add_entry(self, entry: Entry, tag_data: TagData):
        amount_of_tag_in_show: float = tag_data.tag_weight
        completion_weight: float = entry.get_completion_weight()
        run_time_in_hours: float = entry.runtime_hours_weight
        decay_factor: float = entry.get_decay_weight(
            datetime.now(timezone.utc)
        )

        entry_score = (amount_of_tag_in_show ** tag_weight_exponent) * (completion_weight) * (run_time_in_hours) * (decay_factor)

        self.total_tag_score += entry_score