import re
import glob
from typing import Literal

import pandas as pd
import tqdm

DATA_DIR='data'

def parse_tables(pct_or_number:Literal['n','p']):

    parsed_dfs =  []

    files = glob.glob(f'{DATA_DIR}/*_{pct_or_number}.html')

    with tqdm.tqdm(total=len(files)) as pbar:

        for file in files:
            dfs = pd.read_html(file)
            year = re.sub(r'\D','',file)
            # sort by length and pick the longest
            df = sorted(dfs, key=lambda x: len(x), reverse=True)[0]
            df['Year'] = int(year)
            # remove all rows where rank is not a number
            df = df[df['Rank'].apply(lambda x: x.isnumeric())]

            # rename linebreaks and extra spaces
            df = df.rename(columns=lambda x: re.sub(r'\s+',' ',x))
            df = df.rename(columns=lambda x: re.sub(r'\n','',x))
            # if "Percent of total males" column exists then rename it
            try:
                df = df.rename(columns={"Percent of total males": 'PctOfMaleBirths'})
                df = df.rename(columns={"Percent of total females": 'PctOfFemaleBirths'})
            except TypeError as e:
                print(e)
                pass

            try:
                df = df.rename(columns={"Number of males": 'NumMaleBirths'})
                df = df.rename(columns={"Number of females": 'NumFemaleBirths'})
            except:
                pass

            df = df.reset_index(drop=True)

            # convert all rows with numbers to int
            for col in df.columns:
                if df[col].dtype == object:
                    try:
                        df[col] = df[col].astype(int)
                    except ValueError:
                        pass

            m = df.columns.values[2]



            parsed_dfs.append(df)
            pbar.update()

    df = pd.concat(parsed_dfs)
    return df


if __name__ == '__main__':
    dfn = parse_tables('n')
    dfp = parse_tables('p')


    df = pd.merge(dfp,dfn,how='outer',on=['Year','Rank','Male name','Female name'])
    df = df.sort_values(by=['Year','Rank'])

    df.to_csv('names_1887-2023.csv',index=False)