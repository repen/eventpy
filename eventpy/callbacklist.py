import eventpy.lock as lock
import eventpy.internal.linkedlist as linkedlist
import eventpy.internal.lockguard as lockguard

class CallbackList :
    class NodeData :
        def __init__(self, callback, counter) :
            self._callback = callback
            self._counter = counter

    def __init__(self, lockClass = lock.Lock) :
        self._lockClass = lockClass
        self._lock = self._lockClass()
        self._list = linkedlist.LinkedList(self._lock)
        self._currentCounter = 0

    def empty(self) :
        return self._list.empty()

    def append(self, callback) :
        node = linkedlist.LinkedListNode(CallbackList.NodeData(callback, self._getNextCounter()))
        self._list.append(node)
        return node

    def prepend(self, callback) :
        node = linkedlist.LinkedListNode(CallbackList.NodeData(callback, self._getNextCounter()))
        self._list.prepend(node)
        return node

    def insert(self, callback, before) :
        node = linkedlist.LinkedListNode(CallbackList.NodeData(callback, self._getNextCounter()))
        self._list.insert(node, before)
        return node

    def remove(self, node) :
        node.getData()._counter = 0
        self._list.remove(node)
        
    def forEach(self, func) :
        with lockguard.LockGuard(self._lock) :
            node = self._list.getHead()
        counter = self._currentCounter
        while node != None :
            nodeCounter = node.getData()._counter
            if nodeCounter != 0 and counter >= nodeCounter :
                func(node.getData()._callback)
            with lockguard.LockGuard(self._lock) :
                node = node._next

    def forEachIf(self, func) :
        with lockguard.LockGuard(self._lock) :
            node = self._list.getHead()
        counter = self._currentCounter
        while node != None :
            nodeCounter = node.getData()._counter
            if nodeCounter != 0 and counter >= nodeCounter :
                if not func(node.getData()._callback) :
                    return False
            with lockguard.LockGuard(self._lock) :
                node = node._next
        return True
        
    def __call__(self, *args, **kwargs) :
        with lockguard.LockGuard(self._lock) :
            node = self._list.getHead()
        counter = self._currentCounter
        while node != None :
            nodeCounter = node.getData()._counter
            if nodeCounter != 0 and counter >= nodeCounter :
                node.getData()._callback(*args, **kwargs)
            with lockguard.LockGuard(self._lock) :
                node = node._next

    def _getNextCounter(self) :
        self._currentCounter += 1
        result = self._currentCounter
        if result == 0 : # overflow, let's reset all nodes' counters.
            with lockguard.LockGuard(self._lock) :
                node = self._list.getHead()
                while node != None :
                    node.getData()._counter = 1
                    node = node.getNext()
            self._currentCounter += 1
            result = self._currentCounter

        return result

