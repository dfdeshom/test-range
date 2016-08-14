import ui
import unittest

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        ui.app.config['TESTING'] = True
        self.app = ui.app.test_client()

    def tearDown(self):
        pass

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'[]' in rv.data    

    def test_write(self):
        rv = self.app.post('/write',data={'{"identifier":"data", "ranges":["1","4"]}':""})
        assert b'success' in rv.data    

    def test_ranges(self):
        self.app.post('/write',data={'{"identifier":"data1", "ranges":["1","4"]}':""})
        self.app.post('/write',data={'{"identifier":"data2", "ranges":["100","400"]}':""})
        self.app.post('/write',data={'{"identifier":"data3", "ranges":["33","75"]}':""})

        # empty range
        rv = self.app.get("/ranges?range=[76,99]")
        assert '[]' in rv.data

        # overlap with data3
        rv = self.app.get("/ranges?range=[40,50]")
        assert 'data3' in rv.data

        # overlap with data1
        rv = self.app.get("/ranges?range=[-20,2]")
        assert 'data1' in rv.data

        # overlap with all
        rv = self.app.get("/ranges?range=[-200,401]")
        assert 'data1' in rv.data
        assert 'data2' in rv.data
        assert 'data3' in rv.data

    def test_get(self):
        self.app.post('/write',data={'{"identifier":"data1", "ranges":["1","4"]}':""})
        rv = self.app.get("/get?identifier=data1")
        assert 'data1' in rv.data

    def test_index(self):
        self.app.post('/write',data={'{"identifier":"data1", "ranges":["1","4"]}':""})
        self.app.post('/write',data={'{"identifier":"data2", "ranges":["1","4"]}':""})
        
        rv = self.app.get("/")
        assert 'data1' in rv.data
        assert 'data2' in rv.data
        assert 'data3' not in rv.data
        
if __name__ == '__main__':
    unittest.main()
