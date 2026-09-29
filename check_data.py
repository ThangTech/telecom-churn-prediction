"""
Quick dataset verification script for Iranian Churn Dataset.
Checks: file exists, loads correctly, basic shape and structure.
"""
import pandas as pd

print("=" * 60)
print("IRANIAN CHURN DATASET - QUICK CHECK")
print("=" * 60)

# Load Iranian dataset
df = pd.read_csv('data/raw/Customer Churn.csv')

print('\n1. SHAPE')
print(f'   Rows: {df.shape[0]:,}')
print(f'   Total columns: {df.shape[1]}')

print('\n2. COLUMNS')
for i, col in enumerate(df.columns.tolist(), 1):
    print(f'   {i:2d}. {col}')

print('\n3. TARGET CHECK')
if 'Churn' in df.columns:
    print(f'   ✓ Target "Churn" found')
    print(f'   Unique values: {df["Churn"].unique()}')
    print(f'   Distribution:')
    for val, count in df['Churn'].value_counts().sort_index().items():
        pct = count / len(df) * 100
        print(f'     {val}: {count:,} ({pct:.2f}%)')
else:
    print('   ✗ Target "Churn" NOT FOUND')

print('\n4. MISSING VALUES')
missing_total = df.isnull().sum().sum()
print(f'   Total: {missing_total}')
if missing_total > 0:
    print('   Columns with missing:')
    for col, count in df.isnull().sum()[df.isnull().sum() > 0].items():
        print(f'     {col}: {count}')
else:
    print('   ✓ No missing values')

print('\n5. DUPLICATES')
n_dup = df.duplicated().sum()
print(f'   Duplicate rows: {n_dup}')
if n_dup > 0:
    print(f'   Percentage: {n_dup/len(df)*100:.2f}%')
else:
    print('   ✓ No duplicates')

print('\n6. FIRST 3 ROWS')
print(df.head(3).to_string())

print('\n' + '=' * 60)
print('QUICK CHECK COMPLETE')
print('=' * 60)
