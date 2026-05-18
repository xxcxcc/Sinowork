"""
技能管理器 - 兼容OpenHanako技能包格式
支持安装、启用/禁用、自动生成（Hermes-Agent Curator模式）
"""
import json
import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Skill:
    id: str
    name: str
    description: str
    role: str  # engineer / clerk / accountant / project_manager
    version: str = "1.0.0"
    enabled: bool = True
    source: str = "builtin"  # builtin / installed / auto_generated


# 内置技能清单
BUILTIN_SKILLS = [
    # 工程师
    Skill("eng-001", "技术方案生成", "根据需求自动生成技术方案文档", "engineer"),
    Skill("eng-002", "PLC代码生成与解释", "生成西门子S7系列ST语言/梯形图代码", "engineer"),
    Skill("eng-003", "电缆选型计算", "380V工业用电功率、电流、电缆选型计算", "engineer"),
    Skill("eng-004", "防爆等级查询", "根据危险区域划分查询所需防爆等级", "engineer"),
    Skill("eng-005", "项目周报生成", "自动生成项目周报模板并汇总进度", "engineer"),
    Skill("eng-006", "C#/Python代码调试", "代码自动生成、审查与优化", "engineer"),
    Skill("eng-007", "BOM表生成", "自动生成与核对物料清单", "engineer"),
    Skill("eng-008", "工业标准查询", "GB/GJB/IEC标准智能检索与解读", "engineer"),
    # 文员
    Skill("clk-001", "会议纪要生成", "语音/文字转结构化会议纪要，提取待办事项", "clerk"),
    Skill("clk-002", "文档标准化排版", "一键标准化Word文档格式", "clerk"),
    Skill("clk-003", "Excel数据统计", "自动统计、筛选、可视化Excel数据", "clerk"),
    Skill("clk-004", "邮件模板生成", "自动生成各类商务邮件模板", "clerk"),
    Skill("clk-005", "审批单填充", "自动填充各类审批单已知信息", "clerk"),
    Skill("clk-006", "批量文件重命名", "按规则批量重命名文件", "clerk"),
    Skill("clk-007", "考勤数据汇总", "自动汇总员工考勤数据", "clerk"),
    Skill("clk-008", "公文写作", "通知、公告、邀请函等公文模板", "clerk"),
    # 会计
    Skill("acc-001", "发票OCR识别", "批量识别增值税发票信息并录入", "accountant"),
    Skill("acc-002", "财务报表生成", "自动生成三大财务报表", "accountant"),
    Skill("acc-003", "增值税计算", "自动计算增值税及可抵扣进项税", "accountant"),
    Skill("acc-004", "报销单据审核", "智能审核报销单据合规性", "accountant"),
    Skill("acc-005", "工资条生成", "自动计算工资并生成工资条", "accountant"),
    Skill("acc-006", "发票验真", "对接查验平台验证发票真伪", "accountant"),
    Skill("acc-007", "税务政策查询", "最新税收政策查询与解读", "accountant"),
    Skill("acc-008", "财务指标分析", "自动计算并分析财务指标", "accountant"),
]


class SkillManager:
    def __init__(self):
        self._skills: dict[str, Skill] = {}
        self._load_builtin()

    def _load_builtin(self):
        for sk in BUILTIN_SKILLS:
            self._skills[sk.id] = sk

    def list_skills(self, role: Optional[str] = None) -> list:
        skills = self._skills.values()
        if role:
            skills = [s for s in skills if s.role == role]
        return [{"id": s.id, "name": s.name, "description": s.description,
                 "role": s.role, "enabled": s.enabled, "version": s.version} for s in skills]

    def install(self, name: str, package_path: str = "") -> dict:
        sk_id = f"inst-{name.lower().replace(' ', '-')}"
        skill = Skill(id=sk_id, name=name, description="用户安装技能", role="engineer", source="installed")
        self._skills[sk_id] = skill
        return {"id": sk_id, "status": "installed"}

    def toggle(self, skill_id: str) -> dict:
        if skill_id in self._skills:
            sk = self._skills[skill_id]
            sk.enabled = not sk.enabled
            return {"id": skill_id, "enabled": sk.enabled}
        return {"error": "技能未找到"}
