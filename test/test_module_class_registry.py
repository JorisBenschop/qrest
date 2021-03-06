import inspect
import unittest

from qrest import APIConfig, ResourceConfig
from qrest.module_class_registry import ModuleClassRegistry


class MyAPIConfig(APIConfig):
    pass


class FirstResourceConfig(ResourceConfig):
    name = "first"
    path = ["my", "first", "resource", "config"]
    method = "GET"


class SecondResourceConfig(ResourceConfig):
    name = "second"
    path = ["my", "first", "resource", "config"]
    method = "GET"


class ModuleClassRegistryTests(unittest.TestCase):
    def setUp(self):
        self.current_module = inspect.getmodule(ModuleClassRegistryTests)

    def test_find_APIConfig_classes(self):
        classes = ModuleClassRegistry(self.current_module)
        config_classes = classes.retrieve(APIConfig)
        self.assertEqual(
            1, len(config_classes), "the current module should contain a single APIConfig class"
        )
        self.assertTrue(
            issubclass(config_classes[0], MyAPIConfig),
            f"Class {config_classes[0]} should be a subclass of APIConfig",
        )

    def test_find_ResourceConfig_classes(self):
        classes = ModuleClassRegistry(self.current_module)
        config_classes = classes.retrieve(ResourceConfig)
        self.assertEqual(
            2, len(config_classes), "the current module should contain 2 ResourceConfig classes"
        )
        for config_class in config_classes:
            self.assertTrue(
                issubclass(config_class, ResourceConfig),
                f"Class {config_class} should be a subclass of ResourceConfig",
            )
