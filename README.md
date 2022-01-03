# ft-api-scripts

42 APIで遊ぶためのスクリプト集。

## 必要物

- Python >= 3.8
- [Poetry](https://python-poetry.org/docs/)
- [42 APIのUID, Secret](https://api.intra.42.fr/apidoc/guides/getting_started)

## 使い方

### インストール

1. リポジトリをclone

   ```bash
   git clone https://github.com/nafuka11/ft-api-scripts.git
   ```

1. 必要なパッケージをインストール

   ```bash
   cd ft-api-scripts
   poetry install --no-root
   ```

1. `.env` に42 APIのclient UID, Secretを記載する。

   `.env.example` を `.env` としてコピーし、
   ```bash
   cp .env.example .env
   ```
   `.env` 内の `your_uid` と `your_secret` をご自身のUID, Secretに書き換えてください。

### 各種スクリプト

#### login毎のレビュー数を表示するスクリプト

##### ヘルプ

```bash
poetry run python srcs/scale_teams.py -h
```

##### 例

campus_id=26, cursus_id=21,28,50のscale_teamsのデータをjsonに保存

```bash
poetry run python srcs/scale_teams.py dump --campus_id 26 --cursus_id 21 28 50
```

scale_teamsのjsonから、login毎のレビュー数をcsv出力

```bash
poetry run python srcs/scale_teams.py count scale_teams_yyyymmdd-HHMM.json
```

csvを元にヒストグラム作成

```
poetry run python srcs/scale_teams.py visualize correctors.csv
```

#### 指定loginがレビューした/された時に付けたflagを表示するスクリプト

![screenshot](docs/user_scale_teams.png)

##### ヘルプ

```bash
poetry run python srcs/user_scale_teams.py -h
```

##### 例

login=your_login, cursus_id=21,28,50のscale_teamsのデータをjsonに保存

```bash
poetry run python srcs/user_scale_teams.py dump --cursus_id 21 28 50 -- your_login
```

scale_teamsのjsonから、login=your_loginが付けた/付けられたflagを表示

```bash
poetry run python srcs/user_scale_teams.py count your_login user_scale_teams_your_login_yyyymmdd-HHMM.json
```

#### 各campusのBH率と学生数を表示するスクリプト

![screenshot](docs/campus.png)

##### ヘルプ
```bash
poetry run python srcs/campus.py -h
```

##### 例
cursus_id=21, range[begin_at]="2021-01-01T00:00:00.000Z,2042-12-31T23:59:59.999Z" の cursus_users のデータを取得
```bash
poetry run python srcs/campus.py dump --cursus_id 21 --begin_at 2021-01-01T00:00:00.000Z 2042-12-31T23:59:59.999Z
```
- 以下のファイルが出力されます。
  - `campus.json`
  - `cursus_users_cursusid_{cursusid}_campusid_{campusid}.json`

`cursus_users_cursusid_21_campusid_*.json` からBH率をカウントする
```bash
poetry run python srcs/campus.py count data/campus.json data/cursus_users_cursusid_21_campusid_*.json
```
- 以下のファイルが出力されます。
  - `campus_blackholed.csv`

`campus_blackholed.csv` からBH率と学生数を表示する
```bash
poetry run python srcs/campus.py visualize data/campus_blackholed.csv
```
