import datetime

def main():
    # 今日の日付と時刻を取得
    now = datetime.datetime.now()
    output_content = f"スクリプトが実行されました: {now}\n"

    # ファイルに結果を書き込む
    with open("output.txt", "a") as f: # "a" で追記モード
        f.write(output_content)
    
    print("output.txtに結果が書き込まれました。")

if __name__ == "__main__":
    main()