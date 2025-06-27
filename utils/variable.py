from datetime import date, datetime, time
import json
import os
import base64

import streamlit as st
from utils.cryptograph import encrypt_and_write, read_and_decrypt


class DataEntry:
    def __init__(self, date, value, note, isFromFitFile):
        self.date = date
        self.value = value
        self.note = note
        self.isFromFitFile = isFromFitFile

class Variable:
    """
    Represents a created variable. Stores DataEntries.
    """
    
    def __init__(self, name: str, goal: str, alert_times: list, variable_type: str, unit=None, decrease_preferred=None, data=[]):
        self.name = name
        self.goal = goal
        self.alert_times = alert_times
        self.variable_type = variable_type
        self.unit = unit
        self.decrease_preferred = decrease_preferred
        self.data = data 

class VariableHandle:
    """
    Stores and serializes variable data and associated entries.
    """

    def __init__(self):
        self.current_variables = []
        self.user = ""
        self.password = ""  
        self.salt = self.user.encode()
        self.read_variables()

    def read_variables(self):
        file_path = f'data/{self.user}.json'
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            self.current_variables = []
            return
        try:
            variables_list = read_and_decrypt(file_path, self.password, self.salt)
            self.current_variables = []
            for var in variables_list:
                data_entries = [DataEntry(**entry) for entry in var.get("data", [])]
                self.current_variables.append(
                    Variable(
                        name=var.get("name"),
                        goal=var.get("goal"),
                        alert_times=[datetime.fromisoformat(dt).time() for dt in var.get("alert_times", [])],
                        variable_type=var.get("type"),
                        unit=var.get("unit"),
                        decrease_preferred=var.get("decrease_preferred"),
                        data=data_entries
                    )
                )

        except Exception as e:
            st.warning(f'There was an error reading the variable data: "{str(e)}"')

    def write_variables(self):
        file_path = f'data/{self.user}.json'
        data = [
            {
                "name": variable.name,
                "goal": variable.goal,
                "alert_times": [
                    datetime.combine(date.today(), dt).isoformat() for dt in variable.alert_times
                ],
                "type": variable.variable_type,
                "unit": variable.unit,
                "decrease_preferred": variable.decrease_preferred,
                "data": [
                    {
                        **{k: (v.isoformat() if isinstance(v, (datetime, date, time)) else v) for k, v in entry.__dict__.items()}
                    }
                    for entry in variable.data
                ]
            }
            for variable in self.current_variables
        ]
        encrypt_and_write(data, file_path, self.password, self.salt)


