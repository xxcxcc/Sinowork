# 智工助手 v0.1

> IntelliEngineer Assistant — 专属本地化桌面AI助理系统

## 技术栈

- **桌面壳**：WPF + Blazor Hybrid（`BlazorWebView` 嵌入 WPF 窗口，.NET 10）
- **前端 UI**：Blazor Hybrid（Razor组件运行于桌面进程，非WASM独立）
- **AI 引擎**：Python FastAPI（本地 REST API，localhost:8000）
- **数据库**：SQLite（WAL模式，AES-256加密）
- **AI模型**：Ollama（本地离线）+ DeepSeek API（云端，前缀缓存优化）
- **通信**：HTTP REST API（Blazor HttpClient → Python FastAPI）

## 参考开源项目

本产品深度整合以下三个开源项目的核心设计模式：

| 项目 | 核心参考点 |
|------|-----------|
| **OpenHanako** | 三栏式桌面布局、PathGuard四级访问控制、技能包格式 |
| **Hermes-Agent** | Curator自学习闭环、子Agent调度、Context Engine |
| **DeepSeek-Reasonix** | ImmutablePrefix+AppendOnlyLog缓存、SEARCH/REPLACE编辑、成本控制 |

## 项目结构

```
Zingon/
├── IntelliEngineer.sln              # 解决方案（2个.NET项目）
├── docs/                            # 文档目录
├── src/
│   ├── IntelliEngineer.Shared/      # .NET 共享类库（模型/枚举/DTO）
│   ├── IntelliEngineer.Desktop/     # WPF + BlazorHybrid 桌面壳
│   │   ├── MainWindow.xaml          # WPF窗口→托管BlazorWebView
│   │   ├── PythonServiceManager.cs  # Python进程生命周期管理
│   │   ├── Components/              # 22个Blazor组件
│   │   └── Services/                # ApiClient/ChatService/StateContainer
│   └── IntelliEngineer.AIService/   # Python FastAPI AI引擎
│       ├── main.py                  # FastAPI入口（localhost:8000）
│       ├── api/                     # chat/skill/memory/model路由
│       └── services/                # Agent/前缀缓存/技能/记忆/沙盒
```

## 开发环境要求

- Windows 10 21H2+ (64位)
- .NET 10 SDK
- Python 3.11+
- Visual Studio 2022+ 或 VS Code
- WebView2 运行时

## 启动方式

```bash
# 1. 安装Python依赖
cd src/IntelliEngineer.AIService
pip install -r requirements.txt

# 2. 启动Python AI服务
python -m uvicorn main:app --host 127.0.0.1 --port 8000

# 3. 启动WPF桌面（会自动拉起Python服务）
cd src/IntelliEngineer.Desktop
dotnet run
```
