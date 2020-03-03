from unittest import TestCase


class Test(TestCase):
    def test_valido_dni(self):
        '''
        Comprobacion si dni es valido
        :return:
        '''
        from funcionescli import validoDNI
        self.assertTrue(validoDNI('53821397V'))

    def test_habitaciones_libres(self):
        '''
        Comprobacion si una habitacion es libre, si es True está libre
        :return:
        '''
        from funcionesreser import versilibre
        self.assertTrue(versilibre(True))
