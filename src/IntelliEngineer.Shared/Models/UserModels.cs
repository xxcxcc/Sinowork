using IntelliEngineer.Shared.Enums;

namespace IntelliEngineer.Shared.Models;

/// <summary>
/// 用户模型
/// </summary>
public class AppUser
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string Name { get; set; } = string.Empty;
    public UserRole Role { get; set; }
    public EngineerSubType? EngineerSubType { get; set; }
    public string PasswordHash { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.Now;
    public DateTime LastLoginAt { get; set; }
    public bool IsActive { get; set; } = true;
}

/// <summary>
/// RBAC权限定义
/// </summary>
public class Permission
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string Name { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public List<UserRole> AllowedRoles { get; set; } = new();
    public bool RequiresApproval { get; set; }
}
