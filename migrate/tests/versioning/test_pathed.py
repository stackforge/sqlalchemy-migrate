from migrate.tests import fixture
from migrate.versioning.pathed import *

class TestPathed(fixture.Base):
    def test_parent_path(self):
        """Default parent_path should behave correctly"""
        filepath='/fgsfds/moot.py'
        dirpath='/fgsfds/moot'
        sdirpath='/fgsfds/moot/'

        result='/fgsfds'
        self.assert_(result==Pathed._parent_path(filepath))
        self.assert_(result==Pathed._parent_path(dirpath))
        self.assert_(result==Pathed._parent_path(sdirpath))

    def test_new(self):
        """Pathed(path) shouldn't create duplicate objects of the same path"""
        path='/fgsfds'
        class Test(Pathed):
            attr=None
        o1=Test(path)
        o2=Test(path)
        self.assert_(isinstance(o1, Test))
        self.assert_(o1.path==path)
        self.assert_(o1 is o2)
        o1.attr='herring'
        self.assert_(o2.attr=='herring')
        o2.attr='shrubbery'
        self.assert_(o1.attr=='shrubbery')

    def test_parent(self):
        """Parents should be fetched correctly"""
        class Parent(Pathed):
            parent=None
            children=0
            def _init_child(self, child, path):
                """Keep a tally of children.
                (A real class might do something more interesting here)
                """
                self.__class__.children+=1

        class Child(Pathed):
            parent=Parent

        path='/fgsfds/moot.py'
        parent_path='/fgsfds'
        object=Child(path)
        self.assert_(isinstance(object, Child))
        self.assert_(isinstance(object.parent, Parent))
        self.assert_(object.path==path)
        self.assert_(object.parent.path==parent_path)
