class TagData:
    def __init__(self, tag_id: int, tag_name: str, tag_rank: int) -> None:
        self.tag_id: int = tag_id

        self.tag_name: str = tag_name

        self.tag_weight: float = tag_rank / 100.0