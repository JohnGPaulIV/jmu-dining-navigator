# GP1 Feedback

## Project title

- JMU Dining Navigator
- JMU Dining Navigator
- JMU Dining Navigator
- JMU Dining Navigator
- JMU Dining Navigator
- JMU Dining Navigator
- JMU Dining Navigator
- JMU Dining Navigator

## Strengths (1)

- The first strength is the usefulness of the database. If they can implement this, then it would be a staple for all students. I like that it focuses on local JMU issues instead of a broader problem.
- The real time features of the project. The fact that the purpose is to update the database in real time provides real impact to students allowing them to act on the information
- The project brings together dining hours, menus, dietary tags, crowd levels, and cost information into one system. This is a strength because right now students need to visit multiple sites or physically check locations. By combining this data, JDN directly reduces the time and frustration students face when planning meals.
- The project proposal has extremely clear language which ensures all the team members have the same vision.
- One strength I found in the project is the inclusion of dietary restrictions for the menus at the different dining options that JMU offers. It will help students who have allergies find places to eat quickly without having to study the menus or visit the establishment first.
- One strength is the ability to filter by dietary restrictions. While I do not have dietary restrictions, I have friends who do, and it would be super helpful to put it in one centralized location not only for the safety of the student but to keep the integrity of the school intact.
- One strength is the strong connection to student life at JMU. Dining is something every student interacts with daily, and the project provides solutions to real problems like changing hours and dietary needs. This makes the project meaningful and ensures that the system will have direct value for users on campus.
- You have a clear problem statement. You connect the system directly to JMU students’ lived experience, which makes the project feel relevant and practical.

## Strengths (2)

- The strength of the proposal is how well thought it is. This team seems to have a firm grasp of how they want to implement this project. The table and users are well thought out!
- The personalization features. This adds ease of use for students who may have not used the system if it felt "clunky" and not in tune with what they need.
- The inclusion of dietary filters and personalization features (favorites, recommendations, notifications) shows clear consideration for the diverse needs of JMU’s student body. This is a strength because it makes the system practical for people with dietary restrictions and enhances overall user engagement by tailoring the experience to individuals.
- The project proposal shows how the product will solve a real problem customers have.
- I also like the idea of showing out of stock items so students are not disappointed if they went to a specific dining option for a certain item that is no longer available. It would save time for the student and cut down on unnecessary wait times.
- One strength would be the usage of the dining hall capacity. I notice in E hall there's a screen that says how many people are in the building and how many more are allowed, and that information would be nice to know before I leave my house in case its packed and not worth it to go.
- Another strength is the variety of system features that make the proposal well rounded. Real time updates, personalization, and dietary filters all add depth to the design. This is a strength because it shows the team thought beyond a simple database and created a system that can improve convenience and user experience.
- You have well defined features. The functionality (finding open dining halls, dietary filters, hours, crowd levels, personalization, etc.) is realistic and aligns well with what a database-backed application can do.

## Improvements (1)

- One area for improvement for this project could be to make certain aspects more achievable. For example, tt's a really cool idea to be able to find the closest spot to eat but how would you implement that? You could have live tracking on your phone but that seems tough. You could also create a different DB that has distance relationships between any building on campus and eating spots, but this seems kinda though too. It might make it more achievable if instead of finding the closest spot to eat relative to you, you give each food spot entity a multi valued attribute that lists the buildings or campus locations they are close too.
- Real time features may be found to be infeasible. Without support from the school, it will be important to separate static features of the database from ones where you would need real time data. You could use static data as a proof of concept for these real time implementations.
- While the proposal mentions tracking crowd levels and updating menus in real time, it doesn’t explain how this data will be collected. To improve this, they should specify the data sources and update mechanisms, and address potential challenges (like delays in crowd data or manager compliance in updating menus).
- The way crowding levels will be tracked in dining halls could be improved. While tracking the rate customers swipe in is perfectly reasonable, that seems insufficient without some way of tracking the rate customers exit too. You could assume the length of an average visit and extrapolate but special events or changes in customer behavior may make that data less accurate.
- I think displaying which dining hall is closest to the student could be a big challenge if being implement through real time location. The only other option that I could think of is to ask the student what building they are in on campus and then calculate the distance to all the dining options.
- One area of improvement could be to add integration for food suppliers so that they can see what JMU dining is missing and offer to provide their food to increase diversity.
- One area for improvement is to clarify how data will be gathered. The proposal mentions menu items and crowd levels, but it is not clear how this information will stay accurate and up to date. The team could improve by outlining specific data sources or methods, such as APIs, manager input, or sensors.
- You may want to improve scalability & data sources. How will “real-time crowd levels” be measured? (Turnstiles? ID swipes? Manual updates?) The proposal mentions “punching into dining halls” but doesn’t clarify if that data is accessible. Stating assumptions here would make it more grounded.

