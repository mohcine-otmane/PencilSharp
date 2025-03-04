from typing import Optional, Dict
from src.models.subject import Subject, Unit, Topic
from src.models.user import UserProgress
from src.utils.observer import Observable, Observer

class AppController(Observable):
    def __init__(self):
        super().__init__()
        self.user_progress = UserProgress()
        self.subjects: Dict[str, Subject] = {}
        self.current_subject: Optional[str] = None
        self.current_unit: Optional[int] = None
        self.current_topic: Optional[str] = None

    def load_subjects(self, subjects_data: Dict):
        """Load subjects from configuration data"""
        for subject_name, data in subjects_data.items():
            units = []
            for i, unit_data in enumerate(data["units"]):
                topics = [
                    Topic(
                        name=topic,
                        content={},  # Content will be loaded on demand
                        is_locked=i > 0 or j > 0  # Lock all except first topic of first unit
                    )
                    for j, topic in enumerate(unit_data["topics"])
                ]
                units.append(Unit(name=unit_data["name"], topics=topics))
            
            self.subjects[subject_name] = Subject(
                name=subject_name,
                icon=data["icon"],
                color=data["color"],
                units=units
            )

    def select_subject(self, subject_name: str):
        """Select a subject to study"""
        if subject_name in self.subjects:
            self.current_subject = subject_name
            self.current_unit = None
            self.current_topic = None
            self.notify_observers("subject_changed", subject_name)

    def select_unit(self, unit_index: int):
        """Select a unit within the current subject"""
        if self.current_subject and 0 <= unit_index < len(self.subjects[self.current_subject].units):
            self.current_unit = unit_index
            self.current_topic = None
            self.notify_observers("unit_changed", unit_index)

    def select_topic(self, topic_name: str):
        """Select a topic within the current unit"""
        if not (self.current_subject and self.current_unit is not None):
            return

        unit = self.subjects[self.current_subject].units[self.current_unit]
        for topic in unit.topics:
            if topic.name == topic_name and not topic.is_locked:
                self.current_topic = topic_name
                self.notify_observers("topic_changed", topic_name)
                break

    def complete_topic(self):
        """Mark current topic as completed"""
        if not (self.current_subject and self.current_unit is not None and self.current_topic):
            return

        # Update topic progress
        unit = self.subjects[self.current_subject].units[self.current_unit]
        for topic in unit.topics:
            if topic.name == self.current_topic:
                topic.progress = 100
                # Unlock next topic if available
                next_topic_index = unit.topics.index(topic) + 1
                if next_topic_index < len(unit.topics):
                    unit.topics[next_topic_index].is_locked = False
                break

        # Update subject progress
        self.subjects[self.current_subject].update_progress()

        # Update user progress
        self.user_progress.complete_lesson(self.current_subject)
        self.notify_observers("progress_updated", self.user_progress)

    def get_current_subject(self) -> Optional[Subject]:
        """Get the currently selected subject"""
        return self.subjects.get(self.current_subject) if self.current_subject else None

    def get_current_unit(self) -> Optional[Unit]:
        """Get the currently selected unit"""
        subject = self.get_current_subject()
        if subject and self.current_unit is not None:
            return subject.units[self.current_unit]
        return None

    def get_current_topic(self) -> Optional[Topic]:
        """Get the currently selected topic"""
        unit = self.get_current_unit()
        if unit and self.current_topic:
            return next((t for t in unit.topics if t.name == self.current_topic), None)
        return None 