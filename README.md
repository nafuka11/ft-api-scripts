# ft-api-scripts

42 APIで遊ぶためのスクリプト集。

## 必要物

- Python >= 3.8
- Poetry

## 使い方

### インストール

1. リポジトリをclone
   ```bash
   git clone https://github.com/nafuka11/ft-api-scripts.git
   ```
2. 必要なパッケージをインストール
   ```bash
   cd ft-api-scripts
   poetry install --no-root
   ```
3. `.env` に42 APIのclient uid, secretを記載する。
   ```bash
   echo 'FT_CLIENT_UID="your_uid"' >> .env
   echo 'FT_CLIENT_SECRET="your_secret"' >> .env
   ```

### 各種スクリプト

```bash
# scale_teams系のスクリプト
poetry run python src/scale_teams.py -h
```

#### 例
```bash
# campus_id=26, cursus_id=21,28,50のscale_teamsのデータをjsonに保存
poetry run python src/scale_teams.py dump --campus_id 26 --cursus_id 21 28 50
# scale_teamsのjsonから、login毎のreview数をcsv出力
poetry run python src/scale_teams.py count scale_teams_yyyymmdd-hhmm.json
# csvを元にヒストグラム作成
poetry run python src/scale_teams.py visualize correctors.csv
```
