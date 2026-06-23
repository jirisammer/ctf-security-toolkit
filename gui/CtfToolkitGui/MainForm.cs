using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using CtfToolkitGui.Models;
using CtfToolkitGui.Services;

namespace CtfToolkitGui;

public sealed class MainForm : Form
{
    private readonly PythonToolkitService _pythonToolkitService = new();
    private readonly GuiSettingsService _guiSettingsService = new();

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

    private readonly List<OperationDefinition> _operations =
    [
        new("Encoding / Decoding", "Base64 Encode", "base64-encode"),
        new("Encoding / Decoding", "Base64 Decode", "base64-decode"),
        new("Encoding / Decoding", "Hex Encode", "hex-encode"),
        new("Encoding / Decoding", "Hex Decode", "hex-decode"),
        new("Encoding / Decoding", "URL Encode", "url-encode"),
        new("Encoding / Decoding", "URL Decode", "url-decode"),

        new("Crypto", "ROT13", "rot13"),
        new("Crypto", "Caesar Encrypt", "caesar-encrypt", "Shift:", "3"),
        new("Crypto", "Caesar Decrypt", "caesar-decrypt", "Shift:", "3"),
        new("Crypto", "Caesar Brute Force", "caesar-bruteforce"),

        new("Hashing", "Generate Hash", "hash", "Algorithm:", "sha256"),
        new(
            "Hashing",
            "Verify Hash",
            "verify-hash",
            "Expected hash:",
            "",
            "Algorithm:",
            "sha256"
        ),

        new("Detection", "Analyze Input", "analyze"),

        new("Extraction", "Extract Indicators", "extract"),

        new("Web", "Decode JWT", "jwt-decode"),

        new("Files / Forensics", "File Info", "file-info"),
        new("Files / Forensics", "File Hash", "file-hash", "Algorithm:", "sha256"),
        new("Files / Forensics", "Extract Strings From File", "file-strings", "Min length:", "4")
    ];

    public MainForm()
    {
        Text = "CTF Security Toolkit GUI";
        StartPosition = FormStartPosition.CenterScreen;
        MinimumSize = new Size(1000, 740);

        InitializeLayout();
        InitializeDefaults();
        RegisterEvents();
    }

