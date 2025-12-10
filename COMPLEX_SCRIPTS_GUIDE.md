# Complex TaskLang Scripts Guide

This guide explains the complex, multi-step automation scripts that start from Google and navigate through multiple pages to complete lengthy tasks.

## Overview

All complex scripts follow this pattern:
1. **Start from Google** - Begin navigation from Google search
2. **Perform searches** - Search for information
3. **Navigate to results** - Click on search results
4. **Gather information** - Take screenshots at each step
5. **Continue workflow** - Return to Google and repeat for multiple topics
6. **Complete task** - Finish with comprehensive data collection

## Available Complex Scripts

### 1. Complex Research Task (`complex_research.task`)

**Purpose:** Research multiple topics starting from Google

**Workflow:**
- Search Google for "Python programming language"
- Navigate to Wikipedia article
- Return to Google, search for "web automation selenium"
- Navigate to Selenium documentation
- Return to Google, search for "TaskLang compiler"
- Take screenshots at each step

**Steps:** 10 steps, 3 searches, 3 navigations

**Use Case:** Academic research, information gathering, multi-topic exploration

---

### 2. Complex Shopping Research (`complex_shopping.task`)

**Purpose:** Research products, compare prices, read reviews

**Workflow:**
- Search Google for "best laptop 2024"
- Navigate to Amazon product page
- Return to Google, search for "laptop price comparison"
- Navigate to price comparison site
- Return to Google, search for "laptop reviews 2024"
- Take screenshots at each step

**Steps:** 11 steps, 3 searches, 2 navigations

**Use Case:** Product research, price comparison, purchase decision making

---

### 3. Complex Learning Journey (`complex_learning.task`)

**Purpose:** Comprehensive learning path starting from Google

**Workflow:**
- Search Google for "Python tutorial for beginners"
- Navigate to tutorial site (W3Schools)
- Return to Google, search for "Python coding practice online"
- Navigate to practice platform (HackerRank/LeetCode)
- Return to Google, search for "Python official documentation"
- Navigate to Python.org docs
- Return to Google, search for "Python community forum stackoverflow"
- Take screenshots at each step

**Steps:** 14 steps, 4 searches, 3 navigations

**Use Case:** Learning new skills, educational research, skill development

---

### 4. Complex News Research (`complex_news_research.task`)

**Purpose:** Gather news from multiple sources

**Workflow:**
- Search Google for "latest technology news 2024"
- Navigate to tech news article (TechCrunch/The Verge)
- Return to Google, search for "artificial intelligence news today"
- Navigate to AI news article
- Return to Google, search for "programming language trends 2024"
- Navigate to trends article
- Take screenshots at each step

**Steps:** 13 steps, 3 searches, 3 navigations

**Use Case:** News gathering, staying updated, multi-source research

---

### 5. Complex Job Search (`complex_job_search.task`)

**Purpose:** Comprehensive job hunting workflow

**Workflow:**
- Search Google for "Python developer jobs remote"
- Navigate to job board (LinkedIn/Indeed)
- Return to Google, search for "Python developer skills requirements"
- Navigate to skills guide
- Return to Google, search for "Python developer interview questions"
- Navigate to interview prep site
- Return to Google, search for "Python developer salary 2024"
- Take screenshots at each step

**Steps:** 15 steps, 4 searches, 3 navigations

**Use Case:** Job hunting, career research, interview preparation

---

### 6. Complex Travel Planning (`complex_travel_planning.task`)

**Purpose:** Plan a complete trip starting from Google

**Workflow:**
- Search Google for "best travel destinations 2024"
- Navigate to travel guide (TripAdvisor/Lonely Planet)
- Return to Google, search for "best hotels booking"
- Navigate to booking site (Booking.com/Expedia)
- Return to Google, search for "cheap flights booking"
- Navigate to flight booking site (Skyscanner/Kayak)
- Return to Google, search for "travel destination reviews"
- Take screenshots at each step

**Steps:** 15 steps, 4 searches, 3 navigations

**Use Case:** Trip planning, vacation research, travel booking

---

### 7. Complex Recipe Research (`complex_recipe_research.task`)

**Purpose:** Complete recipe research and cooking preparation

**Workflow:**
- Search Google for "chocolate chip cookie recipe"
- Navigate to recipe site (AllRecipes/Food Network)
- Return to Google, search for "chocolate chip cookie ingredients where to buy"
- Return to Google, search for "baking tips for beginners"
- Navigate to cooking tips site
- Return to Google, search for "chocolate chip cookie recipe video tutorial"
- Navigate to YouTube tutorial
- Take screenshots at each step

