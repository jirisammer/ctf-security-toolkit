using System;
using System.IO;
using System.Text.Json;
using CtfToolkitGui.Models;

namespace CtfToolkitGui.Services;

public sealed class GuiSettingsService
{
    private readonly string _settingsDirectory;
    private readonly string _settingsFilePath;

    public GuiSettingsService()
    {
        _settingsDirectory = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
            "CtfToolkitGui"
        );

        _settingsFilePath = Path.Combine(_settingsDirectory, "gui_settings.json");
    }

    public GuiSettings LoadSettings()
    {
        try
        {
            if (!File.Exists(_settingsFilePath))
            {
                return new GuiSettings();
            }

            string json = File.ReadAllText(_settingsFilePath);

            GuiSettings? settings = JsonSerializer.Deserialize<GuiSettings>(
                json,
                new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                }
            );

            return settings ?? new GuiSettings();
        }
        catch
        {
            return new GuiSettings();
        }
    }

    public void SaveSettings(GuiSettings settings)
    {
        if (settings is null)
        {
            return;
        }

        Directory.CreateDirectory(_settingsDirectory);

        string json = JsonSerializer.Serialize(
            settings,
            new JsonSerializerOptions
            {
                WriteIndented = true
            }
        );

        File.WriteAllText(_settingsFilePath, json);
    }
}