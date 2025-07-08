# PR Review Analysis & Commit Planning

You are analyzing a PR's review comments to create an actionable commit plan.

## Strategy: Think Step-by-Step

<planning>
Before analyzing, I will:
1. Understand what the PR originally intended to solve
2. Map each review comment to its impact and required effort
3. Identify dependencies between fixes
4. Group related changes into atomic commits
5. Present prioritized options for the user to choose
</planning>

## Analysis Framework

### Step 1: Context Gathering
- Read PR description, linked issues, and diff
- Understand codebase patterns and standards
- Map reviewer personas to their comments

### Step 2: Triage Matrix

For each comment, determine:
```
Severity: CRITICAL (security/legal) > HIGH (architecture/bugs) > MEDIUM > LOW
Effort: TRIVIAL (<30m) | SMALL (<2h) | MEDIUM (2-4h) | LARGE (>4h)
Priority: P1 (CRITICAL) > P2 (HIGH+blocking) > P3 (HIGH) > P4 (MEDIUM) > P5 (LOW)
```

### Step 3: Dependency Analysis
- Which fixes block others?
- Which can be parallelized?
- What's the optimal sequence?

### Step 4: Output Structure

```markdown
## PR: [Title] - Solving: [Original Intent]

**Review Stats**: X comments → Y must-fix → ~Z hours

### Changes by Priority

□ [1] **[Persona]** - [Issue] at [File:Line]
   Fix: [Specific solution]
   Effort: [TIME] | Commit: `fix(scope): description`

[Group by P1, P2, P3...]

### Commit Plan
1. `fix(security): ...` → Fixes #1
2. `refactor(core): ...` → Fixes #3, #4
[Ordered by dependencies]

### Dependencies
- #3 blocks #5
- #1, #2 parallel

### Options
A: Critical only (#1, #2) - 3h
B: Critical+High (#1-5) - 8h  
C: All code (#1-6) - 10h
D: Everything (#1-7) - 11h
E: Custom (specify)

Recommended: [Letter] - [Reasoning]

---

## Which changes should I address?

Your choice (A-E, numbers, "all", "critical"): _
```

## Execution Notes

- Start with understanding the PR's purpose
- Be concise: one-line descriptions, clear fixes
- Group commits logically (security → architecture → features → tests → docs)
- Always end by asking for user's choice