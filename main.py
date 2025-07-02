import streamlit as st
import threading
from utils.authenticator import Authenticator
from utils.variable import VariableHandle, Variable


# Streamlit sadly does not support background threads. It neither has functions like QThread in PyQt nor does it support the threading module.
#
# from utils.push_notif import send_push

# def notification_task(variableHandle):
#     print("thread_started")
#     try:
#         variableHandle.read_variables()
#         print("testing")
#         for variable in st.session_state.variableHandle.current_variables:
#             for alert_time in variable.alert_times:
#                 if alert_time in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
#                     if alert_time == time.strftime('%A'):
#                         send_push(variable.name,
#                                   f"Reminder for {variable.name}")
#                 else:
#                     current_time = time.strftime('%H:%M')
#                     if alert_time == current_time:
#                         send_push(variable.name,
#                                   f"Reminder for {variable.name}")

#         time.sleep(5)
#     except Exception as e:
#         print("Error in Task:", e)


ss = st.session_state
if "variableHandle" not in ss:
    ss.variableHandle = VariableHandle()

authenticator = Authenticator()
