
My Choice of Platform:
I chose to use Flask and python as well as sqlite and html because of my experience using these languages, as well as their simplicity and flexibility of use. I have made two websites with flask so far, and combining the flask application with logic and data from databases makes anything possible.
Nowadays the most popular and easiest access applications are literal applications on phones, but for those who use computers often such as myself websites are a close second. Thus my decision to make Crimson Contacts a website on Flask was a combination of simplicity, convenience, and expertise.


Basic Website Aesthetic, website mechanics.:

the Website features a Crimson Clear Signitur logo at the top left as well as a simple bar at the top for easy navigation. I carried these over from a similar template from pset 9: finances, but I added my own logo and new headers to go to new pages. I kept the smae color cheme for the most part.
I did make the design decision to use color to indicate threat level, from ed to green. These colors tend to indicate danger or the absence of danger, so I use vivid color when later describing threat rankings. Most of the color magic is done in html using font color changing commands.
I also chose to use a combination of radio buttons and text boxes to simplify user input, which I will get into later. I took full advatage of jinja so as to not have to keep remaking the same headers and footers on every template sheet.


Registry and Login:

registry page and logic: the registry page is a simple form that has both GET and POST pathways, with GET bringing users to the empty form to fill out, and POST submitting their information.If any text boxes are left empty the registry form will not go through thanks to many if and elif conditions.
I used request.form to get user responses and use them in python.Most responses are transferred into the SQL users table, which houses most user info. The register page has the location information broken up into many seperate parts so I can pass them through the API (i'll get more into that later)
with limited confusion. I take the parts of the address and later format them together into a string to be passed into the API. After I confirm the attemp to register is valid, the user is saved in the users table, is assigned a session, is assigned a log id and inserted in logs, and is allowed to use Crimson Contacts.


Home page main features:

the home page was designed to house all of the important data about the user and their surroundings in one place. As a result the user's environmental risk level, personal risk, and contacts table are all displayed there:

    Environmental Risk Level Mechanics:

    The environmental risk level is determined based on the status of the most threatening user in the vicinity, with vicinity determined by the user's address they submitted at registry. I decided to use the API to convert the addresses into coordinates so I can work with them easier. Since Crimson Contacts is meant for dorms , apartments, and other high density
    population buildings, the environmental risk holds more weight in those environments. using SQL statements on the users table, Crimson Contacts determines the highest risk perosn in your building aside from you, and the environmental risk directly reflects that. this method not only is simple, but make sense because it
    only takes one infected person to infect many others. Based on the highest risk level, the home page will display one of four rik levels. This dynamic page generation was made possible by jinja, which allowed me to use logic on the html page to change it based on the risk level. instead of having to make 4 seperate pages with different risk levels I could put all on the same page using
    if statements.



    Your Current Personal Risk level:

    The current personal risk level operates similarly to the environmental risk level except it is based only on your status you have self reported to Crimson Contacts. It does not change based on the health of your environmenta at all. it is meant to show how the user is affecting their environment's safety.
    I also used aan SQL query to obatin the information needed for this ranking, as well as jinja in the html template to put all 4 personal status levels on one page

    Your Crimson Contacts:


    Crimson Contacts, perhaps the pinnicle of the application is a table that shows interactions a user had had with other users based on the location and date of their travel. It also displays the status of that perosn as theyw ere traveling, so a user can determine for themselves the risk of them having COVID.
    I mmade this table by first getting geographical data from the two Surveys. If users decide to provide dates and locations, the locations are converted to coordinates (for easy comparison) and the dates are stored. An SQL statement is used to find interactions based on those two factors, and those inetractions are displayed
    via table in the Crimson Contacts table. I decided it would be appropriate to keep users anonymous here because otherwise users would know a little too much information about eachother otherwise. Even though Crimson Contacts is built off of the voluntary sharing of information, most of that information is only seen by the Crimson Conatacts servers and data processing.


Surveys page:

The Surveys app route consists of two routes and two pages, /survey and /survey 2, and "survey.html" and "survey2.html". I had to use two because putting two seperate forms on the smae page proved to be incredibly difficult. One survey is for if a user is infected and the other is for uninfected users.
I did it this way because if a user was already infected, questions on the first survey would be rather pointless. Also I needed a way for users to change their status back from infected to Healthy, and a way for them to indicate they have tested negative after infection. (notice users status only changes away from infected after they confirm they tested negative)
Also I made it so after a user tests negative they still have a minor risk level until their next survey, just in case there may have been an innaccuracy in the test.

    Normal Survey (If uninfected):

    The normal Survey Consists of two radio button questions and an optional three location and date entries. The radio buttons are automatically set on the most common responses (via checked in html) to make the process easier for everyday use. Also this makes submitting an emoty form impossible, which was vey helpful for preventing errors.
    Since the locations are optional, the user does not have to include them in the survey. If they do, the responses are passes through logic in applications.py to make sure they are valid addresses able to pass through the API. useres don't have to include a date, but entries without dates are not used in the Crimson Contacts table.

    Infected Survey:

    The infected Survey was designed to be simple: either you have tested negative or you are still infected. The survey consists of one yes or no question with the radio button on no by default, as it will probably take a few days and many surveys until the user is clear. Even though users should not travel while infected, in case they have the option to share those dates and locations.
    the dates and locations submitted in survey2 are also placed into logs. travel dates are simplified from the timestamps though so they take their own place aside from datetime.

Logs:

The logs page is a hub of user activity that shows what user did and when. Essentially after users do any task like logging in or taking the survey that is recorded in the logs table. Their individual user logs are then displayed to them in the form of dynamically genrated html tables.

    Activity Table: Shows when users registered, when they logged in, and when they completed surveys. It also shows their status when they completed surveys. this was accomplished by passing dictionaries containing user data into the html table, and generating the table based on rows of that data.
    Since all activities are properly timestamped, the activities table shows date/time and not just date.

    Travel History table: Shows the date and location that users have self reported over their time using Crimson Contacts. based on information from logs, but only activity of the 'travel' type. Since it is hard to know exactly when you went somehere, travel is displayed in the month day year format. this table was also generated
    dynamically using jinja.

Logout:

The logout button is pretty straightforward, it clears the session and thus your browser and the website do not know you as a user anymore. You have to sign back in after that.


API use and helping functions:

I decided to use Geopify because it was free (main one) easy to use, and gave me free API keys. Implementing it was hard, but I turned it into a function that takes a prepared string as input. I pass the string into the request url, the parse and format the response into a dictionary. The coordinates were really the only information I needed so I only passed those back.
It took A LOT of trial and error to figure out how to propoerly use the API, but it works like a charm so it was worth it. Also I have helper function apology, which I repurposed from pset9. Now it does not give an image but just an error code and directions about what you did wrong.
