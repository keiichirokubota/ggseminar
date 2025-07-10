import re
import requests

def get_arxiv_info(arxiv_id):
    """
    arXiv IDに基づいて論文のタイトルと著者を取得します。
    """
    base_url = "http://export.arxiv.org/api/query?"
    query = f"id_list={arxiv_id}"
    response = requests.get(base_url + query)
    
    if response.status_code == 200:
        # XMLレスポンスからタイトルと著者を抽出
        title_match = re.search(r"<title>(.*?)</title>", response.text)
        author_match = re.findall(r"<name>(.*?)</name>", response.text)
        
        title = title_match.group(1).strip().replace('\n', ' ') if title_match else "タイトル不明"
        authors = ", ".join(author_match) if author_match else "著者不明"
        return title, authors
    else:
        print(f"arXiv ID {arxiv_id} の情報取得に失敗しました。ステータスコード: {response.status_code}")
        return "タイトル不明", "著者不明"

def update_arxiv_links(filename="index.markdown"):
    """
    index.markdownファイル内のarXivリンクを論文情報で更新します。
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # \arxiv{****}のパターンを検索してカウント
        arxiv_pattern = r"\\arxiv\{([^}]+)\}"
        matches = re.findall(arxiv_pattern, content)
        
        if not matches:
            print("\\arxiv{****} のパターンが見つかりませんでした。")
            return
        
        print(f"{len(matches)}個のarXiv IDが見つかりました: {matches}")
        
        # 各マッチについて置換を実行
        for arxiv_id in matches:
            print(f"arXiv ID: {arxiv_id} の情報を取得中...")
            title, authors = get_arxiv_info(arxiv_id)
            
            # 置換文字列を作成（Markdownリンク形式）
            replacement = f"[{arxiv_id}](https://arxiv.org/abs/{arxiv_id}) - {authors} - {title}"
            
            # 元のパターンを置換
            old_pattern = f"\\arxiv{{{arxiv_id}}}"
            content = content.replace(old_pattern, replacement)
            
            print(f"置換完了: {old_pattern} -> {replacement[:100]}...")
        
        # ファイルに書き戻し
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"{filename} が正常に更新されました。")

    except FileNotFoundError:
        print(f"エラー: ファイル '{filename}' が見つかりません。")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    # 使用例
    print("arXiv情報取得・更新スクリプトを開始します...")
    update_arxiv_links()