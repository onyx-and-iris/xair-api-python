Function RunTests {
    "Running tests in directory $PSScriptRoot" | Write-Host
    $coverage = Join-Path $PSScriptRoot "pytest_coverage.log"
    $run_tests = "pytest -v $PSScriptRoot --capture=tee-sys --junitxml=$(Join-Path $PSScriptRoot ".coverage.xml")"
    $match_pattern = "^=|^\s*$|^Running|^Using|^plugins|^collecting|^tests"

    if ( Test-Path $coverage ) { Clear-Content $coverage }

    ForEach ($line in $(Invoke-Expression $run_tests)) {
        If ( $line -Match $match_pattern ) {
            if ( $line -Match "^Running tests for kind \[(\w+)\]" ) { $kind = $Matches[1] }
            $line | Tee-Object -FilePath $coverage -Append 
        }
    }
    Write-Output "$(Get-TimeStamp)" | Out-File $coverage -Append

    Invoke-Expression "genbadge tests -t 90 -i $(Join-Path $PSScriptRoot ".coverage.xml") -o $(Join-Path $PSScriptRoot "$kind.svg")"
}

Function Get-TimeStamp {
    
    return "[{0:MM/dd/yy} {0:HH:mm:ss}]" -f (Get-Date)
    
}

if ($MyInvocation.InvocationName -ne ".") {
    Invoke-Expression ".\.venv\Scripts\Activate.ps1"

    RunTests

    Invoke-Expression "deactivate"
}