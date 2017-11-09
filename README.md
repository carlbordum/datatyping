# datatyping
Safe data validation for greater documentation and maintainability.

``` python
>>> import datatyping
>>> structure = {
...     'id': int,
...     'cars': [{'model': str, 'passengers': int}],
... }
>>> data = {
...     'id': 215,
...     'cars': [
...         {'model': 'Cadillac', 'passengers': 2},
...         {'model': 'Volvo', 'passengers': 4},
...     ]
... }
>>> datatyping.validate(structure, data)
```

``` bash
pip install git+https://github.com/Zaab1t/datatyping
```


## Benefits
- Documentation of incoming data in source code.
- Good for testing (especially if you offer something like a json api).
- Early failure in a specific spot if data is malformed.
- Readable, explicit code base.


## Features
### Basics
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
### Custom types
``` python
>>> from datatyping import validate, customtype
>>> @customtype
>>> def positive_int(i):
...     if i < 1:
...         raise TypeError('%d is not positive' % i)

>>> validate([positive_int], [1, 2, 3, 4])
>>> validate([positive_int], [1, 2, 3, -4])
TypeError: -4 is not positive
```

### Structure generation
Since typing out the structure can be quite tedious, `datatyping` provides a tool that does most of the work for you:

``` python
>>> from datatyping.printer import pprint
>>> import requests
>>> r = requests.get('http://httpbin.org/anything')
>>> pprint(r.json())
{   
    'args': dict,
    'data': str,
    'files': dict,
    'form': dict,
    'headers': {   
        'Accept': str,
        'Accept-Encoding': str,
        'Connection': str,
        'Host': str,
        'User-Agent': str,
    },
    'json': NoneType,
    'method': str,
    'origin': str,
    'url': str,
}

```


## Testimonials
> does the data good
>> -- [theelous3](https://github.com/theelous3)


## Develop with me :)

``` bash
# fork it
$ git clone https://github.com/your_name/datatyping
$ cd datatyping
$ sudo python3 setup.py develop
# make your changes, commit and push
$ python3 -m pytest
# submit a pull request
```


## Notes
- Inspired by ["How Python Makes Working With Data More Difficult in the Long Run"](https://jeffknupp.com/blog/2016/11/13/how-python-makes-working-with-data-more-difficult-in-the-long-run/).
- Any and all contributions are welcome.
- Please open an issue if there's anything you can't make work (read: I messed up).
- Please let me know if there is an unsupported data structure, you'd like to see support for.
- If you enjoy and use the software, you can [say thanks](https://saythanks.io/to/Zaab1t) :)
