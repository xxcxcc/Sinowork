using System.Net.Http;
using System.Net.Http.Json;
using IntelliEngineer.Shared.DTOs;
using IntelliEngineer.Shared.Models;

namespace IntelliEngineer.Desktop.Services;

public class ApiClient
{
    private readonly HttpClient _http;

    public ApiClient(HttpClient http) => _http = http;

    public async Task<ChatResponse?> SendChatAsync(ChatRequest request)
    {
        var response = await _http.PostAsJsonAsync("/api/chat", request);
        return response.IsSuccessStatusCode
            ? await response.Content.ReadFromJsonAsync<ChatResponse>()
            : null;
    }

    public async Task<List<ChatSession>> GetSessionsAsync() =>
        await _http.GetFromJsonAsync<List<ChatSession>>("/api/chat/sessions") ?? new();

    public async Task<List<SkillPackage>> GetSkillsAsync() =>
        await _http.GetFromJsonAsync<List<SkillPackage>>("/api/skill") ?? new();

    public async Task<List<MemoryEntry>> GetMemoriesAsync() =>
        await _http.GetFromJsonAsync<List<MemoryEntry>>("/api/memory") ?? new();

    public async Task<List<ModelConfig>> GetModelsAsync() =>
        await _http.GetFromJsonAsync<List<ModelConfig>>("/api/model") ?? new();

    public async Task<CostSummary?> GetCostSummaryAsync() =>
        await _http.GetFromJsonAsync<CostSummary>("/api/model/stats");
}
