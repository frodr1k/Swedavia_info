"""Key rotation management for Swedavia Flight Information."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import logging
from typing import Final

_LOGGER = logging.getLogger(__name__)

# Key rotation schedule (based on Swedavia's 6-month rotation)
# Primary key rotations (April)
PRIMARY_KEY_ROTATIONS: Final[list[str]] = [
    "2025-04-09",
    "2026-04-08",
    "2027-04-07",
    "2028-04-12",
    "2029-04-11",
    "2030-04-10",
]

# Secondary key rotations (October)
SECONDARY_KEY_ROTATIONS: Final[list[str]] = [
    "2025-10-03",
    "2026-10-02",
    "2027-10-01",
    "2028-10-06",
    "2029-10-05",
    "2030-10-03",
]

# Warning threshold (days before rotation)
WARNING_DAYS_BEFORE: Final[int] = 3


def get_next_rotation_date(key_type: str = "primary") -> datetime | None:
    """Get the next rotation date for the specified key type.
    
    Args:
        key_type: Either "primary" or "secondary"
        
    Returns:
        Next rotation date or None if no future rotation found
    """
    now = datetime.now(timezone.utc)
    rotations = PRIMARY_KEY_ROTATIONS if key_type == "primary" else SECONDARY_KEY_ROTATIONS
    
    for rotation_str in rotations:
        rotation_date = datetime.strptime(rotation_str, "%Y-%m-%d").replace(
            tzinfo=timezone.utc
        )
        if rotation_date > now:
            return rotation_date
    
    return None


def days_until_rotation(key_type: str = "primary") -> int | None:
    """Get number of days until next key rotation.
    
    Args:
        key_type: Either "primary" or "secondary"
        
    Returns:
        Number of days until rotation or None if no future rotation
    """
    next_rotation = get_next_rotation_date(key_type)
    if next_rotation is None:
        return None
    
    now = datetime.now(timezone.utc)
    delta = next_rotation - now
    return delta.days


def should_warn_about_rotation(key_type: str = "primary") -> bool:
    """Check if a warning should be issued about upcoming key rotation.
    
    Args:
        key_type: Either "primary" or "secondary"
        
    Returns:
        True if warning should be issued (within 3 days of rotation)
    """
    days = days_until_rotation(key_type)
    if days is None:
        return False
    
    return 0 <= days <= WARNING_DAYS_BEFORE


def get_rotation_warning_message(key_type: str = "primary") -> str:
    """Get warning message for upcoming key rotation.
    
    Args:
        key_type: Either "primary" or "secondary"
        
    Returns:
        Warning message string
    """
    days = days_until_rotation(key_type)
    next_rotation = get_next_rotation_date(key_type)
    
    if days is None or next_rotation is None:
        return ""
    
    key_name = "primary" if key_type == "primary" else "secondary"
    
    if days == 0:
        return (
            f"⚠️ IMPORTANT: Your {key_name} API key rotates TODAY! "
            f"Update your key from https://apideveloper.swedavia.se/ "
            f"to avoid service interruption."
        )
    elif days == 1:
        return (
            f"⚠️ WARNING: Your {key_name} API key rotates TOMORROW ({next_rotation.strftime('%Y-%m-%d')})! "
            f"Update your key from https://apideveloper.swedavia.se/"
        )
    else:
        return (
            f"ℹ️ Reminder: Your {key_name} API key will rotate in {days} days "
            f"({next_rotation.strftime('%Y-%m-%d')}). "
            f"Prepare by getting new key from https://apideveloper.swedavia.se/"
        )


def get_all_rotation_info() -> dict[str, any]:
    """Get complete rotation information for both keys.
    
    Returns:
        Dictionary with rotation information
    """
    primary_days = days_until_rotation("primary")
    secondary_days = days_until_rotation("secondary")
    primary_date = get_next_rotation_date("primary")
    secondary_date = get_next_rotation_date("secondary")
    
    return {
        "primary_key": {
            "next_rotation": primary_date.isoformat() if primary_date else None,
            "days_until_rotation": primary_days,
            "warning_active": should_warn_about_rotation("primary"),
            "warning_message": get_rotation_warning_message("primary") if should_warn_about_rotation("primary") else None,
        },
        "secondary_key": {
            "next_rotation": secondary_date.isoformat() if secondary_date else None,
            "days_until_rotation": secondary_days,
            "warning_active": should_warn_about_rotation("secondary"),
            "warning_message": get_rotation_warning_message("secondary") if should_warn_about_rotation("secondary") else None,
        },
    }
