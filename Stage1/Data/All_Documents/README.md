# Project Stage 1 Documents

### Summary
**Entity:** Person Names

**Mark Ups:** Each name begins with a <n> tag and ends with a </n> tag.

### Details:

This directory contains all 300 documents that we have labled. Each document contains an article found on CNN.com and 
we have marked up the document for person names.

**How We Mark Up a Name**

We use two tags to mark up names in the documents. Each name begins with <n> and ends with </n>. For example, if we encounter
the name "Paul Chryst" we would mark it like this: "<n>Paul Chryst</n>". Note that there are no spaces between the tags
and the name.

**What We Consider a Person Name:**

We only consider the actual name as an entity. 
- We only count the entire name
  - Example: If we encounter the full name "Scott Walker", we only count the full name "Scott Walker".
  We do not count just "Scott" or just "Walker"
- We do not include “Doctor,” “Mr.” or any other prefixes/sufixes as part of the name.
  - Example: Governor <n>Scott Walker</n>
  - In the above example, "Governor" is not considered to be a part of the name
- We do not consider grammatical endings as part of a name. For example, if an article contains the phrase 
  “President Obama’s administration” we would only extract “Obama.” The apostrophe ‘s’ (‘s) is not considered 
  part of the name.
