"""ARTS (Adaptive Response Time Sequencing) tracker for PLM Factory.

Implements the adaptive sequencing algorithm from:
- Kellman, Massey & Son (2010), Topics in Cognitive Science
- Kellman & Massey (2013)

Tracks accuracy and response time per category, retiring categories after
4 consecutive fast-and-correct answers.
"""

import time
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CategoryState:
    """State for a single category in the ARTS tracker."""
    name: str
    rt_threshold_s: float = 10.0
    consecutive_correct: int = 0
    consecutive_correct_fast: int = 0
    total_trials: int = 0
    total_correct: int = 0
    total_time: float = 0.0
    retired: bool = False
    last_presentation: float = 0.0
    
    @property
    def accuracy(self) -> float:
        """Return accuracy as a fraction (0-1)."""
        if self.total_trials == 0:
            return 0.0
        return self.total_correct / self.total_trials
    
    @property
    def mean_rt(self) -> float:
        """Return mean response time in seconds."""
        if self.total_correct == 0:
            return 0.0
        return self.total_time / self.total_correct


class ArtsTracker:
    """Adaptive Response Time Sequencing tracker.
    
    Manages multiple categories and selects the next category to present
    based on error rate, response time, and spacing (recency suppression).
    """
    
    RETIREMENT_THRESHOLD = 4  # consecutive correct under RT threshold to retire
    
    def __init__(self, categories: List[CategoryState]):
        """Initialize tracker with a list of CategoryState objects."""
        self.categories = {c.name: c for c in categories}
        self.trial = 0
        self.session_start = time.time()
    
    def all_retired(self) -> bool:
        """Check if all categories have been retired."""
        return all(c.retired for c in self.categories.values())
    
    def next_category(self) -> str:
        """Select the next category to present using ARTS priority.
        
        Priority is increased by:
        - High error rate (lower accuracy)
        - Slow but correct responses (high RT but correct)
        - Recency suppression (recently presented categories have lower priority)
        
        Returns the name of the selected category.
        """
        now = time.time()
        best_cat = None
        best_score = -1
        
        for name, cat in self.categories.items():
            if cat.retired:
                continue
            
            # Base score: inverse of accuracy (lower accuracy = higher priority)
            accuracy_score = 1.0 - cat.accuracy
            
            # RT penalty: slower correct responses get higher priority
            rt_score = 0.0
            if cat.mean_rt > 0:
                rt_score = min(cat.mean_rt / cat.rt_threshold_s, 2.0) / 2.0
            
            # Recency penalty: recently presented categories get lower priority
            recency_penalty = 0.0
            if cat.last_presentation > 0:
                time_since = now - cat.last_presentation
                # Suppress for 30 seconds after presentation
                if time_since < 30:
                    recency_penalty = (30 - time_since) / 30
            
            # Combine scores
            score = accuracy_score + rt_score * 0.5 - recency_penalty
            
            if score > best_score:
                best_score = score
                best_cat = name
        
        # If all categories are retired or no category found, pick first non-retired
        if best_cat is None:
            for name, cat in self.categories.items():
                if not cat.retired:
                    best_cat = name
                    break
        
        return best_cat
    
    def record(self, category: str, correct: bool, rt: float):
        """Record a response for a category.
        
        Args:
            category: Name of the category
            correct: Whether the response was correct
            rt: Response time in seconds
        """
        if category not in self.categories:
            raise ValueError(f"Unknown category: {category}")
        
        cat = self.categories[category]
        cat.total_trials += 1
        cat.last_presentation = time.time()
        
        if correct:
            cat.total_correct += 1
            cat.total_time += rt
            
            # Check if fast enough
            if rt < cat.rt_threshold_s:
                cat.consecutive_correct_fast += 1
                cat.consecutive_correct += 1
                
                # Check for retirement
                if cat.consecutive_correct_fast >= self.RETIREMENT_THRESHOLD:
                    cat.retired = True
            else:
                # Correct but too slow - reset streak
                cat.consecutive_correct_fast = 0
                cat.consecutive_correct += 1
        else:
            # Incorrect - reset all streaks
            cat.consecutive_correct = 0
            cat.consecutive_correct_fast = 0
        
        self.trial += 1
    
    def summary(self) -> List[List]:
        """Return a summary table of all categories.
        
        Returns a list of lists suitable for gr.Dataframe:
        [Category, Accuracy, Mean RT, Consecutive Correct, Retired]
        """
        rows = []
        for name, cat in self.categories.items():
            rows.append([
                name,
                f"{cat.accuracy:.1%}",
                f"{cat.mean_rt:.1f}s" if cat.mean_rt > 0 else "N/A",
                f"{cat.consecutive_correct_fast}/{self.RETIREMENT_THRESHOLD}",
                "✓ Retired" if cat.retired else "Active"
            ])
        return rows
