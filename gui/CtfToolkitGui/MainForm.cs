using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using CtfToolkitGui.Models;
using CtfToolkitGui.Services;

namespace CtfToolkitGui;

public sealed partial class MainForm : Form
{
    private readonly PythonToolkitService _pythonToolkitService = new();
    private readonly GuiSettingsService _guiSettingsService = new();
    private readonly IReadOnlyList<OperationDefinition> _operations = OperationCatalog.GetOperations();

    private GuiSettings _guiSettings = new();

    private readonly TextBox _pythonExecutableTextBox = new();
    private readonly TextBox _mainScriptPathTextBox = new();
    private readonly Button _browseButton = new();

    private readonly ComboBox _categoryComboBox = new();
    private readonly ComboBox _operationComboBox = new();

    private readonly TextBox _inputTextBox = new();

    private readonly Label _firstExtraArgumentLabel = new();
    private readonly TextBox _firstExtraArgumentTextBox = new();

    private readonly Label _secondExtraArgumentLabel = new();
    private readonly TextBox _secondExtraArgumentTextBox = new();

    private readonly Button _runButton = new();
    private readonly Button _clearButton = new();
    private readonly TextBox _outputTextBox = new();

    public MainForm()
    {
        InitializeLayout();
        InitializeDefaults();
        RegisterEvents();
    }

    private void InitializeDefaults()
    {
        _guiSettings = _guiSettingsService.LoadSettings();

        _pythonExecutableTextBox.Text = string.IsNullOrWhiteSpace(_guiSettings.PythonExecutable)
            ? "python"
            : _guiSettings.PythonExecutable;

        _mainScriptPathTextBox.Text = string.IsNullOrWhiteSpace(_guiSettings.MainScriptPath)
            ? GuessMainPyPath()
            : _guiSettings.MainScriptPath;

        string[] categories = _operations
            .Select(operation => operation.Category)
            .Distinct()
            .ToArray();

        _categoryComboBox.Items.AddRange(categories);

        if (_categoryComboBox.Items.Count > 0)
        {
            _categoryComboBox.SelectedIndex = 0;
        }

        _inputTextBox.Text = "hello";

        RefreshOperationComboBox();
        UpdateExtraArgumentControls();
    }

    private void RegisterEvents()
    {
        _browseButton.Click += BrowseButton_Click;

        _categoryComboBox.SelectedIndexChanged += (_, _) =>
        {
            RefreshOperationComboBox();
            UpdateExtraArgumentControls();
        };

        _operationComboBox.SelectedIndexChanged += (_, _) =>
        {
            UpdateExtraArgumentControls();
        };

        _runButton.Click += async (_, _) =>
        {
            await RunSelectedCommandAsync();
        };

        _clearButton.Click += (_, _) =>
        {
            _inputTextBox.Clear();
            _outputTextBox.Clear();
        };

        FormClosing += (_, _) =>
        {
            SaveGuiSettings();
        };
    }

    private void BrowseButton_Click(object? sender, EventArgs e)
    {
        using OpenFileDialog dialog = new()
        {
            Title = "Select Python main.py",
            Filter = "Python files (*.py)|*.py|All files (*.*)|*.*"
        };

        if (dialog.ShowDialog(this) == DialogResult.OK)
        {
            _mainScriptPathTextBox.Text = dialog.FileName;
            SaveGuiSettings();
        }
    }

    private async Task RunSelectedCommandAsync()
    {
        if (_operationComboBox.SelectedItem is not OperationDefinition operation)
        {
            MessageBox.Show(
                this,
                "No operation selected.",
                "Error",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error
            );

            return;
        }

        SaveGuiSettings();

        _runButton.Enabled = false;
        _outputTextBox.Text = "Running command...";

        try
        {
            List<string> arguments = BuildCommandArguments(operation);

            PythonCommandResult result = await _pythonToolkitService.RunCommandAsync(
                pythonExecutable: _pythonExecutableTextBox.Text,
                mainScriptPath: _mainScriptPathTextBox.Text,
                command: operation.Command,
                commandArguments: arguments
            );

            ShowCommandResult(result);
        }
        finally
        {
            _runButton.Enabled = true;
        }
    }

