from datetime import datetime
import json

class Variable:
    def __init__(self, name: str, goal: str, alert_times: list[datetime], variable_type: str, data: list[str], unit=None, decrease_preferred=None):
        self.name = name
        self.goal = goal
        self.alert_times = alert_times
        self.variable_type = variable_type
        self.unit = unit
        self.decrease_preferred = decrease_preferred
        self.data = data
 
class VariableHandle:
    def __init__(self):
        self.current_variables = []

        self.read_variables()

    def read_variables(self):
        try:
            with open('variables.json', 'r') as f:
                variables_list = json.load(f)
                self.current_variables = []
                for var in variables_list:
                    self.current_variables.append(
                    Variable(
                        name=var.get("name"),
                        goal=var.get("goal"),
                        alert_times=[datetime.fromisoformat(dt) for dt in var.get("alert_times", [])],
                        variable_type=var.get("type"),
                        data=var.get("data"),
                        unit=var.get("units"),
                        decrease_preferred=var.get("decrease_preferred")
                    )
                )
        except (FileNotFoundError, json.JSONDecodeError):
            self.current_variables = []

    def write_variables(self):
        with open('variables.json', 'w') as f:
            for variable in self.current_variables:
                json.dump(
                    [
                        {
                            "name": variable.name,
                            "goal": variable.goal,
                            "alert_times": [dt.isoformat() for dt in variable.alert_times],
                            "type": variable.variable_type,
                            "units": variable.units,
                            "decrease_preferred": variable.decrease_preferred,
                            "data": variable.data
                        }
                        for variable in self.current_variables
                    ],
                    f,
                    default=VariableHandle.default_serializer,
                    indent=4
                )

    @staticmethod
    def default_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")



