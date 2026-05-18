using IntelliEngineer.Shared.Enums;
using IntelliEngineer.Shared.Models;

namespace IntelliEngineer.Desktop.Services;

public class StateContainer
{
    public event Action? OnChange;

    public UserRole CurrentRole { get; set; } = UserRole.Engineer;
    public string CurrentPage { get; set; } = "chat";
    public bool ShowRightPanel { get; set; } = true;

    public ChatSession? ActiveSession { get; set; }
    public List<ChatSession> Sessions { get; set; } = new();
    public List<MemoryEntry> ActiveMemories { get; set; } = new();

    public bool IsStreaming { get; set; }
    public string StreamingContent { get; set; } = "";

    public void NotifyStateChanged() => OnChange?.Invoke();
}
