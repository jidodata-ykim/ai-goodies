---
description: Instructions for analyzing GitHub issues and creating comprehensive implementation specifications with actionable plans
globs: ""
---

# GitHub Issue Analysis and Implementation Planning

You are an AI assistant tasked with analyzing GitHub issues and creating detailed implementation specifications. Your goal is to thoroughly understand the issue, research the codebase, and produce a comprehensive plan that guides the implementation process.

First, you will be given an issue number or issue URL. Here it is:

<issue_reference> #$ARGUMENTS </issue_reference>

Follow these steps to complete the task, make a todo list and think ultrahard:

### 1. Parse arguments and fetch issue:
   - Extract issue number from $ARGUMENTS (can be just number or full GitHub URL)
   - Use `gh issue view <issue-number>` to get complete issue details
   - Parse issue title, description, labels, and any comments
   - Note any mentioned files, error messages, or specific requirements

### 2. Research the codebase:
   - Search for files mentioned in the issue
   - Identify related components and modules
   - Review existing patterns and conventions in the project
   - Check for similar implementations or related features
   - Look for reusable utilities or helpers
   - Understand the project structure and architecture

### 3. Analyze requirements:
   - Break down the issue into specific technical requirements
   - Identify edge cases and potential complications
   - Consider performance, security, and maintainability implications
   - Determine if this is a bug fix, feature, or improvement
   - Assess the scope and complexity of the change

### 4. Present initial findings:
   - Summarize your understanding of the issue
   - List key findings from codebase research
   - Identify any ambiguities or questions
   - Present this analysis in <initial_findings> tags

### 5. Create implementation specification:
   Generate a comprehensive technical specification with these sections:

   #### Issue Summary
   - Brief overview of the issue and its impact
   - Link to original issue

   #### Problem Statement
   - Clear definition of what needs to be solved
   - Current behavior vs expected behavior
   - Root cause analysis if applicable

   #### Technical Approach
   - High-level solution approach
   - Architecture decisions and rationale
   - Design patterns to be used
   - Integration points with existing code

   #### Implementation Plan
   - Step-by-step breakdown of implementation tasks
   - Ordered list of changes to make
   - Dependencies between tasks
   - Estimated complexity for each step

   #### Test Plan
   - Testing strategy (unit, integration, e2e)
   - Specific test cases to write
   - Edge cases to cover
   - How to verify the fix works

   #### Files to Modify
   - List of existing files that need changes
   - Brief description of changes for each file
   - Potential impact on other parts of the system

   #### Files to Create
   - New files that need to be created
   - Purpose and structure of each new file
   - Where they fit in the project structure

   #### Existing Utilities to Leverage
   - Project utilities/helpers that can be reused
   - External libraries already in use
   - Patterns from similar features

   #### Success Criteria
   - Measurable criteria for completion
   - How to verify the issue is resolved
   - Performance benchmarks if applicable

   #### Out of Scope
   - What won't be addressed in this implementation
   - Related issues that should be handled separately
   - Future improvements to consider

### 6. Implementation guidelines:
   - Follow strict TDD principles - write tests first
   - Apply KISS (Keep It Simple, Stupid) approach
   - Enforce 300-line file limit where applicable
   - Use descriptive variable and function names
   - Add comprehensive comments for complex logic
   - Follow project's coding standards and conventions

### 7. Final output:
   - Present the complete implementation specification in <implementation_spec> tags
   - Provide time estimates for implementation if possible

Remember to think carefully about the issue and consider all aspects of the implementation. The specification should be detailed enough that another developer could implement the solution without ambiguity.

## Example Analysis Output Structure:

```markdown
# Implementation Specification for Issue #123

## Issue Summary
[Brief overview with link to issue]

## Problem Statement
[Clear problem definition]

## Technical Approach
[Solution architecture]

## Implementation Plan
1. [First task]
2. [Second task]
...

## Test Plan
- [ ] Unit test for X
- [ ] Integration test for Y
...

## Files to Modify
- `src/components/Widget.js` - Add error handling
- `src/utils/validation.js` - Update validation logic
...

## Files to Create
- `src/components/Widget.test.js` - Unit tests
- `src/utils/errorHandler.js` - Centralized error handling
...

## Existing Utilities to Leverage
- `src/utils/logger.js` - For error logging
- `src/helpers/format.js` - For data formatting
...

## Success Criteria
- [ ] Error no longer occurs in scenario X
- [ ] All tests pass
- [ ] No regression in existing functionality
...

## Out of Scope
- Performance optimizations (tracked in issue #456)
- UI improvements (separate PR)
...
```

Your analysis should be thorough, actionable, and guide the implementation process from start to finish.