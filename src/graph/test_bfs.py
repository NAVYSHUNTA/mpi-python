import unittest
from bfs import *

class TestPrime(unittest.TestCase):
    def test_bfs_connected_graph_complete_graph(self):
        """連結なグラフに対するテスト（完全グラフ）"""
        n = 4
        m = 6
        edges = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
        expected = [1, 1, 1]
        self.assertEqual(expected, bfs(n, m, edges))

    def test_bfs_connected_graph(self):
        """連結なグラフに対するテスト"""
        n = 8
        m = 8
        edges = [[0, 1], [0, 6], [1, 2], [2, 3], [3, 4], [3, 5], [5, 7], [6, 7]]
        expected = [1, 2, 3, 4, 3, 1, 2]
        self.assertEqual(expected, bfs(n, m, edges))

    def test_bfs_disconnected_graph_small(self):
        """非連結なグラフに対するテスト（小規模）"""
        n = 4
        m = 3
        edges = [[0, 1], [0, 3], [1, 3]]
        expected = [1, -1, 1]
        self.assertEqual(expected, bfs(n, m, edges))

    def test_bfs_disconnected_graph_middle(self):
        """非連結なグラフに対するテスト（中規模）"""
        n = 9
        m = 9
        edges = [[0, 1], [1, 2], [1, 4], [2, 3], [3, 4], [4, 5], [6, 7], [6, 8], [7, 8]]
        expected = [1, 2, 3, 2, 3, -1, -1, -1]
        self.assertEqual(expected, bfs(n, m, edges))


# エントリポイント
if __name__ == "__main__":
    unittest.main()
