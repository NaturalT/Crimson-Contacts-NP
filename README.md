Purpose:
The prupose of Crimson Contacts is to provide a web based application that, similar to Crimson Clear, helps maintain the safety of a community through the voluntary sharing of relevant personal information. The difference is Crimson Contacts brings in location based inferences similar to Contact tracing.
Crimson contacts  gives up to date, real time rankings of the safety of a users immediate environment, as well as informatio about others they may have contacted outside and their risk levels. In an ideal world where the majority of people use Crimson Contacts, users would have a very reliable idea as to the safety of their
environments and everyday interactions thanks to Crimson Contacts. We are not quite there yet, but Crimson Contacts is here nonetheless!






Setup Phase:
Welcome to the official Crimson Contacts guide! My Name is Natural Taylor and I will be your guide to the
ever-inclusive, never-invasive service that is Crimson Contacts! First off we have to get the Crimson Contacts
application up and running, something only the host of the website would need to worry about (not an everyday user).
To properly run the software, make sure you have the "Crimson Contacts Kit" folder ready. Inside is an application file
along with a helper file. Before you run Flask, make sure there is a database ready named users.db, it should have
been provided with the kit but if not make it using sqlite3. Next, make sure all of the html templates for the website
are in the templates folder. There should be an 'apology' template for errors, a 'home' template where users will spend
most of their time, a 'layout' template that holds all of the guts and glory behind the website aesthetic, a 'login' template
housing the login screen, a 'logs' template where user activity is recorded, a 'register' template in which users register,and
two Survey templates, 'Survey' and 'Survey2' in which users log their daily activity. Also make sure there is a CSS file named
styles.css and an icon file named favicon.ico in the static folder. Now, you can run flask to get Crimson Contacts up and running!

Registry and Login:
Next up is navigating the Crimson Contacts User Interface so you can start contributing valuable data to your community! First, you have to follow the link provided by Flask. Once at the Crimson Contacts website, the first thing you have to do as a new
user is register. Click the register button at the top right corner to be taken to register page, which will need some of your personal data. By registering, you are providing some of your location data to Crimson Contacts, so users are giving Crimson Contacts
the permission to use this sensitive data at registry! Make sure you fill out every field, or else the registry will not go through. Also heed the error messages that appear if registry fails, they tell you what you did wrong. After registry, you will be taken
to the login page, where you provide your username and password and then proceed to the Crimson Clear home page.

Navigating the Home page:

the home page is where alot of important information is displayed, including:

    Your Current Environmental Risk Level:

    This is a risk ranking that essentially tells users how safe their immediate home environment is. This risk level can take the form of four levels, low risk, minor risk, moderate risk and high risk. A low risk environment means there are only healthy crimson contacts users around you, and no users have reported any symptoms whatsoever. A minor
    risk environment means one or more users in your vicinity have reported minor symptoms that may or may not be COVID. A moderate risk environment means users have reported having symptoms related to COVID-19, but have not yet tested positive. A high risk
    environment means a user in your vicinity has tested positive for COVID and is currently infected, thus you should be very cautious of your surroundings. ** Some important notes about environmental risk are it does not consider your own personal risk
    (you can't literally infect yourself with COVID or anything else), and Environmental risk only knows the information of Crimson Contacts users, and thus makes these risk rankings with only Crimson Contacts users in consideration.



    Your Current Personal Risk level:

    This is an indicator of your own personal health status you have reported to Crimson Clear. This is also the health status that affects the environmental safety of users in your vicinity. You can have four possible statuses, Healthy, Minor Risk, High Risk, and
    Infected. A healthy status means that as far as you know you are healthy and free of COVID symptioms. A Minor Risk personal status means there is a minor risk you may have COVID based on your minor symptoms. A High Risk Personal Status means you have a high risk of having
    COVID based on you having severe symptoms. An Infected Status means you have tested positive for COVID-19.

    Your Crimson Contacts:


    Your Crimson Contacts is a table that shows interactions you have had with other Crimson Contacts users at other locations. If you and another user visited the same location on the same day and report these locations and dates in the daily survey, Crimson
    Contacts will take notice and save the interaction in your Crimson Contacts table. The users name is kept anonymous for privacy reasons, but you can see the user's personal risk status so you yourslef can determine the risk you have of having contracted COVID from that person in that place.
    **Note ** The Crimson Contacts table is only as accuate as the amount of Crimson Contacts users in the area, so even if no other higher risk users were at a location, it does not gaurantee safety!

Surveys page:

After you have logged in, the Survey page is where you take the daily survey, a survey intended to asses your personal risk level, learn locations you traveled, and as a result enrich the Crimson Contacts database so your community is better informed. There are two versions of the Survey,
the Survey if you are infected with COVID and the Survey if you have not yet confirmed so.

    Normal Survey (If uninfected):

    The Normal Survey asks if you have discovered you are COVID positive, and otherwise how you have been feeling. It also asks for the locations you have been and the dates you went to them, information that is completely voluntary and up to you to disclose!

    Infected Survey:

    The infected Survey, which is only accessible if you have previously self reported yourself as COVID-19 positive, asks if you have tested negative and quarantined long enough to stop being considered infected. it also asks if you have been any places, which you are also free to disclose along with the dates!

Logs:

The Last Amazing Feature of Crimson Contacts is the logs page, in which a user can look at the logs of all of their user activity and travel activity.

    Activity Table: Shows when users registered, when they logged in, and when they completed surveys. It also shows their status when they completed surveys, so they have a history of their own health!

    Travel History table: Shows the date and location that users have self reported over their time using Crimson Contacts.

Logout:

The last step of the user experience is to log out for the day, the logout button can be accessed at the top right of the page.


here is the link to my video, hope you enjoy!
https://youtu.be/TU3_Bm7wLbo