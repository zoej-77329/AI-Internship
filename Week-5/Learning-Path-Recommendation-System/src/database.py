import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = PROJECT_DIR / "data" / "pathfinder.db"


class DatabaseError(Exception):
    """Custom exception for database operation failures."""
    pass


def get_db_path(custom_path: Optional[Union[str, Path]] = None) -> Path:
    """Returns the resolved database path and ensures the parent folder exists."""
    if custom_path is not None:
        path = Path(custom_path)
    else:
        path = DEFAULT_DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_connection(db_path: Optional[Union[str, Path]] = None) -> sqlite3.Connection:
    """
    Creates and returns a SQLite connection with row_factory configured.
    Ensures foreign keys are enabled.
    """
    resolved_path = get_db_path(db_path)
    try:
        conn = sqlite3.connect(str(resolved_path), timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to connect to database at {resolved_path}: {e}") from e


@contextmanager
def managed_connection(db_path: Optional[Union[str, Path]] = None):
    """
    Context manager that yields an active SQLite connection within a transaction,
    ensuring the connection is deterministically closed upon block exit.
    """
    conn = get_connection(db_path)
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def init_db(db_path: Optional[Union[str, Path]] = None) -> None:
    """
    Initializes database tables safely without overwriting existing data.
    Creates user_profiles and learning_progress tables if they do not exist.
    """
    try:
        with managed_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    career_goal TEXT NOT NULL,
                    current_skills TEXT NOT NULL,
                    experience_level TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learning_progress (
                    user_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    completion_status INTEGER NOT NULL DEFAULT 0,
                    completion_date TEXT,
                    last_updated_date TEXT NOT NULL,
                    PRIMARY KEY (user_id, course_id)
                );
            """)
    except sqlite3.Error as e:
        raise DatabaseError(f"Error during database initialization: {e}") from e


# ---------------------------------------------------------------------------
# PROFILE FUNCTIONALITY
# ---------------------------------------------------------------------------

def validate_profile_data(
    full_name: str,
    career_goal: str,
    experience_level: str
) -> None:
    """Validates required user profile fields."""
    if not full_name or not str(full_name).strip():
        raise ValueError("Full name is required and cannot be empty.")
    if not career_goal or not str(career_goal).strip():
        raise ValueError("Career goal is required and cannot be empty.")
    if not experience_level or not str(experience_level).strip():
        raise ValueError("Experience level is required and cannot be empty.")

    valid_levels = {"Beginner", "Intermediate", "Advanced"}
    if str(experience_level).strip() not in valid_levels:
        raise ValueError(
            f"Invalid experience level '{experience_level}'. Allowed: {', '.join(sorted(valid_levels))}"
        )


def _serialize_skills(skills: Union[List[str], Set[str], str]) -> str:
    """Safely converts skill input into a JSON string list."""
    if isinstance(skills, str):
        if skills.strip().startswith("[") and skills.strip().endswith("]"):
            try:
                parsed = json.loads(skills)
                if isinstance(parsed, list):
                    return json.dumps([str(s).strip() for s in parsed if str(s).strip()])
            except json.JSONDecodeError:
                pass
        skill_list = [s.strip() for s in skills.split("|") if s.strip()]
    elif isinstance(skills, (list, set, tuple)):
        skill_list = [str(s).strip() for s in skills if str(s).strip()]
    else:
        skill_list = []
    # Deduplicate while preserving order
    return json.dumps(list(dict.fromkeys(skill_list)))


def _deserialize_skills(skills_raw: str) -> List[str]:
    """Deserializes JSON or pipe-delimited skill strings back into a list."""
    if not skills_raw:
        return []
    try:
        parsed = json.loads(skills_raw)
        if isinstance(parsed, list):
            return [str(s) for s in parsed]
    except (json.JSONDecodeError, TypeError):
        pass
    return [s.strip() for s in str(skills_raw).split("|") if s.strip()]


def _format_profile_row(row: sqlite3.Row) -> Dict[str, Any]:
    """Helper to convert a SQLite profile row into a standardized dictionary."""
    full_name = row["full_name"]
    return {
        "user_id": row["user_id"],
        "full_name": full_name,
        "name": full_name,  # Alias for compatibility with existing UI components
        "career_goal": row["career_goal"],
        "current_skills": _deserialize_skills(row["current_skills"]),
        "experience_level": row["experience_level"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }


def create_profile(
    full_name: str,
    career_goal: str,
    current_skills: Union[List[str], Set[str], str],
    experience_level: str,
    db_path: Optional[Union[str, Path]] = None
) -> Dict[str, Any]:
    """Creates a new user profile with parameterized SQL and returns the profile dict."""
    init_db(db_path)
    validate_profile_data(full_name, career_goal, experience_level)

    serialized_skills = _serialize_skills(current_skills)
    now_iso = datetime.now(timezone.utc).isoformat()

    try:
        with managed_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO user_profiles
                (full_name, career_goal, current_skills, experience_level, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    full_name.strip(),
                    career_goal.strip(),
                    serialized_skills,
                    experience_level.strip(),
                    now_iso,
                    now_iso
                )
            )
            user_id = cursor.lastrowid

        return get_profile(user_id=user_id, db_path=db_path)  # type: ignore[return-value]
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to create profile for '{full_name}': {e}") from e


def update_profile(
    user_id: int,
    full_name: str,
    career_goal: str,
    current_skills: Union[List[str], Set[str], str],
    experience_level: str,
    db_path: Optional[Union[str, Path]] = None
) -> Dict[str, Any]:
    """Updates an existing profile and refreshes updated_at timestamp."""
    init_db(db_path)
    validate_profile_data(full_name, career_goal, experience_level)

    serialized_skills = _serialize_skills(current_skills)
    now_iso = datetime.now(timezone.utc).isoformat()

    try:
        with managed_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE user_profiles
                SET full_name = ?,
                    career_goal = ?,
                    current_skills = ?,
                    experience_level = ?,
                    updated_at = ?
                WHERE user_id = ?;
                """,
                (
                    full_name.strip(),
                    career_goal.strip(),
                    serialized_skills,
                    experience_level.strip(),
                    now_iso,
                    user_id
                )
            )
            if cursor.rowcount == 0:
                raise DatabaseError(f"User profile with user_id={user_id} not found.")

        return get_profile(user_id=user_id, db_path=db_path)  # type: ignore[return-value]
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to update profile for user_id={user_id}: {e}") from e


