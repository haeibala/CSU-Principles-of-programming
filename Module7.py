"""
Course Information Lookup

Reads a course number from stdin and prints room number, instructor,
and meeting time. Validates the course catalog for consistency across
three dictionaries before serving queries.

Robust features:
- Input normalization and validation
- Data integrity check across dictionaries
- Graceful handling of EOF, KeyboardInterrupt, and unexpected errors
- Clear user messaging
"""

from dataclasses import dataclass
from typing import Dict, Mapping


# --- Catalog dictionaries (source of truth) ---

COURSE_TO_ROOM: Dict[str, str] = {
    "CSC101": "3004",
    "CSC102": "4501",
    "CSC103": "6755",
    "NET110": "1244",
    "COM241": "1411",
}

COURSE_TO_INSTRUCTOR: Dict[str, str] = {
    "CSC101": "Haynes",
    "CSC102": "Alvarado",
    "CSC103": "Rich",
    "NET110": "Burke",
    "COM241": "Lee",
}

COURSE_TO_TIME: Dict[str, str] = {
    "CSC101": "8:00 a.m.",
    "CSC102": "9:00 a.m.",
    "CSC103": "10:00 a.m.",
    "NET110": "11:00 a.m.",
    "COM241": "1:00 p.m.",
}


# --- Data structures ---

@dataclass(frozen=True)
class CourseInfo:
    """Aggregate of all attributes for a single course."""
    room: str
    instructor: str
    time: str


# --- Helpers ---

class CatalogIntegrityError(RuntimeError):
    """Raised when the three course dictionaries have mismatched keys."""


def validate_catalog(
    rooms: Mapping[str, str],
    instructors: Mapping[str, str],
    times: Mapping[str, str],
) -> None:
    """
    Ensure all dictionaries describe the same set of courses.
    Raises CatalogIntegrityError with a helpful message if not aligned.
    """
    k_rooms = set(rooms.keys())
    k_instructors = set(instructors.keys())
    k_times = set(times.keys())

    if not (k_rooms == k_instructors == k_times):
        missing_in_rooms = (k_instructors | k_times) - k_rooms
        missing_in_instructors = (k_rooms | k_times) - k_instructors
        missing_in_times = (k_rooms | k_instructors) - k_times
        details = []
        if missing_in_rooms:
            details.append(f"Missing in rooms: {sorted(missing_in_rooms)}")
        if missing_in_instructors:
            details.append(f"Missing in instructors: {sorted(missing_in_instructors)}")
        if missing_in_times:
            details.append(f"Missing in times: {sorted(missing_in_times)}")
        raise CatalogIntegrityError(
            "Catalog dictionaries are not aligned. " + " ".join(details)
        )


def build_index(
    rooms: Mapping[str, str],
    instructors: Mapping[str, str],
    times: Mapping[str, str],
) -> Dict[str, CourseInfo]:
    """
    Build a unified index mapping course code to CourseInfo.
    Validates the three dictionaries for key consistency first.
    """
    validate_catalog(rooms, instructors, times)
    index: Dict[str, CourseInfo] = {}
    for code in rooms:
        index[code] = CourseInfo(
            room=rooms[code],
            instructor=instructors[code],
            time=times[code],
        )
    return index


def normalize_course_code(code: str) -> str:
    """Trim and uppercase a user supplied course code."""
    return code.strip().upper()


def get_course_info(code: str, index: Mapping[str, CourseInfo]) -> CourseInfo:
    """
    Return CourseInfo for a normalized course code.
    Raises KeyError if the course does not exist.
    """
    norm = normalize_course_code(code)
    return index[norm]  # KeyError is intentional for clean error flow


# --- CLI ---

def main() -> None:
    try:
        index = build_index(COURSE_TO_ROOM, COURSE_TO_INSTRUCTOR, COURSE_TO_TIME)
    except CatalogIntegrityError as e:
        print("Configuration error. Please contact the instructor.")
        print(str(e))
        return
    except Exception as e:
        # Catch any unexpected configuration error
        print("Unexpected error during setup.")
        print(f"{type(e).__name__}: {e}")
        return

    print("Course Lookup. Enter a course number like CSC101.")
    print('Type "Q" to quit.')

    while True:
        try:
            raw = input("> ")
        except EOFError:
            print()  # Move to a new line for clean exit
            print("Goodbye.")
            break
        except KeyboardInterrupt:
            print()  # New line after Ctrl+C
            print("Goodbye.")
            break
        except Exception as e:
            print("Input error. Please try again.")
            print(f"{type(e).__name__}: {e}")
            continue

        if raw is None:
            print("Please enter a course number.")
            continue

        code = normalize_course_code(raw)
        if code == "" or code == "Q":
            print("Goodbye.")
            break

        try:
            info = get_course_info(code, index)
        except KeyError:
            print("Course not found. Available courses:")
            print(", ".join(sorted(index.keys())))
            continue
        except Exception as e:
            print("Lookup failed. Please try again.")
            print(f"{type(e).__name__}: {e}")
            continue

        print(f"Course: {code}")
        print(f"Room Number: {info.room}")
        print(f"Instructor: {info.instructor}")
        print(f"Meeting Time: {info.time}")


if __name__ == "__main__":
    main()
