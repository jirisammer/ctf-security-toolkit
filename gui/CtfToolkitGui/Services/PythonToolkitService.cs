using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using CtfToolkitGui.Models;

namespace CtfToolkitGui.Services;

public sealed class PythonToolkitService
{
    public async Task<PythonCommandResult> RunCommandAsync(
        string pythonExecutable,
        string mainScriptPath,
        string command,
        IReadOnlyList<string> commandArguments,
        CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(pythonExecutable))
        {
            return CreateError("Python executable cannot be empty.");
        }

        if (string.IsNullOrWhiteSpace(mainScriptPath))
        {
            return CreateError("Python main.py path cannot be empty.");
        }

        if (!File.Exists(mainScriptPath))
        {
            return CreateError($"Python main.py file does not exist: {mainScriptPath}");
        }

        if (string.IsNullOrWhiteSpace(command))
        {
            return CreateError("Command cannot be empty.");
        }

        try
        {
            using Process process = new();

            process.StartInfo = new ProcessStartInfo
            {
                FileName = pythonExecutable,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            };

            process.StartInfo.ArgumentList.Add(mainScriptPath);
            process.StartInfo.ArgumentList.Add("--output");
            process.StartInfo.ArgumentList.Add("json");
            process.StartInfo.ArgumentList.Add(command);

            foreach (string argument in commandArguments)
            {
                process.StartInfo.ArgumentList.Add(argument);
            }

            process.Start();

            Task<string> outputTask = process.StandardOutput.ReadToEndAsync();
            Task<string> errorTask = process.StandardError.ReadToEndAsync();

            await process.WaitForExitAsync(cancellationToken);

            string output = await outputTask;
            string error = await errorTask;

            if (string.IsNullOrWhiteSpace(output))
            {
                if (!string.IsNullOrWhiteSpace(error))
                {
                    return CreateError(error.Trim());
                }

                return CreateError("Python returned empty output.");
            }

            PythonCommandResult? result = JsonSerializer.Deserialize<PythonCommandResult>(
                output,
                new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                }
            );

            if (result is null)
            {
                return CreateError("Could not parse JSON result from Python.");
            }

            if (process.ExitCode != 0 && result.Success)
            {
                return CreateError($"Python command failed with exit code {process.ExitCode}.");
            }

            return result;
        }
        catch (Exception exception)
        {
            return CreateError(exception.Message);
        }
    }

    private static PythonCommandResult CreateError(string message)
    {
        return new PythonCommandResult
        {
            Success = false,
            Error = message
        };
    }
}