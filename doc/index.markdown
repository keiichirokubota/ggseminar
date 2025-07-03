---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
title: "GG Seminar 2024"

---

## ようこそ、私のブログへ！

ここでは、最新の投稿や特別な情報を提供しています。

---

### 最新の投稿

{% for post in site.posts limit:3 %}
* [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.date | date: "%Y年%m月%d日" }}
{% endfor %}

---

[私についてもっと知る](/about/)
