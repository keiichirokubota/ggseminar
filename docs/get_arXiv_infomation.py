import re
import arxiv

# 1. index.markdown を読み込む
with open('docs/index.markdown', 'r', encoding='utf-8') as f:
    content = f.read()

# 2. \arxiv{****} をすべて探す
pattern = r'\\arxiv\{([\d\.]+)\}'
arxiv_ids = re.findall(pattern, content)
unique_ids = list(set(arxiv_ids)) # 重複を排除したリスト
print(f'Found {len(arxiv_ids)} arXiv IDs ({len(unique_ids)} unique).')

if unique_ids:
    # クライアントはループの外で1度だけ定義（今回は一括取得するのでディレイも不要に）
    client = arxiv.Client()
    
    # ★ 改善ポイント: 全てのIDを1回のリクエストでまとめて問い合わせる
    search = arxiv.Search(id_list=unique_ids)
    
    try:
        # 3. 取得した結果を処理する
        for result in client.results(search):
            arxiv_id = result.entry_id.split('/abs/')[-1].split('v')[0] # URLから純粋なIDを抽出
            
            # 著者名とタイトル
            authors = ', '.join(author.name for author in result.authors)
            title = result.title.replace('\n', ' ').strip()

            # 置換後の文字列
            replacement = f'[arXiv:{arxiv_id}](https://arxiv.org/abs/{arxiv_id})  \n{authors}  \n_{title}_'
            print(f'Replacing {arxiv_id} with info...')

            # 元のテキストを置換
            content = re.sub(rf'\\arxiv\{{{re.escape(arxiv_id)}\}}', lambda _: replacement, content)
            
    except arxiv.HTTPError as e:
        print(f"\nエラーが発生しました。arXivの制限にかかっている可能性があります。: {e}")
        print("5分ほど待ってから再実行してください。")
        exit(1)

# 4. 上書き保存
with open('docs/index.markdown', 'w', encoding='utf-8') as f:
    f.write(content)

print('置換完了！')

# import re
# import arxiv

# # index.markdown を読み込む
# with open('docs/index.markdown', 'r', encoding='utf-8') as f:
#     content = f.read()

# # \arxiv{****} をすべて探す
# pattern = r'\\arxiv\{([\d\.]+)\}'
# arxiv_ids = re.findall(pattern, content)
# print(f'Found {len(arxiv_ids)} arXiv IDs.')

# for arxiv_id in set(arxiv_ids):  # 重複は一回だけ処理
#     # arxivパッケージで検索
#     client = arxiv.Client()

#     search = arxiv.Search(id_list=[arxiv_id])
#     result = next(client.results(search), None)
#     if result is None:
#         print(f'Not found: {arxiv_id}')
#         continue

#     # 著者名とタイトル
#     authors = ', '.join(author.name for author in result.authors)
#     title = result.title.replace('\n', ' ').strip()

#     # 置換後の文字列
#     replacement = f'[arXiv:{arxiv_id}](https://arxiv.org/abs/{arxiv_id})  \n{authors}  \n_{title}_'
#     print(f'Replacing {arxiv_id} with: {replacement}')

#     # 元のテキストを置換
#     # use a function as repl to avoid backreference/backslash escapes in replacement
#     content = re.sub(rf'\\arxiv\{{{re.escape(arxiv_id)}\}}', lambda _: replacement, content)
# # 
# # 上書き保存
# with open('docs/index.markdown', 'w', encoding='utf-8') as f:
#     f.write(content)

# print('置換完了！')