**Steps:** 15 steps, 4 searches, 3 navigations

**Use Case:** Cooking research, recipe gathering, meal planning

---

## How to Use Complex Scripts

### Step 1: Choose a Script

Select the script that matches your needs from the `examples/` directory.

### Step 2: Review the Script

Open the `.task` file and review the workflow. You can customize:
- Search queries
- Wait times
- Screenshot filenames
- Navigation targets

### Step 3: Compile the Script

**Using GUI:**
```bash
python run_gui.py
# Browse and select your complex script
```

**Using Command Line:**
```bash
python -m src.main examples/complex_research.task
```

### Step 4: Run the Script

```bash
python output/complex_research.py
```

The script will:
1. Open Chrome browser
2. Navigate through Google searches
3. Click on search results
4. Take screenshots at each step
5. Complete the entire workflow automatically

## Customizing Complex Scripts

### Change Search Queries

Edit the search terms in the script:

```tasklang
# Original
type "Python programming language" in name "q"

# Customized
type "JavaScript tutorial" in name "q"
```

### Adjust Wait Times

Increase wait times for slower connections:

```tasklang
# Original
wait 3

# Longer wait
wait 5
```

### Change Screenshot Names

Customize screenshot filenames:

```tasklang
# Original
screenshot python_wikipedia.png

# Customized
screenshot my_research_step1.png
```

### Modify Navigation Targets

Change which sites to navigate to:

```tasklang
# Original
click css "a[href*='wikipedia.org']"

# Customized - target different site
click css "a[href*='stackoverflow.com']"
```

## Tips for Complex Scripts

### 1. Test Incrementally

Test one search at a time before running the full script:

```tasklang
open chrome
go https://www.google.com/
wait 2
type "test query" in name "q"
enter in name "q"
wait 3
screenshot test.png
close
```

### 2. Increase Wait Times

Complex scripts need more time between steps:

```tasklang
wait 4  # Use longer waits for complex navigation
```

### 3. Use Screenshots Strategically

Take screenshots at key decision points:

```tasklang
screenshot before_navigation.png
click css "a[href*='target-site.com']"
wait 4
screenshot after_navigation.png
```

### 4. Handle Failures

If a step fails, the script continues. Check screenshots to see where it stopped.

## Common Patterns in Complex Scripts

### Pattern: Search → Navigate → Return

```tasklang
go https://www.google.com/
wait 2
type "query" in name "q"
enter in name "q"
wait 3
click css "a[href*='target-site.com']"
wait 4
screenshot result.png
go https://www.google.com/  # Return to Google
wait 2
```

### Pattern: Multiple Related Searches

```tasklang
# First search
type "topic basics" in name "q"
enter in name "q"
wait 3

# Second search
go https://www.google.com/
wait 2
type "topic advanced" in name "q"
enter in name "q"
wait 3
```

## Troubleshooting Complex Scripts

### Issue: Script stops at a certain step

**Solution:**
- Check the screenshot before the failure
- Increase wait time before that step
- Verify the CSS selector is correct

### Issue: Wrong site navigated to

**Solution:**
- Use more specific CSS selectors
- Add more wait time after search
- Check if the site structure changed

### Issue: Script runs too fast

**Solution:**
- Increase all wait times
- Add extra waits after navigation
- Use `wait 5` instead of `wait 3`

## Best Practices

1. **Start Simple:** Begin with 2-3 steps, then expand
2. **Test Each Step:** Verify each search and navigation works
3. **Use Descriptive Screenshots:** Name screenshots clearly
4. **Add Comments:** Document what each step does
5. **Handle Errors:** Scripts continue even if one step fails

## Example: Creating Your Own Complex Script

```tasklang
# My Complex Research Script
open chrome
go https://www.google.com/
wait 2

# Research topic 1
type "my research topic" in name "q"
enter in name "q"
wait 3
click css "a[href*='reliable-source.com']"
wait 4
screenshot topic1.png

# Research topic 2
go https://www.google.com/
wait 2
type "related topic" in name "q"
enter in name "q"
wait 3
screenshot topic2.png

close
```

## Summary

Complex scripts demonstrate:
- ✅ Multi-step workflows
- ✅ Starting from Google
- ✅ Navigating through multiple pages
- ✅ Gathering comprehensive information
- ✅ Real-world automation scenarios

All scripts are ready to use and can be customized for your specific needs!

