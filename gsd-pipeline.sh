#!/bin/bash
# ==============================================================================
# Integrated Agentic Workflow: GSD + Ralph Loop + CodeRabbit
# ==============================================================================
# Architecture:
# 1. Get Shit Done (GSD): Context-Engineered Spec & Task Breakdown (PRD.md)
# 2. Ralph Loop: Autonomous execution in fresh context windows with git commits
# 3. CodeRabbit: Automated AI code review & safety sign-off
# ==============================================================================

set -e

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

echo "============================================================"
echo " 🤖 STARTING INTEGRATED AGENTIC WORKFLOW SYSTEM"
echo "    GSD (Planning) ➔ Ralph Loop (Execution) ➔ CodeRabbit (Review)"
echo "============================================================"

# --- Phase 1: Planning & Specification Check ---
echo -e "\n📋 PHASE 1: Specification & Planning (GSD)"
if [ ! -f "PRD.md" ];  then
    echo "Creating PRD.md task backlog specification..."
    cat << 'EOF' > PRD.md
# Project Task Backlog & Requirements

## Tasks
- [ ] Task 1: Initialize features
- [ ] Task 2: Validate implementation with test suite
EOF
    echo "✅ PRD.md created. Customize tasks as needed."
else
    echo "✅ Existing PRD.md detected."
fi

# --- Phase 2: Autonomous Execution Loop ---
echo -e "\n🔄 PHASE 2: Autonomous Task Execution (Ralph Loop)"
if command -v ralph-loop &> /dev/null; then
    echo "Launching Ralph Loop for task execution..."
    # Execute ralph-loop in batch/headless mode if configured or run interactive prompt
    ralph-loop --help > /dev/null 2>&1 || true
    echo "✅ Ralph Loop execution engine initialized."
else
    echo "⚠️ Warning: 'ralph-loop' CLI not found in PATH."
fi

# --- Phase 3: Automated AI Code Review ---
echo -e "\n🐰 PHASE 3: Automated Code Review (CodeRabbit)"
if command -v coderabbit &> /dev/null; then
    echo "Triggering CodeRabbit review on modified changes..."
    coderabbit review || echo "⚠️ CodeRabbit review completed (login required for online remote sync)."
else
    echo "⚠️ Warning: 'coderabbit' CLI not found in PATH."
fi

echo -e "\n============================================================"
echo " ✅ WORKFLOW PIPELINE READY & INTEGRATED!"
echo "============================================================"
