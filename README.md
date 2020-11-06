# ryanryan
Hannah and Ryan build a database

this lives here https://web.engr.oregonstate.edu/~ryanh/340/
also here https://quarpedia.herokuapp.com/


***process flow:***  

1. new users fill out the "add a new user" form on their user profile.  
	- this populates:    
		- users table:  
			- firstName (from user)  
			- lastName (from user)  
			- userID (auto-increment) 
			- localeID at this point is null  
		- locales table:  
			- localeName (from user)   
			- localeID (auto-increment)   
			- userID (pulls from users table)  
	- then we need an update statement to:  
		- populate localeID in the users table 
2. existing users can update their name or localeID -- this should be on the user profile page, and should update the users table and locales table
3. user books an activity -- they can only book/create activities in their locale, so we don't need localeID from the user
	- this can be either taking an existing activity where userID is NULL or by creating a new activity
4. user books a walk -- they can only book/create activities in their locale, so we don't need localeID from the user

5. user completes an activity or walk
