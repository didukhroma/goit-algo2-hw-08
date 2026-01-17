import random
import time


class Node:
    def __init__(self, key, value):
        self.data = (key, value)
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def push(self, key, value):
        new_node = Node(key, value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        return new_node

    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = None
        node.next = None

    def move_to_front(self, node):
        if node is None or node == self.head:
            return
        self.remove(node)
        node.next = self.head
        if self.head:
            self.head.prev = node
        else:
            self.tail = node
        node.prev = None
        self.head = node

    def remove_last(self):
        if self.tail:
            last = self.tail
            self.remove(last)
            return last
        return None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.list = DoublyLinkedList()

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.list.move_to_front(node)
            return node.data[1]
        return -1

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.data = (key, value)
            self.list.move_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                last = self.list.remove_last()
                if last:
                    del self.cache[last.data[0]]
            new_node = self.list.push(key, value)
            self.cache[key] = new_node
        return

    def clear(self):
        self.cache = {}
        self.list = DoublyLinkedList()


def range_sum_no_cache(a, left, right):
    return sum(a[left : right + 1])


def update_no_cache(a, idx, val):
    a[idx] = val


def range_sum_with_cache(a, left, right, cache):
    key = (left, right)
    cached_sum = cache.get(key)
    if cached_sum != -1:
        return cached_sum

    cached_sum = range_sum_no_cache(a, left, right)
    cache.put(key, cached_sum)
    return cached_sum


def update_with_cache(a, idx, val, cache):
    a[idx] = val
    cache.clear()


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [
        (random.randint(0, n // 2), random.randint(n // 2, n - 1))
        for _ in range(hot_pool)
    ]
    queries = []
    for _ in range(q):
        if random.random() < p_update:  # ~3% запитів — Update
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:  # ~97% — Range
            if random.random() < p_hot:  # 95% — «гарячі» діапазони
                left, right = random.choice(hot)
            else:  # 5% — випадкові діапазони
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries


if __name__ == "__main__":
    n = 100000
    q = 50000
    k = 1000

    a = [random.randint(1, 100) for _ in range(n)]
    queries = make_queries(n, q)

    t1 = time.time()
    for q in queries:
        if q[0] == "Range":
            range_sum_no_cache(a, q[1], q[2])
        else:
            update_no_cache(a, q[1], q[2])
    print(f"Without cache: {time.time() - t1:.2f} seconds.  ")

    lru_cache = LRUCache(k)
    t2 = time.time()
    for q in queries:
        if q[0] == "Range":
            range_sum_with_cache(a, q[1], q[2], lru_cache)
        else:
            update_with_cache(a, q[1], q[2], lru_cache)
    print(f"LRU-cache: {time.time() - t2:.2f} seconds")
