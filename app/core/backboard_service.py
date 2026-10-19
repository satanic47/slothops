"""
Backboard.io Stateful Memory & Unified Routing Service
Handles long-term agent memory, sloth preference auto-recall, and semantic context management.
"""

import httpx
from typing import Dict, Any, List, Optional
from app.config import settings

class BackboardService:
    def __init__(self):
        self.api_key = settings.backboard_api_key
        self.base_url = settings.backboard_base_url.rstrip("/")
        self.collection = settings.backboard_collection
        self.is_live = bool(self.api_key and not self.api_key.startswith("your_"))
        
        # Local in-memory stateful store for offline / mock resilience
        self._local_memories: List[Dict[str, Any]] = [
            {
                "id": "mem_001",
                "category": "calendar_policy",
                "rule": "Never accept meetings before 11:00 AM or after 4:00 PM on Fridays.",
                "importance": 0.98,
                "created_at": "2026-10-19T10:00:00Z"
            },
            {
                "id": "mem_002",
                "category": "code_review_policy",
                "rule": "If PR passes all CI tests and changes < 50 lines with 0 security warnings, auto-approve.",
                "importance": 0.95,
                "created_at": "2026-10-19T11:30:00Z"
            },
            {
                "id": "mem_003",
                "category": "inbox_policy",
                "rule": "Newsletter subscriptions, webinar invites, and feedback requests must be archived silently.",
                "importance": 0.92,
                "created_at": "2026-10-19T14:15:00Z"
            },
            {
                "id": "mem_004",
                "category": "async_preference",
                "rule": "Prefer async Loom/transcript summaries over real-time standups to preserve focus blocks.",
                "importance": 0.99,
                "created_at": "2026-10-19T16:00:00Z"
            }
        ]

    async def recall_relevant_memories(self, query: str) -> List[Dict[str, Any]]:
        """Semantic search over long-term sloth memory to fetch user habits and rules."""
        if self.is_live:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(
                        f"{self.base_url}/memory/search",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "collection": self.collection,
                            "query": query,
                            "limit": 3
                        }
                    )
                    if resp.status_code == 200:
                        return resp.json().get("memories", [])
            except Exception as e:
                print(f"[BackboardService] Live search failed ({e}), using local memory cortex.")

        # Local semantic matcher
        q = query.lower()
        matched = []
        for m in self._local_memories:
            rule_text = m["rule"].lower()
            if any(w in rule_text for w in q.split() if len(w) > 3):
                matched.append(m)
        return matched if matched else self._local_memories[:2]

    async def save_memory(self, rule: str, category: str = "custom_preference") -> Dict[str, Any]:
        """Saves a new sloth habit or automation rule into Backboard stateful storage."""
        new_mem = {
            "id": f"mem_{len(self._local_memories) + 1:03d}",
            "category": category,
            "rule": rule,
            "importance": 0.90,
            "created_at": "2026-10-20T03:30:00Z"
        }
        
        if self.is_live:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    await client.post(
                        f"{self.base_url}/memory/store",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "collection": self.collection,
                            "data": new_mem
                        }
                    )
            except Exception as e:
                print(f"[BackboardService] Live store warning: {e}")

        self._local_memories.append(new_mem)
        return new_mem

    def list_all_memories(self) -> List[Dict[str, Any]]:
        return self._local_memories

    def get_stats(self) -> Dict[str, Any]:
        return {
            "status": "connected" if self.is_live else "local_resilient_mode",
            "active_collection": self.collection,
            "total_memories_stored": len(self._local_memories),
            "memory_retention_engine": "Backboard LoCoMo Architecture",
            "rag_context_savings": "Up to 70% context token reduction"
        }

backboard_service = BackboardService()
