from hypothesis import given
from hypothesis.strategies import lists, integers, data

from ranges import find_overlap
import unittest

class TestInterval(unittest.TestCase):

    @given(data())
    def test_non_overlapping(self, data):
        x1 = data.draw(integers())
        y1 = data.draw(integers(min_value=x1))

        x2 = data.draw(integers(min_value=y1 + 1))
        y2 = data.draw(integers(min_value=x2))

        intervals = [[x1, y1], [x2, y2]]

        assert find_overlap(intervals) == []

    @given(data())
    def test_overlapping(self, data):
        x1 = data.draw(integers())
        y1 = data.draw(integers(min_value=x1 + 1))

        x2 = y1 - 1  
        y2 = x2  

        intervals = [[x1, y1], [x2, y2]]

        assert len(find_overlap(intervals)) > 0

if __name__ == "__main__":
    unittest.main()
