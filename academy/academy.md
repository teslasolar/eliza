# Academy — Getting Started

Welcome to the ACG Academy. This platform auto-discovers `academy.md` files from every directory in the project and builds a curriculum automatically.

## How It Works

1. Every directory can contain an `academy.md` file
2. The Academy HTML scans for these files on load
3. Each module can also have lessons in `academy/lessons/<dir>/`
4. Lessons can contain runnable JavaScript code blocks
5. The curriculum is always in sync with the codebase

## Creating New Modules

Add an `academy.md` to any directory:

```markdown
# Module Name

Description of what this module teaches.

## What You'll Learn
- Topic 1
- Topic 2

## Key Concepts
**Concept**: Explanation.
```

Then create lesson files in `academy/lessons/<dir>/01-lesson-name.md`.

## Philosophy

> "The best documentation teaches. The best teaching is hands-on." — ACG

The Academy is designed for *live testing* — code blocks execute in-browser, tools can be called, and standards can be queried interactively. Learning by doing, not just reading.