## Improvements (2)

- I could be wrong, but the meal plan entity might not be necessary. If all it contains are values related to the student like balance, and swipes left you could make at an attribute for the student/person entity. If you want it to be its own entity it might be a good idea to add an attribute that specifies what locations accept that meal plan. That way there is a relationship between people and eating spots.
- Data inaccuracy with hours or other aspects could be an issue. For example, it would be useful to find a way to scrape the data on hours regularly from say the jmu website to ensure that the hours haven't changed unexpectedly.
- The proposal describes many useful features but doesn’t explain how users will interact with them. For example, will there be a mobile app, a website, or integration with the existing JMU app? To improve, maybe add details or mockups of the user interface, highlighting how students will search, filter, and receive recommendations.
- The project's scope may be too large for all planned features to be properly implemented. Some features may need to be put in reserve so that if there isn't enough time the features aren't left incomplete but if time permits they can be implemented.
- Giving recommendations on preferences based off past ordering could also be a challenge just based off of the limited options presented on campus. I think it would be more impactful to show the students favorite spots and display the wait time and distance to that spot on a dashboard or user profile.
- One area of improvement could be to allow for students to check for rotating items in the menu at the dining halls as they change regularly
- Another improvement is to prioritize features. The proposal lists many useful ideas, but real time crowd tracking or notifications could be difficult within one semester. The team could improve by choosing a smaller set of core features to guarantee, while marking others as stretch goals.
- You could also improve user experience considerations. Personalization is a nice feature, but how will it be stored? (User profile table with preference attributes?) Mentioning that ties back to the database focus.

## Insights (1)

- After looking at team 25s proposal I think the scope of ours is a little large. Our project, as of right now, doesn’t seem super ambitious but I really like the idea of focusing on problems people in our community face.
- This project emphasized the importance of real time data. Real time data could be used to show trends as they form with the data in peoples' music choice.
- They put a lot of emphasis in the fact that they are designing this project to help the STUDENTS (WOOOOOO!). It made me think about the bigger picture for our project, like who are we really doing this for?
- Our project lacks the scope that JMU Dining Navigator does. While I think their scope might be a little too large, we certainly need to plan more features should we finish what we've planned.
- This proposal made me think more about the application implementation for the database. When we created the idea we mostly were just thinking about how the data would be stored and how they are related to each other not so much user interaction.
- Allowing for more user customization would be a better experience for the user
- From this proposal I learned how important it is to connect a project to a daily routine for users. The dining navigator solves a common student problem in a direct way. For Auralytics this reminds me that we should highlight how our system connects to the everyday experience of listening to music, not just the data behind it.
- We should make sure every feature we propose has a clear user benefit. A good check: if you removed a feature, could you still solve the problem? If not, it’s core. If yes, it might be “stretch.”

## Insights (2)

- Looking at this proposal makes me think that it might be really hard for us to find real data for our project. There is probably good menu, and restaurant data which makes this project a good idea. I can't imagine where we will find data on venues and when they are available
- Again it was stressed to me that it is important to implement core functionality before attempting stretch goals.
- I liked how at the bottom, in their introductions, most of the members included their role in the project, such as data collection, backend, frontend, etc. Role planning is definitely something that will be discussed within the near future.
- The JMU Dining Navigator proposal has much clearer language than our proposal.
- It also made me consider the target audience more critically, specifically how this project is directed toward JMU students allowing them to personalize the information and specifications more narrowly.
- We did not add a short name in our README file...
- I also learned that including personalization can make a project stand out. Their idea of favorites and recommendations shows how the system adapts to individual needs. For Auralytics we could emphasize how personalized reports and predictions make the user feel more connected to their music habits.
- We could also better define user groups
