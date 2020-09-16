---
name: bug report
about: Create a report to a bug or regression
title: 'bug: '
labels: regression
assignees: ''

---

**Describe the bug**

A clear and concise description of what the bug is. [e.g. "`bleach.clean` does not escape script tag contents"]

** python and bleach versions (please complete the following information):**

 - Python Version: [e.g. 3.8.2]
 - Bleach Version: [e.g. 3.2.0]

**To Reproduce**

Steps to reproduce the behavior:

[e.g. ```python
>>> bleach.clean("><script>alert("XSS")</script>&")
"><script>alert("XSS")</script>&"
```]

**Expected behavior**

[e.g. ```python
>>> bleach.clean("><script>alert("XSS")</script>&")
'&gt;"&gt;&lt;script&gt;alert("XSS")&lt;/script&gt;&amp;'
```]

**Additional context**

Add any other context about the problem here.