    private List<string> BuildCommandArguments(OperationDefinition operation)
    {
        List<string> arguments = new()
        {
            _inputTextBox.Text
        };

        if (operation.RequiresFirstExtraArgument)
        {
            arguments.Add(_firstExtraArgumentTextBox.Text.Trim());
        }

        if (operation.RequiresSecondExtraArgument)
        {
            arguments.Add(_secondExtraArgumentTextBox.Text.Trim());
        }

        return arguments;
    }

    private void ShowCommandResult(PythonCommandResult result)
    {
        if (!result.Success)
        {
            _outputTextBox.Text = $"ERROR:{Environment.NewLine}{result.Error}";
            return;
        }

        _outputTextBox.Text =
            $"{result.Title}{Environment.NewLine}" +
            $"{new string('-', 60)}{Environment.NewLine}" +
            result.GetDisplayText();
    }

    private void RefreshOperationComboBox()
    {
        if (_categoryComboBox.SelectedItem is not string selectedCategory)
        {
            return;
        }

        List<OperationDefinition> filteredOperations = _operations
            .Where(operation => operation.Category == selectedCategory)
            .ToList();

        _operationComboBox.DataSource = null;
        _operationComboBox.DataSource = filteredOperations;
        _operationComboBox.DisplayMember = nameof(OperationDefinition.DisplayName);

        if (filteredOperations.Count > 0)
        {
            _operationComboBox.SelectedIndex = 0;
        }
    }

    private void UpdateExtraArgumentControls()
    {
        if (_operationComboBox.SelectedItem is not OperationDefinition operation)
        {
            ClearExtraArgumentControls();
            return;
        }

        _firstExtraArgumentLabel.Text = operation.FirstExtraArgumentLabel;
        _secondExtraArgumentLabel.Text = operation.SecondExtraArgumentLabel;

        if (operation.RequiresFirstExtraArgument)
        {
            _firstExtraArgumentTextBox.Enabled = true;
            _firstExtraArgumentTextBox.Text = operation.DefaultFirstExtraArgument;
        }
        else
        {
            _firstExtraArgumentTextBox.Enabled = false;
            _firstExtraArgumentTextBox.Text = string.Empty;
        }

        if (operation.RequiresSecondExtraArgument)
        {
            _secondExtraArgumentTextBox.Enabled = true;
            _secondExtraArgumentTextBox.Text = operation.DefaultSecondExtraArgument;
        }
        else
        {
            _secondExtraArgumentTextBox.Enabled = false;
            _secondExtraArgumentTextBox.Text = string.Empty;
        }
    }

    private void ClearExtraArgumentControls()
    {
        _firstExtraArgumentLabel.Text = string.Empty;
        _firstExtraArgumentTextBox.Text = string.Empty;
        _firstExtraArgumentTextBox.Enabled = false;

        _secondExtraArgumentLabel.Text = string.Empty;
        _secondExtraArgumentTextBox.Text = string.Empty;
        _secondExtraArgumentTextBox.Enabled = false;
    }

    private void SaveGuiSettings()
    {
        _guiSettings.PythonExecutable = _pythonExecutableTextBox.Text.Trim();
        _guiSettings.MainScriptPath = _mainScriptPathTextBox.Text.Trim();

        _guiSettingsService.SaveSettings(_guiSettings);
    }

    private static string GuessMainPyPath()
    {
        DirectoryInfo? directory = new(AppContext.BaseDirectory);

        for (int i = 0; i < 12 && directory is not null; i++)
        {
            string possiblePath = Path.Combine(directory.FullName, "main.py");

            if (File.Exists(possiblePath))
            {
                return possiblePath;
            }

            directory = directory.Parent;
        }

        return string.Empty;
    }
}