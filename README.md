# datatyping
Safe data validation for greater documentation and maintainability.

``` python
>>> import datatyping
>>> structure = {
...	'id': int,
...	'cars': [{'model': str, 'passengers': int}],
... }
>>> data = {
... 	'id': 215,
...	'cars': [
...		{'model': 'Cadillac', 'passengers': 2},
...		{'model': 'Volvo', 'passengers': 4},
...	]
... }
>>> datatyping.validate(structure, data)
```


## Motivation
Inspired by ["How Python Makes Working With Data More Difficult in he Long Run"](https://jeffknupp.com/blog/2016/11/13/how-python-makes-working-with-data-more-difficult-in-the-long-run/). In the blog post, the author Jeff Knupp explains that Python is great for interactive data analysis, but once your code is in place, it's hard to see what's really going on, because you can't tell datatypes. E.g. if you data comes from an API you can only later see that some value is truthy or iterable or whatever and there is no way to refer to the structure in your code. This makes it hard to maintain. You really should read the article.


## Testimonials
> does the data good
>> -- [theelous3](https://github.com/theelous3)


## Justification
Type checking is not very pythonic.
- Explicit is better than implicit.
- Readability counts.
- Unlike most dynamic languages, you can't do `'a' + 1` in Python, because it could cause unwanted errors another place, later in your code. This prevents the same.


## Examples
``` python
>>> from datatyping import validate
>>> # Working with lists
>>> validate([int, str], [1, 'a'])
>>> validate([dict], [{'can have': 1}, {'any keys': 2}])
>>> validate([[int], [str]], [[1, 2, 3], ['a', 'b', 'c'])
>>> 
>>> # Working with dicts
>>> validate({'a': int, 'b': str}, {'a': 4, 'b': 'c'})
>>> validate({'a': int}, {'a': 2, 'b': 'oops'})
KeyError: {'b'}
>>> validate({'a': int}, {'a': 2, 'b': 'yay'}, strict=False)
```


## Notes
- Any and all contributions are welcome.
- Please open an issue if there's anything you can't make work.
- Please let me know if there is an unsupported data structure, you'd like to see support for.
- If you enjoy and use the software, you can [say thanks](https://saythanks.io/to/Zaab1t).
