using System.Diagnostics;
using System.IO;

namespace IntelliEngineer.Desktop;

/// <summary>
/// 管理Python AI服务的进程生命周期
/// WPF启动时自动拉起Python FastAPI，退出时关闭
/// </summary>
public static class PythonServiceManager
{
    private static Process? _pythonProcess;

    public static void Start()
    {
        try
        {
            var serviceDir = Path.Combine(
                AppDomain.CurrentDomain.BaseDirectory,
                "..", "..", "..", "..", "IntelliEngineer.AIService");

            // 相对于项目目录查找Python服务
            if (!Directory.Exists(serviceDir))
            {
                // 尝试从发布目录查找
                serviceDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "aiservice");
            }

            if (!Directory.Exists(serviceDir))
            {
                System.Windows.MessageBox.Show(
                    "未找到Python AI服务目录，请确保 IntelliEngineer.AIService 已正确部署。",
                    "服务未找到", System.Windows.MessageBoxButton.OK, System.Windows.MessageBoxImage.Warning);
                return;
            }

            _pythonProcess = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = "-m uvicorn main:app --host 127.0.0.1 --port 8000",
                    WorkingDirectory = serviceDir,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true
                },
                EnableRaisingEvents = true
            };

            _pythonProcess.OutputDataReceived += (s, e) =>
                LogToFile($"[AI服务] {e.Data}");
            _pythonProcess.ErrorDataReceived += (s, e) =>
                LogToFile($"[AI服务-错误] {e.Data}");

            _pythonProcess.Start();
            _pythonProcess.BeginOutputReadLine();
            _pythonProcess.BeginErrorReadLine();

            LogToFile("[智工助手] Python AI服务已启动 (localhost:8000)");
        }
        catch (Exception ex)
        {
            LogToFile($"[错误] 启动Python服务失败: {ex.Message}");
        }
    }

    public static void Stop()
    {
        if (_pythonProcess is { HasExited: false })
        {
            _pythonProcess.Kill();
            _pythonProcess.WaitForExit(3000);
            LogToFile("[智工助手] Python AI服务已停止");
        }
    }

    private static void LogToFile(string message)
    {
        try
        {
            var logDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "IntelliEngineer");
            Directory.CreateDirectory(logDir);
            var logPath = Path.Combine(logDir, "service.log");
            File.AppendAllText(logPath, $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] {message}{Environment.NewLine}");
        }
        catch { /* 日志写入失败不崩溃 */ }
    }
}
