# Stage 2 Data

### The Data
Our data contains product information for laptops from Walmart and Amazon.

The Attributes:
  1. Name (String): The name of the laptop listed on the website.
  2. Price (Float): The price of the laptop in dollars.
  3. Brand (String): The company who created the laptop.
  4. Screen Size (String): The size of the screen. This is a string because it often contains units.
  5. RAM (String): The amount of RAM included with the laptop
  6. Hard Drive Capacity (String): The sise of the hard drive.
  7. Processor Type (String): The name of the processor.
  8. Processor Speed (String): The speed of the processor.
  9. Operating System (String): The operating system included with the laptop.
  10. Battery Life (String): The amount of time the battery generally will last.

### Table A: Walmart Data
The data for table A was retrieved from walmart's website and conforms to the schema listed above. Unfortunatly, walmart's website does not allow the user to access more than 1000 results for a single search. We decided to combat this by splitting up our search by brand and the smaller tables for each brand can be found in the /Walmart_Brand_Data/ directory.

Length of the Walmart table: 3038 tuples

### Table B: Amazon Data
The data for table A was retrieved from Amazon.com and conforms to the schema listed above.

Length of the Amazon table: 3102 tuples