    private void InitializeLayout()
    {
        TableLayoutPanel mainLayout = new()
        {
            Dock = DockStyle.Fill,
            ColumnCount = 1,
            RowCount = 4,
            Padding = new Padding(12)
        };

        mainLayout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
        mainLayout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
        mainLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 45));
        mainLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 55));

        mainLayout.Controls.Add(CreatePythonSettingsGroupBox(), 0, 0);
        mainLayout.Controls.Add(CreateCommandGroupBox(), 0, 1);
        mainLayout.Controls.Add(CreateInputGroupBox(), 0, 2);
        mainLayout.Controls.Add(CreateOutputGroupBox(), 0, 3);

        Controls.Add(mainLayout);
    }

    private GroupBox CreatePythonSettingsGroupBox()
    {
        GroupBox groupBox = new()
        {
            Text = "Python Toolkit Settings",
            Dock = DockStyle.Top,
            AutoSize = true
        };

        TableLayoutPanel layout = new()
        {
            Dock = DockStyle.Fill,
            ColumnCount = 3,
            RowCount = 2,
            Padding = new Padding(10),
            AutoSize = true
        };

        layout.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 140));
        layout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        layout.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 110));

        Label pythonLabel = CreateLabel("Python:");
        Label mainScriptLabel = CreateLabel("main.py:");

        _pythonExecutableTextBox.Dock = DockStyle.Fill;
        _mainScriptPathTextBox.Dock = DockStyle.Fill;

        _browseButton.Text = "Browse";
        _browseButton.Dock = DockStyle.Fill;

        layout.Controls.Add(pythonLabel, 0, 0);
        layout.Controls.Add(_pythonExecutableTextBox, 1, 0);
        layout.Controls.Add(new Label(), 2, 0);

        layout.Controls.Add(mainScriptLabel, 0, 1);
        layout.Controls.Add(_mainScriptPathTextBox, 1, 1);
        layout.Controls.Add(_browseButton, 2, 1);

        groupBox.Controls.Add(layout);

        return groupBox;
    }

    private GroupBox CreateCommandGroupBox()
    {
        GroupBox groupBox = new()
        {
            Text = "Command",
            Dock = DockStyle.Top,
            AutoSize = true
        };

        TableLayoutPanel layout = new()
        {
            Dock = DockStyle.Fill,
            ColumnCount = 4,
            RowCount = 4,
            Padding = new Padding(10),
            AutoSize = true
        };

        layout.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 140));
        layout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50));
        layout.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 140));
        layout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50));

        Label categoryLabel = CreateLabel("Category:");
        Label operationLabel = CreateLabel("Operation:");

        _categoryComboBox.Dock = DockStyle.Fill;
        _categoryComboBox.DropDownStyle = ComboBoxStyle.DropDownList;

        _operationComboBox.Dock = DockStyle.Fill;
        _operationComboBox.DropDownStyle = ComboBoxStyle.DropDownList;

        _firstExtraArgumentLabel.Dock = DockStyle.Fill;
        _firstExtraArgumentLabel.TextAlign = ContentAlignment.MiddleLeft;

        _firstExtraArgumentTextBox.Dock = DockStyle.Fill;

        _secondExtraArgumentLabel.Dock = DockStyle.Fill;
        _secondExtraArgumentLabel.TextAlign = ContentAlignment.MiddleLeft;

        _secondExtraArgumentTextBox.Dock = DockStyle.Fill;

        _runButton.Text = "Run";
        _runButton.Dock = DockStyle.Fill;
        _runButton.Height = 36;

        _clearButton.Text = "Clear";
        _clearButton.Dock = DockStyle.Fill;
        _clearButton.Height = 36;

        layout.Controls.Add(categoryLabel, 0, 0);
        layout.Controls.Add(_categoryComboBox, 1, 0);
        layout.Controls.Add(_firstExtraArgumentLabel, 2, 0);
        layout.Controls.Add(_firstExtraArgumentTextBox, 3, 0);

        layout.Controls.Add(operationLabel, 0, 1);
        layout.Controls.Add(_operationComboBox, 1, 1);
        layout.Controls.Add(_secondExtraArgumentLabel, 2, 1);
        layout.Controls.Add(_secondExtraArgumentTextBox, 3, 1);

        layout.Controls.Add(_runButton, 2, 3);
        layout.Controls.Add(_clearButton, 3, 3);

        groupBox.Controls.Add(layout);

        return groupBox;
    }

    private GroupBox CreateInputGroupBox()
    {
        GroupBox groupBox = new()
        {
            Text = "Input",
            Dock = DockStyle.Fill
        };

        _inputTextBox.Multiline = true;
        _inputTextBox.ScrollBars = ScrollBars.Vertical;
        _inputTextBox.Dock = DockStyle.Fill;
        _inputTextBox.Font = new Font(FontFamily.GenericMonospace, 10);

        groupBox.Controls.Add(_inputTextBox);

        return groupBox;
    }

    private GroupBox CreateOutputGroupBox()
    {
        GroupBox groupBox = new()
        {
            Text = "Output",
            Dock = DockStyle.Fill
        };

        _outputTextBox.Multiline = true;
        _outputTextBox.ScrollBars = ScrollBars.Both;
        _outputTextBox.Dock = DockStyle.Fill;
        _outputTextBox.ReadOnly = true;
        _outputTextBox.Font = new Font(FontFamily.GenericMonospace, 10);

        groupBox.Controls.Add(_outputTextBox);

        return groupBox;
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

    private static Label CreateLabel(string text)
    {
        return new Label
        {
            Text = text,
            Dock = DockStyle.Fill,
            TextAlign = ContentAlignment.MiddleLeft
        };
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

    private sealed class OperationDefinition
    {
        public OperationDefinition(
            string category,
            string displayName,
            string command,
            string firstExtraArgumentLabel = "",
            string defaultFirstExtraArgument = "",
            string secondExtraArgumentLabel = "",
            string defaultSecondExtraArgument = "")
        {
            Category = category;
            DisplayName = displayName;
            Command = command;
            FirstExtraArgumentLabel = firstExtraArgumentLabel;
            DefaultFirstExtraArgument = defaultFirstExtraArgument;
            SecondExtraArgumentLabel = secondExtraArgumentLabel;
            DefaultSecondExtraArgument = defaultSecondExtraArgument;
        }

        public string Category { get; }

        public string DisplayName { get; }

        public string Command { get; }

        public string FirstExtraArgumentLabel { get; }

        public string DefaultFirstExtraArgument { get; }

        public string SecondExtraArgumentLabel { get; }

        public string DefaultSecondExtraArgument { get; }

        public bool RequiresFirstExtraArgument =>
            !string.IsNullOrWhiteSpace(FirstExtraArgumentLabel);

        public bool RequiresSecondExtraArgument =>
            !string.IsNullOrWhiteSpace(SecondExtraArgumentLabel);
    }
}