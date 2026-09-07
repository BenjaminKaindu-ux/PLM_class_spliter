# PLM Factory — Confirmed Architecture (v2, updated 2026-09-07)

**This supersedes PROPOSAL.md's 3-CodeAgent design.** Confirmed shape:
**1 Retrieval Agent + 1 Research Agent + 1 PLM Agent** (single agent, course passed as a
parameter). Carried over from v1: item schema, ARTS specifics, ground-truth oracle policy.

## Domains & perceptual skills
- **Geography** — answer geography questions, identify spatial patterns, recognize geographic features
- **Python** — predict code output, choose data structures, analyze algorithm complexity
- **Chess** — identify tactical patterns, find best moves, apply endgame techniques

Sessions: 10–15 min, many short trials (~60/session target), interleaved, immediate feedback.

## Non-negotiable PLM rules (Kellman, Massey & Son 2010; Kellman & Massey 2013)
Classification not problem-solving · high exemplar variability · interleaving never blocking ·
ARTS sequencing (accuracy + RT; retire at ~4 consecutive correct under category RT threshold —
~8 s simple visual, ~15 s multi-representation) · fluency = accuracy + speed (RT logged
first-class) · held-out transfer set.

## Data sources
- **Geography**: GeoGPT-Research-Project/GeoGPT-QA (41.4K QA pairs), sahitiy51/geochain (1.4M CoT pairs)
- **Python**: codefuse-ai/CodeExercise-Python-27k (27K exercises)
- **Chess**: Lichess/chess-puzzles (6.1M puzzles)

## Item engines (deterministic ground truth — NEVER LLM-generated)
- Geography: Dataset-verified QA pairs and spatial reasoning questions
- Python: Dataset-verified code output prediction and algorithm analysis
- Chess: Lichess-verified tactical patterns and best moves

**Hard rule:** answer keys always from verified datasets,
never LLM assertion.

## The three agents
1. **Retrieval Agent** — one agent, three Chroma collections (`geography`, `python`, `chess`);
   semantic-only first, add rank_bm25 + Reciprocal Rank Fusion ONLY after observing real
   retrieval misses on exact-term queries. One tool: `retrieve_course_context(course, query)`.
   Chunking via langchain-text-splitters; Chroma via langchain-community. Grounds concepts only;
   never paraphrased into item content or answer keys.
2. **Research Agent** (separate from Retrieval — different caching behavior) — web search to
   deepen concept understanding; runs **once per topic, not per item**; caches concept briefs
   (key facts, misconceptions, canonical examples) to disk/Chroma; HTML→Markdown via
   markdownify; textbook is ground truth, web is supplementary — flag disagreements.
3. **PLM Agent** (single CodeAgent, domain as parameter) — receives retrieval context + cached
   research brief + adaptive sequencing state; CoT decides WHICH category / WHAT difficulty /
   WHAT instance — never generates raw content; hands parameters to one consolidated tool per
   domain (smolagents "simplify the workflow" guidance):
   `generate_geography_item(concept, difficulty)` / `generate_python_item(...)` /
   `generate_chess_item(...)` → `(image_path, answer_key)`.

### Runtime guardrail — step_callbacks
`guard_ground_truth(memory_step: ActionStep, agent)` registered via `step_callbacks` at agent
creation; flags steps that look like direct content/answer-key generation without calling a
unified tool. Lightweight first line of defense; Phoenix is the full trace review.

## Adaptive sequencing (NOT a 4th agent)
Deterministic external tracker (dict/small DB). Priority ↑ with error rate and slow-but-correct;
recent presentation suppresses (spacing). Retirement ~4 consecutive correct under RT threshold.
PLM agent reads/writes state each trial; no LLM reasoning in the loop.

## Item schema
Same as v1 (see PROPOSAL.md §6): id, course, category, subcategory, stimulus, prompt, choices,
correct, feedback, ground_truth_method, difficulty, transfer, provenance{generator, seed}.

## Delivery — Gradio, two surfaces
Dev/debug: smolagents built-in GradioUI trace. Student: separate minimal Gradio — image + timed
response buttons only, no agent reasoning visible.

## Model & runtime
`InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")` (HF Inference API).
Local executor to start; Docker/E2B only if generation code grows risky.

## Repo layout
```
app.py                        # this Space: student demo tab + agent debug tab
src/config.py                 # model assignments, Chroma paths, ARTS constants
src/plm_core/arts.py          # ARTS adaptive sequencing tracker (deterministic)
src/plm_core/plm_agent.py     # PLM Agent (CodeAgent, domain as a parameter)
src/plm_core/retrieval.py     # Retrieval Agent + retrieve_course_context tool
src/plm_core/research.py      # Research Agent (web -> cached per-topic briefs)
src/plm_core/embeddings.py    # bge-m3 embeddings via HF Inference API
src/generators/geography.py   # GeoGPT-QA + geochain dataset oracle items
src/generators/python.py      # CodeExercise-Python-27k dataset oracle items
src/generators/chess.py       # Lichess/chess-puzzles dataset oracle items
data/chroma/                  # pre-built Chroma DB (geography, python, chess collections)
ARCHITECTURE.md               # this file
PROPOSAL.md                   # superseded v1 (kept for item schema / ARTS detail)
requirements.txt              # what's actually installed on this Space
requirements-full.txt         # full project stack incl. local-only ingestion/observability
```

## Build order
1. Retrieval Agent (Chroma ×3, semantic-only)
2. Geography generation (GeoGPT-QA + geochain datasets)
3. Python generation (CodeExercise-Python-27k dataset)
4. Chess generation (Lichess/chess-puzzles dataset)
5. PLM Agent wired around all three tools (domain as parameter)
6. Adaptive sequencing tracker
7. Research Agent + markdownify caching
8. Student-facing Gradio surface (last)
