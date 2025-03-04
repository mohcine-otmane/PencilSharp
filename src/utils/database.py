import sqlite3
import hashlib
import os
from typing import Optional, Tuple

class Database:
    def __init__(self):
        self.db_path = "users.db"
        self._create_tables()
    
    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, email: str, password: str, name: str = None) -> Tuple[bool, str]:
        """Create a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Hash the password
            password_hash = self._hash_password(password)
            
            # Insert the user
            cursor.execute(
                "INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)",
                (email, password_hash, name)
            )
            
            conn.commit()
            conn.close()
            
            return True, "User created successfully"
            
        except sqlite3.IntegrityError:
            return False, "Email already exists"
        except Exception as e:
            return False, f"Error creating user: {str(e)}"
    
    def verify_user(self, email: str, password: str) -> Tuple[bool, str, Optional[dict]]:
        """Verify user credentials"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get user by email
            cursor.execute(
                "SELECT id, email, password_hash, name FROM users WHERE email = ?",
                (email,)
            )
            user = cursor.fetchone()
            
            if not user:
                return False, "Invalid email or password", None
            
            # Verify password
            password_hash = self._hash_password(password)
            if password_hash != user[2]:  # Index 2 is password_hash
                return False, "Invalid email or password", None
            
            # Return user data
            user_data = {
                "id": user[0],
                "email": user[1],
                "name": user[3]
            }
            
            return True, "Login successful", user_data
            
        except Exception as e:
            return False, f"Error verifying user: {str(e)}", None
        finally:
            conn.close()
    
    def user_exists(self, email: str) -> bool:
        """Check if a user exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists 