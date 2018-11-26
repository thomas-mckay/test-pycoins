from pycoins.models import Symbol
from ..utils import PyCoinsTestCase


class SymbolModelTests(PyCoinsTestCase):
    def test_symbol_model__manager(self):
        coin_ids = {self.bitcoin.pk, self.ethereum.pk}
        currency_ids = {self.euro.pk, self.us_dollar.pk}

        self.assertEqual(set(Symbol.objects.coins().values_list('id', flat=True)), coin_ids)
        self.assertEqual(set(Symbol.objects.currencies().values_list('id', flat=True)), currency_ids)

    def test_symbol_model__str(self):
        self.assertEqual('{}'.format(self.bitcoin), 'Bitcoin (btc/BTC)')
        self.assertEqual('{}'.format(self.euro), 'Euro (€/EUR)')
