# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - generic [ref=e3]:
    - generic [ref=e4]:
      - 'heading "Ping Champions: pinging the ponging" [level=1] [ref=e5]'
      - combobox "Language" [ref=e7] [cursor=pointer]:
        - option "Português (BR)"
        - option "English (US)" [selected]
    - navigation "breadcrumb" [ref=e8]:
      - link "Home" [ref=e9] [cursor=pointer]:
        - /url: /
      - text: /
      - link "Events" [ref=e10] [cursor=pointer]:
        - /url: /events
    - generic [ref=e11]:
      - heading "Events" [level=2] [ref=e12]
      - generic [ref=e14]:
        - textbox "Event Name" [ref=e15]
        - textbox [ref=e16]
        - textbox [ref=e17]
        - button "Create" [ref=e18] [cursor=pointer]
  - generic [ref=e19]:
    - generic "Toggle devtools panel" [ref=e20] [cursor=pointer]:
      - img [ref=e21]
    - generic "Toggle Component Inspector" [ref=e26] [cursor=pointer]:
      - img [ref=e27]
```