# TaskLang Quick Reference Guide

## Command Syntax

### Browser Control

```tasklang
open chrome          # Open Chrome browser
open firefox         # Open Firefox browser
open edge            # Open Edge browser
open safari          # Open Safari browser
go https://example.com/    # Navigate to URL
close                # Close the browser
```

### Element Interaction

**Type text into an element:**
```tasklang
type "your text" in name "input_name"
type "search query" in id "search-box"
type "text" in css "input.search-field"
type "text" in xpath "//input[@type='text']"
```

**Click an element:**
```tasklang
click id "submit-button"
click name "login-btn"
click css "button.primary"
click xpath "//button[text()='Submit']"
```

**Press Enter in an element:**
```tasklang
enter in name "search"
enter in id "search-input"
```

### Other Commands

```tasklang
wait 3               # Wait for 3 seconds
screenshot output.png # Take a screenshot
```

## Selector Types

| Selector Type | Example | Description |
|--------------|---------|-------------|
| `id` | `id "search-box"` | Select by element ID |
| `name` | `name "q"` | Select by name attribute |
| `css` | `css "input.search"` | Select by CSS selector |
| `xpath` | `xpath "//input[@type='text']"` | Select by XPath |
| `tag` | `tag "button"` | Select by HTML tag name |

## Complete Examples

### Example 1: Google Search
```tasklang
open chrome
go https://google.com/
type "python tutorial" in name "q"
enter in name "q"
wait 3
screenshot results.png
close
```

### Example 2: Form Submission
```tasklang
open chrome
go https://example.com/form
type "John Doe" in id "name"
type "john@example.com" in id "email"
click id "submit-button"
wait 2
screenshot confirmation.png
close
```

### Example 3: GitHub Search
```tasklang
open chrome
go https://github.com/
wait 2
click css "input[placeholder*='Search']"
type "selenium" in css "input[placeholder*='Search']"
enter in css "input[placeholder*='Search']"
wait 3
screenshot github_results.png
close
```

## Tips

1. **Always specify selectors** for `type`, `click`, and `enter` commands to target specific elements
2. **Use `wait`** commands to allow pages to load before interacting
3. **Close browsers** with the `close` command to free resources
4. **Selector syntax**: Use `in selector_type "value"` format for clarity
5. **Quotes**: Always use double quotes for strings and selector values

## Running Scripts

**Compile a script:**
```bash
python -m src.main examples/your_script.task
```

**Use interactive selector:**
```bash
python run_scripts.py
```

