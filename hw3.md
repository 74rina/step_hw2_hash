# メモ

cache = {url: webページ} 要素数X
新たなサイトを閲覧したとき、
bucketsを更新するが、
lru: queueにしてpopleftする
lfu: bucketsで登場回数が一番少ないものをreplaceする

目標：「もっとも直近にアクセスされた上位 X 個の <URL, Web ページ> の組が保存できるデータ構造」を作ればよい
与えられた <URL, Web ページ> があるかないかを検索
もしない場合、キャッシュ内で一番古い <URL, Web ページ> を捨てて、
代わりに与えられた <URL, Web ページ> を追加する

どの <URL, Web ページ> が一番古いかを O(1) で知るために、
ハッシュテーブルに工夫を加えて <URL, Web ページ> をアクセスされた順に並べておけばよい

↑ハッシュテーブルだけだと順序を管理できない（新たなサイトを閲覧したとき
どれを捨てるか判断できない）ので、他のデータ構造を組み合わせる
fifo: queue
lru: 連結リスト

# Cacheクラス

## 1. 初期化

- 訪問履歴の「新→古」順の双方向連結リスト Item()
  - key (urlの文字列)

  - value (web_page)

  - next, prev (Item)

- size（連結リストのノード数）

- capacity（連結リストの最大容量）

- urlとリストノードの対応表 hash_table = HashTable()

を用意する。

## 2. Webサイトを訪問した時の処理 visit(url, web_page)

url を hash_table から検索する。O(1)

- 見つかった場合
  1. そのノードを連結リストから削除する O(1)
  2. そのノードを連結リストの最初に挿入する O(1)
  3. ノードの value を web_page に更新する

- 見つからなかった場合
  1. 新たなノード（key=url, value=web_page）を作る
  2. そのノードを連結リストの最初に挿入する O(1)

連結リストの要素数 size が、最大容量 capacity を超えたら、

1. 連結リストの末尾のノードを削除する O(1)
2. その末尾ノード（とそのキー）を hash_table から削除する O(1)

## 3. 連結リストの最初にノードを挿入する insert_front(node)

head.next で最初のノード initial_node を取得し、

1. initial_node の prev を更新
2. 挿入するノード node の next を更新
3. head.next を挿入するノードにする

## 4. 連結リストのノードを削除する delete(node)

1. 削除するノードの prev, next を取得
2. prev_node.next および next_node.prev を更新
3. 削除するノードの prev, next を None にする

## 5. 連結リストの末尾のノードを削除する delete_last()

tail.prev で末尾のノードを取得し、それを delete(node) する。O(1)
