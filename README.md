# BiaBoro

---------------------------------------
### List of APIs

- #### Sign-up
  - Sign-up is for employees and managers.
  - For sign up you need to send a request with the following parameters:
    - `username`: The username of the user.
    - `password`: The password of the user.
    - `password_2`: The confirmation of the password.
    
- #### Complete Profile
  - Each user should complete their information on their profile.
  - The items required from the employee are:
    - `national id number`
    - `role (position)`
    - `phone number`
    - `contract type`
    - `first name`
    - `last name`
    - `email`

- #### Approve sign-up 
  - Entities should approve their direct-reports after they sign up.
  - Managers should approve employees registration using their `username`.
  - Same for owners + they should approve Managers.
  - (Implemented without applying hierarchy. Now anyone can activate/deactivate anyone.)
  
- #### Sign-in
  - Authentication implemented using Token Auth method.
  - With each login, `last_login` column in `auth_user` will be updated for the user.
  - With each login, a new row will be added to `login_logout` table.
  
- #### Sign-out
  - When logout endpoint is called, token of the user will be removed from `authtoken` table if there is any token.
  - With each login, a new row will be added to `login_logout` table.
  
- #### Get user info
  - Accessible only for Admins, Owners, and Managers.
  - User info can be retrieved by sending a request with at least on of the following parameters:
    - `role`
    - `contract type`
    - `national ID`
    - `email`
    - `first name`
    - `last name`
    - `username` 
  - Admin and Owner can access everyone's data. (not implemented yet)
  - No one can access anyone above theirs. (not implemented yet)

- #### Remove user
  - Removes a user using its `username`.
  - Accessible only for Admins, Owners, and Managers.
  
- #### Add arrival/departure
  - Employees and Managers can add their arrivals\departures.
  - The following items are needed in the request body:
    - `datetime`: date and time of action.
    - `type`: indicates that action is arrival or departure.
    - `description`: any short description about the record. i.e. *have doctor's appointment.*

- #### Get activity
  - Gets the employee's activity based using their username or email.
  - The following items are needed in the request body:
    - `email`: employee's email.
    - `username`: employee's username.
    - `action_type`: it can be one of `arrival`, `departure`, or `all`.
    - `approved`: it can be one of `denied`, `approved`, or `all`.
    - `from_date`: start of time range in `yyyy-mm-dd` format.
    - `to_date`: end of time range in `yyyy-mm-dd` format.
  
- #### Approve activity
  - Send approval result for the employee's activity using their employee_id.
  - The following items are needed in the request body:
    - `employee_id`: an integer which is the id of the employee in the `employee` table.
    - `records`: a list of dictionaries with keys record_id and approval_state:
      - `record_id`: an integer which is the id of the record in the `arrival_departure` table.
      - `approval_state`: it can be either of `deny`, `approve`.
    
- #### Get arrivals and departures
- #### Get logins
- #### Edit arrival
- #### Edit departure
- #### Delete arrival
- #### Delete departure
- #### Change password
- #### Change username
- #### Change user info

## Next step:
0. Learn Django User.
1. Learn about User Authentication in Django.
2. Develop Sign in.
3. Develop Sign up.
4. Develop Sign out.
5. Develop Refresh token API.

