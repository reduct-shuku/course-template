param(
  [ValidateSet('frontend','backend','agent-demo','all')][string]$Kind = 'frontend',
  [string]$Python = $env:IDL_PYTHON
)
$ErrorActionPreference = 'Stop'
$repository = Split-Path -Parent $PSScriptRoot
$npm = if (Get-Command npm.cmd -ErrorAction SilentlyContinue) { 'npm.cmd' } else { 'npm' }
Push-Location $repository
try {
  if ($Kind -in @('frontend','all')) {
    & $npm --prefix (Join-Path $PSScriptRoot 'frontend') ci
    if ($LASTEXITCODE) { throw 'Frontend installation failed.' }
  }
  if ($Kind -in @('agent-demo','all')) {
    & $npm --prefix (Join-Path $PSScriptRoot 'agent-demo') ci
    if ($LASTEXITCODE) { throw 'Agent demo installation failed.' }
  }
  if ($Kind -in @('backend','all')) {
    $interpreter = if ($Python) { $Python } else { 'python' }
    & $interpreter -c 'import sys; assert sys.version_info >= (3,10), "Python 3.10+ is required"'
    if ($LASTEXITCODE) { throw 'Select Python 3.10+ with -Python or IDL_PYTHON.' }
    $venv = Join-Path $PSScriptRoot 'backend/.venv'
    if (-not (Test-Path -LiteralPath $venv)) {
      & $interpreter -m venv $venv
      if ($LASTEXITCODE) { throw 'Virtual environment creation failed.' }
    }
    $localPython = Join-Path $venv 'Scripts/python.exe'
    if (-not (Test-Path -LiteralPath $localPython)) { $localPython = Join-Path $venv 'bin/python' }
    & $localPython -m pip install -e './environment/backend[vision,projection,assessment,dev,tools,test]'
    if ($LASTEXITCODE) { throw 'Backend installation failed.' }
  }
} finally { Pop-Location }
