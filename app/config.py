import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class PartnerConfig(BaseModel):
    # Thinking Machines (Tinker)
    tinker_api_key: str = os.getenv("TINKER_API_KEY", "")
    tinker_base_model: str = os.getenv("TINKER_BASE_MODEL", "meta-llama/Llama-3-8B-Instruct")
    tinker_fine_tuned_model: str = os.getenv("TINKER_FINE_TUNED_MODEL", "sloth-distill-v1")
    tinker_endpoint: str = os.getenv("TINKER_ENDPOINT", "https://tinker.thinkingmachines.dev/services/tinker-prod/oai/api/v1/chat/completions")
    
    # Backboard.io
    backboard_api_key: str = os.getenv("BACKBOARD_API_KEY", "")
    backboard_base_url: str = os.getenv("BACKBOARD_BASE_URL", "https://app.backboard.io/api")
    backboard_assistant_name: str = os.getenv("BACKBOARD_ASSISTANT_NAME", "SlothOps Agent")
    backboard_assistant_id: str = os.getenv("BACKBOARD_ASSISTANT_ID", "")
    
    # Render
    render_service_name: str = os.getenv("RENDER_SERVICE_NAME", "slothops-web")
    render_external_url: str = os.getenv("RENDER_EXTERNAL_URL", "https://slothops.onrender.com")
    is_render_env: bool = bool(os.getenv("RENDER", False))
    
    # .tech Domains
    tech_custom_domain: str = os.getenv("TECH_CUSTOM_DOMAIN", "slothops.shivysidinfo.tech")
    tech_subpath: str = os.getenv("TECH_SUBPATH", "")
    tech_cname_target: str = os.getenv("TECH_CNAME_TARGET", "slothops.onrender.com")
    
    # App
    port: int = int(os.getenv("PORT", 8000))
    host: str = os.getenv("HOST", "0.0.0.0")
    environment: str = os.getenv("ENVIRONMENT", "development")

settings = PartnerConfig()
