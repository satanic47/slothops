"""
SlothOps - Autonomous 'Channel Your Inner Sloth' AI Agent Platform
FastAPI Server connecting Thinking Machines Tinker, Backboard.io, Render, and .tech.
Supports root '/' and subpath '/slothops' (e.g. shivysidinfo.tech/slothops).
"""

import os
from fastapi import FastAPI, Request, APIRouter
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
static_dir = os.path.join(BASE_DIR, "static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.mount("/slothops/static", StaticFiles(directory=static_dir), name="slothops_static")

# --- Request Models ---
class TriageRequest(BaseModel):
    title: str
    content: str

class MemoryRequest(BaseModel):
    rule: str
    category: Optional[str] = "custom_rule"

# --- Reusable Route Logic ---
async def render_dashboard(request: Request):
    try:
        stats = sloth_orchestrator.get_summary_stats()
        domain_status = domain_verifier.verify_domain_status()
        tasks = sloth_orchestrator.processed_tasks
        memories = backboard_service.list_all_memories()
        benchmark = tinker_service.get_benchmark_metrics()
        
        context = {
            "request": request,
            "stats": stats,
            "domain_status": domain_status,
            "tasks": tasks,
            "memories": memories,
            "benchmark": benchmark,
            "settings": settings
        }
        try:
            return templates.TemplateResponse(request=request, name="index.html", context=context)
        except Exception:
            return templates.TemplateResponse("index.html", context)
    except Exception as e:
        import traceback
        return HTMLResponse(f"<h3>Dashboard Render Error</h3><pre>{traceback.format_exc()}</pre>", status_code=500)

async def get_health():
    return {
        "status": "healthy",
        "service": "SlothOps Web API",
        "environment": settings.environment,
        "render_runtime": settings.is_render_env,
        "domain": f"{settings.tech_custom_domain}{settings.tech_subpath}",
        "partners": {
            "thinking_machines_tinker": "connected",
            "backboard_io": "connected",
            "render": "active",
            "tech_domains": f"{settings.tech_custom_domain}{settings.tech_subpath}"
        }
    }

async def get_partner_status():
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
                "role": "Stateful Long-Term Memory & Assistant Cortex",
                "assistant": settings.backboard_assistant_name,
                "retention_engine": "LoCoMo Memory Architecture",
                "status": "Active (Stateful Assistant)"
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
                "role": "Custom Production Domain & Subpath Routing",
                "domain": f"{settings.tech_custom_domain}{settings.tech_subpath}",
                "cname_target": settings.tech_cname_target,
                "status": "Active (DNS Telemetry Online)"
            }
        ]
    }

async def execute_triage(req: TriageRequest):
    result = await sloth_orchestrator.triage_chore(req.title, req.content)
    return result

# Router definition so routes mount on both "/" and "/slothops"
router = APIRouter()

router.add_api_route("/", render_dashboard, methods=["GET"], response_class=HTMLResponse)
router.add_api_route("/api/health", get_health, methods=["GET"])
router.add_api_route("/api/partners/status", get_partner_status, methods=["GET"])
router.add_api_route("/api/sloth/triage", execute_triage, methods=["POST"])
router.add_api_route("/api/sloth/tasks", lambda: sloth_orchestrator.processed_tasks, methods=["GET"])
router.add_api_route("/api/memory", lambda: {"memories": backboard_service.list_all_memories(), "stats": backboard_service.get_stats()}, methods=["GET"])
router.add_api_route("/api/memory", lambda req: backboard_service.save_memory(req.rule, req.category), methods=["POST"])
router.add_api_route("/api/tinker/benchmark", lambda: tinker_service.get_benchmark_metrics(), methods=["GET"])
router.add_api_route("/api/domain/verify", lambda: domain_verifier.verify_domain_status(), methods=["GET"])

# Mount at root "/"
app.include_router(router)

# Also mount with prefix "/slothops" for subpath hosting (shivysidinfo.tech/slothops)
app.include_router(router, prefix="/slothops")
