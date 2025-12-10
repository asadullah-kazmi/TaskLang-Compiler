# Writing Your Own TaskLang Scripts

Yes! You can absolutely write your own TaskLang scripts. This guide will show you how.

## Creating a New Script

### Step 1: Create a `.task` File

Create a new file with the `.task` extension. You can:

- **Save it in the `examples/` folder** (recommended for organization)
- **Save it anywhere** on your computer

Example: `my_automation.task`

### Step 2: Write Your Script

Use the TaskLang syntax to write your automation script. Here's the basic structure:

```tasklang
open chrome                    # Open browser
go https://example.com/        # Navigate to URL
wait 2                        # Wait for page to load
type "text" in id "input"     # Type text into element
click id "button"             # Click a button
screenshot result.png         # Take screenshot
close                         # Close browser
```

### Step 3: Compile Your Script

**Using GUI:**

```bash
python run_gui.py
# Then browse and select your .task file
```

**Using Command Line:**

```bash
python -m src.main path/to/your_script.task
```

### Step 4: Run the Generated Script

```bash
python output/your_script.py
```

## Complete Syntax Reference

### Browser Commands

```tasklang
open chrome          # Open Chrome browser
open firefox         # Open Firefox browser
open edge            # Open Edge browser
open safari          # Open Safari browser
go https://url.com/  # Navigate to a URL
close                # Close the browser
```

### Element Interaction

**Type text:**

```tasklang
type "your text" in name "input_name"
type "search" in id "search-box"
type "text" in css "input.search"
type "text" in xpath "//input[@type='text']"
```

**Click elements:**

```tasklang
click id "submit-button"
click name "login-btn"
click css "button.primary"
click xpath "//button[text()='Submit']"
```

**Press Enter:**

```tasklang
enter in name "search"
enter in id "search-input"
```

### Other Commands

```tasklang
wait 3               # Wait for 3 seconds
screenshot file.png  # Take a screenshot
```

## Selector Types

| Type    | Example                           | Use Case                  |
| ------- | --------------------------------- | ------------------------- |
| `id`    | `id "username"`                   | Unique element ID         |
| `name`  | `name "email"`                    | Form input names          |
| `css`   | `css "button.submit"`             | CSS selectors             |
| `xpath` | `xpath "//div[@class='content']"` | Complex element selection |
| `tag`   | `tag "button"`                    | HTML tag names            |

## Real-World Examples

### Example 1: Login Form

```tasklang
open chrome
go https://example.com/login
wait 2
type "myusername" in id "username"
type "mypassword" in id "password"
click id "login-button"
wait 3
screenshot login_result.png
close
```

### Example 2: Search and Click

```tasklang
open chrome
go https://example.com/
wait 2
type "python tutorial" in css "input.search-field"
enter in css "input.search-field"
wait 3
click css "a.result-link"
wait 2
screenshot tutorial_page.png
close
```

### Example 3: Form Submission

```tasklang
open chrome
go https://example.com/contact
wait 2
type "John Doe" in name "name"
type "john@example.com" in name "email"
type "Hello, this is a test message" in id "message"
click id "submit"
wait 2
screenshot confirmation.png
close
```

### Example 4: Multiple Page Navigation

```tasklang
open chrome
go https://example.com/
wait 2
click css "a.about-link"
wait 2
screenshot about_page.png
go https://example.com/products
wait 2
screenshot products_page.png
close
```

## Tips for Writing Scripts

### 1. Always Use Wait Commands

Pages need time to load. Use `wait` after navigation:

```tasklang
go https://example.com/
wait 2                    # Wait for page to load
```

### 2. Use Specific Selectors

Prefer `id` or `name` over `tag` when possible:

```tasklang
# Good - specific
click id "submit-button"

# Less specific - use only if needed
click tag "button"
```

### 3. Test Your Selectors

Before writing a full script, test if your selectors work:

```tasklang
open chrome
go https://example.com/
wait 2
click id "your-element"    # Test this selector
wait 2
close
```

### 4. Take Screenshots for Debugging

Screenshots help verify your script is working:

```tasklang
screenshot step1.png
# ... do something ...
screenshot step2.png
```

### 5. Always Close the Browser

Don't forget to close the browser at the end:

```tasklang
close
```

## Finding Element Selectors

### Using Browser Developer Tools

1. **Right-click** on an element on the webpage
2. **Select "Inspect"** or "Inspect Element"
3. **Look for:**
   - `id="..."` → Use `id "value"`
   - `name="..."` → Use `name "value"`
   - `class="..."` → Use `css ".class-name"`
   - Complex elements → Use `xpath` or `css`

### Example: Finding a Search Box

HTML:

```html
<input id="search" name="q" class="search-input" type="text" />
```

TaskLang options:

```tasklang
type "text" in id "search"        # Best - unique ID
type "text" in name "q"            # Good - name attribute
type "text" in css ".search-input"  # Good - CSS class
```

## Common Patterns

### Pattern 1: Search Flow

```tasklang
open chrome
go https://search-site.com/
wait 2
type "query" in id "search-box"
enter in id "search-box"
wait 3
screenshot results.png
close
```

### Pattern 2: Form Fill

```tasklang
open chrome
go https://form-site.com/
wait 2
type "value1" in id "field1"
type "value2" in id "field2"
click id "submit"
wait 2
screenshot submitted.png
close
```

### Pattern 3: Navigation Flow

```tasklang
open chrome
go https://site.com/page1
wait 2
click css "a.next-page"
wait 2
screenshot page2.png
close
```

## Troubleshooting

### Script doesn't find element

- **Check selector:** Use browser dev tools to verify the selector
- **Add wait:** Elements might not be loaded yet
- **Try different selector:** Use `id` or `name` instead of `css`

### Browser doesn't open

- **Check browser name:** Use `chrome`, `firefox`, `edge`, or `safari`
- **Install drivers:** Make sure browser drivers are installed

### Script runs too fast

- **Add wait commands:** Use `wait 2` or `wait 3` between actions
- **Increase wait time:** Some pages need more time to load

## Next Steps

1. **Start simple:** Write a basic script that opens a page and takes a screenshot
2. **Add interactions:** Add typing and clicking
3. **Test frequently:** Compile and run after each change
4. **Use the GUI:** The GUI makes it easy to test and debug

## Example: Your First Script

Create `my_first_script.task`:

```tasklang
open chrome
go https://www.example.com/
wait 2
screenshot my_first_screenshot.png
close
```

Compile it:

```bash
python -m src.main my_first_script.task
```

Run it:

```bash
python output/my_first_script.py
```

Congratulations! You've written your first TaskLang script! 🎉
