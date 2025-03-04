import customtkinter as ctk
from datetime import datetime
from src.utils.theme import theme

class CourseCard(ctk.CTkFrame):
    def __init__(self, master, title, lessons, duration, instructor, price, color, **kwargs):
        super().__init__(master, fg_color=color, corner_radius=15, **kwargs)
        
        # Course info
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Helvetica", 16, "bold"),
            text_color="#1a1b1e"
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        info_text = f"{lessons} lessons - {duration} Minutes"
        info_label = ctk.CTkLabel(
            self,
            text=info_text,
            font=("Helvetica", 12),
            text_color="#1a1b1e"
        )
        info_label.pack(anchor="w", padx=15, pady=0)
        
        instructor_label = ctk.CTkLabel(
            self,
            text=instructor,
            font=("Helvetica", 12),
            text_color="#1a1b1e"
        )
        instructor_label.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Bottom section with price and button
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        price_label = ctk.CTkLabel(
            bottom_frame,
            text=f"$ {price}",
            font=("Helvetica", 16, "bold"),
            text_color="#1a1b1e"
        )
        price_label.pack(side="left")
        
        watch_btn = ctk.CTkButton(
            bottom_frame,
            text="Watch Now",
            font=("Helvetica", 12),
            fg_color="#1a1b1e",
            text_color="#ffffff",
            width=100,
            height=32,
            corner_radius=16
        )
        watch_btn.pack(side="right")

class LessonScheduleItem(ctk.CTkFrame):
    def __init__(self, master, course, lecturer, time, lesson_num, duration, **kwargs):
        super().__init__(master, fg_color="#ffffff", corner_radius=8, **kwargs)
        
        # Course icon/indicator
        icon_frame = ctk.CTkFrame(
            self,
            width=30,
            height=30,
            fg_color="#1a1b1e",
            corner_radius=8
        )
        icon_frame.pack(side="left", padx=(15, 10), pady=10)
        icon_frame.pack_propagate(False)
        
        # Course info
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, pady=10)
        
        course_label = ctk.CTkLabel(
            info_frame,
            text=course,
            font=("Helvetica", 14, "bold"),
            text_color="#1a1b1e"
        )
        course_label.pack(anchor="w")
        
        lecturer_text = f"Lecturer: {lecturer} - {time}"
        lecturer_label = ctk.CTkLabel(
            info_frame,
            text=lecturer_text,
            font=("Helvetica", 12),
            text_color="gray"
        )
        lecturer_label.pack(anchor="w")
        
        # Lesson info
        lesson_frame = ctk.CTkFrame(self, fg_color="transparent")
        lesson_frame.pack(side="right", padx=15, pady=10)
        
        lesson_label = ctk.CTkLabel(
            lesson_frame,
            text=f"Lesson {lesson_num}",
            font=("Helvetica", 12, "bold"),
            text_color="#1a1b1e"
        )
        lesson_label.pack()
        
        duration_label = ctk.CTkLabel(
            lesson_frame,
            text=f"{duration} Min",
            font=("Helvetica", 12),
            text_color="gray"
        )
        duration_label.pack()

