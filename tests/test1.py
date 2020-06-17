import os
import unittest

from confyaml import Config


class SanityTest(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    def test_app_name(self):
        config = Config()
        self.assertEqual(config.app_name, "test")

    def test_list(self):
        config = Config()
        for elem in config.a_list:
            if hasattr(elem, "element_1"):
                self.assertEqual(getattr(elem, "element_1"), "I am the first element")
            elif hasattr(elem, "element_2"):
                self.assertEqual(getattr(elem, "element_2"), 2)
            elif hasattr(elem, "element_3"):
                self.assertEqual(getattr(elem, "element_3"), "I am a dict")
            elif hasattr(elem, "subelement_1"):
                self.assertEqual(getattr(elem, "subelement_1"), 1)
            elif hasattr(elem, "subelement_2"):
                self.assertEqual(getattr(elem, "subelement_2"), "Second element")
            elif hasattr(elem, "subelement_3"):
                self.assertEqual(getattr(elem, "subelement_3"), 3.14)

    def test_nested_element(self):
        config = Config()
        self.assertEqual(config.another.nested.element, "Oh, you found me!")

    def test_another_file(self):
        config = Config(os.path.abspath(os.path.join(__file__, os.pardir, "another_config.yaml")))
        self.assertEqual(config.app_name, "test another config")
        self.assertEqual(config.number_1, 1)
        self.assertEqual(config.number_pi, 3.1415)

    def test_bracket_operator(self):
        config = Config()
        self.assertEqual(config["app_name"], "test")
        self.assertEqual(config["another"]["nested"]["element"], config.another.nested.element)
        config["app_name"] = "test2"
        self.assertEqual(config["app_name"], "test2")
        self.assertEqual(config.app_name, "test2")

    def test_inexistent_params(self):
        config = Config()
        with self.assertRaises(AttributeError):
            config["souveniers"]
        with self.assertRaises(AttributeError):
            config.souveniers
        with self.assertRaises(AttributeError):
            config.get("souveniers")


class GetSetSaveTest(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    def test_get(self):
        config = Config()
        self.assertEqual(config.get("app_name"), "test")

    def test_set(self):
        config = Config()
        config.set("app_name", "test2")
        self.assertEqual(config.get("app_name"), "test2")
        self.assertEqual(config.app_name, "test2")
        self.assertEqual(config["app_name"], "test2")

    def test_save(self):
        config = Config()
        new_config = Config()
        new_config.app_name = "new config"
        new_config_path = os.path.abspath(os.path.join(__file__, os.pardir, "new_config.yaml"))
        new_config.save(new_config_path)
        del new_config
        new_config = Config(new_config_path)
        self.assertEqual(config.another.nested.element, new_config.another.nested.element)
        self.assertNotEqual(config.app_name, new_config.app_name)
        os.remove(new_config_path)


if __name__ == '__main__':
    unittest.main()
