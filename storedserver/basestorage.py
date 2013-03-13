"""
BaseStorage is an abstraction for a dictionary
meant to store values depending if the user wants to append values to a list or
replace the values
"""
class BaseStorage(object):

    def __init__(self,replace=True):
        self.dict = {}
        self.replace = replace


    def add(self,k,v):
        if k not in self.dict:
            self.dict[k] = v
            print 'keys ' + ''.join(self.dict.keys())
        elif( self.replace ):
            self.dict[k] = v

        elif k in self.dict:
            v_original = self.dict[k]
            if( isinstance(v,list) ):
                for item in v:
                    v_original.append(item)
            else:
                newlist = []
                newlist.append(v_original)
                newlist.append(v)
                self.dict[k]=newlist
    
    def delete(self,k):
       self.dict[k] = None


    def get(self,k):
       if k in self.dict :
          return self.dict[k]
       return None

    def keys(self):
       return self.dict.keys()
    def entries(self):
        return self.dict.items()
