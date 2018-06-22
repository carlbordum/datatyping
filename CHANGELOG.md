# Changelog
## 0.6.0 (2017-11-09)
- Better exception messages with `reprlib.repr`
- External documentation (http://datatyping.rtfd.io)
- Checks that types are actually the same or a subclass instead of just of the
    same abstract type Sequence/Mapping


## 0.5.0 (2017-11-09)
- Replaced "contracts" with @customtype
- Works with all `collections.abc.Mapping` instead of just dicts.
- `validate` throws ValueError instead of undocumented AssertionError.
- New description: "Pythonic type checking"
- First PyPI release!


## 0.4.0 (2017-09-18)
- Added support for tuples
- Fixed bug with str (not considered sequence anymore)
- Reasonble versioning scheme :p


## 0.0.3 (2017-08-20)
- Added printer


## 0.0.2 (2017-07-27)
- Added contracts


## 0.0.1 (2017-07-26)
- Initial release
