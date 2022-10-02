### Loading data into Pandas

# Import panda package
import pandas as pd
import re # regular expressions

# Load data
df = pd.read_csv("pokemon_data.csv")                        # load a .csv file
df_xlsx = pd.read_excel("pokemon_data.xlsx")                # load a .xlsx file
df_txt = pd.read_csv("pokemon_data.txt", delimiter = "\t")  # load a .txt file with the tab delimiter

# print loaded data sets
print(df)               # look at the whole data set
print(df.head(10))      # print the first 10 rows
print(df.tail(3))       # print the last 3 rows



### Reading Data in Pandas

# Read Headers
print(df.columns)

# Reach each Column
print(df["Name"]) # pokud chci vytisknout jeden urcity sloupec
print(df[["Name", "Type 1", "Type 2"]]) # pokud chci vytisknout nekolik sloupcu najednou

# Read each Row
# iloc = Integer LOCation
print(df.iloc[1]) # vytisknout radek s indexem 1
print(df.iloc[0:4]) # tytisknout radky 1 - 3

for index, row in df.iterrows():
    print(index, row)

for index, row in df.iterrows():
    print(index, row["Name"])

print(df.loc[df["Type 1"] == "Fire"]) # vytisknout radky, kde Type 1 = "Fire"

# Read a specific location
print(df.iloc[2, 1]) # vytisknout hodnotu v druhem radku a druhem sloupci



### Sorting / Describing Data

# Basic statistical stuff
df.describe()

# print the data frame
df

# sort by name ASC
df.sort_values("Name")

# sort by name DESC
df.sort_values("Name", ascending = False)

# sort by multiple columns ascending
df.sort_values(["Type 1", "HP"])

 # sort by multiple columns descending
df.sort_values(["Type 1", "HP"], ascending = False)

# sort by multiple columns
# type 1 should be ascending (1) and hp descending (0)
df.sort_values(["Type 1", "HP"], ascending = [1, 0])



### Making changes to the data

df["Total"] = df["Attack"] + df["Defense"] # will add a new colum "Total"
df.head(5)

# Drop columns
df = df.drop(columns = ["Total"]) # musim stanovit df znovu
df.head(5)

# axis = 1 -> adding horizontally
# axis = 0 -> adding vertically
# .sum()
df["Total"] = df.iloc[:, 4:10].sum(axis = 1)
df.head(5)

# create a list of columns
cols = list(df.columns.values)
print(cols)

#cols[-1] vyda pouze string, ale potrebuju list, tj. musim mit [cols[-1]]
df = df[cols[0:4] + [cols[-1]] + cols[4:12]]
df.head(5)



### Saving our Data (Exporing into Desired Format

# export df as .csv
# exportiert Daten
df.to_csv("modified.csv")

# ohne indexen in der ersten Spalte exportieren .csv
df.to_csv("modified.csv", index = False)

# ins Excel exportieren
df.to_excel("modified.xlsx", index = False)

# ins .csv exportieren mit dem tabulator als Trennung
df.to_csv("modified.txt", index = False, sep = "\t")



### Filtering Data

# Filtere Reihen, die als Type 1 "Grass" haben
df.loc[df["Type 1"] == "Grass"]

# Filtere Reihen, die als Type 1 "Grass" und als Type 2 "Poison" haben
# Podminky mezi "&" musim rozdelit pomoci kulatych zavorek "()"
df.loc[(df["Type 1"] == "Grass") & (df["Type 2"] == "Poison")]

# Filtere Reihen, die als Type 1 "Grass" ODER als Type 2 "Poison" haben
# Podminky mezi "|" musim rozdelit pomoci kulatych zavorek "()"
df.loc[(df["Type 1"] == "Grass") | (df["Type 2"] == "Poison")]

new_df = df.loc[(df["Type 1"] == "Grass") & (df["Type 2"] == "Poison") & (df["HP"] > 70)]
new_df

# reset indexes
# stary index se ale ulozi
new_df = new_df.reset_index()
new_df

# pokud chci stary index smazat
new_df = new_df.reset_index(drop = True)
new_df

# Vyfiltruje jmena, kt. obsahuji "Mega"
df.loc[df["Name"].str.contains("Mega")]

# vyfiltruje jmena, kt. neobsahuji "Mega" --> pouzit "~"
df.loc[~df["Name"].str.contains("Mega")]

# Najdi pouze pokemony, kt. obsahuji Type 1 "fire" nebo "grass"
# re.I = case insensitive
# regex = Regular Expression
df.loc[df["Type 1"].str.contains("fire|grass", flags = re.I, regex = True)]

# I want all pockemons name including "pi"
# pi[a-z]* -> hledam vyraz(y), kt. zacina "pi" a pak pokracuje pismenem od "a" do "z" a "*" znamena zero or more
df.loc[df["Name"].str.contains("pi[a-z]*", flags = re.I, regex = True)]

# chci vsechny pokemony, kt. zacinaji s "pi"
# pouziji "^" -> "^pi[a-z]*"
df.loc[df["Name"].str.contains("^pi[a-z]*", flags = re.I, regex = True)]



### Conditional Changes

# change the data frame based on the condition
# I want to change the type "Fire" in the column "Type 1" into "Flamer"
df.loc[df["Type 1"] == "Fire", "Type 1"] = "Flamer"
df

# All the "Fire" Pokemons are Legendary = True
df.loc[df["Type 1"] == "Grass", "Legendary"] = True
df

# Jelikoz jsem pozmenilad data, tak uploaduji data znovu
df = pd.read_csv("modified.csv")
df

# Pokud chci zmenit nekolik columns najednou
# Pokud sloupec "Total" je vetsi nez 500, tak zmenim u sloupcu "Generation" a "Legendary" values na "TEST VALUE"
df.loc[df["Total"] > 500, ["Generation", "Legendary"]] = "TEST VALUE"
df

# Pokud sloupec "Total" je vetsi nez 500, tak zmenim u sloupcu "Generation" a "Legendary" values na "Test 1" a "Test 2"
df.loc[df["Total"] < 500, ["Generation", "Legendary"]] = ["Test 1", "Test 2"]
df



### Aggregate Statistics (Groupby)

# Bilde Mittelwert pro Type in der Spalte "Type 1" und sortiere absteigend nach der Spalte "Defense"
df.groupby(["Type 1"]).mean().sort_values("Defense", ascending = False)

df.groupby(["Type 1"]).count()

# pridani sloupc "count" s hodnotou 1
df["count"] = 1
df

df.groupby(["Type 1"]).count()["count"]

# group by multiple variables
df.groupby(["Type 1", "Type 2"]).count()["count"]



### Working with large amounts of data

# chucksize = 5 -> najednou se zpracovava pet radku
# pd.concat -> pokud chci spojit nekolik ruznych souboru
new_df = pd.DataFrame(columns = df.columns) # the columns in new dataframe new_df are the same like in the old data frame

for df in pd.read_csv("modified.csv", chunksize = 5):
    results = df.groupby(["Type 1"]).count()

    new_df = pd.concat([new_df, results])
