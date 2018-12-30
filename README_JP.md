## 免責事項: 使用はすべて自己責任でお願いします。

## 機能:
温度管理
湿度表示

# Todo:
データログ取得
OTAアップデート

## セットアップ:
1. `sudo apt-get update && sudo apt-get install -y git` でGitをインストールする。  
2. このレポジトリーをクローンする `git clone https://github.com/sotakan/RPi-Incubator.git`
3. クローンしたレポジトリーに移動する　`cd RPi-Incubator`
4. セットアップ用のスクリプトを実行可能にする `sudo chmod a+x installer.sh`
5. `./installer.sh`でセットアップ用のスクリプトを実行する
6. `sudo python incubator.py` 又は `./exec.sh`でインキュベーターのスクリプトを実行する  
*6のコマンドを[crontab](https://qiita.com/tossh/items/e135bd063a50087c3d6a)に設定をすると起動時に自動的に実行されるようになります*
