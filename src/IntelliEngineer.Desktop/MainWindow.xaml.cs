using System.Net.Http;
using System.Windows;
using IntelliEngineer.Desktop.Services;
using Microsoft.AspNetCore.Components.WebView.WindowsForms;
using Microsoft.Extensions.DependencyInjection;

namespace IntelliEngineer.Desktop;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    private void OnLoaded(object sender, RoutedEventArgs e)
    {
        var services = new ServiceCollection();
        services.AddWindowsFormsBlazorWebView();
        services.AddScoped<HttpClient>(_ => new HttpClient { BaseAddress = new Uri("http://localhost:8000") });
        services.AddScoped<ApiClient>();
        services.AddScoped<ChatService>();
        services.AddScoped<ThemeService>();
        services.AddSingleton<StateContainer>();

        var sp = services.BuildServiceProvider();

        var blazorWebView = new BlazorWebView
        {
            HostPage = "wwwroot/index.html",
            Services = sp,
            Dock = System.Windows.Forms.DockStyle.Fill
        };
        blazorWebView.RootComponents.Add(
            new RootComponent("#app", typeof(RouterComponent), null));

        FormsHost.Child = blazorWebView;
    }
}
