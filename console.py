#!/usr/bin/python3
"""
    Implementing the console for the HBnB project.
"""
import cmd
import json
import shlex
import models
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import classes


class HBNBCommand(cmd.Cmd):
    """
        Contains the entry point of the command interpreter.
    """

    prompt = ("(hbnb) ")
    all_classes = classes

    def do_quit(self, args):
        '''
            Quit command to exit the program.
        '''
        return True

    def do_EOF(self, args):
        '''
            Exits after receiving the EOF signal.
        '''
        return True

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        arg_array = args.split(' ')
        if arg_array[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        kwargs = dict()
        for i in range(1, len(arg_array)):
            attr_array = arg_array[i].split('=')
            if "\"" in attr_array[1] and attr_array[1][-1] == "\"":
                attr_array[1] = attr_array[1][1:-1]
                if "_" in attr_array[1]:
                    attr_array[1] = attr_array[1].replace("_", " ")
            elif "." in attr_array[1]:
                try:
                    attr_array[1] = float(attr_array[1])
                except Exception:
                    continue
            else:
                try:
                    attr_array[1] = int(attr_array[1])
                except Exception:
                    continue
            kwargs[attr_array[0]] = attr_array[1]
        new_instance = HBNBCommand.classes[arg_array[0]]()
        new_instance.__dict__.update(kwargs)
        print(new_instance.id)
        new_instance.save()

    def do_show(self, line):
        '''
            Print the string representation of an instance based on
            the class name and id given as args.
        '''
        args = shlex.split(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.all_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            objs = models.storage.all()
            key = '{}.{}'.format(args[0], args[1])
            try:
                obj = objs[key]
                print(obj)
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, line):
        '''
            Deletes an instance based on the class name and id.
        '''
        args = shlex.split(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.all_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            objs = models.storage.all()
            key = '{}.{}'.format(args[0], args[1])
            try:
                obj = objs[key]
                objs.pop(key)
                del obj
                models.storage.save()
            except KeyError:
                print("** no instance found **")

    def do_all(self, line):
        '''
            Prints all string representation of all instances
            based or not on the class name.
        '''
        args = shlex.split(line)
        obj_list = []
        if len(args) >= 1:
            if args[0] not in self.all_classes:
                print("** class doesn't exist **")
            else:
                objs = models.storage.all(args[0])
                for key, obj in objs.items():
                    if key.startswith(args[0]):
                        obj_list.append(obj)
                print(obj_list)
        else:
            objs = models.storage.all()
            for obj in objs.values():
                obj_list.append(obj)
            print(obj_list)

    def do_update(self, args):
        '''
            Update an instance based on the class name and id
            sent as args.
        '''
        models.storage.reload()
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        elif len(args) == 2:
            print("** attribute name missing **")
            return
        elif len(args) == 3:
            print("** value missing **")
            return
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        obj_dict = models.storage.all()
        try:
            obj_value = obj_dict[key]
        except KeyError:
            print("** no instance found **")
            return
        try:
            attr_type = type(getattr(obj_value, args[2]))
            args[3] = attr_type(args[3])
        except AttributeError:
            pass
        setattr(obj_value, args[2], args[3])
        obj_value.save()

    def emptyline(self):
        '''
            Prevents printing anything when an empty line is passed.
        '''
        pass

    def do_count(self, line):
        '''
            Counts/retrieves the number of instances.
        '''
        args = shlex.split(line)
        if len(args) >= 1:
            if args[0] not in self.all_classes:
                print("** class doesn't exist **")
            else:
                objs = models.storage.all(args[0])
                print(len(objs))
        else:
            objs = models.storage.all()
            print(len(objs))

    def default(self, args):
        '''
            Catches all the function names that are not expicitly defined.
        '''
        functions = {"all": self.do_all, "update": self.do_update,
                     "show": self.do_show, "count": self.do_count,
                     "destroy": self.do_destroy, "update": self.do_update}
        args = (args.replace("(", ".").replace(")", ".")
                .replace('"', "").replace(",", "").split("."))

        try:
            cmd_arg = args[0] + " " + args[2]
            func = functions[args[1]]
            func(cmd_arg)
        except:
            print("*** Unknown syntax:", args[0])


if __name__ == "__main__":
    '''
        Entry point for the loop.
    '''
    HBNBCommand().cmdloop()
