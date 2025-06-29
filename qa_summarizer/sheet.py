import pandas as pd

def fetch_questions(sheet_url: str, max_questions: int):
    # 編集用 URL → CSV エクスポート用 URL に変換
    if '/edit' in sheet_url:
        sheet_url = sheet_url.split('/edit')[0] + '/export?format=csv'
    df = pd.read_csv(sheet_url)
    # カラム名を統一 ("質問" → "Question")
    if '質問' in df.columns:
        df.rename(columns={'質問':'Question'}, inplace=True)
    if 'Question' not in df.columns:
        df.rename(columns={df.columns[0]:'Question'}, inplace=True)
    df = df.head(max_questions)
    try:
        sheet_id = sheet_url.split('/d/')[1].split('/')[0]
    except:
        sheet_id = ''
    modified_time = ''
    return df, sheet_id, modified_time
