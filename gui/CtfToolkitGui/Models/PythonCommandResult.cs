using System.Text.Json;
using System.Text.Json.Serialization;

namespace CtfToolkitGui.Models;

public sealed class PythonCommandResult
{
    [JsonPropertyName("success")]
    public bool Success { get; set; }

    [JsonPropertyName("title")]
    public string? Title { get; set; }

    [JsonPropertyName("data")]
    public JsonElement Data { get; set; }

    [JsonPropertyName("error")]
    public string? Error { get; set; }

    public string GetDisplayText()
    {
        if (!Success)
        {
            return Error ?? "Unknown error.";
        }

        if (Data.ValueKind == JsonValueKind.Undefined || Data.ValueKind == JsonValueKind.Null)
        {
            return string.Empty;
        }

        if (Data.ValueKind == JsonValueKind.String)
        {
            return Data.GetString() ?? string.Empty;
        }

        return JsonSerializer.Serialize(
            Data,
            new JsonSerializerOptions
            {
                WriteIndented = true
            }
        );
    }
}