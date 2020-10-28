# ryanryan
Hannah and Ryan build a database


process flow:  
new users fill out the "add a new user" form on their user profile.  
this populates:    
	locales table:  
		localeName (from user) 
		localeID (auto-increment) 
		userID at this point is null
	users table:  
		firstName (from user)  
		lastName (from user)  
		userID (auto-increment)  
		localeID at this point is null  
then we need an update statement to: 
	populate userID in the locales table
	