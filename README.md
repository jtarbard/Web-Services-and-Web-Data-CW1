
# I. instructions on using the client

client is implemented as instructed, example commands below:

## Commands

- **Command: arguments (in order)**
- register: url
- login: url
- logout: n/a
- list: n/a
- view: n/a
- average:  professor_id, module_code
- rate: professor_id, module_code, year, semester, rating

Commands will provide information on their use if they are used incorrectly, including how many args are expected and in what order. If there are any unexpected results, check the order of the args passed.

# II. the name of your pythonanywhere domain.
sc18jt.pythonanywhere.com

# III. the password I have to use to login to my admin account on your service.
username: ammar

password: password1234

# IV. any other information I need in order to use your client
The client uses tokens as recommended on the docs. The token is stored in a token.pkl file upon login. Url is also stored in a url.pkl file upon login or registration for persistence. This does not required any user interaction but if these files are deleted you will have to login again. Registering an account logs out the current user.
