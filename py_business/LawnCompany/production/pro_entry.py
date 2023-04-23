from pathlib import Path

import PySimpleGUI as sg
import pandas as pd
import datetime

# Add some color to the window
sg.theme('LightGreen5')

# excel file path and name
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
EXCEL_FILE = current_dir / 'production.xlsx'
df = pd.read_excel(EXCEL_FILE)

# All the stuff for the entry form.
layout = [ 
    [sg.Text('Please fill out the following fields:')],
    [sg.Text('Date', size=(15,1)), sg.InputText(key='Date')],
    [sg.Text('Crew Lead', size=(15,1)), sg.InputText(key='Crew Lead')],
    [sg.Text('Crew Size', size=(15,1)), sg.InputText(key='Crew Size')],
    [sg.Text('Mowing', size=(45,1), font='Helvetica 12 bold', justification='center')],
    [sg.Text('Service Type', size=(15,1)), sg.Combo(['Mowing', 'Leaves', 'Other'], size=(30,3), key='Mowing Service Type')],   
    [sg.Text('Properties Done', size=(15,1)), sg.InputText(key='Properties Done')],
    [sg.Text('Sales', size=(15,1)), sg.InputText(key='Sales')],
    [sg.Text('Labor', size=(15,1)), sg.InputText(key='Labor')],
    [sg.Text('Landscaping', size=(45,1), font='Helvetica 12 bold', justification='center')],
    [sg.Text('Service Type', size=(15,1)), sg.Combo(['Mulch', 'Planting', 'Seed', 'Sod', 'Drainage', 'Tear-Out', 'Install', 'Clean-Up', 'Other'], size=(30,3), key='Landscape Service Type')],
    [sg.Text('Hours Quoted', size=(15,1)), sg.InputText(key='Hours Quoted')],
    [sg.Text('Hours Used', size=(15,2)), sg.InputText(key='Hours Used')],
    [sg.Text('Weed Treatment', size=(45,1), font='Helvetica 12 bold', justification='center')],
    [sg.Text('Service Type', size=(15,1)), sg.Combo(['Spraying', 'Fertilizer', 'Other'], size=(30,3), key='Spray Service Type')], 
    [sg.Text('Product Used', size=(15,1)), sg.Combo(['Round-up', 'Diaquat', 'Suregaurd', 'Mix'], key='Product Used')],
    [sg.Text('Product Amount', size=(15,1)), sg.InputText(key='Product Amount')],
    [sg.Text('Sales', size=(15,1)), sg.InputText(key='Other Sales')],
    [sg.Text('Jobber Times', size=(15,1)), sg.InputText(key='Jobber times')],
    [sg.Text('Notes', size=(45,1), font='Helvetica 12 bold', justification='center')],
    [sg.Multiline(default_text='', size=(65, 4), no_scrollbar='True', key='Notes')],
    [sg.Submit(), sg.Button('Clear'), sg.Exit()]
]

# window title
window = sg.Window('Production Sheet Entry', layout)

# clear input function
def clear_input():
    for key in values:
        window[key]('')
    return None

# main event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear':
        clear_input()
    if event == 'Submit':
        # check if the "Date" field is a valid date
        if values['Date'] == '':
            sg.popup('Please enter a date')
            continue
        try:
            date = datetime.datetime.strptime(values['Date'], '%m/%d/%Y').date()
        except ValueError:
            sg.popup('Please enter a valid date (MM/DD/YYYY)')
            continue
        
        # convert other fields to integers or floats
        crew_size = properties_done = hours_quoted = hours_used = jobber_times = 0
        sales = labor = product_amount = other_sales = 0.0
        if values['Crew Size'] != '':
            try:
                crew_size = int(values['Crew Size'])
            except ValueError:
                sg.popup('Please enter an integer for Crew Size')
                continue
        if values['Properties Done'] != '':
            try:
                properties_done = int(values['Properties Done'])
            except ValueError:
                sg.popup('Please enter an integer for Properties Done')
                continue
        if values['Sales'] != '':
            try:
                sales = float(values['Sales'])
            except ValueError:
                sg.popup('Please enter a number for Sales')
                continue
        if values['Labor'] != '':
            try:
                labor = float(values['Labor'])
            except ValueError:
                sg.popup('Please enter a number for Labor')
                continue
        if values['Hours Quoted'] != '':
            try:
                hours_quoted = float(values['Hours Quoted'])
            except ValueError:
                sg.popup('Please enter a number for Hours Quoted')
                continue
        if values['Hours Used'] != '':
            try:
                hours_used = float(values['Hours Used'])
            except ValueError:
                sg.popup('Please enter a number for Hours Used')
                continue
        if values['Product Amount'] != '':
            try:
                product_amount = float(values['Product Amount'])
            except ValueError:
                sg.popup('Please enter a number for Product Amount')
                continue
        if values['Other Sales'] != '':
            try:
                other_sales = float(values['Other Sales'])
            except ValueError:
                sg.popup('Please enter a number for Other Sales')
                continue
        if values['Jobber times'] != '':
            try:
                jobber_times = float(values['Jobber times'])
            except ValueError:
                sg.popup('Please enter a number for Jobber times')
                continue
        
        # create new record and append to dataframe
        new_record = pd.DataFrame({
            'Date': [date],
            'Crew Lead': [values['Crew Lead']],
            'Crew Size': [crew_size],
            'Mowing Service Type': [values['Mowing Service Type']],
            'Properties Done': [properties_done],
            'Sales': [sales],
            'Labor': [labor],
            'Landscape Service Type': [values['Landscape Service Type']],
            'Hours Quoted': [hours_quoted],
            'Hours Used': [hours_used],
            'Spray Service Type': [values['Spray Service Type']],
            'Product Used': [values['Product Used']],
            'Product Amount': [product_amount],
            'Other Sales': [other_sales],
            'Jobber times': [jobber_times],
            'Notes': [values['Notes']]
        })
        df = pd.concat([df, new_record], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data saved!')
        clear_input()

window.close()


