# DensityCalculator
A web application that measures crowd density

アプリのURL：
https://density-calculator.herokuapp.com/detect_mitsu

GitHubと連携しているため、masterブランチにプッシュすると自動的にHerokuにもデプロイされる。

## スマホアプリの開発

```
cd Client
yarn install // 初回のみ
yarn start
```
表示されたQRコードをスマホのカメラで読み込み、Expoアプリで開く。
QRコードが表示されてから実際にアクセスできるまで結構時間がかかる。
アクセス時にjsのバンドル処理が走るため。
