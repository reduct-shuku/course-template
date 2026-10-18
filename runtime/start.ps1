param(
  [ValidateSet('frontend','agent-demo','records','vision','proxy','assessment','api','backend','all')][string]$Kind = 'frontend',
  [switch]$Status,
  [int]$Port = 0,
  [string]$Course = '',
  [ValidateSet('auto','cpu','cuda','mps')][string]$Device = 'auto',
  [string]$Python = $env:IDL_PYTHON
)
$ErrorActionPreference = 'Stop'
if ($Port -and $Kind -in @('all','backend')) { throw '-Port requires a single service.' }
if ($Kind -in @('frontend','agent-demo','all')) {
  $previewKind = if ($Kind -eq 'all') { 'frontend' } else { $Kind }
  $previewArguments = @((Join-Path $PSScriptRoot 'services/preview.mjs'), '--kind', $previewKind)
  if ($Status) { $previewArguments += '--status' }
  if ($Port) { $previewArguments += @('--port', "$Port") }
  & node @previewArguments
  if ($LASTEXITCODE) { throw 'Preview command failed.' }
}
if ($Kind -notin @('frontend','agent-demo')) {
  $backendKind = if ($Kind -in @('all','backend')) { 'all' } else { $Kind }
  & (Join-Path $PSScriptRoot 'services/start-backend.ps1') -Kind $backendKind -Status:$Status -Port $Port -Course $Course -Device $Device -Python $Python
  if ($LASTEXITCODE) { throw 'Backend command failed.' }
}
