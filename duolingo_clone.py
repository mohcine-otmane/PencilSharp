import os
import sys
from colorama import init, Fore, Back, Style
from termcolor import colored

# Initialize colorama for Windows support
init()

class DuolingoClone:
    def __init__(self):
        self.xp = 0
        self.level = 1
        self.current_section = 1
        self.current_unit = 2
        self.league = "Sapphire"
        self.league_rank = 16
        self.daily_xp = 82
        self.daily_goal = 10
        self.daily_progress = 10

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self):
        print(f"\n{Fore.GREEN}Duolingo Clone - The world's best way to learn languages{Style.RESET_ALL}")
        print("=" * 60)

    def display_stats(self):
        print(f"\n{Fore.YELLOW}🏆 {self.xp} XP{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💎 {self.league} League - Rank #{self.league_rank}{Style.RESET_ALL}")
        print(f"⚡ Daily XP: {self.daily_xp}")
        print(f"🎯 Daily Goal: {self.daily_progress}/{self.daily_goal}")

    def display_section(self):
        print(f"\n{Fore.MAGENTA}SECTION {self.current_section}, UNIT {self.current_unit}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Describe basic contexts{Style.RESET_ALL}")
        print("\n📖 GUIDEBOOK")

    def display_progress_path(self):
        print("\n" + "=" * 20 + " Progress Path " + "=" * 20)
        print("🌟 START")
        print("  |")
        print("⭐ [Current Lesson]")
        print("  |")
        print("🔒 [Locked]")
        print("  |")
        print("📦 [Treasure Chest]")

    def display_menu(self):
        print("\n" + "=" * 20 + " Menu " + "=" * 20)
        print("1. Start Lesson")
        print("2. View Guidebook")
        print("3. View League")
        print("4. Exit")

    def run(self):
        while True:
            self.clear_screen()
            self.display_header()
            self.display_stats()
            self.display_section()
            self.display_progress_path()
            self.display_menu()

            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                print("\nStarting lesson...")
            elif choice == '2':
                print("\nOpening guidebook...")
            elif choice == '3':
                print("\nViewing league standings...")
            elif choice == '4':
                print("\nThank you for learning with us!")
                sys.exit(0)
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    app = DuolingoClone()
    app.run() 