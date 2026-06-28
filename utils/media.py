from utils.tag_data import TagData

fallback_total_episodes = 12

class Media:
    def __init__(self, raw_media: dict) -> None:
        self.title: str = raw_media["title"]["english"] or raw_media["title"]["romaji"] or raw_media["title"]["native"] or "Unknown Title"

        self.total_episodes: int = raw_media["episodes"] or fallback_total_episodes

        self.episode_duration_hours: float = (raw_media["duration"] or 24)  / 60.0

        self.total_runlength_hours: float = self.total_episodes * self.episode_duration_hours

        self.tags: list[TagData] = []

        for raw_tag_data in raw_media["tags"]:
            self.tags.append(
                TagData(raw_tag_data["name"], raw_tag_data["rank"])
            )
        
