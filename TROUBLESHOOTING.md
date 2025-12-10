# Troubleshooting Common Issues

## Element Not Found Errors

### Error: `NoSuchElementException: Unable to locate element`

This happens when the script tries to find an element that doesn't exist on the page.

**Common Causes:**
1. **Element ID/name changed** - Websites update their HTML frequently
2. **Page not fully loaded** - Element appears after page loads
3. **Wrong selector** - Selector doesn't match the actual element

**Solutions:**

#### Solution 1: Use Enter Instead of Click
Instead of clicking a search button, press Enter in the input field:

```tasklang
# Instead of this (might fail):
type "query" in name "search"
click id "search-button"

# Use this (more reliable):
type "query" in name "search"
enter in name "search"
```

#### Solution 2: Increase Wait Time
Add more wait time for pages to load:

```tasklang
go https://example.com/
wait 5              # Increase from 2 to 5 seconds
type "text" in id "input"
```

#### Solution 3: Verify Selector in Browser
1. Open the webpage in your browser
2. Press F12 to open Developer Tools
3. Use the element inspector to find the correct selector
4. Update your script with the correct selector

#### Solution 4: Try Different Selector Types
If `id` doesn't work, try `name`, `css`, or `xpath`:

```tasklang
# Try different selectors:
click id "button-id"           # First try ID
click name "button-name"        # Then try name
click css "button.search-btn"   # Then try CSS
click xpath "//button[@type='submit']"  # Finally try XPath
```

## Fixed Examples

### YouTube Search (Fixed)
The original script tried to click a button that doesn't exist. Fixed version:

```tasklang
open chrome
go https://www.youtube.com/
wait 3
type "python tutorial" in name "search_query"
enter in name "search_query"    # Press Enter instead of clicking button
wait 3
screenshot youtube_results.png
close
```

## Best Practices to Avoid Errors

### 1. Always Use Enter for Search Boxes
Search boxes usually respond to Enter key, which is more reliable than clicking buttons:

```tasklang
type "search query" in id "search-box"
enter in id "search-box"    # More reliable than clicking
```

### 2. Add Adequate Wait Times
Modern websites load content dynamically. Give them time:

```tasklang
go https://example.com/
wait 3              # Wait for page to fully load
# Then interact with elements
```

### 3. Test Selectors First
Before writing a full script, test if your selector works:

```tasklang
open chrome
go https://example.com/
wait 3
click id "your-element"    # Test this first
wait 2
close
```

### 4. Use Screenshots for Debugging
Take screenshots at different steps to see what's happening:

```tasklang
go https://example.com/
wait 2
screenshot step1.png    # See if page loaded
type "text" in id "input"
screenshot step2.png    # See if typing worked
```

## Common Error Messages

### `selenium.common.exceptions.NoSuchElementException`
**Meaning:** Element not found on the page
**Fix:** Check selector, add wait time, or use different selector

### `selenium.common.exceptions.TimeoutException`
**Meaning:** Page took too long to load
**Fix:** Increase wait time or check internet connection

### `selenium.common.exceptions.WebDriverException`
**Meaning:** Browser driver issue
**Fix:** Make sure browser drivers (ChromeDriver, GeckoDriver) are installed

## Getting Help

1. **Check the error message** - It usually tells you what went wrong
2. **Verify selectors** - Use browser dev tools (F12) to check elements
3. **Test incrementally** - Add one command at a time and test
4. **Check website changes** - Websites update frequently, selectors may change

## Debugging Workflow

1. **Start simple:**
   ```tasklang
   open chrome
   go https://example.com/
   wait 3
   screenshot test.png
   close
   ```

2. **Add one interaction at a time:**
   ```tasklang
   open chrome
   go https://example.com/
   wait 3
   type "test" in id "input"    # Add this
   screenshot step1.png
   close
   ```

3. **Test each step** before adding the next one

4. **Use screenshots** to verify each step worked

