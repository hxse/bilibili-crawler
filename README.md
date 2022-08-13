$biliPath="D:\bilibili"

Function ydb {
yt-dlp -o $biliPath\"%(uploader)s/%(upload_date)s %(playlist)s/%(title)s %(id)s.%(ext)s"  -i $args[0] 
}

Function cydb {
cd "D:\my_repo\bilibili-crawler"
pdm run python main.py gb $args[0] | ConvertFrom-Json |Select -ExpandProperty data|ForEach {ydb $_.url}
}