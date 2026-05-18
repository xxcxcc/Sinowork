using System.Windows;

namespace IntelliEngineer.Desktop;

public partial class App : System.Windows.Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);
        PythonServiceManager.Start();
    }

    protected override void OnExit(ExitEventArgs e)
    {
        PythonServiceManager.Stop();
        base.OnExit(e);
    }
}
