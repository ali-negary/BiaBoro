# BiaBoro

---------------------------------------
### List of APIs

- #### Sign-up
  - Sign-up is for employees and managers.
  - For sign up you need to send a request with the following parameters:
    - `username`: The username of the user.
    - `password`: The password of the user.
    - `password_2`: The confirmation of the password.
    
- #### Complete Profile (Not implemented yet)
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
  
- #### Sign-in
  - Authentication implemented using Token Auth method.
  
- #### Sign-out
  - When logout endpoint is called, token of the user will be removed from authtoken table if there is any token.
  
- #### Remove user
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
  - Managers cannot access anyone above theirs. (not implemented yet)

- #### Add arrival
- #### Add departure
- #### Approve activity
- #### Get arrivals
- #### Get departures
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

