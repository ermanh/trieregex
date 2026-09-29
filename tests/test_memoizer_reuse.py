import gc
import unittest

from trieregex import TrieRegEx as TRE


class TestMemoizerAddressReuse(unittest.TestCase):
    """regex() must not return another instance's pattern after address reuse."""

    def test_regex_stable_across_many_ephemeral_instances(self):
        stale = 0
        for i in range(20000):
            words = ("alpha", "alphabet") if i % 2 == 0 else ("beta", "betamax")
            pat = TRE(*words).regex()
            if words[0] == "beta" and "alpha" in pat and "beta" not in pat:
                stale += 1
            if i % 500 == 0:
                gc.collect()
        self.assertEqual(stale, 0, f"{stale} stale patterns after address reuse")


if __name__ == "__main__":
    unittest.main()