def save_profile(
    full_name: str,
    career_goal: str,
    current_skills: Union[List[str], Set[str], str],
    experience_level: str,
    user_id: Optional[int] = None,
    db_path: Optional[Union[str, Path]] = None
) -> Dict[str, Any]:
    """
    Saves profile: updates existing if user_id or latest profile exists,
    otherwise creates a new profile.
    """
    init_db(db_path)
    if user_id is not None:
        existing = get_profile(user_id=user_id, db_path=db_path)
        if existing:
            return update_profile(
                user_id=user_id,
                full_name=full_name,
                career_goal=career_goal,
                current_skills=current_skills,
                experience_level=experience_level,
                db_path=db_path
            )

    latest = get_profile(db_path=db_path)
    if latest:
        return update_profile(
            user_id=latest["user_id"],
            full_name=full_name,
            career_goal=career_goal,
            current_skills=current_skills,
            experience_level=experience_level,
            db_path=db_path
        )

    return create_profile(
        full_name=full_name,
        career_goal=career_goal,
        current_skills=current_skills,
        experience_level=experience_level,
        db_path=db_path
    )


def get_profile(
    user_id: Optional[int] = None,
    db_path: Optional[Union[str, Path]] = None
) -> Optional[Dict[str, Any]]:
    """
    Retrieves a user profile. If user_id is None, returns the most recent profile.
    Returns None if no profile exists.
    """
    init_db(db_path)
    try:
        with managed_connection(db_path) as conn:
            cursor = conn.cursor()
            if user_id is not None:
                cursor.execute(
                    "SELECT * FROM user_profiles WHERE user_id = ? LIMIT 1;",
                    (user_id,)
                )
            else:
                cursor.execute(
                    "SELECT * FROM user_profiles ORDER BY user_id DESC LIMIT 1;"
                )
            row = cursor.fetchone()
            if row is None:
                return None
            return _format_profile_row(row)
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to retrieve profile: {e}") from e


# ---------------------------------------------------------------------------
# PROGRESS FUNCTIONALITY
# ---------------------------------------------------------------------------

