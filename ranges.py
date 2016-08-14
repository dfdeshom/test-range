from collections import defaultdict
from threading import RLock
 
class RangeDB(object):
    """
    An in-memory database that supports range queries and updates
    """
    def __init__(self):
        self.dict = {}
        self.lock = RLock()
        
    def __str__(self):
        """Print a string representation of all the data in this database."""
        res = []
        for (k,v) in self.dict.iteritems():
            res.append({"identifier":k,"ranges":v})
        return str(res)

    def get(self,key):
        """Get an entry, if it exists."""
        data = self.dict.get(key,[])
        return {"identifier":key, "ranges": data}
    
    def update(self,key, ranges):
        """
        Update an object. An object consists of an identifier (an arbitrary string) 
        and a list of numeric ranges.
        If an object already exists with the same identifier, overwrite it.
        """
        # store a list, overwrite previous value if present
        with self.lock:
            self.dict[key] = ranges
        
    def find_range(self,interval):
        """
        Retrieve a list of objects whose ranges overlap a specified range.
        """
        with self.lock:
            res = []
            for (key,sorted_ranges) in self.dict.iteritems():
                matching_ranges = {}
                match = _find_matching_ranges(sorted_ranges,interval)
                if match:
                    matching_ranges["identifier"] = key
                    matching_ranges["ranges"] = match["match_range"]
                    matching_ranges["intersection"] = _compute_intersection(match["match"])
                    res.append(matching_ranges)
            return res 
    
def _compute_intersection(intersections):
    """Compute the total intersection from start and end points."""
    total = 0
    for m in intersections:
        total += (m[1]-m[0]) + 1
    return total

def _find_matching_ranges(ranges,interval):
    """Find all matching intervals for a set of ranges."""
    res = defaultdict(list)
    for sr in ranges:
        m = find_overlap([sr,interval])
        if m:
            res["match"].append(m)
            res["match_range"].append(sr)
    return res

def find_overlap(intervals):
    """
    Find overlap between 2 intervals, if any
    """
    intervals = sorted(intervals, key=lambda(L):L[0])
    a = intervals[0]
    b = intervals[1]
    start = 0
    end = 0

    # early exit
    if b[0] > a[1]:      
        return []

    if b[0] <= a[1]:
        start = b[0]
    if b[1] >= a[1]:
        end = a[1]
    if b[1] < a[1]:
        end = b[1]

    if start == end:
        return [start,start]

    return [start,end]
  
