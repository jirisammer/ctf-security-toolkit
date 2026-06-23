using System.Collections.Generic;
using CtfToolkitGui.Models;

namespace CtfToolkitGui.Services;

public static class OperationCatalog
{
    public static IReadOnlyList<OperationDefinition> GetOperations()
    {
        return new List<OperationDefinition>
        {
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
        };
    }
}