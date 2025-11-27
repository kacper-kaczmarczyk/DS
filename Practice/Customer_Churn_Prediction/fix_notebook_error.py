import json

nb_path = r'c:\Users\konta\OneDrive\IT\DS\Practice\Customer_Churn_Prediction\analyze.ipynb'

try:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    found = False
    for i, cell in enumerate(nb['cells']):
        source = cell.get('source', [])
        source_text = "".join(source)
        if "if df[col].unique() == ['Yes', 'No']:" in source_text:
            print(f"Found problematic code in cell index {i}")
            # Fix the code
            new_source = []
            for line in source:
                if "if df[col].unique() == ['Yes', 'No']:" in line:
                    new_source.append("    # Fixed comparison to handle numpy array and potential order/missing values\n")
                    new_source.append("    unique_vals = set(df[col].dropna().unique())\n")
                    new_source.append("    if unique_vals == {'Yes', 'No'}:\n")
                else:
                    new_source.append(line)
            
            cell['source'] = new_source
            found = True
            break
    
    if found:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=4)
        print("Fixed the notebook.")
    else:
        print("Could not find the problematic code in the notebook file.")

except Exception as e:
    print(f"Error: {e}")
