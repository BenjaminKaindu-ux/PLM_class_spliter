"""PLM Agent — single CodeAgent, course passed as a parameter (ARCHITECTURE.md).

CoT decides WHICH category / WHAT difficulty / WHAT instance — it never generates raw
item content itself. Every item comes from one consolidated, course-specific tool that
wraps a deterministic generator (GeoGPT-QA/geochain for Geography, CodeExercise for
Python, Lichess for Chess). That tool call is the only sanctioned path to a persisted
image + answer key.
"""

import re
from pathlib import Path

from smolagents import CodeAgent, InferenceClientModel, Tool

from src.config import PLM_AGENT_MODEL
from src.generators import geography as geography_gen
from src.generators import python as python_gen
from src.generators import chess as chess_gen
from src.plm_core.retrieval import build_retrieval_agent

ITEMS_DIR = Path("data/items")


def _persist_item(item: dict, course: str) -> dict:
    """Save the stimulus image to disk and return everything else as the answer key —
    the (image_path, answer_key) contract from ARCHITECTURE.md, flattened into one dict.

    Includes `correct_answer` (the resolved choice text, not just the `correct` index):
    an agent doing its own `choices[correct]` arithmetic in generated code can get the
    off-by-one wrong even when the index itself came straight from the sanctioned tool —
    observed this exact failure in testing. Pre-resolving removes that arithmetic entirely."""
    out_dir = ITEMS_DIR / course
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Handle different stimulus types
    stimulus = item.get("stimulus", {})
    if stimulus.get("type") == "pil_image":
        img_path = out_dir / f"{item['id']}.png"
        stimulus["image"].save(img_path)
        item["stimulus"]["image_path"] = str(img_path)
    
    answer_key = {k: v for k, v in item.items() if k != "stimulus"}
    answer_key["correct_answer"] = item["choices"][item["correct"]]
    return answer_key


class GenerateGeographyItemTool(Tool):
    name = "generate_geography_item"
    description = (
        "The ONLY way to create a Geography item. Never assert geographic facts "
        "yourself — this uses verified datasets (GeoGPT-QA and geochain) and returns "
        "the dataset's own verified answer key. Read the returned `correct_answer` "
        "field directly (already resolved to the right choice text) — don't index "
        "`choices` with `correct` yourself, that's an easy off-by-one to get wrong."
    )
    inputs = {
        "concept": {
            "type": "string",
            "description": "One of: geo_qa, spatial_reasoning, landmark_recognition",
        },
        "difficulty": {
            "type": "integer",
            "description": "Difficulty tier, reserved for future use — pass 1",
            "nullable": True,
        },
    }
    output_type = "object"

    def forward(self, concept: str, difficulty: int = 1) -> dict:
        item = geography_gen.make_item(concept, difficulty=difficulty)
        return _persist_item(item, "GEOGRAPHY")


class GeneratePythonItemTool(Tool):
    name = "generate_python_item"
    description = (
        "The ONLY way to create a Python item. Never assert code output "
        "yourself — this uses verified datasets (CodeExercise-Python-27k) and returns "
        "the dataset's own verified answer key. Read the returned `correct_answer` "
        "field directly (already resolved to the right choice text) — don't index "
        "`choices` with `correct` yourself, that's an easy off-by-one to get wrong."
    )
    inputs = {
        "concept": {
            "type": "string",
            "description": "One of: basic_syntax, data_structures, algorithm_logic, code_output",
        },
        "difficulty": {
            "type": "integer",
            "description": "Difficulty tier, reserved for future use — pass 1",
            "nullable": True,
        },
    }
    output_type = "object"

    def forward(self, concept: str, difficulty: int = 1) -> dict:
        item = python_gen.make_item(concept, difficulty=difficulty)
        return _persist_item(item, "PYTHON")


class GenerateChessItemTool(Tool):
    name = "generate_chess_item"
    description = (
        "The ONLY way to create a Chess item. Never assert chess moves "
        "yourself — this uses verified datasets (Lichess/chess-puzzles) and returns "
        "the dataset's own verified answer key. Read the returned `correct_answer` "
        "field directly (already resolved to the right choice text) — don't index "
        "`choices` with `correct` yourself, that's an easy off-by-one to get wrong."
    )
    inputs = {
        "concept": {
            "type": "string",
            "description": "One of: tactical_pattern, best_move, endgame_technique, opening_principle",
        },
        "difficulty": {
            "type": "integer",
            "description": "Difficulty tier, reserved for future use — pass 1",
            "nullable": True,
        },
    }
    output_type = "object"

    def forward(self, concept: str, difficulty: int = 1) -> dict:
        item = chess_gen.make_item(concept, difficulty=difficulty)
        return _persist_item(item, "CHESS")


class GeographyActiveCategoriesTool(Tool):
    name = "geography_active_categories"
    description = "Lists which Geography categories are available for generation."
    inputs = {}
    output_type = "array"

    def forward(self) -> list[str]:
        return list(geography_gen.CATEGORIES.keys())


class PythonActiveCategoriesTool(Tool):
    name = "python_active_categories"
    description = "Lists which Python categories are available for generation."
    inputs = {}
    output_type = "array"

    def forward(self) -> list[str]:
        return list(python_gen.CATEGORIES.keys())


class ChessActiveCategoriesTool(Tool):
    name = "chess_active_categories"
    description = "Lists which Chess categories are available for generation."
    inputs = {}
    output_type = "array"

    def forward(self) -> list[str]:
        return list(chess_gen.CATEGORIES.keys())


_GUARDED_TOOLS = ("generate_geography_item", "generate_python_item", "generate_chess_item")
_ASSERTION_PATTERN = re.compile(r"\b(correct|answer_key|ground_truth|is_correct)\s*=")


def guard_ground_truth(memory_step, agent) -> None:
    """Lightweight first line of defense (ARCHITECTURE.md): flags steps whose code looks
    like it's asserting an answer key directly instead of calling a sanctioned generator
    tool. Not a hard block — Phoenix tracing is the full review, once wired."""
    code = getattr(memory_step, "code_action", None)
    if not code:
        return
    calls_sanctioned_tool = any(name in code for name in _GUARDED_TOOLS)
    if _ASSERTION_PATTERN.search(code) and not calls_sanctioned_tool:
        agent.logger.log(
            f"[guard_ground_truth] step {memory_step.step_number}: code assigns an "
            f"answer/ground-truth-looking variable without calling {_GUARDED_TOOLS} — "
            "verify this isn't an LLM-asserted answer key:\n" + code,
            level=1,  # LogLevel.INFO — visible but non-blocking
        )


def build_plm_agent(course: str) -> CodeAgent:
    """One PLM Agent, course passed as a parameter — not one agent per course."""
    if course == "GEOGRAPHY":
        tools = [GenerateGeographyItemTool(), GeographyActiveCategoriesTool()]
    elif course == "PYTHON":
        tools = [GeneratePythonItemTool(), PythonActiveCategoriesTool()]
    elif course == "CHESS":
        tools = [GenerateChessItemTool(), ChessActiveCategoriesTool()]
    else:
        raise ValueError(f"no generator wired for course {course!r}")

    return CodeAgent(
        tools=tools,
        model=InferenceClientModel(model_id=PLM_AGENT_MODEL),
        managed_agents=[build_retrieval_agent()],
        step_callbacks=[guard_ground_truth],
        name=f"plm_agent_{course.lower()}",
        description=f"Generates perceptual learning items for {course}.",
    )
