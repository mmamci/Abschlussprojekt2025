from datetime import date, datetime, time
import json
import os

import streamlit as st

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
    
    def __init__(self, name: str, goal: str, alert_times: list, variable_type: str, unit=None, decrease_preferred=None, data=None):
        self.name = name
        self.goal = goal
        self.alert_times = alert_times
        self.variable_type = variable_type
        self.unit = unit
        self.decrease_preferred = decrease_preferred
        self.data = data if data is not None else []

class VariableHandle:
    """
    Stores and serializes variable data and associated entries.
    """

    def __init__(self):
        self.current_variables = []
        self.read_variables()

    def read_variables(self):
        if not os.path.exists('data/variables.json') or os.path.getsize('data/variables.json') == 0:
            self.current_variables = []
            return

        with open('data/variables.json', 'r') as f:
            try:
                variables_list = json.load(f)
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
                st.warning(f"There was an error reading the variable data: {str(e)}")


    def write_variables(self):
        with open('data/variables.json', 'w') as f:
            for variable in self.current_variables:
                json.dump(
                    [
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
                    ],
                    f,
                    indent=4,
                    default=VariableHandle.default_serializer
                )

    @staticmethod
    def default_serializer(obj):
        if isinstance(obj, (datetime, time)):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        raise TypeError(f"Type {type(obj)} not serializable")