def mark_course_complete(
    course_id: int,
    user_id: int = 1,
    db_path: Optional[Union[str, Path]] = None
) -> None:
    """Marks a course as completed for the given user, saving timestamp."""
    init_db(db_path)
    now_iso = datetime.now(timezone.utc).isoformat()
    try:
        with managed_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO learning_progress
                    (user_id, course_id, completion_status, completion_date, last_updated_date)
                VALUES (?, ?, 1, ?, ?)
                ON CONFLICT(user_id, course_id) DO UPDATE SET
                    completion_status = 1,
                    completion_date = excluded.completion_date,
                    last_updated_date = excluded.last_updated_date;
                """,
                (user_id, int(course_id), now_iso, now_iso)
            )
    except sqlite3.Error as e:
        raise DatabaseError(
            f"Failed to mark course {course_id} complete for user {user_id}: {e}"
        ) from e


def mark_course_incomplete(
    course_id: int,
    user_id: int = 1,
    db_path: Optional[Union[str, Path]] = None
) -> None:
    """Marks a course as incomplete for the given user."""
    init_db(db_path)
    now_iso = datetime.now(timezone.utc).isoformat()
    try:
        with managed_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO learning_progress
                    (user_id, course_id, completion_status, completion_date, last_updated_date)
                VALUES (?, ?, 0, NULL, ?)
                ON CONFLICT(user_id, course_id) DO UPDATE SET
                    completion_status = 0,
                    completion_date = NULL,
                    last_updated_date = excluded.last_updated_date;
                """,
                (user_id, int(course_id), now_iso)
            )
    except sqlite3.Error as e:
        raise DatabaseError(
            f"Failed to mark course {course_id} incomplete for user {user_id}: {e}"
        ) from e


def get_completed_courses(
    user_id: int = 1,
    db_path: Optional[Union[str, Path]] = None
) -> Set[int]:
    """Returns a set of completed course IDs for the user."""
    init_db(db_path)
    try:
        with managed_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT course_id FROM learning_progress
                WHERE user_id = ? AND completion_status = 1;
                """,
                (user_id,)
            )
            rows = cursor.fetchall()
            return {int(row["course_id"]) for row in rows}
    except sqlite3.Error as e:
        raise DatabaseError(
            f"Failed to retrieve completed courses for user {user_id}: {e}"
        ) from e


def get_course_progress(
    user_id: int = 1,
    db_path: Optional[Union[str, Path]] = None
) -> Dict[int, Dict[str, Any]]:
    """Returns full progress mapping for all tracked courses of the user."""
    init_db(db_path)
    try:
        with managed_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT course_id, completion_status, completion_date, last_updated_date
                FROM learning_progress
                WHERE user_id = ?;
                """,
                (user_id,)
            )
            rows = cursor.fetchall()
            return {
                int(row["course_id"]): {
                    "completed": bool(row["completion_status"]),
                    "completion_date": row["completion_date"],
                    "last_updated_date": row["last_updated_date"]
                }
                for row in rows
            }
    except sqlite3.Error as e:
        raise DatabaseError(
            f"Failed to retrieve course progress for user {user_id}: {e}"
        ) from e


def calculate_progress(
    learning_path: Union[pd.DataFrame, List[Dict[str, Any]]],
    user_id: int = 1,
    db_path: Optional[Union[str, Path]] = None
) -> Dict[str, Any]:
    """
    Calculates completed and remaining course counts, completion percentage,
    and remaining learning hours based on database progress.
    """
    completed_ids = get_completed_courses(user_id=user_id, db_path=db_path)

    if isinstance(learning_path, pd.DataFrame):
        records = learning_path.to_dict(orient="records")
    else:
        records = list(learning_path)

    total_courses = len(records)
    if total_courses == 0:
        return {
            "total_courses": 0,
            "completed_courses": 0,
            "remaining_courses": 0,
            "completion_percentage": 0.0,
            "total_duration": 0.0,
            "completed_hours": 0.0,
            "remaining_hours": 0.0,
            "completed_course_ids": set()
        }

    completed_courses = 0
    total_duration = 0.0
    completed_hours = 0.0

    for course in records:
        cid = int(course.get("course_id", 0))
        duration = float(course.get("duration_hours", 0.0))
        total_duration += duration

        if cid in completed_ids:
            completed_courses += 1
            completed_hours += duration

    remaining_courses = total_courses - completed_courses
    remaining_hours = max(0.0, total_duration - completed_hours)
    completion_percentage = round((completed_courses / total_courses) * 100, 1)

    return {
        "total_courses": total_courses,
        "completed_courses": completed_courses,
        "remaining_courses": remaining_courses,
        "completion_percentage": completion_percentage,
        "total_duration": round(total_duration, 1),
        "completed_hours": round(completed_hours, 1),
        "remaining_hours": round(remaining_hours, 1),
        "completed_course_ids": completed_ids
    }
