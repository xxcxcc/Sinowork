using IntelliEngineer.Shared.DTOs;
using IntelliEngineer.Shared.Enums;
using IntelliEngineer.Shared.Models;

namespace IntelliEngineer.Desktop.Services;

public class ChatService
{
    private readonly ApiClient _api;
    private readonly StateContainer _state;

    public ChatService(ApiClient api, StateContainer state)
    {
        _api = api;
        _state = state;
    }

    public async Task SendMessageAsync(string message)
    {
        var session = _state.ActiveSession;
        if (session is null)
        {
            session = new ChatSession
            {
                Id = Guid.NewGuid().ToString(),
                Title = message.Length > 20 ? message[..20] + "..." : message,
                AssignedRole = _state.CurrentRole
            };
            _state.ActiveSession = session;
            _state.Sessions.Add(session);
        }

        session.Messages.Add(new ChatMessage
        {
            SessionId = session.Id,
            Sender = MessageSender.User,
            Content = message,
            CreatedAt = DateTime.Now
        });

        _state.IsStreaming = true;
        _state.StreamingContent = "";

        var response = await _api.SendChatAsync(new ChatRequest
        {
            SessionId = session.Id,
            Message = message,
            Role = _state.CurrentRole
        });

        if (response is not null)
        {
            session.Messages.Add(new ChatMessage
            {
                SessionId = session.Id,
                Sender = MessageSender.Assistant,
                Content = response.Content,
                Type = MessageType.Text,
                CreatedAt = DateTime.Now,
                TokenCount = response.TokenCount,
                CostUsd = response.CostUsd
            });
        }

        _state.IsStreaming = false;
        _state.StreamingContent = "";
        _state.NotifyStateChanged();
    }
}
