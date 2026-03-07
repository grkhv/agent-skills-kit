# Hook PreToolUse for WebFetch
# Fetches content via markdown.new (clean markdown, saves tokens)
# On failure: fallback to standard WebFetch (exit 0, no output)
# markdown.new limit: 500 requests/day per IP

param()

[Console]::InputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'SilentlyContinue'

try {
    $inputJson = $input | Out-String
    $hookData = $inputJson | ConvertFrom-Json
    $url = $hookData.tool_input.url

    if (-not $url) {
        exit 0
    }

    $body = @{ url = $url; method = 'auto' } | ConvertTo-Json -Compress
    $response = Invoke-WebRequest -Uri 'https://markdown.new/' `
        -Method Post `
        -ContentType 'application/json' `
        -Body $body `
        -TimeoutSec 15 `
        -UseBasicParsing

    if ($response.StatusCode -ne 200) {
        exit 0
    }

    # markdown.new returns JSON: {"success":true,"url":"...","title":"...","content":"..."}
    $parsed = $response.Content | ConvertFrom-Json

    if (-not $parsed.success -or -not $parsed.content) {
        exit 0
    }

    $markdown = $parsed.content
    if ($markdown.Length -lt 50) {
        exit 0
    }

    $title = $parsed.title
    $contextText = "Content fetched via markdown.new ($title):`n$markdown"

    $output = @{
        hookSpecificOutput = @{
            hookEventName = 'PreToolUse'
            permissionDecision = 'allow'
            additionalContext = $contextText
        }
    } | ConvertTo-Json -Depth 3 -Compress

    Write-Output $output
    exit 0

} catch {
    exit 0
}
