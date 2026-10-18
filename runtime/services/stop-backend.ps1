param(
  [ValidateSet('all','vision','assessment','proxy','records','api')][string]$Kind = 'all',
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
  $interpreter = Resolve-DevelopmentPython -Requested $Python -Kind $Kind -ManagementOnly
  Write-Host "Python: $interpreter"
  & $interpreter -m idl_backend.local.development --action stop --kind $Kind
  exit $LASTEXITCODE
} finally {
  $env:PYTHONPATH = $previousPythonPath
  $env:IDL_REPOSITORY_ROOT = $previousRepository
  $env:PYTHONPYCACHEPREFIX = $previousBytecodeCache
}
