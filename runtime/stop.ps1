param(
  [ValidateSet('frontend','agent-demo','records','vision','proxy','assessment','api','backend','all')][string]$Kind = 'all',
  [string]$Python = $env:IDL_PYTHON
)
$ErrorActionPreference = 'Stop'
foreach ($previewKind in @('frontend','agent-demo')) {
  if ($Kind -in @('all', $previewKind)) {
    & node (Join-Path $PSScriptRoot 'services/preview.mjs') --kind $previewKind --stop
    if ($LASTEXITCODE) { throw 'Preview stop failed.' }
  }
}
if ($Kind -notin @('frontend','agent-demo')) {
  if ($Kind -eq 'all' -and -not (Test-Path -LiteralPath (Join-Path $PSScriptRoot 'data/logs/development.json'))) { return }
  $backendKind = if ($Kind -in @('all','backend')) { 'all' } else { $Kind }
  & (Join-Path $PSScriptRoot 'services/stop-backend.ps1') -Kind $backendKind -Python $Python
  if ($LASTEXITCODE) { throw 'Backend stop failed.' }
}
