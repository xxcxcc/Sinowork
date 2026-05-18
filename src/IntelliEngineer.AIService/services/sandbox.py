"""
安全沙盒 - OpenHanako PathGuard四级访问控制移植
Denied / ReadOnly / ReadWrite / Full
"""
from enum import Enum
from typing import Optional


class AccessLevel(Enum):
    DENIED = "denied"
    READONLY = "readonly"
    READWRITE = "readwrite"
    FULL = "full"


class PathGuard:
    """
    四级路径权限控制
    默认只允许访问白名单目录
    """
    def __init__(self, config: dict):
        self._config = config
        self._allowed_paths = config.get("allowed_paths", [])
        self._denied_commands = config.get("denied_commands", [])

    def check_file_access(self, path: str, required_level: AccessLevel = AccessLevel.READONLY) -> bool:
        """检查文件路径是否有足够权限"""
        if required_level == AccessLevel.DENIED:
            return False

        import os
        resolved = os.path.expanduser(path)

        for allowed in self._allowed_paths:
            allowed_resolved = os.path.expanduser(allowed)
            if resolved.startswith(allowed_resolved):
                return True

        return required_level == AccessLevel.DENIED  # Denied总是拒绝

    def check_command(self, command: str) -> bool:
        """检查终端命令是否被允许"""
        cmd_lower = command.lower()
        for denied in self._denied_commands:
            if denied.lower() in cmd_lower:
                return False
        return True

    def get_access_level(self, path: str) -> AccessLevel:
        """获取某路径的访问级别"""
        import os
        resolved = os.path.expanduser(path)

        # 配置文件目录: 完全访问
        for allowed in self._allowed_paths:
            allowed_resolved = os.path.expanduser(allowed)
            if resolved.startswith(allowed_resolved + "/data"):
                return AccessLevel.READWRITE
            if resolved.startswith(allowed_resolved):
                return AccessLevel.READONLY

        return AccessLevel.DENIED
