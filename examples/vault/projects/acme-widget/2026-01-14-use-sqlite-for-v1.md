---
type: decision
title: 2026-01-14-use-sqlite-for-v1
category: "[[acme-widget]]"
status: active
agent_load: high
created: 2026-01-14
updated: 2026-01-14
tags: [Decision]
---

# Use SQLite for v1

**Date:** 2026-01-14

_Fictional example._

## Decision
acme-widget v1 stores everything in a single SQLite file.

## Context
One shop, one location, a few hundred SKUs. No concurrent writers.

## Options considered
- SQLite file next to the app
- Hosted Postgres
- A spreadsheet as the backend

## Why this one
Zero ops, trivially backed up, and fast enough for the scale. Decisions are immutable;
if this changes, a new dated decision supersedes it.

## Supersedes / Links
- [[acme-widget]]
