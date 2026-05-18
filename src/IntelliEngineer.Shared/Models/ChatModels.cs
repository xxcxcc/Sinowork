using IntelliEngineer.Shared.Enums;

namespace IntelliEngineer.Shared.Models;

/// <summary>
/// 聊天消息模型
/// </summary>
public class ChatMessage
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string SessionId { get; set; } = string.Empty;
    public UserRole Role { get; set; }
    public MessageSender Sender { get; set; }
    public MessageType Type { get; set; } = MessageType.Text;
    public string Content { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.Now;
    public bool IsEdited { get; set; }
    public string? ParentMessageId { get; set; }
    public int TokenCount { get; set; }
    public double CostUsd { get; set; }
}

/// <summary>
/// 聊天会话模型
/// </summary>
public class ChatSession
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string Title { get; set; } = "新对话";
    public UserRole AssignedRole { get; set; }
    public EngineerSubType? EngineerSubType { get; set; }
    public string ModelId { get; set; } = "default";
    public List<ChatMessage> Messages { get; set; } = new();
    public DateTime CreatedAt { get; set; } = DateTime.Now;
    public DateTime LastActiveAt { get; set; } = DateTime.Now;
    public string? GroupId { get; set; }
    public double TotalCostUsd { get; set; }
    public int TotalTokens { get; set; }
    public int CacheHitTokens { get; set; }
    public int CacheMissTokens { get; set; }
    public bool IsArchived { get; set; }
}

/// <summary>
/// 会话分组
/// </summary>
public class SessionGroup
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string Name { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.Now;
    public List<string> SessionIds { get; set; } = new();
}
