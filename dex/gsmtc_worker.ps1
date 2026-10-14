param(
    [string]$Action = "query",
    [double]$PositionSeconds = 0
)

Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager, Windows.Media, ContentType = WindowsRuntime]

function Invoke-WinRTTask($asyncOp, $type) {
    $asTaskGeneric = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
        $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
    } | Select-Object -First 1
    $asTask = $asTaskGeneric.MakeGenericMethod($type)
    $task = $asTask.Invoke($null, @($asyncOp))
    return $task.GetAwaiter().GetResult()
}

try {
    $async = [Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager]::RequestAsync()
    $mgr = Invoke-WinRTTask $async ([Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager])
    $session = $mgr.GetCurrentSession()
    
    if (-not $session) {
        $sessions = $mgr.GetSessions()
        if ($sessions.Count -gt 0) {
            $session = $sessions[0]
        }
    }

    if (-not $session) {
        Write-Output '{"has_session":false}'
        exit 0
    }

    if ($Action -eq "query") {
        $props = Invoke-WinRTTask ($session.TryGetMediaPropertiesAsync()) ([Windows.Media.Control.GlobalSystemMediaTransportControlsSessionMediaProperties])
        $info = $session.GetPlaybackInfo()
        $timeline = $session.GetTimelineProperties()

        $obj = @{
            has_session = $true
            app_id = $session.SourceAppId
            title = $props.Title
            artist = $props.Artist
            album = $props.AlbumTitle
            playback_status = $info.PlaybackStatus.ToString()
            can_play = $info.Controls.IsPlayEnabled
            can_pause = $info.Controls.IsPauseEnabled
            can_next = $info.Controls.IsNextEnabled
            can_previous = $info.Controls.IsPreviousEnabled
            can_fast_forward = $info.Controls.IsFastForwardEnabled
            can_rewind = $info.Controls.IsRewindEnabled
            position = if ($timeline) { $timeline.Position.TotalSeconds } else { 0 }
            duration = if ($timeline) { $timeline.EndTime.TotalSeconds } else { 0 }
        }
        $obj | ConvertTo-Json -Compress
    }
    elseif ($Action -eq "play_pause") {
        $info = $session.GetPlaybackInfo()
        if ($info.PlaybackStatus -eq [Windows.Media.Control.GlobalSystemMediaTransportControlsSessionPlaybackStatus]::Playing) {
            $res = Invoke-WinRTTask ($session.TryPauseAsync()) ([System.Boolean])
        } else {
            $res = Invoke-WinRTTask ($session.TryPlayAsync()) ([System.Boolean])
        }
        Write-Output ("{`"success`":" + ($res.ToString().ToLower()) + "}")
    }
    elseif ($Action -eq "next") {
        $res = Invoke-WinRTTask ($session.TrySkipNextAsync()) ([System.Boolean])
        Write-Output ("{`"success`":" + ($res.ToString().ToLower()) + "}")
    }
    elseif ($Action -eq "previous") {
        $res = Invoke-WinRTTask ($session.TrySkipPreviousAsync()) ([System.Boolean])
        Write-Output ("{`"success`":" + ($res.ToString().ToLower()) + "}")
    }
    elseif ($Action -eq "fast_forward") {
        $info = $session.GetPlaybackInfo()
        if ($info.Controls.IsFastForwardEnabled) {
            $res = Invoke-WinRTTask ($session.TryFastForwardAsync()) ([System.Boolean])
            Write-Output ("{`"success`":" + ($res.ToString().ToLower()) + "}")
        } else {
            Write-Output '{"success":false,"unsupported":true}'
        }
    }
    elseif ($Action -eq "rewind") {
        $info = $session.GetPlaybackInfo()
        if ($info.Controls.IsRewindEnabled) {
            $res = Invoke-WinRTTask ($session.TryRewindAsync()) ([System.Boolean])
            Write-Output ("{`"success`":" + ($res.ToString().ToLower()) + "}")
        } else {
            Write-Output '{"success":false,"unsupported":true}'
        }
    }
    elseif ($Action -eq "seek") {
        $ticks = [long]($PositionSeconds * 10000000)
        $timeSpan = [System.TimeSpan]::FromTicks($ticks)
        $res = Invoke-WinRTTask ($session.TryChangePlaybackPositionAsync($timeSpan.Ticks)) ([System.Boolean])
        Write-Output ("{`"success`":" + ($res.ToString().ToLower()) + "}")
    }
}
catch {
    Write-Output ('{"has_session":false,"error":' + ($_ | ConvertTo-Json -Compress) + '}')
}
