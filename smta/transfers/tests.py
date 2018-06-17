from django import test

from transfers import factories


class TransferModelTests(test.TestCase):
    def test_str(self):
        transfer = factories.TransferFactory()

        self.assertEqual(
            str(transfer),
            'paying_user transfers 35.79 to receiving_user'
        )
