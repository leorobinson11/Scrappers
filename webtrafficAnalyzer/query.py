import os

def CreateSearchtermTable(db, searchterm):
    columns = ''
    for country in os.listdir('cleaned_lists'):
        columns += country.replace('.csv', '') +' int, '
    columns = columns[:-2] 
    db.engine.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {searchterm} (
            date DATE Primary key, {columns}
        );
        '''
    )

def InsertValues(db, table, values):
    formated_values = ''
    for value in values:
        formated_values += str(value) + ', '
    formated_values = formated_values[:-2]
    db.engine.execute(
        f'''
        INSERT OR REPLACE INTO {table}
        VALUES ({formated_values})
        '''
    )

def QueryValues(db, table):
    return db.engine.execute(
        f'''
        SELECT * FROM {table};
        '''
    )