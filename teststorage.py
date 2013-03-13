import unittest
from storedserver.basestorage import BaseStorage



class TestStorageCase(unittest.TestCase):

    def setUp(self):
        self.dict = BaseStorage()

    def test_with_replace(self):
        self.dict.add('data','val')
        self.assertEquals('val',self.dict.get('data'))
        self.dict.add('data','val2')
        self.assertEquals('val2',self.dict.get('data'))
        self.dict.delete('data')
        self.assertEquals(None,self.dict.get('data'))
        self.dict.add('data','val')
        self.dict.add('data2','val2')
        self.assertEquals(2,len(self.dict.keys()))
   
    def test_without_replace(self):
        self.dict.replace = False
        self.dict.add('data','val')
        self.dict.add('data','val2')
        self.assertEquals(['val','val2'],self.dict.get( 'data' ))
        self.dict.delete('data')
        self.assertEquals(None,self.dict.get('data'))

    def test_keys(self):
        self.dict.add('data','val')
        self.assertEquals(1,len(self.dict.keys()))

       

if __name__ == '__main__':
     unittest.main()

