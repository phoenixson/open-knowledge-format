---
type: Data Object
title: TaskCard
description: Carries the state and assignment of one kanban task.
resource: kanban board storage (SQLite)
kind: json
domain: software
standard_version: 0.1.0
generated: { by: human:operator, at: 2026-08-23T12:00:00-04:00 }
verified:
  - { by: human:operator, at: 2026-08-23T12:00:00-04:00 }
status: stable
stale_after: 2026-12-31T00:00:00Z
sources:
  - id: ste-data-objects
    resource: Documentation-standards/technical/data-objects.md
    title: Data Object Specification (STE)
    author: human:operator
    last_modified: 2026-08-18T00:00:00Z
---

# Data Object: TaskCard

**Kind:** json
**Domain:** software
**Source:** kanban board storage (SQLite)
**Standard version:** 0.1.0

## Purpose
Carries the state and assignment of one kanban task.

## Fields
| Field | Type | Required | Constraint | Meaning |
|---|---|---|---|---|
| id | string | yes | pattern ^t_[a-f0-9]+$ | Task identifier |
| title | string | yes | ≤ 200 chars | Short instruction |
| body | string | no | — | Detail and context |
| status | string | yes | enum: inbox, ready, in_progress, done, blocked | Lifecycle state |
| assignee | string | no | — | Worker identity or null |
| created_at | timestamp | yes | ISO-8601 UTC | Creation time |

## Example
{ "id": "t_3b536e81", "title": "Dispatcher race fix",
  "body": "Make protocol cards dispatcher-invisible.",
  "status": "done", "assignee": "node-ph-01",
  "created_at": "2026-08-17T11:45:00Z" }

## Validation
- id and created_at are immutable after creation.
- status transitions follow the protocol state machine.
- assignee is set only when status is in_progress or done.

## Relationships
- Used by: orchestrator.createTask, orchestrator.claimTask,
  orchestrator.completeTask.
- Contains: none. Is contained by: the kanban board.
