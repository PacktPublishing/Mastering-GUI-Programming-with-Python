CREATE TABLE roasts (
	id INTEGER PRIMARY KEY,
	description TEXT NOT NULL UNIQUE,
	color TEXT NOT NULL UNIQUE
	)
    ;

INSERT INTO roasts(description, color) VALUES
    ('Light', '#FFD99B'),
    ('Medium', '#947E5A'),
    ('Dark', '#473C2B'),
    ('Burnt to a Crisp', '#000000')
;

CREATE TABLE coffees (
	id  INTEGER PRIMARY KEY,
	coffee_brand TEXT NOT NULL,
	coffee_name TEXT NOT NULL,
	roast_id INTEGER REFERENCES roasts(id),
	UNIQUE(coffee_brand, coffee_name)
	)
    ;

INSERT INTO coffees(coffee_brand, coffee_name, roast_id) VALUES
    ('Dumpy''s Donuts', 'Breakfast Blend', 2),
    ('Boise''s Better than Average', 'Italian Roast', 3),
    ('Strawbunks', 'Sumatra', 3),
    ('Chartreuse Hillock', 'Pumpkin Spice', 1),
    ('Strawbunks', 'Espresso', 4),
    ('9 o''clock', 'Original Decaf', 2)
;

UPDATE coffees SET roast_id = 4 WHERE id = 2;
UPDATE coffees SET roast_id = roast_id + 1
WHERE coffee_brand LIKE 'Strawbunks';

CREATE TABLE reviews (
	id INTEGER PRIMARY KEY,
	coffee_id REFERENCES coffees(id),
	reviewer TEXT NOT NULL,
	review_date DATE NOT NULL DEFAULT CURRENT_DATE,
	review TEXT NOT NULL
	)
;

INSERT INTO reviews (coffee_id, reviewer, review_date, review) VALUES
    (1, 'Maxwell', '2019-02-01', 'Acidic but uneventful, best consumed with large amounts of sugar and a pastry.'),
    (1, 'Peet', '2019-02-23', 'Bright and warm, a perfect companion to breakfast or any meal.'),
    (2, 'Tully', '2019-02-14', 'Rich and complex with hints of chocolate and toasted bread.'),
    (2, 'Maxwell', '2019-02-20', 'Oh my, I think someone emptied the ashtray into my cup.'),
    (3, 'Tully', '2019-03-01', 'Strong and earthy, tastes great with bacon and eggs.'),
    (4, 'Peet', '2019-03-04', 'Overpoweringly fake flavor.  Like drinking a scented candle.'),
    (4, 'Gloria Jean', '2019-03-04', 'The taste of October!  Perfect with whipped cream and a generous amount of sugar.'),
    (5, 'Maxwell', '2019-03-06', 'My mouth is full of the ashy taste of despair.'),
    (5, 'Gloria Jean', '2019-03-10', 'Rich and toasty, great by itself or in a latte.'),
    (6, 'Tully', '2019-04-01', 'Can''t type review... need real coffee....')
;


SELECT reviewer, review_date
FROM reviews
WHERE  review_date > '2019-03-01'
ORDER BY reviewer DESC;


SELECT coffees.coffee_brand,
    coffees.coffee_name,
    roasts.description AS roast,
    COUNT(reviews.id) AS reviews
FROM coffees
    JOIN roasts ON coffees.roast_id = roasts.id
    LEFT OUTER JOIN reviews ON reviews.coffee_id = coffees.id
GROUP BY coffee_brand, coffee_name, roast
ORDER BY reviews DESC;


SELECT coffees.coffee_brand, coffees.coffee_name
FROM coffees
    JOIN (
    SELECT * FROM roasts WHERE id > (
	SELECT id FROM roasts WHERE description = 'Medium'
	    )) AS dark_roasts
    ON coffees.roast_id = dark_roasts.id
WHERE coffees.id IN (
    SELECT coffee_id FROM reviews WHERE reviewer = 'Maxwell');
