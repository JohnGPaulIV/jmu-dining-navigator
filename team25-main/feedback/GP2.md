# GP2 Feedback

## Project title

- Team 25, JMU Dining Navigator
- JMU Dining Navigator
- 25, JMU Dining Navigator
- 25,  JMU Dining Navigator
- Team 25
- Team 25
 JMU Dining Navigator
- Team 25, JMU Dining Navigator
- 25
JMU Dining Navigator

## Consistency

- One thing that doesn't align between the README and the diagram is that the diagram doesn't have the administration user listed. However, that is a easy fix.
- The team's proposal aligns with the EER diagram. The EER diagram contains all of the system entities that were in the proposal. The EER diagram also includes multiple relationships that align with how the system was described in the proposal.
- They have all of the system entities and their system users. There is one discrepancy that I found where they mentioned that their users will have dietary preferences but I do not see that.
- Everything seems to align. I especially like the dietary restriction idea.
- Since a Dining Hall Manager is inheriting User, that means a Dining Hall Manager can also have a favorite location and dietary restrictions and a meal plan? In that case, these attributes should be added as an attribute to that  Dining Hall Managers as well, not just student faculty. Otherwise, only student/faculty should be able to favorite/have dietary restrictions/have meal plans.
- To me it looks like everything is aligned. At first I thought the User entity was missing a couple attributes on the diagram but saw that they were divided through the related primary system users.
- -Its surprising to me is no explicit exception category for hours, only all grouped into one "hours" category
-Do Dining Hall managers have meal plans?
-The menu item is good
- The attributes & entities listed in Primary System Entities match with the attributes & entities in the EER diagram. There is a new entity, Dietary Restriction, that has relationships to User and Menu Item. I'm a bit iffy on it because a User could theoretically have a multivalued allergies field instead of a new table.
- Your EER diagram aligns nicely with your project proposal. The only major changes are the addition of Dietary Restriction as an entity and the omission of Administrators. If you still intend to include an Administrator but don't wish to add it as an entity, you may want to include a note explaining the Administrative role.

## Completeness

- Yes, the EER diagram is complete. One suggestion that I'd make is that it would be hard to keep track of some of these attributes, such as crowd level in the Dining Hall entity, along with availability in the Menu Item entity. You don't want to end up with multiple attributes that are primarily NULL.
- I don't think the diagram is mostly complete. The entities Student Faculty, Dining Hall Manager, User, and Meal Plan don't have primary keys. The relationships and cardinality are there as well as sufficient attributes.
- A lot of the entities do not have their primary keys underlined, I can see that they have things that are probably supposed to be the key but it isn't specified.
- Almost. Primary keys should be specified for each entity.
- Everything has a clearly labeled name. There are a couple missing primary keys within Dining Hall, Meal Plan and User. It seems that all relationships have valid crows foot notations, surprised there aren't any 1-N's.
- Student faculty should be student/faculty or create two different tables
- Only two entities, Dietary Restriction & Menu Item, have primary keys. All relationships are clearly named, and while the entities are readable, I would change "Student Faculty" to be "Student/Faculty" or maybe just "Customer."
- JACard ID should be underlined in Student Faculty because it is the primary key for Faculty and User. Every strong entity should have a primary key. It makes more sense to me that each user sets their Dietary Restrictions, so a user could have 0 to many Dietary Restrictions, and a Dietary Restriction would always have 1 User. I think a meal plan should only have one user, not one or zero.

## Correctness

- The only possible issue I see is with the Dining Hall Manager entity. I would think that you would just get the dining hall data from somewhere online or a JMU specific dataset, not have it managed by anyone in JMU's system. What is the point of the manager?
- I don't think everything is correct in the diagram. I don't think the Dining Hall's open status needs to be a multi-valued attribute. Also, the relationship between User and Meal Plan reads "One User has many Meal Plans", so I think the crow's foot and the one should be swapped so it reads "Many Users can have one Meal Plan".
- All the entities are connected through a relationship, and I do not see any blaring problems with any of the entities or relationships.
- For dining hall, the "open status" should be derived (from hours), not multi-attribute.
What is the primary key of a dining hall manager? name? email? jacard?
- I believe everything looks good. I'm glad the dietary restriction is part of a relationship and not just an attribute within User. All relationships make sense and are necessary.
- There is no key or assumptions
Should there be a primary key for Student faculty?
- There aren't many any technical errors. With that said, I'm a bit confused on why Dining Hall's open status attribute is multivalued -- if it's a simple t/f for open/closed, wouldn't it just be single-valued? Or is it a list of operating hours?
- You did a good job ensuring all the entities have connections and keeping unnecessary complexity to a minimum. The keys, as mentioned before, need to be completed. The Meal Plan could be a weak entity because it seems to depend on its user.

## Organization

- The diagram is pretty easy to follow. The design is clear and I have no issue with their relationship names.
- I think overall the diagram looks good and is pretty easy to understand. There is a crow's foot relationship that could be moved so it isn't overlapping with another one. Specifically, the one coming from favorite and going into User.
- I believe that the diagram is easy to understand and follow. The positioning of each entity could probably be min/maxed but overall I think it looks good.
- I really like the colors, it helps a lot to identify stuff. There are a lot of crooked lines that could be straightened for simplicity and ease of reading. For neatness, Student Faculty and Dining Hall Manager could move under 'User', which would be more organized.
- The layout is very easy to understand and are spaced out in a good manner. One thing that I would recommend is moving the line for User has Dietary restriction because it interferes with another crows foot. I think they did a good job with making everything understandable and left me with all info I needed.
- The diagram is really well organized and eye catching with the colors. The ideas are neatly grouped together (users in one area and dining stuff in another)
- Overall, it's clean and makes sense, which is important for a diagram. On the topic of high-level implementation, I question the validity of adding a User entity. If I'm a user of a website, how am I connected to the database? Do I need to put in my info via a login or field and then that's added to the database, so in order to find out things about myself I just query myself? The relationships the User has might be more apt as a feature of a web app (ex: a list of allergens formatted like check boxes so you can check which ones you want to filter by)
- The layout could be structured more orderly.  For example, one of the lines overlaps with another unnecessarily. Nevertheless, that does not prevent the diagram from being easy to follow. The entities, attributes, and relationship names are all clear and descriptively named. I couldn't think of any assumptions either.
