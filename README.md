# STL file analyzer

## Running
Only requires core library

#### Option 1 (python3 install locally)
Run `python3 cli.py /path/to/stl.file`

#### Option 2 (python3 container; docker installed locally)
Run `run-container.sh /path/to/stl.file`. Full disclosure I cant get the mount to work
properly on windows for the moment due to a rogue windows char. But it might work on a mac. 

## Run Tests
`python -m unittest`

### Testing philosophy
I tend to be a BDD testing person. That is, make sure the interface of your service is well defined and well tested. I grant that smaller scoped unit tests have there value, but that value is a calculation that is a function of the business's domain, cost structure, and risk tolerance vs speed of development. Now, I'd think a logistics platform would require a good amount of code coverage and nitty gritty testing.

## Design thinking
I prefer designing projects in a functional style. The goal here is conceptual simplicity. I defer abstraction until necessary if possible because although abstraction is very powerful, the wrong abstraction can be some very dangerous momentum.

### Typing
With regards to functional coding, I think well defined interfaces are super powerful. Im not a static typing guy per say but I am a fan of duck typing. python3 has this nice typing hint syntax that I think makes the code more understandable. I also like typed data _when the program/domain assumes it_, ie. defacto schemas.

### this program's interface
The program interface is the `api.py` and the current user interface is via the command line with `cli.py`. Truthfully the parser.py could be a bit cleaner. The thought experiment being: how easy would it be to update this code (per improvements below) for someone whose never seen it? and I think the hairiness around the stream.next_line muddles interfaces of the functions a bit.

## Performance improvements
Currently this streams a file into list of objects essentially. Although the file stream is lazy and therefore fairly efficient, the resulting in-memory data structure would be pretty hefty. Given the stats being calculated can be easily rolled up, ie. calculated with a running min/max coordinates and running sum, it would sufficient to just read 1 facet at a time and calculate its area and min/max coordinates and then recompute the running surface area and boundaries. So the in-memory use of the program would actually be pretty small.
