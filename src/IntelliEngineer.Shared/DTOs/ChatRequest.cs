using IntelliEngineer.Shared.Enums;
using IntelliEngineer.Shared.Models;

namespace IntelliEngineer.Shared.DTOs;

/// <summary>
/// 聊天请求
/// </summary>
public class ChatRequest
{
    public string SessionId { get; set; } = string.Empty;
    public string Message { get; set; } = string.Empty;
    public UserRole Role { get; set; }
    public string? ModelId { get; set; }
    public string? SkillId { get; set; }
    public List<string>? AttachedFileIds { get; set; }
}

/// <summary>
/// 聊天响应
/// </summary>
public class ChatResponse
{
    public string MessageId { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public bool IsComplete { get; set; }
    public int TokenCount { get; set; }
    public double CostUsd { get; set; }
    public CacheStats? CacheStats { get; set; }
}

/// <summary>
/// 技能执行请求
/// </summary>
public class SkillExecuteRequest
{
    public string SkillId { get; set; } = string.Empty;
    public Dictionary<string, string> Parameters { get; set; } = new();
    public string? SessionId { get; set; }
}

/// <summary>
/// 子Agent任务请求
/// </summary>
public class SubAgentRequest
{
    public string ParentSessionId { get; set; } = string.Empty;
    public string TaskDescription { get; set; } = string.Empty;
    public string? ModelId { get; set; }
    public int MaxTurns { get; set; } = 10;
}

/// <summary>
/// 文档生成请求
/// </summary>
public class DocumentGenerateRequest
{
    public string DocumentType { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
    public Dictionary<string, string> Content { get; set; } = new();
    public string OutputFormat { get; set; } = "docx";
}
