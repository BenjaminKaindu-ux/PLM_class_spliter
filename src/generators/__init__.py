"""Generator modules for PLM Factory domains.

Each module provides:
- CATEGORIES: dict of category names to metadata (including rt_threshold_s)
- make_item(category_name, seed=None) -> dict with standardized item schema
"""

from . import geography, python, chess

__all__ = ["geography", "python", "chess"]
