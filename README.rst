===============
singleton-admin
===============

Using singleton-admin will allow users to only add one instance of a model via the django admin site. Once created, the instance can be updated and deleted, but additional instances cannot be created. 

This is useful if you'd like to store a page content in the database for example.

I found myself using this package (https://github.com/tttallis/django-singletons) a lot, but some of the code has now been depreciated through newer releases of Django.

I originally had the intention of forking the package and making the fixes, but in the end I ended up re-writing from scratch. The end goal is the same, but with a different approach.

I appreciate that there are probably plenty of packages out there that offer similar functionality, but as I've put this together and have used in my own projects, I thought I'd get it out there.




Quick start
-----------

1. Install singleton-admin.

2. Add "singleton_admin" to your INSTALLED_APPS::

    INSTALLED_APPS = [
        ...
        'singleton_admin',
    ]

3. In your apps admin.py file to make your model a singleton-admin you can either do::

    from singleton_admin.admin import SingletonAdmin

    admin.site.register(your_model, SingletonAdmin)


Or if you'd like to add your own admin class::

    from singleton_admin.admin import SingletonAdmin

    class your_model_admin(SingletonAdmin):
    	...

    admin.site.register(your_model, your_model_admin)

    
