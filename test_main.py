import unittest

from main import find_emails, is_email


class EmailTests(unittest.TestCase):
    def test_valid_addresses(self):
        addresses = (
            "user@example.org", " Anna.Petrova+lab@sub.example.net ",
            "o'neal@example.org", "test@my-site.example",
        )
        for address in addresses:
            with self.subTest(address=address):
                self.assertTrue(is_email(address))

    def test_invalid_addresses(self):
        addresses = (
            "", "user", "user@@example.org", "user@localhost",
            ".a@example.org", "a..b@example.org", "a.@example.org",
            "a@-example.org", "a@example-.org", "a@exam_ple.org",
            "a@example.123", "a@example.org.", "a b@example.org",
        )
        for address in addresses:
            with self.subTest(address=address):
                self.assertFalse(is_email(address))

    def test_length_limits(self):
        self.assertTrue(is_email("a" * 64 + "@example.org"))
        self.assertFalse(is_email("a" * 65 + "@example.org"))
        self.assertFalse(is_email("a@" + "b" * 64 + ".org"))
        long_domain = ("b" * 63 + ".") * 3 + "org"
        self.assertFalse(is_email("a" * 64 + "@" + long_domain))

    def test_search_and_duplicates(self):
        text = "Почта: <a@Example.org>, b+tag@site.net. Повтор: a@example.org"
        self.assertEqual(find_emails(text), ["a@example.org", "b+tag@site.net"])

    def test_search_skips_invalid_fragments(self):
        text = "a..b@example.org a@example.org@x.org a@example.org_bad"
        self.assertEqual(find_emails(text), [])

    def test_no_matches(self):
        self.assertEqual(find_emails("Почтовых адресов нет"), [])


if __name__ == "__main__":
    unittest.main()
