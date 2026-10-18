param(
  [ValidateSet('frontend','backend','agent-demo','courses','all')][string]$Kind = 'frontend',
  [string]$Python = $env:IDL_PYTHON
)
$ErrorActionPreference = 'Stop'
$repository = Split-Path -Parent $PSScriptRoot
$npm = if (Get-Command npm.cmd -ErrorAction SilentlyContinue) { 'npm.cmd' } else { 'npm' }
if ($Kind -in @('courses','all')) {
  # Shuku validation uses only the standard library; do not require backend packages.
  $coursePython = if ($Python) { $Python } else { 'python' }
  Write-Host 'Checking Shuku package: courses/modules'
  & $coursePython (Join-Path $PSScriptRoot 'tools/checks/validate_shuku_skill.py') (Join-Path $repository 'courses/modules')
  if ($LASTEXITCODE) { throw 'Shuku validation failed: courses/modules' }
}
foreach ($project in @('frontend','agent-demo')) {
  if ($Kind -in @($project,'all')) {
    & $npm --prefix (Join-Path $repository "environment/$project") run build
    if ($LASTEXITCODE) { throw "$project build failed." }
  }
}
if ($Kind -in @('backend','all')) {
  . (Join-Path $repository 'environment/backend/development-python.ps1')
  $interpreter = Resolve-DevelopmentPython -Requested $Python -ManagementOnly
  $previousPath = $env:PYTHONPATH
  $previousRepository = $env:IDL_REPOSITORY_ROOT
  $previousBytecodeCache = $env:PYTHONPYCACHEPREFIX
  try {
    $env:PYTHONPATH = (Join-Path $repository 'runtime/backend/src') + [IO.Path]::PathSeparator + (Join-Path $repository 'creater-skills/tools/python') + [IO.Path]::PathSeparator + $previousPath
    $env:IDL_REPOSITORY_ROOT = $repository
    $env:PYTHONPYCACHEPREFIX = Join-Path $repository 'runtime/data/cache/python'
    & $interpreter -m pytest (Join-Path $PSScriptRoot 'tests') -q -o "cache_dir=$(Join-Path $repository 'runtime/data/cache/pytest')"
    if ($LASTEXITCODE) { throw 'Backend tests failed.' }
    & $interpreter -m idl_authoring.identity --check
    if ($LASTEXITCODE) { throw 'Module identity validation failed.' }
  } finally {
    $env:PYTHONPATH = $previousPath
    $env:IDL_REPOSITORY_ROOT = $previousRepository
    $env:PYTHONPYCACHEPREFIX = $previousBytecodeCache
  }
}
