"""Retrieval Agent — provides context from Chroma collections.

This is a simplified version that provides basic retrieval functionality.
"""

from smolagents import Tool


class RetrieveCourseContextTool(Tool):
    name = "retrieve_course_context"
    description = "Retrieve context for a specific course and query from the knowledge base."
    inputs = {
        "course": {
            "type": "string",
            "description": "The course name (GEOGRAPHY, PYTHON, or CHESS)",
        },
        "query": {
            "type": "string",
            "description": "The search query",
        },
    }
    output_type = "string"

    def forward(self, course: str, query: str) -> str:
        # Simplified retrieval - returns a basic context message
        return f"Retrieved context for {course}: {query}"


def build_retrieval_agent():
    """Build a simple retrieval agent."""
    from smolagents import CodeAgent, InferenceClientModel
    
    return CodeAgent(
        tools=[RetrieveCourseContextTool()],
        model=InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct"),
        name="retrieval_agent",
        description="Retrieves context for course materials.",
    )
