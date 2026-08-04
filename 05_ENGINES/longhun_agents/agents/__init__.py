#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2
# DNA: #龍芯⚡️2026-08-04-AGENTS-INIT-UID9622

from .persona_agents import (
    AGENT_REGISTRY, AGENT_META,
    create_agent, create_all_agents,
)
from .integrator_agent import IntegratorAgent

__all__ = [
    "AGENT_REGISTRY", "AGENT_META",
    "create_agent", "create_all_agents",
    "IntegratorAgent",
]