class ProgressCard(ctk.CTkFrame):
    def __init__(self, master, course, progress, total, price, **kwargs):
        super().__init__(master, fg_color="#1e2124", corner_radius=8, **kwargs)
        
        # Course name and progress
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        course_label = ctk.CTkLabel(
            header_frame,
            text=course,
            font=("Helvetica", 14, "bold"),
            text_color="#ffffff"
        )
        course_label.pack(side="left")
        
        progress_text = f"{progress}/{total} lessons"
        progress_label = ctk.CTkLabel(
            header_frame,
            text=progress_text,
            font=("Helvetica", 12),
            text_color="#8a8d93"
        )
        progress_label.pack(side="right")
        
        # Progress bar
        progress_value = progress / total
        progress_bar = ctk.CTkProgressBar(self)
        progress_bar.pack(fill="x", padx=15, pady=5)
        progress_bar.set(progress_value)
        
        # Price
        price_label = ctk.CTkLabel(
            self,
            text=f"Price: {price} Coins",
            font=("Helvetica", 12),
            text_color="#8a8d93"
        )
        price_label.pack(anchor="w", padx=15, pady=(0, 15))

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Header section
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(40, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="My Courses",
            font=("Helvetica", 24, "bold"),
            text_color="#ffffff"
        )
        title_label.pack(side="left")
        
        greeting_label = ctk.CTkLabel(
            header_frame,
            text=f"Good Morning {self._get_user_name()}!",
            font=("Helvetica", 16),
            text_color="#8a8d93"
        )
        greeting_label.pack(side="left", padx=20)
        
        date_label = ctk.CTkButton(
            header_frame,
            text=datetime.now().strftime("%B"),
            font=("Helvetica", 14),
            fg_color="#1e2124",
            text_color="#ffffff",
            width=100,
            height=32,
            corner_radius=16
        )
        date_label.pack(side="right")
        
        # Course cards section
        courses_frame = ctk.CTkFrame(self, fg_color="transparent")
        courses_frame.pack(fill="x", padx=40, pady=10)
        courses_frame.grid_columnconfigure((0,1,2,3), weight=1, uniform="column")
        
        course_data = [
            {
                "title": "Course One",
                "lessons": 18,
                "duration": 240,
                "instructor": "Michael Brown",
                "price": 1200,
                "color": "#B2E5E5"  # Light blue
            },
            {
                "title": "Course Two",
                "lessons": 15,
                "duration": 200,
                "instructor": "John Johnson",
                "price": 1200,
                "color": "#E5D5B5"  # Light brown
            },
            {
                "title": "Course Three",
                "lessons": 24,
                "duration": 360,
                "instructor": "William Jones",
                "price": 1500,
                "color": "#E5E5B5"  # Light yellow
            },
            {
                "title": "Course Four",
                "lessons": 18,
                "duration": 240,
                "instructor": "John Johnson",
                "price": 850,
                "color": "#E5B5B5"  # Light red
            }
        ]
        
        for i, course in enumerate(course_data):
            card = CourseCard(
                courses_frame,
                title=course["title"],
                lessons=course["lessons"],
                duration=course["duration"],
                instructor=course["instructor"],
                price=course["price"],
                color=course["color"]
            )
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
        
        # Bottom section container
        bottom_container = ctk.CTkFrame(self, fg_color="transparent")
        bottom_container.pack(fill="both", expand=True, padx=40, pady=10)
        bottom_container.grid_columnconfigure(0, weight=3)
        bottom_container.grid_columnconfigure(1, weight=2)
        
        # Lesson schedule section
        schedule_frame = ctk.CTkFrame(bottom_container, fg_color="transparent")
        schedule_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        schedule_header = ctk.CTkFrame(schedule_frame, fg_color="transparent")
        schedule_header.pack(fill="x", pady=(0, 10))
        
        schedule_title = ctk.CTkLabel(
            schedule_header,
            text="Lesson Schedule",
            font=("Helvetica", 16, "bold"),
            text_color="#ffffff"
        )
        schedule_title.pack(side="left")
        
        filter_btn = ctk.CTkButton(
            schedule_header,
            text="Popular",
            font=("Helvetica", 12),
            fg_color="#1e2124",
            text_color="#ffffff",
            width=80,
            height=28,
            corner_radius=14
        )
        filter_btn.pack(side="right")
        
        # Schedule items
        schedule_items = [
            {
                "date": "20/12/2023",
                "courses": [
                    {
                        "course": "Course One",
                        "lecturer": "Michael Brown",
                        "time": "11:30 AM",
                        "lesson": 4,
                        "duration": 50
                    },
                    {
                        "course": "Course Two",
                        "lecturer": "John Johnson",
                        "time": "14:30 PM",
                        "lesson": 5,
                        "duration": 30
                    }
                ]
            },
            {
                "date": "21/12/2023",
                "courses": [
                    {
                        "course": "Course Three",
                        "lecturer": "William Jones",
                        "time": "10:30 AM",
                        "lesson": 1,
                        "duration": 40
                    },
                    {
                        "course": "Course Four",
                        "lecturer": "John Johnson",
                        "time": "16:30 PM",
                        "lesson": 4,
                        "duration": 60
                    }
                ]
            }
        ]
        
        for schedule in schedule_items:
            date_label = ctk.CTkLabel(
                schedule_frame,
                text=schedule["date"],
                font=("Helvetica", 14),
                text_color="#8a8d93"
            )
            date_label.pack(anchor="w", pady=(10, 5))
            
            for course in schedule["courses"]:
                item = LessonScheduleItem(
                    schedule_frame,
                    course=course["course"],
                    lecturer=course["lecturer"],
                    time=course["time"],
                    lesson_num=course["lesson"],
                    duration=course["duration"]
                )
                item.pack(fill="x", pady=5)
        
        # Progress section
        progress_frame = ctk.CTkFrame(bottom_container, fg_color="transparent")
        progress_frame.grid(row=0, column=1, sticky="nsew")
        
        progress_header = ctk.CTkFrame(progress_frame, fg_color="transparent")
        progress_header.pack(fill="x", pady=(0, 10))
        
        progress_title = ctk.CTkLabel(
            progress_header,
            text="Progress",
            font=("Helvetica", 16, "bold"),
            text_color="#ffffff"
        )
        progress_title.pack(side="left")
        
        view_all_btn = ctk.CTkButton(
            progress_header,
            text="",
            image=self._get_view_all_icon(),
            fg_color="transparent",
            width=24,
            height=24
        )
        view_all_btn.pack(side="right")
        
        # Progress cards
        progress_data = [
            {
                "course": "Course One",
                "progress": 15,
                "total": 18,
                "price": 155
            },
            {
                "course": "Course Two",
                "progress": 7,
                "total": 15,
                "price": 270
            },
            {
                "course": "Course Three",
                "progress": 10,
                "total": 24,
                "price": 400
            }
        ]
        
        for data in progress_data:
            card = ProgressCard(
                progress_frame,
                course=data["course"],
                progress=data["progress"],
                total=data["total"],
                price=data["price"]
            )
            card.pack(fill="x", pady=5)
    
    def _get_user_name(self):
        """Get the current user's name"""
        return "James"  # This should be fetched from user data
    
    def _get_view_all_icon(self):
        """Get the view all icon image"""
        # This should return a CTkImage instance
        return None 