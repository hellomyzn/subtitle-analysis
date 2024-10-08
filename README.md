# Subtitle analysis
This is for subtitle analysis.
- [Subtitle analysis](#subtitle-analysis)
    - [docker commands](#docker-commands)
    - [start](#start)
    - [containers](#containers)
    - [vscode settings](#vscode-settings)
    - [References](#references)
      - [NLTK](#nltk)
      - [Subtitles](#subtitles)
      - [English](#english)

### docker commands
```bash
# run as production (docker-compose up -d --build)
$ make up
# run as develop (docker-compose -f docker-compose-dev.yml up -d --build)
$ make dev
# get into a container (docker-compose exec python bash)
$ make python
# down (docker-compose down)
$ make down
# destroy (docker-compose down --rmi all --volumes --remove-orphans)
$ make destroy
```

### start
1. run container
```bash
$ make up
```
2. reopen in container in vscode
![start_vscode](./docs/images/start_vscode.png)

3. set up [WakaTime](https://wakatime.com/) API key ([link](https://wakatime.com/settings/api-key))
![wakatime_api_key](./docs/images/wakatime_api_key.png)

4. copy `src/common/config/config.template.ini` to `src/common/config/config.ini`
```bash
cp src/common/config/config.template.ini src/common/config/config.ini
cp src/common/config/config.template.ini src/common/config/config.dev.ini
```

### containers
- python
  - python container to exec
- vscode
  - for dev containers in vscode
- plantuml
  - for sequences


### vscode settings
How do I press and hold a key and have it repeat in VSCode?
```bash
$ defaults write com.microsoft.VSCode ApplePressAndHoldEnabled -bool false
```

### References
#### NLTK
- [英語の文章から自動で、単語帳を生成するプログラムを作ってみた](https://qiita.com/ryoheiroi/items/f443e2aaafebb042d189)
- [NLTKの使い方をいろいろ調べてみた](https://qiita.com/m__k/items/ffd3b7774f2fde1083fa)
- [Python 3: NLTKを用いた自然言語処理](https://qiita.com/KentOhwada_AlibabaCloudJapan/items/3c9130a2a28498baf93f)
#### Subtitles
- [Subtitleseeker](https://subtitleseeker.in/)
- [YTS Subs](https://yts-subs.com/)
- [TVsubs](https://www.tvsubs.net/)
#### English
- [英語の群前置詞100語まとめ！一覧と使い方を例文を使ってわかりやすく説明します](https://toiguru.jp/group-preposition)
