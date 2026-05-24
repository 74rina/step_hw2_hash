from hash_table import HashTable
import random

cache_capacity = 10

class Item:
    # 'key': The key of the item. The key must be a string.
    # 'value': The value of the item.
    # 'next': The next item in the linked list. If this is the last item in the
    #         linked list, 'next' is None.
    # 'prev': 双方向リストに拡張
    def __init__(self, key, value, next, prev):
        self.key = key
        self.value = value
        self.next = next
        self.prev = prev
  
            
class Cache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.hash_table = HashTable()
        
        # 双方向連結リストの初期化
        self.head = Item(None, None, None, None)
        self.tail = Item(None, None, None, None)       
        self.head.next = self.tail
        self.tail.prev = self.head
        
    def visit(self, url, web_page):
        node, found = self.hash_table.get(url)
        
        if found:
            assert type(node) == Item
            
            initial_node = self.head.next # 現在の最初ノードを退避
            self.head.next = node
            node.prev = self.head
            node.next = initial_node
            initial_node.prev = node

            if self.hash_table.size() > self.capacity:  
                self.hash_table.delete(self.tail.prev.key)
                
                last_node = self.tail.prev # 現在の末尾ノードを記憶
                last_node.prev.next = self.tail
                self.tail.prev = last_node
            
        else:
            new_node = Item(url, web_page, None, None)
            
            initial_node = self.head.next # 現在の最初ノードを退避
            self.head.next = new_node
            new_node.prev = self.head
            new_node.next = initial_node
            initial_node.prev = new_node
            
            self.hash_table.put(new_node.key, new_node)
            if self.hash_table.size() > self.capacity:
                self.hash_table.delete(self.tail.prev.key)

def main():
    cache = Cache(cache_capacity)

    while True:
        accessed_url = input("URLを入力してください(str)")
        
        web_page = random.randint(1, 1000) # 簡単のため 1-1000 の整数で表す
        
        cache.visit(accessed_url, web_page)
        
        print(cache.hash_table.buckets) # キャッシュを表示

if __name__ == "__main__":
    main()