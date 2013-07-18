
# DataProxy Plugin for Hyde

```
# * yamlにキーが見つからないなどのエラーフック
#   - validation 機構?
#   - エラーはちゃんとエラーを出す => loggerの使用
# * 生成するタイミング
#   - 新規ファイル
#   - 既存のファイル: テンプレートが更新された || データファイルが更新された
#   - 更新のためのファイル検出機能が対応していないので不可能(coreに手を入れないと無理)
# * deployされていないとserveで not found エラー
#   - serveの仕組み上, coreに手を入れないとFIXは不可能 => 運用でカバー

## DONE
# * templates を ignore する
#   - target list から除外するには
#   - 今は適当なデータで出力しちゃってる
```



