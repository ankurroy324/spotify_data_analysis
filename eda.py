import json

notebook_path = 'c:/Users/ankur/Downloads/dataanalysisproject2/spotify.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 1. Update data loading cell
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "pd.read_csv('cardata.csv')" in source:
            cell['source'] = [
                "df = pd.read_csv('music.csv')\n",
                "print(df.head(10))"
            ]
            # Clear outputs as they are stale
            cell['outputs'] = []
            break

# 2. Remove cells related to cardata.csv specific columns (Car ID, etc.)
# We will filter out cells that reference 'Car ID', 'car_id', 'car_age'
new_cells = []
for cell in nb['cells']:
    keep_cell = True
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "Car ID" in source or "car_id" in source or "car_age" in source or "df.columns.str.lower()" in source:
             keep_cell = False
    if keep_cell:
        new_cells.append(cell)

nb['cells'] = new_cells

# 3. Add popularity categorization logic
# Find where to insert (e.g., after df.info() or df.describe())
insert_index = -1
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "df.describe" in source:
            insert_index = i + 1
            break

if insert_index == -1:
    insert_index = len(nb['cells'])

popularity_cell = {
    "cell_type": "code",
    "execution_count": None,
    "id": "popularity_category",
    "metadata": {},
    "outputs": [],
    "source": [
        "def categorize_poularity(popularity):\n",
        "    if popularity < 30:\n",
        "        return 'Low'\n",
        "    elif popularity < 70:\n",
        "        return 'Medium'\n",
        "    else:\n",
        "        return 'High'\n",
        "\n",
        "df['popularity_category'] = df['track_popularity'].apply(categorize_poularity)\n",
        "print(df[['track_popularity', 'popularity_category']].head())"
    ]
}

nb['cells'].insert(insert_index, popularity_cell)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook updated successfully.")
