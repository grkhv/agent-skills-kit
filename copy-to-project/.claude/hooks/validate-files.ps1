# Хук PostToolUse для Edit/Write
# Валидирует .json и .md файлы после редактирования
# При ошибке — возвращает decision:block с описанием проблемы

param()

# Форсируем UTF-8 для ввода/вывода
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$ErrorActionPreference = 'SilentlyContinue'

try {
    $inputJson = $input | Out-String
    $hookData = $inputJson | ConvertFrom-Json

    $filePath = $hookData.tool_input.file_path
    if (-not $filePath) { exit 0 }
    if (-not (Test-Path $filePath)) { exit 0 }

    $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
    $errors = @()

    # --- Валидация JSON ---
    if ($ext -eq '.json') {
        try {
            $content = Get-Content -Path $filePath -Raw -Encoding UTF8
            $null = $content | ConvertFrom-Json -ErrorAction Stop
        } catch {
            $msg = $_.Exception.Message
            $errors += "JSON: невалидный синтаксис - $msg"
        }
    }

    # --- Валидация Markdown ---
    if ($ext -eq '.md') {
        $content = Get-Content -Path $filePath -Raw -Encoding UTF8

        # Проверка: незакрытые блоки кода
        $fencePattern = '(?m)^```'
        $fenceCount = ([regex]::Matches($content, $fencePattern)).Count
        if ($fenceCount % 2 -ne 0) {
            $errors += 'Markdown: незакрытый блок кода'
        }

        # Проверка: пустые ссылки
        $emptyLinkPattern = '\[[^\]]+\]\(\s*\)'
        if ($content -match $emptyLinkPattern) {
            $errors += 'Markdown: ссылка с пустым URL'
        }

        # Проверка: битые @imports
        $importPattern = '(?m)^@(\S+)'
        $importMatches = [regex]::Matches($content, $importPattern)
        foreach ($m in $importMatches) {
            $importPath = $m.Groups[1].Value
            $resolvedPath = Join-Path (Split-Path $filePath -Parent) $importPath
            if (-not (Test-Path $resolvedPath)) {
                $projectRoot = $env:CLAUDE_PROJECT_DIR
                if ($projectRoot) {
                    $resolvedPath = Join-Path $projectRoot $importPath
                }
                if (-not (Test-Path $resolvedPath)) {
                    $errors += "Markdown: @import - файл не найден - @$importPath"
                }
            }
        }
    }

    # --- Результат ---
    if ($errors.Count -gt 0) {
        $errorText = $errors -join '; '
        $result = @{
            decision = 'block'
            reason = "Валидация $filePath : $errorText"
        }
        $result | ConvertTo-Json -Depth 3 -Compress | Write-Output
        exit 0
    }

    exit 0

} catch {
    # Ошибка хука - не блокируем
    exit 0
}
