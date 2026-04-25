# Antigravity Agent Configuration

## Superpowers & Skills
This agent is equipped with the "Superpowers" and "Context7" extensions located in WSL. 

### Skill Discovery & Activation
When a task matches one of the following skills, you **MUST** load the skill content using `wsl cat <path>` and follow its instructions as a `SkillFile`.

#### Process Skills
- **brainstorming**: Use before any creative work. Explores user intent, requirements, and design.
  - Path: `/home/auditar/.gemini/extensions/superpowers/skills/brainstorming/SKILL.md`
- **writing-plans**: Use when you have a spec for a multi-step task, before touching code.
  - Path: `/home/auditar/.gemini/extensions/superpowers/skills/writing-plans/SKILL.md`
- **executing-plans**: Use when executing a written plan in a session with review checkpoints.
  - Path: `/home/auditar/.gemini/extensions/superpowers/skills/executing-plans/SKILL.md`
- **systematic-debugging**: Use when encountering any bug or unexpected behavior.
  - Path: `/home/auditar/.gemini/extensions/superpowers/skills/systematic-debugging/SKILL.md`
- **test-driven-development**: Use when implementing any feature or bugfix, before writing code.
  - Path: `/home/auditar/.gemini/extensions/superpowers/skills/test-driven-development/SKILL.md`
- **verification-before-completion**: Use before claiming work is complete. Requires evidence.
  - Path: `/home/auditar/.gemini/extensions/superpowers/skills/verification-before-completion/SKILL.md`

#### Documentation & Tools
- **find-docs**: Retrieves up-to-date documentation/API references via Context7.
  - Path: `/home/auditar/.gemini/extensions/context7/skills/find-docs/SKILL.md`
- **context7-cli**: Use when the user mentions "ctx7" or "context7".
  - Path: `/home/auditar/.gemini/extensions/context7/skills/context7-cli/SKILL.md`
- **context7-mcp**: Use for library/framework setup or API examples.
  - Path: `/home/auditar/.gemini/extensions/context7/skills/context7-mcp/SKILL.md`

#### Agent Coordination
- **subagent-driven-development**: Use when executing plans with independent tasks in the current session.
  - Path: `/home/auditar/.gemini/extensions/superpowers/skills/subagent-driven-development/SKILL.md`
- **dispatching-parallel-agents**: Use for 2+ independent tasks without shared state.
  - Path: `/home/auditar/.gemini/extensions/superpowers/skills/dispatching-parallel-agents/SKILL.md`

### Guidelines
1. **Invoke BEFORE responding**: If a skill applies (even 1%), load it before giving a full response.
2. **Evidence before assertions**: Always run verification commands before claiming success.
3. **Plan before code**: For complex tasks, always write a plan first.

---
*Configured based on user's Gemini CLI extensions.*
