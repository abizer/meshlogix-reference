# twitter for apartment dwellers

write a simple python web application using fastapi and sqlite for the backend and minimal reactjs
for the frontend that can be used by people who live in apartments to post and view short text status
updates in a manner akin to twitter. the following features should be present:
1. the main page should have a form where a user can enter their name, apartment number, and a short
text update. Below the form should be a reverse-chronologically sorted list of status updates that have
already been posted. the updates should be accompanied by the time the update was posted, the name of
the person who posted it, and their apartment number.
2. when the user submits the form, the information should be inserted to a sqlite database, and then
the user should be redirected to the main page.
3. on the main page, when a user clicks the name associated with a status update, the feed should show
only status updates from the name the user clicked on. similarly, if the user clicks on an apartment
number, the feed should only show posts from that apartment.
4. there is no need to implement account management or to authenticate the user.
5. the backend should create the sqlite database if it does
not already exist. the schema should have 4 columns: timestamp, author, apartment, post.
6. the frontend should be contained within a single file and should communicate with the backend
via standard REST API interactions.
7. the backend should be contained in a single file and should run via a uvicorn server that listens on
port 8080.