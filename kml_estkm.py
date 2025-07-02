import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output
import mplcursors

# Load data if not already
try:
    master_df
except NameError:
    master_df = pd.read_excel('task1.xlsx')

# Prepare dataframe
master_df['Est_fuel_Consumed'] = pd.to_numeric(master_df['Est_fuel_Consumed'], errors='coerce')
master_df['Last_Tnx_Kmpl'] = pd.to_numeric(master_df['Last_Tnx_Kmpl'], errors='coerce')
base_df = master_df[(master_df['Est_fuel_Consumed'] <= 90)].dropna(subset=['Est_fuel_Consumed','Last_Tnx_Kmpl','Vehicle_no']).copy()

# Widgets
text_in = widgets.Text(description='Vehicle No:')
output_area = widgets.Output()

# Callback

def handle_submit(change):
    with output_area:
        clear_output(wait=True)
        v = change.value.strip()
        if v == '':
            print('Please enter a vehicle number.')
            return
        vdf = base_df[base_df['Vehicle_no'] == v].copy()
        if vdf.empty:
            print('No records found for vehicle', v)
            return
        if 'Created_date' in vdf.columns:
            vdf['Created_date'] = pd.to_datetime(vdf['Created_date'], errors='coerce')
            vdf = vdf.sort_values('Created_date')
        fig, ax = plt.subplots(figsize=(9,5))
        line, = ax.plot(vdf['Last_Tnx_Kmpl'], vdf['Est_fuel_Consumed'], marker='o', linestyle='-', color='navy')
        ax.set_xlabel('Last Transaction KMPL')
        ax.set_ylabel('Estimated Fuel Consumed (<=70)')
        ax.set_title('Vehicle ' + v + ': KMPL vs Fuel Consumed')
        ax.grid(True)
        mplcursors.cursor(line, hover=True).connect("add", lambda sel: sel.annotation.set_text(
            'Fuel Consumed: ' + str(round(vdf['Est_fuel_Consumed'].iloc[sel.target.index],2)) + '\
KMPL: ' + str(round(vdf['Last_Tnx_Kmpl'].iloc[sel.target.index],2))))
        plt.tight_layout()
        plt.show()
        print(vdf[['Vehicle_no','Last_Tnx_Kmpl','Est_fuel_Consumed']].head())

text_in.on_submit(handle_submit)

display(text_in)
display(output_area)

print('Type a vehicle number and press Enter to generate its graph. Hover over points to see fuel-consumed and KMPL values.')