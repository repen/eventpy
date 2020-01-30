from . import lockguard

class LinkedListNode :
    def __init__(self, data = None) :
        self._data = data
        self._previous = None
        self._next = None
        
    def getData(self) :
        return self._data
        
    def setData(self, data) :
        self._data = data

# need Lock        
class LinkedList :
    def __init__(self, lock) :
        self._lock = lock
        self._head = None
        self._tail = None
        
    def getHead(self) :
        return self._head
        
    def getTail(self) :
        return self._tail
    
    def append(self, node) :
        with lockguard.LockGuard(self._lock) :
            if self._head == None :
                self._head = node
                self._tail = node
            else :
                node._previous = self._tail
                self._tail._next = node
                self._tail = node

    def prepend(self, node) :
        with lockguard.LockGuard(self._lock) :
            if self._head == None :
                self._head = node
                self._tail = node
            else :
                node._next = self._head
                self._head._previous = node
                self._head = node

    def insert(self, node, beforeNode) :
        with lockguard.LockGuard(self._lock) :
            node._previous = beforeNode._previous
            node._next = beforeNode
            if beforeNode._previous != None :
                beforeNode._previous._next = node
            beforeNode._previous = node
            if beforeNode == self._head :
                self._head = node