# Portable Development Loop for Antigravity

This repository implements the **Agentic Architecture Pattern (Portable Development Loop)** for Google Antigravity and other agentic development environments.

## What is this?
When working with AI coding agents, the goal is not to exhaust human context by reviewing massive amounts of generated code. Instead, we aim to stabilize the generation and review tempo—balancing speed and quality without overwhelming the developer.

To achieve this, we do not start with heavy, upfront speculation. We rely on an iterative loop:
`Build a small working piece` → `Verify behavior locally` → `Expand with higher resolution`.

## Core Philosophy
1. **Test is Specification**: The truth lies in observable behavior, not in lengthy documentation. By anchoring our regression suite to the CLI contract (inputs, outputs, and exit codes), we define exactly "what must not break."
2. **Start Small, Expand Later**: Do not aim for perfect architecture initially. Pass the minimal end-to-end path first, and abstract or decouple only when complexity demands it.
3. **Tracer Bullet First**: When uncertain, build a "tracer bullet"—the smallest viable technical path. Having something that actually runs uncovers hidden design flaws, integration gaps, and UX issues faster than any diagram.
4. **Investigate Before Modifying**: Never write code based on assumptions. Gather facts, separate them from hypotheses, and decide your next move.

## Workflow Structure
The commands in this repository are explicitly designed around **Human Inspection** breakpoints. Agents should never complete an entire feature in one massive run; they must pause and present verifiable artifacts at specific milestones.

### The 3 Core Commands

#### 1. `/mission` (Phase 1: Prove Viability)
**Purpose**: Determine the direction and build the smallest working implementation (Tracer Bullet).
- Investigates the current state.
- Defines the observable CLI Contract.
- Builds a minimum viable end-to-end path.
- **[STOP]** Waits for human inspection of the tracer bullet.

#### 2. `/expand` (Phase 2: Flesh Out Implementation)
**Purpose**: Expand the tracer bullet into robust, production-ready code using Test-Driven Development (TDD).
- Expands coverage via Examples → Contracts → Invariants.
- Iterates through a self-review and fix loop.
- **[STOP]** Waits for human inspection of tests and quality.

#### 3. `/drift-check` (Phase 3: Architectural Governance)
**Purpose**: Ensure the new code has not violated the architectural guardrails.
- Verifies 5 key constraints: dependency direction, cyclic dependencies, boundaries, contracts, and technology choices.
- Classifies the drift as `NO_CHANGE`, `MINOR_UPDATE`, or `STRUCTURAL_ADJUST`.
- If a structural adjust is needed, it drafts an Architecture Decision Record (ADR).
- **[STOP]** Waits for human inspection and approval of the drift classification or evolution proposal.

---

## Technical Stack & Compatibility
This framework optimizes for:
- **Modifiability & Observability**
- **Cognitive Scalability** (Keeping context demands low)
- **Governability** (Preventing AI-driven architectural decay)

While optimized for Antigravity's native primitives (Rules, Workflows, Skills), the concepts can be ported to other agentic tools.

---

## Installation (How to Add to Any Project)

This repository serves as the central manager for your Antigravity instructions. You can install the `.agent` configuration into any target project using the provided `Makefile`.

### Step 1: Install via Make
Run the following command from the root of this repository, specifying your target project's path as `DEST`:
```bash
make install DEST=/path/to/your/target/project
```

### Step 2: Ensure Directory Structure
Your target project should now have the following structure at its root:
```text
your-project/
├── .agent/
│   ├── rules.md
│   ├── workflows/
│   │   ├── mission.md
│   │   ├── expand.md
│   │   └── drift-check.md
│   └── skills/
│       ├── investigation/SKILL.md
│       ├── cli-contract/SKILL.md
│       ├── tracer-bullet/SKILL.md
│       ├── test-first/SKILL.md
│       └── architecture/SKILL.md
└── (your project files...)
```

### Step 3: Start Antigravity
Open the target project in Google Antigravity. The agent will automatically detect the `.agent/rules.md` file as its core system prompt.

You can now start development by using the slash commands in the chat:
- `/mission Create a new login feature`
- `/expand`
- `/drift-check`
