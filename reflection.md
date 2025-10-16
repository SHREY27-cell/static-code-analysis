## Issue Documentation Table

| Issue                  | Type     | Line(s) | Description                                                                                      | Fix Approach                                                                  |
| :--------------------- | :------- | :------ | :----------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------- |
| Use of `eval()`        | Security | 58      | Using `eval()` is a significant security risk as it can execute arbitrary code.                  | Remove the `eval()` call entirely as it's not needed.                         |
| Mutable Default Arg    | Bug      | 8       | The `logs=[]` list is created once and shared across all calls, leading to unexpected behavior.    | Change the default to `None` and initialize a new list inside the function.   |
| Bare `except` Clause   | Bug      | 17      | `except:` catches all exceptions, hiding bugs and making debugging difficult.                    | Specify the exact exception you expect, which is a `KeyError`.                |
| Unsafe File Handling   | Bug      | 29, 34  | Opening files without a `with` statement risks resource leaks if an error occurs.                | Use the `with open(...) as f:` syntax to ensure files are automatically closed. |

## Reflection Questions

**1. Which issues were the easiest to fix, and which were the hardest? Why?**
The easiest issue to fix was the use of `eval()`, as the solution was to simply remove the unnecessary and dangerous line. The mutable default argument was the most difficult because it requires understanding a subtle concept in Python about how default arguments are instantiated only once.

**2. Did the static analysis tools report any false positives? If so, describe one example.**
Yes, Pylint often flags single-letter variable names like `f` in `with open(...) as f:` as being too short (`invalid-name`). While technically a style violation, this is a very common and accepted convention in Python, so it could be considered a false positive in a practical sense.

**3. How would you integrate static analysis tools into your actual software development workflow?**
I would use them in two key places:
* **Locally:** Integrated into my code editor (like VS Code) to provide real-time feedback as I write code.
* **CI/CD Pipeline:** As part of a GitHub Action to automatically scan every code push. This would act as a quality gate, preventing code with security flaws or major bugs from being merged into the main branch.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**
The code is now significantly more robust and secure. Removing `eval` closed a major security hole, while adding specific exception handling and using `with open` prevents the program from crashing unexpectedly and leaking resources. The code is also more readable and predictable now that the shared `logs` list b