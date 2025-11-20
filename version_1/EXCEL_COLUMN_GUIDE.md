# Excel Report Column Guide

## Understanding the Navigation Validation Results

When you open the Excel report (`navigation_report_*.xlsx`), you'll see different sheets with specific columns. Here's what each column means:

---

## Sheet 1: "Summary"
This sheet shows an overview of the validation results.

| Column | Meaning |
|--------|---------|
| **Main Menu Items** | Total number of main menu items (Product, Insights, Support, Partner, Company) |
| **Visible Main Menu Items** | How many of them are visible on the page |
| **Sub-Menu Items** | Total number of sub-menu links found |
| **Links Checked** | Total navigation links that were tested |
| **Valid Links** | Number of links that returned HTTP 200 (working) |
| **Broken Links** | Number of links that returned errors (404, 403, etc.) |

---

## Sheet 2: "Main Menu"
This sheet shows the status of each main menu item.

| Column | Meaning |
|--------|---------|
| **Menu Name** | The name of the main menu (Product, Insights, etc.) |
| **Text** | The actual text displayed |
| **Is Visible** | TRUE if the menu item is visible on the page |
| **Has Mega Menu** | TRUE if the menu has a dropdown/mega menu |
| **Status** | PASS = All good, FAIL = Something wrong |

---

## Sheet 3: "Sub-Menu Details" ⭐ **NEW!**

This is the detailed breakdown showing **every sub-menu link** with its validation status.

### Column Meanings:

#### Column A: "Menu"
- Which main menu this link belongs to (Product, Insights, Support, etc.)

#### Column B: "Link Text"  
- The clickable text of the link (e.g., "Solid State Drives (SSDs)")

#### Column C: "URL"
- The web address the link points to (e.g., "/products/data-center.html")

#### Column D: "Status Code" ⚠️ **This is what you saw as "0" and "FALSE"**
- **HTTP Status Code** - Response from the server when checking the link
- **200** = Link works perfectly ✅
- **404** = Page not found ❌
- **403** = Access forbidden ❌
- **500** = Server error ❌
- **0** = Not checked yet (may take time to validate all links)

#### Column E: "Is Visible"
- **TRUE** = Link is visible on the page
- **FALSE** = Link exists but may be hidden or require interaction (like hovering over menu)

---

## Color Coding:

- 🟢 **Green Background** = Link works (Status Code 200)
- 🟡 **Yellow Background** = Not yet checked or pending (Status Code 0)
- 🔴 **Red Background** = Link is broken or returns error

---

## Sheet 4: "Broken Links"
This sheet lists only the links that failed validation.

| Column | Meaning |
|--------|---------|
| **Text** | Link text |
| **URL** | Link URL |
| **Status Code** | Error code (404, 403, etc.) |
| **Is Visible** | Whether link was visible |

---

## What "0" and "FALSE" Mean:

### Status Code = 0
- The link exists in the navigation structure
- But it hasn't been fully validated yet (checking takes time)
- This is normal for some validation runs

### Is Visible = FALSE
- The link exists in the HTML
- But it's not visible in the current view (might be inside a collapsed menu)
- This is normal for sub-menu items that only appear on hover

---

## How to Read the Results:

### Example Row:
```
Menu: Product
Link Text: Solid State Drives (SSDs)
URL: /products/data-center.html
Status Code: 0
Is Visible: FALSE
```

**This means:**
- The link is in the "Product" menu
- It points to "/products/data-center.html"  
- It hasn't been fully validated yet (Status Code 0)
- It's not currently visible (probably hidden in dropdown)

### Better Example (After Full Validation):
```
Menu: Product
Link Text: Solid State Drives (SSDs)
URL: /products/data-center.html
Status Code: 200 ✅
Is Visible: TRUE
```

**This means:**
- The link is valid and works! ✅
- Returns HTTP 200 (success)
- Is visible to users

---

## Next Steps:

To get actual status codes (not 0):

1. The script validates links sequentially
2. Some links may show "0" if validation is still in progress
3. Re-run the script to get complete results
4. Check the "Broken Links" sheet for actual broken links

---

## Quick Guide:

- **Status Code 200** = ✅ Working
- **Status Code 0** = ⏳ Checking...
- **Status Code 404** = ❌ Page Not Found
- **Status Code 403** = ❌ Forbidden
- **Status Code 500** = ❌ Server Error

All columns help you understand what links work and what doesn't!

