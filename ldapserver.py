import hashlib
import ldap
import sys
import cons

### user : username (pseudo/login) , firstname , lastname, pwd , num_carte

def login(pseudo,pwd):
    """
    Function that attempts to log a user in with given username and password
    Returns a message indicating success or failure of the login
    """
    msg = ""
    l = ldap.initialize(cons.LDAP_HOST)
    # search for specific user
    search_filter = "cn=" + pseudo
    user_dn="cn="+pseudo+","+cons.USERS_DN
    print(user_dn)

    # hashing the password
    hash_object = hashlib.sha256()
    hash_object.update(pwd.encode("UTF-8"))
    hashed_password = hash_object.hexdigest().encode("UTF-8")
    print(hashed_password)

    try:
        # Try to bind to the LDAP server using the username and hashed password
        l.bind_s(user_dn,hashed_password)
        result = l.search_s(user_dn,ldap.SCOPE_SUBTREE,search_filter)
        print(result)
        msg = "Authentification succeeded"
    except (ldap.INVALID_CREDENTIALS):
        msg = "Authentification failed : username or password invalid"

    # Unbind and free memory
    l.unbind_s()
    return msg

def getallUsers():
    """
    Function that retrieves a list of all usernames from the LDAP server
    Returns a list of usernames
    """
    # connect to host with admin
    l = ldap.initialize(cons.LDAP_HOST)
    l.simple_bind_s(cons.ADMIN_DN, cons.ADMIN_PWD)
    # Search for all users
    result = l.search_s(cons.USERS_DN, ldap.SCOPE_SUBTREE, "(objectClass=person)")
    logins=[]
    # Print the results
    for dn, entry in result:
        logins.append(entry['cn'][0].decode("UTF-8"))

    return logins


def register(user):
    """
    Function that adds a new user to the LDAP server
    Takes a dictionary with the user details as an argument
    Returns None if success or an error message if the registration fails
    """
    dn="cn="+user['username']+','+cons.USERS_DN

    # Hash the password
    hash_object = hashlib.sha256()
    hash_object.update(user['password'].encode("UTF-8"))
    hashed_password = hash_object.hexdigest()

    entry=[]
# This code is adding an LDAP entry for a user to an LDAP directory

# Extend the entry with the following information:
    entry.extend([
        ('objectClass', [b"top", b"person", b"organizationalPerson", b"inetOrgPerson"]),
        ('givenname', user['firstname'].encode("UTF-8")),
        ('sn', user['lastname'].encode("UTF-8")),
        ('uid', user['numCarte'].encode("UTF-8")),
        ('userPassword', hashed_password.encode("UTF-8") )
    ])

    # Connect to host with admin credentials
    l = ldap.initialize(cons.LDAP_HOST)
    l.simple_bind_s(cons.ADMIN_DN, cons.ADMIN_PWD)

    try:
        # Add the entry to the directory
        l.add_s(dn, entry)
        print("success")
        return None
    except Exception:
        # Return the exception if adding the entry fails
        return sys.exc_info()[0]
    finally:
        # Disconnect from the host and free memory
        l.unbind_s()

# Define the user object with the following properties
user_obj = {
    'username': 'username',
    'password': 'pwd',
    'numCarte': '00000',  
    'firstname':'fname',
    'lastname':'lname'
}
