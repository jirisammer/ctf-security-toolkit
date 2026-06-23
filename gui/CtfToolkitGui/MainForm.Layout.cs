using System.Drawing;
using System.Windows.Forms;

namespace CtfToolkitGui;

public sealed partial class MainForm
{
    private void InitializeLayout()
    {
        Text = "CTF Security Toolkit GUI";
        StartPosition = FormStartPosition.CenterScreen;
        MinimumSize = new Size(1000, 740);

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

    private static Label CreateLabel(string text)
    {
        return new Label
        {
            Text = text,
            Dock = DockStyle.Fill,
            TextAlign = ContentAlignment.MiddleLeft
        };
    }
}