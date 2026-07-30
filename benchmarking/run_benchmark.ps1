# Prepare results file with header
"row_index,success,latency_ms,prediction" | Set-Content -Encoding ascii results.csv

for ($i = 0; $i -lt 25; $i++) {
    # Write payload for this row
    "{`"row_index`": $i}" | Set-Content -Encoding ascii payload.json

    # Invoke Lambda
    aws lambda invoke --function-name benchmark-titanic-endpoint --payload file://payload.json --cli-binary-format raw-in-base64-out output.json | Out-Null

    # Read and parse the output
    $result = Get-Content output.json | ConvertFrom-Json

    $success = $result.success
    $latency = $result.latency_ms
    $prediction = $result.prediction.survived

    # Append to results.csv
    "$i,$success,$latency,$prediction" | Add-Content -Encoding ascii results.csv

    Write-Host "Row $i -> success=$success latency=$latency prediction=$prediction"
}

Write-Host "Done. Results saved to results.csv"
