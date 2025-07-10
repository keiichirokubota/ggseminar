import re
import arxiv

# index.markdown を読み込む
with open('docs/index.markdown', 'r', encoding='utf-8') as f:
    content = f.read()

# \arxiv{****} をすべて探す
pattern = r'\\arxiv\{([\d\.]+)\}'
arxiv_ids = re.findall(pattern, content)

for arxiv_id in set(arxiv_ids):  # 重複は一回だけ処理
    # arxivパッケージで検索
    search = arxiv.Search(id_list=[arxiv_id])
    result = next(search.results(), None)
    if result is None:
        print(f'Not found: {arxiv_id}')
        continue

    # 著者名とタイトル
    authors = ', '.join(author.name for author in result.authors)
    title = result.title.replace('\n', ' ').strip()

    # 置換後の文字列
    replacement = f'[arXiv:{arxiv_id}](https://arxiv.org/abs/{arxiv_id})  \n{authors}  \n_"{title}"_'

    # 元のテキストを置換
    content = re.sub(rf'\\arxiv\{{{re.escape(arxiv_id)}\}}', replacement, content)

# 上書き保存
with open('docs/index.markdown', 'w', encoding='utf-8') as f:
    f.write(content)

print('置換完了！')
