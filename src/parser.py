class Parser():
    'Simple POC for parser I/O'

    def __init__(self, model):
        self.data = model

    # Example data, see `view`
    map = [
        # line | line | content
        # 0 position of 0 level index
        # 1 position in parent
        [0, 0, 'Master | class'],
        [-1, 0, 'randval | func'],
        [-2, 1, '__init_ | func'],
        None,
        [-2, 0, 'change | func'],
        None
    ]

    def loop(self):
        'For testing purposes takes user input to update model'
        while True:
            update = input('Make a change (format: `3 def __init__(self, newarg):i`):')
            lst = self.parseArgs(update)
            if not lst: # There is nothing recorded on this line; obviously should change later
                continue
            line, val, rel_idx, loc_idx, idxs, txt = lst
            if len(idxs) is 1:
                if txt is not val:
                    self.data.item(idxs[0]).setText(val)
            else:
                child = self.data.item(idxs[0]) # top level parent
                for level in idxs[1:]:
                    child = child.child(level)
                if child.text() is not val:
                    child.setText(val)

    def parseArgs(self, update):
        '''
        Very basic arguments parsing:
        input format is `3 some code`
        where `3` is a line number and the rest is the content of the line
        Returns
        - int line number
        - str val
        - int rel_idx relation of line to previous lines
        - in local_idx index of symbol in its scope
        - idx idx actual index in list
        - str txt redundant with val as long as parser doesn’t parse
        '''
        line = int(update[0])
        val = update[2:]

        if line >= len(self.map) or self.map[line] is None:
            return False

        rel_idx = int(self.map[line][0]) # <= 0
        local_idx = int(self.map[line][1])
        idxs = self.walkIndexes(line)
        txt = self.map[line][2]
        return line, val, rel_idx, local_idx, idxs, txt

    def walkIndexes(self, line, *lst):
        '''
        Determine indexes down the hierarchy
        rel_idx <= 0
        Implementation note: given how python handles memory,
        it probably isn’t necessary to pass idx_list around
        '''
        idx_list = lst[0] if len(lst) > 0 else []
        if self.map[line][0] < 0: # relative index
            parent_line = line + self.map[line][0]
            self.walkIndexes(parent_line, idx_list)

        idx_list += [self.map[line][1]] # local index

        return idx_list


