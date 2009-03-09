# -*- coding: utf-8 -*-

"""A simple backend for a TODO app, using Elixir"""

import os
from elixir import *

dbdir=os.path.join(os.path.expanduser("~"),".pyqtodo")
dbfile=os.path.join(dbdir,"tasks.sqlite")

# It's good policy to have your app use a hidden folder in 
# the user's home to store its files. That way, you can 
# always find them, and the user knows where everything is.

class Task(Entity):
    """
    A task for your TODO list.
    """
    
    # By inheriting Entity, we are using Elixir to make this 
    # class persistent, Task objects can easily be stored in 
    # our database, and you can search for them, change them, 
    # delete them, etc.        
    
    using_options(tablename='tasks')
    # This specifies the table name we will use in the database, 
    # I think it's nicer than the automatic names Elixir uses.
    
    text = Field(Unicode,required=True)
    date = Field(DateTime,default=None,required=False)
    done = Field(Boolean,default=False,required=True)
    tags  = ManyToMany("Tag")
    
    # A task has the following:
    #
    # * A text ("Buy groceries"). Always try to use unicode 
    #    in your app. Using anything else is *not worth 
    #    the trouble*. 
    #
    # * A date for when it's due.
    #
    # * A "Done" field. Is it done?
    #
    # * A list of tags. For example, "Buy groceries" could be 
    # tagged "Home" and "Important". It's ManyToMany because 
    # a task can have many tags and a tag can have many tasks.        
    
    def __repr__(self):
        return "Task: "+self.text
        
    # It's always nicer if objects know how to turn themselves 
    # into strings. That way you can help debug your program 
    # just by printing them. Here, our groceries task would 
    # print as "Task: Buy groceries".
    
# Since earlier I mentioned Tags, we need to define them too:

class Tag(Entity):
    """
    A tag we can apply to a task.
    """
    # Again, they go in the database, so they are an Entity.
    
    using_options(tablename='tags')
    name = Field(Unicode,required=True)
    tasks = ManyToMany("Task")
    
    def __repr__(self):
        return "Tag: "+self.name

    # They are much simpler objects: they have a name, 
    # a list of tagged tasks, and can convert themselves 
    # to strings.
    
saveData=None

# Using a database involves a few chores. I put them 
# in the initDB function. Just remember to call it before 
# trying to use Tasks or Tags!

def initDB():
    # Make sure ~/.pyqtodo exists
    if not os.path.isdir(dbdir):
        os.mkdir(dbdir)
    # Set up the Elixir internal thingamajigs
    metadata.bind = "sqlite:///%s"%dbfile
    setup_all()
    # And if the database doesn't exist: create it.
    if not os.path.exists(dbfile):
        create_all()
        
    # This is so Elixir 0.5.x and 0.6.x work
    # Yes, it's kinda ugly, but needed for Debian 
    # and Ubuntu and other distros.
    
    global saveData
    import elixir
    if elixir.__version__ < "0.6":
        saveData=session.flush
    else:
        saveData=session.commit
        
    
# Usually, I add a main() function to all modules that 
# does something useful, perhaps run unit tests. In this 
# case, it demonstrates our backend's functionality. 
# You can try it by running it like this::
#
#   python todo.py

# No detailed comments in this one: study it yourself, it's not complicated!

def main():
    
    # Initialize database
    initDB()
    
    # Create two tags
    green=Tag(name=u"green")
    red=Tag(name=u"red")
    
    #Create a few tags and tag them
    tarea1=Task(text=u"Buy tomatos",tags=[red])
    tarea2=Task(text=u"Buy chili",tags=[red])
    tarea3=Task(text=u"Buy lettuce",tags=[green])
    tarea4=Task(text=u"Buy strawberries",tags=[red,green])
    saveData()
    
    print "Green Tasks:"
    print green.tasks
    print
    print "Red Tasks:"
    print red.tasks
    print
    print "Tasks with l:"
    print [(t.id,t.text,t.done) for t in Task.query.filter(Task.text.like(ur'%l%')).all()]

if __name__ == "__main__":
    main()
