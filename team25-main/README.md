# Team25 CS374 Database Project

Project Title: **JMU Dining Navigator**

Team Name: **The Hungry Dukes**

Short Name: **dining-dukes**

Team Members: **John Henry Adams, Joe DiRocco, Lucas Fisher, John Gilbert Paul IV, Harry Williams**

# Introduction

James Madison University offers several different places for students to eat on campus. (see [JMU Dining](https://jmu.campusdish.com/en/)). These locations vary from coffee shops to restaurants, and all the way to large dining halls with a variety of food for students to choose from. However, it can feel overwhelming for students to pick from such a diverse selection, often leading them to rely on convenience rather than exploring all available options.

We propose to JMU Dining Navigator (JDN), a database that would allow students, staff and faculty to quickly find information they are looking for. The proposed features for this system would include:
* Finding the closest open dining hall/food court
* Filtering menu items by dietary restrictions (e.g. vegan, gluten-free, religious, etc.)
* Checking operating hours in real-time, including holidays or special event cases
* Tracking crowd levels to help prevent wait times
* Allowing user accounts with favorites and recommendations
* Tracking food costs (e.g. Duke deals vs dining dollars)

# Primary System Entities

| SYSTEM ENTITY | ATTRIBUTES |
| :---- | :---- |
| Dining hall | name, location, hours, capacity, current crowd level, open/closed status |
| Menu Item | name, description, allergens, dietary tags, availability, dining hall |
| User | name, email, JACard ID, dietary preferences, favorite locations, favorite items |
| Meal Plan | dining balance, swipes, flex balance meal plan name |

Students at JMU have a lot of dining options, but the info about them is spread out and sometimes hard to find. Hours change on holidays or events, menus aren't always up to date, and it is not clear how busy a place will be until you get there. This often makes students just pick whatever is closest instead of finding the best option.
Our project would put all this information into one system. Students could check what's open, see menus with dietary filters, and even know if a dining hall is crowded before walking over. Over time, the system could also show patterns like which spots are usually packed at lunch. This would make it easier for students to plan meals and avoid surprises.

# Primary System Users

| USER GROUP | ACTIVITIES & PERMISSIONS |
| :---- | :---- |
| Students/Faculty/Staff | Query nearest dining hall, filter by dietary restrictions, view menus, set preferences |
| Dining Hall Managers | Update menus, update hours |
| Administrators | Oversee all data, manage dining hall records, handle special events/closures

While information about each restaurants menu is available online, it can be annoying and tedious for students to look through each menu to figure out where they want to eat. We want users to have a simple way to narrow down dining options, while being able to enter in as few or as many parameters as they would like for the outcome. This database would allow students to spend more time eating food they enjoy, and getting the most out of the provided dining centers on campus.

# System Functionality

## Dining Halls & Hours
* We will Store data on all dining halls with their standard hours and exceptions such as  special events, holidays, and more. Along with this we will allow people to see common query's like "Where's the nearest dining hall?" or "Which dining halls have food that is gluten free?". Along with the commonly asked questions above we will have a filter system where students can define more precise search parameters.

## Menus & Dietary Restrictions
* Each menu item will be tagged with dietary attributes such as: vegetarian, vegan, gluten-free, nut-free, and any other dietary restriction that JMU students may need. Using these tags users can filter menus by restrictions. This will make it much easier for those with strict dietary restrictions to quickly find a place to eat while not sacrificing their taste buds.

## Real-Time Updates
The system will also be able to display current crowd level based on the rate at which students are punching into the dining halls or the number of students at other restaurants on campus.

## Personalization
* Users will be recommended to save favorite items or locations in order to have those be at the top of the page when available or even receive text or email notifications for those items. Following this concept we will give recommendations based on preferences or past selections.

# About the Team

**John Henry Adams** is a senior Computer Science major at James Madison University. His academic interests include software optimization, open source software, and game development. Past software projects include a group project from CS 345, and individual game projects.

**John Paul** is a third year Computer Science major at James Madison University who is minoring in business and robotics. Their academic interests include: web development, quantum computing, AI/ML and game development. For this project he will focus on data scraping, backend logic and front-end development.

**Joe DiRocco** is a third year Computer Science major with a minor in Data Analytics at James Madison University. His academic interests include Data Science, ML/AI, and Cybersecurity. For this project he will focus on database system design/management, communications with relevant JMU departments (JMU Dining), and backend logic.

**Harrison Williams** is a fourth year Computer Science major at James Madison University. His academic interests include: Software engineering, web development, and game development. For this project he will focus on backend logic, and front-end development.

**Lucas Fisher** is a fourth year Physics and Computer Science Dual Major at James Madison University with a Math and Honors Interdisciplinary Studies Minor. Their academic interests include software development, game design, quantum mechanics, and Physics applications.
