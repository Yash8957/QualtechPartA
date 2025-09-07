Intelligent Video Environment Analysis & Item Detection (Part A :
Easy)
Background
Verifying a person’s surroundings is often required in industries such as banking, insurance, real
estate, and e-commerce. Traditionally, this involves manual verification through site visits or
document checks. With AI-driven video analysis, we can automate this process by identifying
the environment type (home, shop, office, etc.), extracting visible items, and generating
structured outputs such as inventory or asset lists.
This reduces manual effort, speeds up verification, and ensures accuracy.

Your Challenge
Build an AI-powered solution that can analyze a video recorded at a location and
automatically:
1. Classify the environment (e.g., home, shop).
2. Detect and identify items in the background.
3. Count the quantity of each detected item.
4. Generate a structured report (e.g., JSON/CSV) with detected objects, counts, and
confidence scores.

Use Case A: Home Environment Analysis
● The system should analyze a video of a home and detect major household
appliances and furniture such as:
○ Sofa, chairs, tables, cupboards, bed, fridge, TV, washing machine, AC,
microwave, decorative items.

●

● Output should include item type + count.
● Example:
○ Sofa: 2
○ Bed: 1
○ TV: 1
○ Refrigerator: 1
○ Chairs: 4

This enables automatic household asset verification for insurance, rental checks, or loan
approvals.

Use Case B: Shop Environment Analysis
● The system should analyze a video of a shop and:
1. Detect shop infrastructure items (shelves, counters, fridges, display
units).
2. Detect and categorize shop inventory (e.g., bottles, boxes, clothing items,
electronics).
3. Provide a count of items per category.
●
● Example:
○ Shelves: 5
○ Chairs: 2
○ Bottled Products: ~120
○ Packaged Boxes: ~75
