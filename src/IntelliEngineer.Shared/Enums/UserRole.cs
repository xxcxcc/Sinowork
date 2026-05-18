namespace IntelliEngineer.Shared.Enums;

/// <summary>
/// 用户角色枚举（四角色：工程师/文员/会计/项目经理）
/// </summary>
public enum UserRole
{
    Engineer = 1,
    Clerk = 2,
    Accountant = 3,
    ProjectManager = 4
}

/// <summary>
/// 工程师子类型（14名工程师的分类）
/// </summary>
public enum EngineerSubType
{
    Software = 1,
    Electrical = 2,
    Mechanical = 3,
    Implementation = 4,
    Simulation = 5
}

/// <summary>
/// 技能状态
/// </summary>
public enum SkillStatus
{
    Installed = 1,
    Enabled = 2,
    Disabled = 3,
    Installing = 4,
    Failed = 5
}

/// <summary>
/// 技能格式（兼容多种格式）
/// </summary>
public enum SkillFormat
{
    OpenHanako = 1,
    Hermes = 2,
    Standard = 3
}

/// <summary>
/// PathGuard四级路径访问级别
/// </summary>
public enum PathAccessLevel
{
    Denied = 0,
    ReadOnly = 1,
    ReadWrite = 2,
    Full = 3
}

/// <summary>
/// 记忆级别
/// </summary>
public enum MemoryLevel
{
    Global = 1,
    Project = 2,
    Role = 3,
    Enterprise = 4
}

/// <summary>
/// 消息类型
/// </summary>
public enum MessageType
{
    Text = 1,
    Code = 2,
    Table = 3,
    Image = 4,
    File = 5
}

/// <summary>
/// 消息发送者类型
/// </summary>
public enum MessageSender
{
    User = 1,
    Assistant = 2,
    System = 3
}

/// <summary>
/// 模型提供者
/// </summary>
public enum ModelProvider
{
    Ollama = 1,
    DeepSeek = 2,
    OpenAI = 3
}

/// <summary>
/// 推理模式
/// </summary>
public enum ReasoningMode
{
    Fast = 1,
    Deep = 2
}

/// <summary>
/// 审计操作类型
/// </summary>
public enum AuditActionType
{
    Create = 1,
    Read = 2,
    Update = 3,
    Delete = 4,
    Execute = 5,
    Login = 6,
    Logout = 7
}
