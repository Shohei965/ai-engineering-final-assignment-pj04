# QA Summarizer

Google スプレッドシートに蓄積された大量の質問を自動でクラスタリングし、Gemini Flash-2.5 を用いて要約・回答を生成する CLI ツールです。

## 目的 / 背景
講義中に寄せられる 1000 件規模の質問を効率的に処理し、講師が一括で回答できるようにすることを目的としています。

## サービスアカウントの作成手順
1. Google Cloud コンソールで新しいプロジェクトを作成
2. 「サービスアカウント」を作成し、JSON キーをダウンロード
3. 対象のスプレッドシートにサービスアカウントのメールアドレスを閲覧権限で追加
4. `.env` の `GOOGLE_SERVICE_ACCOUNT_FILE` に JSON ファイルのパスを設定

## .env 設定例
```env
GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json
GEMINI_API_KEY=your_gemini_key
CALLS_PER_MINUTE=60
```

## インストール
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 実行例
```bash
python -m qa_summarizer.main --sheet-url "https://docs.google.com/spreadsheets/d/..." --max-questions 500
```

## FAQ
- **レート制限に達した場合**: `CALLS_PER_MINUTE` を減らすか、時間を置いて再実行してください。
- **認証エラー**: サービスアカウントの共有設定とキーのパスを確認してください。

### 質問急増時の注意点
質問数が増えるほどクラスタリング処理に時間が掛かります。レート制限を厳しくすると回答生成に時間が掛かるため、処理速度とのバランスを調整してください。

### 回答品質とスピードのトレードオフ
クラスタ数が多いほど回答の精度は向上しますが、Gemini への呼び出し回数も増え時間が掛かります。`--max-questions` やクラスタリングの閾値を調整して最適なバランスを探してください。
