# WorkBringer2
A new resume optimizer that brings you closer to employment



RULES:

Backend API reture rule:
- 'message' means a string
- 'detail' means a nested dict
- 'status' means a bool on the success of the action
    - Note: it conveys a different meaning than the code
    - It is possible that the action was not performed but no error was reached
- 'info' means data
- 'jwt' means a reauthentication jwt for quick auth next time.