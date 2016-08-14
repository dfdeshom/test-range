# RangeDB
RangeDB is a toy in-memory threadsafe query engine that users can interact with
via an HTTP server. The objects it accepts looks like:

    {
     "identifier": "foo",
     "ranges": [[12,34],[37,440],[460,800]]
    }

`identifer` and `ranges` mut be present.

## Operations
There are 3 kinds of operations this server accepts:
 - `/write` which is POST operation that writes a new range object to
 the database. If the object already exists, it will be
 overwritten. The POST data mut be in json string format like so: `{"identifier":"data", "ranges":["1","4"]}`
 - `/get?identifer=<id>` which retrieves a range object that matches
 `idetifier`. 
 - `/ranges?range=<range>` which gets a list of objects that overlap a
   specific range. `<range>` is of the form `[start,end]`. 
- `/` which lists all objects in the database
   
## Building/running
To run:

    $ pip install -r requirements.txt
    $ ./runserver.sh


## Assumptions and implementation notes
We use a dict as the underlying data store, for which most atomic operations are
safe (get, set). For operations that do a get-and-set, we use a
reentrant lock.

Although the code is threadsafe, we assume that the server will be
deployed in a multiprocess environment. This is because meaningful
operations like finding a range are CPU rather than 
I/O-bound and use of threads in Python is prescribed for operations
that are I/O-bound. This also doesn't make evented web servers like
Tornado ideal for use, which is why we chose the Flask web server as a
test server implementation.

A multiprocess environemnt also implies that
clients would have to be smart about which servers they write and request data
to. Such client is not included here.
 
