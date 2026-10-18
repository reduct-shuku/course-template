param(
  [switch]$Status,
  [ValidateSet('all','vision','assessment','proxy','records','api')][string]$Kind = 'all',
  [int]$Port = 0,
  [string]$Course = '',
  [ValidateSet('auto','cpu','cuda','mps')][string]$Device = 'auto',
  [string]$Python = $env:IDL_PYTHON
)
$ErrorActionPreference = 'Stop'
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$sourcePath = Join-Path $repoRoot 'runtime\backend\src'
$previousPythonPath = $env:PYTHONPATH
$previousRepository = $env:IDL_REPOSITORY_ROOT
$previousBytecodeCache = $env:PYTHONPYCACHEPREFIX
. (Join-Path $repoRoot 'environment/backend/development-python.ps1')
try {
  $env:IDL_REPOSITORY_ROOT = $repoRoot
  $env:PYTHONPYCACHEPREFIX = Join-Path $repoRoot 'runtime/data/cache/python'
  $env:PYTHONPATH = if ($previousPythonPath) { "$sourcePath;$previousPythonPath" } else { $sourcePath }
  $serviceAction = if ($Status) { 'status' } else { 'start' }
  $serviceArguments = @('-m','idl_backend.local.development','--action',$serviceAction,'--kind',$Kind,'--device',$Device)
  if ($Port) { $serviceArguments += @('--port',"$Port") }
  if ($Course) { $serviceArguments += @('--course',$Course) }
  $interpreter = Resolve-DevelopmentPython -Requested $Python -Kind $Kind -ManagementOnly:$Status
  Write-Host "Python: $interpreter"
  & $interpreter @serviceArguments
  exit $LASTEXITCODE
} finally {
  $env:PYTHONPATH = $previousPythonPath
  $env:IDL_REPOSITORY_ROOT = $previousRepository
  $env:PYTHONPYCACHEPREFIX = $previousBytecodeCache
}
