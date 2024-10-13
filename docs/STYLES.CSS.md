# STYLES.CSS.md

## Overview of `styles.css`

The `styles.css` file, located in the `assets` directory of the Azure Architecture Map application, contains custom CSS styles that define the appearance and layout of the application's components beyond what is provided by Bootstrap and default styles. This file allows developers to fine-tune the visual aspects of the application, ensuring a cohesive and polished user interface.

In Dash applications, any CSS files placed within the `assets` directory are automatically loaded and applied to the application. This makes it convenient to manage custom styles without the need for additional configuration.

---

## Table of Contents

- [Purpose of `styles.css`](#purpose-of-stylescss)
- [Structure of the File](#structure-of-the-file)
- [Detailed Explanation of Styles](#detailed-explanation-of-styles)
  - [1. Global Styles](#1-global-styles)
  - [2. Graph Element Styles](#2-graph-element-styles)
  - [3. Control Panel Styles](#3-control-panel-styles)
  - [4. Information Panel Styles](#4-information-panel-styles)
  - [5. Responsive Design](#5-responsive-design)
  - [6. Custom Classes](#6-custom-classes)
- [Integration with the Application](#integration-with-the-application)
- [Customization](#customization)
  - [Adding New Styles](#adding-new-styles)
  - [Overriding Bootstrap Styles](#overriding-bootstrap-styles)
  - [Best Practices](#best-practices)
- [Conclusion](#conclusion)
- [Additional Notes](#additional-notes)

---

## Purpose of `styles.css`

- **Customization**: Provides a way to customize the appearance of the application beyond the default styles offered by Dash and Bootstrap.
- **Consistency**: Ensures consistent styling across different components and pages of the application.
- **Fine-tuning**: Allows developers to adjust specific visual elements, improving the user interface and user experience.
- **Override Default Styles**: Enables overriding of default styles applied by external libraries when necessary.

---

## Structure of the File

While the exact content of `styles.css` may vary depending on the application's specific needs, it typically includes:

- **Global Styles**: Styles that affect the entire application or multiple components.
- **Component-Specific Styles**: Styles targeting specific components or elements, such as the graph, control panel, or information panel.
- **Responsive Styles**: Media queries and styles that adjust the layout for different screen sizes.
- **Custom Classes**: Classes defined for applying specific styles to elements, often used in conjunction with the `className` property in Dash components.

---

## Detailed Explanation of Styles

### 1. Global Styles

Global styles set the baseline for the application's appearance.

```css
body {
  margin: 0;
  padding: 0;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
}
```

- **body**: Resets margin and padding, sets a default font family, and applies a background color to the entire application.

### 2. Graph Element Styles

Styles that affect the appearance of the Cytoscape graph and its elements.

```css
/* Adjusts the appearance of the graph container */
#cytoscape-graph {
  border: 1px solid #ccc;
}

/* Styles for nodes when highlighted */
.highlighted {
  border: 2px solid #ff0000;
  background-color: #ffdddd;
}

/* Styles for nodes when selected */
:selected {
  border-color: #0000ff;
  border-width: 4px;
}
```

- **#cytoscape-graph**: Targets the graph component container, adding a border for visual separation.
- **.highlighted**: Defines styles for nodes that have the `highlighted` class applied, such as during a search operation.
- **:selected**: Pseudo-class for styling selected nodes within the graph.

### 3. Control Panel Styles

Styles applied to elements within the control panel.

```css
/* Styles for the control panel buttons */
.btn-group .btn {
  width: 100%;
  margin-bottom: 5px;
}

/* Adjusts input group styling */
.input-group {
  margin-bottom: 15px;
}
```

- **.btn-group .btn**: Ensures that buttons within a button group in the control panel are full-width and have consistent spacing.
- **.input-group**: Adds spacing below input groups, such as the search bar, for visual separation.

### 4. Information Panel Styles

Styles for the node information and notes sections.

```css
/* Styles for the node information section */
#node-info {
  margin-bottom: 15px;
}

/* Styles for the notes section */
#notes-section,
#rendered-notes-section {
  margin-top: 20px;
}

/* Textarea styling */
textarea#node-notes {
  resize: vertical;
}
```

- **#node-info**: Adds spacing below the node information to separate it from other content.
- **#notes-section, #rendered-notes-section**: Adds spacing above the notes sections.
- **textarea#node-notes**: Allows the textarea for notes to be resized vertically by the user.

### 5. Responsive Design

Media queries to adjust styles for different screen sizes.

```css
/* Adjust layout for smaller screens */
@media (max-width: 767px) {
  .control-panel,
  .information-panel {
    width: 100%;
    padding: 10px;
  }

  .graph-panel {
    width: 100%;
    height: 400px;
  }
}
```

- **@media (max-width: 767px)**: Targets screens smaller than 767 pixels wide.
- **.control-panel, .information-panel**: Sets the width to 100% and adjusts padding for better readability on small screens.
- **.graph-panel**: Adjusts the graph's height to fit smaller screens.

### 6. Custom Classes

Defining custom classes to be used in components.

```css
/* Class for hiding elements */
.hidden {
  display: none !important;
}

/* Class for alert styling */
.alert {
  margin-top: 15px;
}
```

- **.hidden**: A utility class to hide elements, using `!important` to override other display properties.
- **.alert**: Adds spacing above alerts to separate them from other content.

---

## Integration with the Application

- **Automatic Loading**: Dash automatically includes CSS files from the `assets` directory. `styles.css` is loaded and applied to the application without additional configuration.
- **Component Styling**:
  - Components in the layout reference classes and IDs defined in `styles.css`.
  - For example, the graph component has the ID `cytoscape-graph`, which is styled in the CSS file.
- **Callbacks and Classes**:
  - In `callbacks.py`, nodes may have classes added or removed (e.g., `'highlighted'`) based on user interactions.
  - These classes correspond to styles defined in `styles.css`.

---

## Customization

### Adding New Styles

To add new styles:

1. **Define Classes or IDs**: Add CSS selectors for the elements you wish to style.

   ```css
   /* New style for buttons */
   .my-custom-button {
     background-color: #123456;
     color: #ffffff;
   }
   ```

2. **Apply Classes in Components**: Use the `className` property in Dash components to apply the new styles.

   ```python
   dbc.Button("Click Me", className="my-custom-button")
   ```

### Overriding Bootstrap Styles

To override Bootstrap styles:

1. **Use Equal Specificity**: Write CSS selectors that match the specificity of Bootstrap's styles.

   ```css
   /* Override Bootstrap button primary color */
   .btn-primary {
     background-color: #ff6600;
     border-color: #ff6600;
   }
   ```

2. **Use `!important` Carefully**: If necessary, use `!important` to force a style override, but this should be done sparingly.

   ```css
   .btn-primary {
     background-color: #ff6600 !important;
   }
   ```

### Best Practices

- **Organize Styles**: Group related styles together and comment sections for readability.
- **Avoid Over-Specificity**: Use classes instead of IDs when possible to keep selectors simple and reusable.
- **Test Responsiveness**: Ensure that styles work well on different screen sizes and devices.
- **Minimize Use of `!important`**: Overusing `!important` can make styles harder to maintain.

---

## Conclusion

The `styles.css` file plays a vital role in defining the visual presentation of the Azure Architecture Map application. By customizing styles, developers can enhance the user interface, improve usability, and ensure a consistent look and feel throughout the application.

Understanding the styles defined in `styles.css` allows developers to:

- **Customize Appearance**: Tailor the application's visual elements to meet specific design requirements.
- **Enhance User Experience**: Improve the clarity and accessibility of components through thoughtful styling.
- **Maintain Consistency**: Ensure that styling is consistent across different parts of the application.

---

## Additional Notes

- **Cytoscape Styles vs. CSS**:
  - While `styles.css` affects the overall application and HTML elements, the Cytoscape graph's internal styles (e.g., node shapes, colors) are defined within the `stylesheet` parameter in the graph component or via Cytoscape's own styling mechanisms.
- **Debugging Styles**:
  - Use browser developer tools to inspect elements and understand how styles are applied and cascaded.
- **Performance Considerations**:
  - Keep the CSS file lean to avoid unnecessary loading times.
  - Minimize the use of large images or complex styles that can impact rendering performance.

---

**By understanding and effectively managing `styles.css`, developers can significantly influence the application's aesthetic appeal and usability, contributing to a more engaging and professional user experience.**