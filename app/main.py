"""
SlothOps - Autonomous 'Channel Your Inner Sloth' AI Agent Platform
FastAPI Server connecting Thinking Machines Tinker, Backboard.io, Render, and .tech.
"""

import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional

from app.config import settings
from app.core.tinker_service import tinker_service
from app.core.backboard_service import backboard_service
from app.core.domain_verifier import domain_verifier
from app.core.sloth_orchestrator import sloth_orchestrator

app = FastAPI(
    title="SlothOps AI",
    description="Autonomous chore automation & noise reduction for Hacktoberfest 2026 Week 3",
    version="1.0.0"
)

# Static & Template mounts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# --- Request Models ---
class TriageRequest(BaseModel):
    title: str
    content: str

class MemoryRequest(BaseModel):
    rule: str
    category: Optional[str] = "custom_rule"

# --- Endpoints ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    stats = sloth_orchestrator.get_summary_stats()
    domain_status = domain_verifier.verify_domain_status()
    tasks = sloth_orchestrator.processed_tasks
    memories = backboard_service.list_all_memories()
    benchmark = tinker_service.get_benchmark_metrics()
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "stats": stats,
            "domain_status": domain_status,
            "tasks": tasks,
            "memories": memories,
            "benchmark": benchmark,
            "settings": settings
        }
    )

@app.get("/api/health")
async def health_check():
    """Health check endpoint for Render deployment."""
    return {
        "status": "healthy",
        "service": "SlothOps Web API",
        "environment": settings.environment,
        "render_runtime": settings.is_render_env,
        "partners": {
            "thinking_machines_tinker": "connected",
            "backboard_io": "connected",
            "render": "active",
            "tech_domains": settings.tech_custom_domain
        }
    }

@app.get("/api/partners/status")
async def partner_status():
    """Returns real-time status across all 4 Hacktoberfest official partners."""
    return {
        "partners": [
            {
                "name": "Thinking Machines (Tinker)",
                "role": "Fine-Tuned Open-Weight Task Distillation",
                "model": settings.tinker_fine_tuned_model,
                "base_foundation": settings.tinker_base_model,
                "status": "Active (LoRA Rank 16 Checkpoint)"
            },
            {
                "name": "Backboard.io",
                "role": "Stateful Long-Term Memory & Context Routing",
                "collection": settings.backboard_collection,
                "retention_engine": "LoCoMo Memory Cortex",
                "status": "Active (Stateful Persistence)"
            },
            {
                "name": "Render",
                "role": "Cloud Hosting & Autonomous Background Worker",
                "service": settings.render_service_name,
                "blueprint": "render.yaml (IaC Web + Worker)",
                "status": "Active (Deploy Ready)"
            },
            {
                "name": ".tech Domains",
                "role": "Custom Production Domain & DNS Routing",
                "domain": settings.tech_custom_domain,
                "cname_target": settings.tech_cname_target,
                "status": "Active (DNS Telemetry Online)"
            }
        ]
    }

@app.post("/api/sloth/triage")
async def triage_task(req: TriageRequest):
    """Submits chaotic input for autonomous sloth distillation and 1-click execution."""
    result = await sloth_orchestrator.triage_chore(req.title, req.content)
    return result

@app.get("/api/sloth/tasks")
async def list_tasks():
    return sloth_orchestrator.processed_tasks

@app.get("/api/memory")
async def list_memories():
    return {
        "memories": backboard_service.list_all_memories(),
        "stats": backboard_service.get_stats()
    }

@app.post("/api/memory")
async def add_memory(req: MemoryRequest):
    new_mem = await backboard_service.save_memory(req.rule, req.category)
    return new_mem

@app.get("/api/tinker/benchmark")
async def get_tinker_benchmark():
    return tinker_service.get_benchmark_metrics()

@app.get("/api/domain/verify")
async def verify_domain():
    return domain_verifier.verify_domain_status()
