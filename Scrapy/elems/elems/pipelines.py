import sqlite3
import copy
import json


class GroupedElementsPipeline:
    def __init__(self):
        self.elems = {}
    
    def process_item(self, item, spiper):
        cg = item['chemical_group']

        if cg not in self.elems:
            self.elems[cg] = {'element_count':0, 'elements': []}
        
        item_copy = copy.deepcopy(item)
        del item_copy['chemical_group']

        self.elems[cg]['elements'].append(dict(item_copy))
        self.elems[cg]['element_count'] += 1
        return item
    
    def close_spider(self, spider):
        with open('grouped_elements.json', 'w') as f:
            json.dump(self.elems, f, indent=2)



class ElemsPipeline:
    def __init__(self) -> None:
        self.con = sqlite3.connect('periodic_elements.db')
        self.cursor = self.con.cursor()

    def open_spider(self, spider):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS periodic_elements (
                                symbol TEXT PRIMARY KEY,
                                name TEXT,
                                atomic_number INTEGER,
                                atomic_mass REAL,
                                chemical_group TEXT
                            )
                            """)
        self.con.commit()
        
    def process_item(self, item, spider):
        self.cursor.execute("""
                            INSERT INTO periodic_elements VALUES (?, ?, ?, ?, ?)
                            """, (
                            item['symbol'],
                            item['name'],
                            item['atomic_number'],
                            item['atomic_mass'],
                            item['chemical_group'],
                        ))
        self.con.commit()
        return item

    def close_spider(self, spider):
        self.con.close()