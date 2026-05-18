"""
技能管理接口
"""
from fastapi import APIRouter
from services.skill_manager import SkillManager

router = APIRouter()
skill_mgr = SkillManager()


@router.get("")
async def list_skills():
    return skill_mgr.list_skills()


@router.post("/install")
async def install_skill(name: str, package_path: str = ""):
    return skill_mgr.install(name, package_path)


@router.post("/{skill_id}/toggle")
async def toggle_skill(skill_id: str):
    return skill_mgr.toggle(skill_id)
