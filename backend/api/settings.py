import os
from fastapi import APIRouter
from backend.config.settings import settings

router = APIRouter()

@router.get("/settings")
async def get_settings():
    return {
        "gemini_connected": settings.is_gemini_available,
        "openai_connected": settings.is_openai_available
    }

@router.post("/settings")
async def update_settings(keys: dict):
    gemini_key = keys.get("gemini_key", "").strip()
    openai_key = keys.get("openai_key", "").strip()
    
    # Resolve the path to .env file in the backend folder
    config_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(config_dir, ".env")
    
    # Read the existing lines of the .env file if it exists
    lines = []
    if os.path.exists(dotenv_path):
        with open(dotenv_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
    # Prepare the new lines to be written
    new_lines = []
    gemini_written = False
    openai_written = False
    
    # We will update the settings object in memory first
    if gemini_key:
        settings.gemini_api_key = gemini_key
    if openai_key:
        settings.openai_api_key = openai_key
        
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("GEMINI_API_KEY="):
            if gemini_key:
                new_lines.append(f'GEMINI_API_KEY="{gemini_key}"\n')
                gemini_written = True
            else:
                new_lines.append(line)
        elif stripped.startswith("OPENAI_API_KEY="):
            if openai_key:
                new_lines.append(f'OPENAI_API_KEY="{openai_key}"\n')
                openai_written = True
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    if not gemini_written and gemini_key:
        new_lines.append(f'GEMINI_API_KEY="{gemini_key}"\n')
    if not openai_written and openai_key:
        new_lines.append(f'OPENAI_API_KEY="{openai_key}"\n')
        
    # Write back to .env
    with open(dotenv_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
        
    return {"status": "success"}
