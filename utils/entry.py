from datetime import datetime, timezone
import math

from utils.media import Media

fixed_watched_runtime_hours_for_dropped = 4.73
decay_speed = 300

class Entry:
    def __init__(self, raw_entry: dict) -> None:
        self.media: Media = Media(raw_entry["media"])

        self.progress: int = raw_entry["progress"]
        self.status: str = raw_entry["status"]
        self.start_date: datetime = datetime.now() if self.status == "PLANNING" else datetime(
            raw_entry["startedAt"]["year"] or 1,
            raw_entry["startedAt"]["month"] or 1,
            raw_entry["startedAt"]["day"] or 1,
            tzinfo = timezone.utc
        )
        self.rewatch_count: int = raw_entry["repeat"]

        self.runtime_hours_weight: float = fixed_watched_runtime_hours_for_dropped if self.status == "DROPPED" else (self.media.episode_duration_hours * self.progress)

        self.normalised_score: float = 0.0

        if self.progress > self.media.total_episodes:
            self.media.total_episodes = self.progress

    def get_completion_weight(self) -> float:
        if self.status == "COMPLETED":
            return 1.0 + self.rewatch_count
        elif self.status == "CURRENT" or self.status == "PAUSED":
            return min(1.0, (self.progress / self.media.total_episodes))
        elif self.status == "REPEATING":
            return min(1.0, (self.progress / self.media.total_episodes)) + self.rewatch_count + 1
        elif self.status == "DROPPED":
            return min(1.0, (self.progress / self.media.total_episodes)) - 1.0
        else:
            return 0.0
        
    def get_decay_weight(self, current_datetime: datetime):
        days_delta = max(0, (current_datetime - self.start_date).days)

        decay_weight = math.exp(-days_delta / decay_speed) # = e^(-days_delta / decay_speed)

        return decay_weight


        





