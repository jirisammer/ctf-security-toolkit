namespace CtfToolkitGui.Models;

public sealed class OperationDefinition
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