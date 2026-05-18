using IntelliEngineer.Shared.Enums;

namespace IntelliEngineer.Shared.Models;

/// <summary>
/// 文房文件元数据模型
/// </summary>
public class StudyFile
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string FileName { get; set; } = string.Empty;
    public string FilePath { get; set; } = string.Empty;
    public string FileType { get; set; } = string.Empty;
    public long FileSize { get; set; }
    public DateTime UploadedAt { get; set; } = DateTime.Now;
    public DateTime ModifiedAt { get; set; } = DateTime.Now;
    public string? Summary { get; set; }
    public List<string> Tags { get; set; } = new();
    public string? OwnerId { get; set; }
    public bool IsShared { get; set; }
}

/// <summary>
/// 写笺便签模型
/// </summary>
public class WriteNote
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string Content { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.Now;
    public DateTime? CompletedAt { get; set; }
    public bool IsCompleted { get; set; }
    public string? AssignedAgentId { get; set; }
}

/// <summary>
/// 模型配置
/// </summary>
public class ModelConfig
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string Name { get; set; } = string.Empty;
    public ModelProvider Provider { get; set; }
    public string ApiEndpoint { get; set; } = string.Empty;
    public string? ApiKey { get; set; }
    public string ModelId { get; set; } = string.Empty;
    public float Temperature { get; set; } = 0.7f;
    public int MaxTokens { get; set; } = 4096;
    public float TopP { get; set; } = 0.9f;
    public bool IsDefault { get; set; }
    public ReasoningMode Mode { get; set; } = ReasoningMode.Fast;
}

/// <summary>
/// 审计日志条目
/// </summary>
public class AuditLogEntry
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public DateTime Timestamp { get; set; } = DateTime.Now;
    public string UserId { get; set; } = string.Empty;
    public string UserName { get; set; } = string.Empty;
    public UserRole UserRole { get; set; }
    public AuditActionType Action { get; set; }
    public string Description { get; set; } = string.Empty;
    public string? IpAddress { get; set; }
    public bool IsSuccess { get; set; }
}

/// <summary>
/// 子Agent任务
/// </summary>
public class SubAgentTask
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string ParentSessionId { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string? Result { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.Now;
    public DateTime? CompletedAt { get; set; }
    public bool IsCompleted { get; set; }
    public string? ErrorMessage { get; set; }
}

/// <summary>
/// 前缀缓存统计
/// </summary>
public class CacheStats
{
    public string SessionId { get; set; } = string.Empty;
    public int TotalPromptTokens { get; set; }
    public int CacheHitTokens { get; set; }
    public int CacheMissTokens { get; set; }
    public double HitRate => TotalPromptTokens > 0 ? (double)CacheHitTokens / TotalPromptTokens : 0;
    public double CostSavedUsd { get; set; }
}

/// <summary>
/// 成本统计（参考DeepSeek-Reasonix颜色标记：绿<0.05/黄<0.20/红≥0.20）
/// </summary>
public class CostSummary
{
    public double TotalCostUsd { get; set; }
    public int TotalTokens { get; set; }
    public int TotalRequests { get; set; }
    public string CostLevel => TotalCostUsd switch
    {
        < 0.05 => "低",
        < 0.20 => "中",
        _ => "高"
    };
}
