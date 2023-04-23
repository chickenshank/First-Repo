from pathlib import Path

import pandas as pd
import datetime
import PySimpleGUI as sg

sg.theme('LightGreen5')

current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
EXCEL_FILE = current_dir / 'employee_database.xlsx'
df = pd.read_excel(EXCEL_FILE)

#update the employee count by counting number of rows in database
employee_count = len(df)

# Define the main layout
layout = [
    [sg.Text('Name:', size=(20,1)), sg.InputText(key='Name')],
    [sg.Text('Date of Hire:', size=(20,1)), sg.InputText(key='Date of Hire', tooltip='Format: MM/DD/YYYY')],
    [sg.Text('Position:', size=(20,1)), sg.InputText(key='Position')],
    [sg.Text('Date of Termination:', size=(20,1)), sg.InputText(key='Date of Termination', tooltip='Format: MM/DD/YYYY')],
    [sg.Text('Pay Rate:', size=(20,1)), sg.InputText(key='Pay Rate')],
    [sg.Text('Notes:', size=(20,1)), sg.Multiline(size=(45,3), key='Notes')],
    [sg.Button('Submit'), sg.Button('View Database'), sg.Button('Exit')],
    [sg.Text('Employee Count:', size=(15,1)), sg.Text('0', size=(10,1), key='Employee Count')],
]

# Create the main window
window = sg.Window('Employee Database', layout, finalize=True)

# load the existing data from excel file
try:
    df = pd.read_excel('employee_database.xlsx')
    employee_count = len(df.index)
    window['Employee Count'].update(employee_count)
except FileNotFoundError:
    df = pd.DataFrame(columns=['Name', 'Date of Hire', 'Position', 'Date of Termination', 'Pay Rate', 'Notes'])


# create PySimpleGUI layout for database view window
db_layout = [
    [sg.Table(values=df.to_dict('records'), headings=list(df.columns), max_col_width=25, auto_size_columns=True,
              justification='center', num_rows=min(25, len(df.index))), sg.Button('Close')],
]

# create database view window
db_window = sg.Window('Employee Database - View', db_layout)

# clear input function
def clear_input():
    window['Name'].update('')
    window['Date of Hire'].update('')
    window['Position'].update('')
    window['Date of Termination'].update('')
    window['Pay Rate'].update('')
    window['Notes'].update('')

# function to calculate the length of employment
def get_employment_length(date):
    today = datetime.date.today()
    employment_length = (today - date).days
    years = employment_length // 365
    months = (employment_length % 365) // 30
    days = (employment_length % 365) % 30
    return f"{years} years, {months} months, {days} days"

# function to create a new record
def create_new_record(values, df):
    # check if the "Date of Hire" field is a valid date
    try:
        hire_date = datetime.datetime.strptime(values['Date of Hire'], '%m/%d/%Y').date()
    except ValueError:
        sg.popup('Please enter a valid date of hire (MM/DD/YYYY)')
    
    # check if the "Date of Termination" field is a valid date
    if values['Date of Termination']:
        try:
            termination_date = datetime.datetime.strptime(values['Date of Termination'], '%m/%d/%Y').date()
        except ValueError:
            sg.popup('Please enter a valid date of termination (MM/DD/YYYY)')
    else:
        termination_date = None
    
    # convert "Pay Rate" to a float
    try:
        pay_rate = float(values['Pay Rate'])
    except ValueError:
        sg.popup('Please enter a valid pay rate')
    
    # create new record and append to dataframe
    new_record = pd.DataFrame({
        'Name': [values['Name']],
        'Date of Hire': [hire_date],
        'Position': [values['Position']],
        'Date of Termination': [termination_date],
        'Pay Rate': [pay_rate],
        'Notes': [values['Notes']]
    })
    
    # calculate the length of employment
    employment_length = get_employment_length(hire_date)
    
    # add the length of employment to the new record
    new_record = new_record.assign(**{'Length of Employment': employment_length})
    
    # add the new record to the main dataframe
    df = df._append(new_record, ignore_index=False)
        
    return df

## main event loop ##
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    for key in values:
        window[key]('')
    if event == 'Submit':
        # check if the "Date of Hire" field is a valid date
        try:
            date_of_hire = datetime.datetime.strptime(values['Date of Hire'], '%m/%d/%Y').date()
        except ValueError:
            sg.popup('Please enter a valid date (MM/DD/YYYY) for Date of Hire')
            continue
        
        # check if the "Date of Termination" field is a valid date
        if values['Date of Termination']:
            try:
                date_of_termination = datetime.datetime.strptime(values['Date of Termination'], '%m/%d/%Y').date()
            except ValueError:
                sg.popup('Please enter a valid date (MM/DD/YYYY) for Date of Termination')
                continue
        else:
            date_of_termination = None
       
        # update the employee db
        df = create_new_record(values, df)
        sg.popup('Employee added successfully')
        clear_input()

    # update the employee count after each entry
    window['Employee Count'].update(len(df))

    ### "View" button event ###
    
    if event == 'View Database':
        # update the dataframe in case new records have been added
        try:
            df = pd.read_excel(EXCEL_FILE)
        except FileNotFoundError:
            sg.popup('No database found')
            continue
        
        # create PySimpleGUI layout for database view window
        db_layout = [
            [sg.Table(values=df.to_dict('records'), headings=list(df.columns), max_col_width=25, auto_size_columns=True,
                      justification='center', num_rows=min(25, len(df.index))), sg.Button('Close')],
        ]
        
        # create database view window
        db_window = sg.Window('Employee Database - View', db_layout)
        
        # event loop for database view window
        while True:
            db_event, db_values = db_window.read()
            if db_event == sg.WIN_CLOSED or db_event == 'Close':
                break

# remove duplicate rows from df
df.drop_duplicates(subset=['Name', 'Date of Hire', 'Position', 'Date of Termination', 'Pay Rate', 'Notes'], inplace=True)       

# save data to excel file
df.to_excel(EXCEL_FILE, index=True, index_label='ID')

window.close()
db_window.close()
