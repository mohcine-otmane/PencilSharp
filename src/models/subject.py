from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Topic:
    name: str
    content: Dict
    is_locked: bool = True
    progress: float = 0.0

@dataclass
class Unit:
    name: str
    topics: List[Topic]
    progress: float = 0.0

@dataclass
class Subject:
    name: str
    icon: str
    color: str
    units: List[Unit]
    progress: float = 0.0

    @property
    def total_topics(self) -> int:
        return sum(len(unit.topics) for unit in self.units)

    @property
    def completed_topics(self) -> int:
        return sum(
            sum(1 for topic in unit.topics if topic.progress >= 100)
            for unit in self.units
        )

    def update_progress(self):
        """Update progress based on completed topics"""
        if self.total_topics > 0:
            self.progress = (self.completed_topics / self.total_topics) * 100
            for unit in self.units:
                unit_completed = sum(1 for topic in unit.topics if topic.progress >= 100)
                unit.progress = (unit_completed / len(unit.topics)) * 100 