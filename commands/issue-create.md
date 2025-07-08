**Purpose**: Create an issue for a feature request, bug report, or improvement idea in a GitHub repository using AI advisors to ensure TDD and KISS principles are followed.

---
# GitHub Issue Creation with AI Advisors

You are an AI assistant tasked with creating **ULTRATHINK** well-structured GitHub issues for feature requests, bug reports, or improvement ideas. Your goal is to turn the provided feature description into a comprehensive GitHub issue that follows TDD (Test-Driven Development) and KISS (Keep It Simple, Stupid) principles.

**IMPORTANT**: You will leverage multiple AI advisors for deeper understanding:
- **Use Devin** (if available) to ask questions about the architecture of the repository
- **Use Zen** to consult with Gemini 2.5 about the codebase - you can provide up to 1 Million context window to ensure deep understanding of large repository sections
- **THINK**: Always use them as advisors, but do your own research and be skeptical about everything. Always double-check their responses.

First, you will be given a feature description and a repository URL:

<feature_description> #$ARGUMENTS </feature_description>

## TODO List - Complete Each Step Methodically

### 1. ✅ AI-Assisted Repository Analysis
**ULTRATHINK** before proceeding:
- [ ] Consult Devin about the repository architecture:
  - Ask about the overall structure and design patterns
  - Understand key modules and their interactions
  - Identify testing frameworks and conventions
- [ ] Use Zen/Gemini 2.5 for deep code analysis:
  - Feed large portions of the codebase for context
  - Ask about code patterns and conventions
  - Understand existing test structures
- [ ] Visit the repository URL and examine:
  - [ ] Repository structure and organization
  - [ ] Existing issues and their patterns
  - [ ] CONTRIBUTING.md, ISSUE_TEMPLATE.md files
  - [ ] Testing setup and CI/CD configuration
  - [ ] Code style guides and conventions

### 2. ✅ Research Best Practices with AI Validation
**THINK** critically about each practice:
- [ ] Search for current GitHub issue best practices
- [ ] Validate findings with AI advisors
- [ ] Look for TDD-specific issue templates
- [ ] Find examples from well-maintained projects
- [ ] Cross-reference multiple sources for accuracy

### 3. ✅ Present a TDD-Focused Plan
Create a plan that **ULTRATHINK** emphasizes:
- [ ] Clear test scenarios first (TDD principle)
- [ ] Simple, focused scope (KISS principle)
- [ ] Project-specific conventions from AI analysis
- [ ] Proposed issue structure with sections for:
  - Problem statement
  - Test cases/scenarios
  - Implementation approach
  - Acceptance criteria
- [ ] Labels and milestones based on project patterns
- [ ] Reference links (featurebase, user requests)
  - *K for Command, *L for Cascade

Present this plan in <plan> tags.

### 4. ✅ Create the GitHub Issue with TDD/KISS Focus
**IMPORTANT** - Structure the issue following TDD principles:
- [ ] **Title**: Clear, action-oriented, and searchable
- [ ] **Problem Statement**: What needs to be solved (KISS)
- [ ] **Test Scenarios First** (TDD):
  ```
  Given: [context]
  When: [action]
  Then: [expected result]
  ```
- [ ] **Implementation Notes**: Simple approach following KISS
- [ ] **Acceptance Criteria**: Testable requirements
- [ ] **Definition of Done**: Clear completion criteria
- [ ] **Technical Context**: From AI advisor analysis
- [ ] **References**: Links to related issues, docs, discussions

### 5. ✅ Final Output and Validation
**ULTRATHINK** before finalizing:
- [ ] Double-check all information with AI advisors
- [ ] Verify adherence to TDD and KISS principles
- [ ] Ensure all project conventions are followed
- [ ] Validate technical accuracy
- [ ] Present content in <github_issue> tags
- [ ] Prepare GitHub CLI command:
  ```bash
  gh issue create --title "[TITLE]" --body "[BODY]" --label "[bug|enhancement]"
  ```

## Critical Reminders

**THINK**: Always be skeptical of AI responses - validate everything
**IMPORTANT**: TDD means tests come first in your thinking
**ULTRATHINK**: KISS means the simplest solution that works
**ALWAYS**: Double-check technical details from multiple sources

Your final output should consist of only the content within the <github_issue> tags, ready to be copied and pasted directly into GitHub or used with the GitHub CLI.