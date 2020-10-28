# ryanryan
Hannah and Ryan build a database


***process flow:***
new users fill out the "add a new user" form on their user profile.  
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
