import pandas as pd
import os

PICKLE_FILE = 'data/articles_database.pkl'
PICKLE_FILE_DUPLICATES = 'data/articles_database_duplicates.pkl'

def update_database(new_df):
    if os.path.exists(PICKLE_FILE):
        existing_df = pd.read_pickle(PICKLE_FILE)
    else:
        existing_df = pd.DataFrame(columns=new_df.columns)
    
    new_links = new_df['Source URL'].isin(existing_df['Source URL'])
    
    articles_to_add = new_df[~new_links]
    
    updated_df = pd.concat([existing_df, articles_to_add], ignore_index=True)
    
    if len(articles_to_add):
        print(f'Database updated: {len(articles_to_add)} articles added. There are now {len(updated_df)} articles in total.')
    else:
        print(f'No changes made to database.')
    print(40*'-')
    
    #print(updated_df)
    updated_df.to_pickle(PICKLE_FILE)
    
    
def update_database_with_duplicates(new_df):
    if os.path.exists(PICKLE_FILE_DUPLICATES):
        existing_df = pd.read_pickle(PICKLE_FILE_DUPLICATES)
    else:
        existing_df = pd.DataFrame(columns=new_df.columns)

    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    print(f'Database updated: {len(new_df)} articles added. There are now {len(updated_df)} articles in total.')
    print(40*'-')
    updated_df.to_pickle(PICKLE_FILE_DUPLICATES)

    
    