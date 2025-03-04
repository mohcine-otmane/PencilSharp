from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime, date

@dataclass
class Achievement:
    name: str
    description: str
    icon: str
    earned_date: datetime

@dataclass
class UserProgress:
    xp: int = 0
    points: int = 0
    streak: int = 0
    daily_goal: int = 5
    lessons_completed_today: int = 0
    last_activity_date: date = field(default_factory=date.today)
    achievements: List[Achievement] = field(default_factory=list)
    subject_progress: Dict[str, float] = field(default_factory=dict)

    def add_xp(self, amount: int):
        """Add XP and update points"""
        self.xp += amount
        self.points += amount // 2

    def update_streak(self):
        """Update streak based on daily activity"""
        today = date.today()
        if (today - self.last_activity_date).days == 1:
            self.streak += 1
        elif (today - self.last_activity_date).days > 1:
            self.streak = 0
        self.last_activity_date = today

    def complete_lesson(self, subject: str):
        """Record completion of a lesson"""
        self.lessons_completed_today += 1
        self.add_xp(10)  # Base XP for completing a lesson
        
        # Update subject progress
        current_progress = self.subject_progress.get(subject, 0)
        self.subject_progress[subject] = min(100, current_progress + 5)

        # Check for achievements
        self._check_achievements()

    def _check_achievements(self):
        """Check and award new achievements"""
        # First lesson achievement
        if self.lessons_completed_today == 1 and not any(a.name == "First Lesson" for a in self.achievements):
            self.achievements.append(Achievement(
                "First Lesson",
                "Complete your first lesson",
                "🌟",
                datetime.now()
            ))

        # Perfect day achievement
        if self.lessons_completed_today >= self.daily_goal:
            if not any(a.name == "Perfect Day" and a.earned_date.date() == date.today() 
                      for a in self.achievements):
                self.achievements.append(Achievement(
                    "Perfect Day",
                    f"Complete {self.daily_goal} lessons in one day",
                    "🎯",
                    datetime.now()
                ))

        # Streak achievements
        streak_milestones = {
            7: "Week Warrior",
            30: "Monthly Master",
            100: "Centurion",
        }
        for days, name in streak_milestones.items():
            if self.streak >= days and not any(a.name == name for a in self.achievements):
                self.achievements.append(Achievement(
                    name,
                    f"Maintain a {days}-day streak",
                    "🔥",
                    datetime.now()
                )) 