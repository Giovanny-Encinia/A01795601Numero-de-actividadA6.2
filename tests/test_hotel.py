import unittest
import os
import __init__  # noqa
from main import SistemaReservas


class TestSistemaReservas(unittest.TestCase):
    """Clase para probar el sistema de reservas."""

    def setUp(self):
        """Configuración inicial para las pruebas."""
        hotel = "test_hoteles.json"
        clientes = "test_clientes.json"
        self.sistema = SistemaReservas(hotel, clientes)
        self.sistema.crear_hotel("Hotel A", "Ubicación A", 10)
        self.sistema.crear_cliente("Cliente A", "clienteA@example.com")

    def tearDown(self):
        """Limpieza después de las pruebas."""
        if os.path.exists("test_hoteles.json"):
            os.remove("test_hoteles.json")
        if os.path.exists("test_clientes.json"):
            os.remove("test_clientes.json")

    def test_crear_hotel(self):
        """Prueba la creación de un hotel."""
        self.sistema.crear_hotel("Hotel B", "Ubicación B", 5)
        hotel = self.sistema.mostrar_hotel("Hotel B")
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel["nombre"], "Hotel B")
        self.assertEqual(hotel["ubicacion"], "Ubicación B")
        self.assertEqual(hotel["habitaciones"], 5)

    def test_eliminar_hotel(self):
        """Prueba la eliminación de un hotel."""
        self.sistema.eliminar_hotel("Hotel A")
        hotel = self.sistema.mostrar_hotel("Hotel A")
        self.assertIsNone(hotel)

    def test_modificar_hotel(self):
        """Prueba la modificación de un hotel."""
        self.sistema.modificar_hotel("Hotel A", "Nueva Ubicación", 15)
        hotel = self.sistema.mostrar_hotel("Hotel A")
        self.assertEqual(hotel["ubicacion"], "Nueva Ubicación")
        self.assertEqual(hotel["habitaciones"], 15)

    def test_crear_cliente(self):
        """Prueba la creación de un cliente."""
        self.sistema.crear_cliente("Cliente B", "clienteB@example.com")
        cliente = self.sistema.mostrar_cliente("clienteB@example.com")
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente["nombre"], "Cliente B")
        self.assertEqual(cliente["email"], "clienteB@example.com")

    def test_eliminar_cliente(self):
        """Prueba la eliminación de un cliente."""
        self.sistema.eliminar_cliente("clienteA@example.com")
        cliente = self.sistema.mostrar_cliente("clienteA@example.com")
        self.assertIsNone(cliente)

    def test_modificar_cliente(self):
        """Prueba la modificación de un cliente."""
        mail = "clienteA@example.com"
        new = "Nuevo Cliente A"
        self.sistema.modificar_cliente(mail, new)
        cliente = self.sistema.mostrar_cliente(mail)
        self.assertEqual(cliente["nombre"], new)

    def test_crear_reserva(self):
        """Prueba la creación de una reserva."""
        cliente = "clienteA@example.com"
        name = "Hotel A"
        date = "2023-10-01"
        mail = "clienteA@example.com"
        self.sistema.crear_reserva(cliente, name, date)
        hotel = self.sistema.mostrar_hotel("Hotel A")
        self.assertEqual(len(hotel["reservas"]), 1)
        reserva = hotel["reservas"][0]
        self.assertEqual(reserva["cliente"]["email"], mail)
        self.assertEqual(reserva["fecha"], date)

    def test_cancelar_reserva(self):
        """Prueba la cancelación de una reserva."""
        cliente = "clienteA@example.com"
        name = "Hotel A"
        date = "2023-10-01"
        self.sistema.crear_reserva(cliente, name, date)
        self.sistema.cancelar_reserva(cliente, name, date)
        hotel = self.sistema.mostrar_hotel(name)
        self.assertEqual(len(hotel["reservas"]), 0)

    def test_eliminar_hotel_inexistente(self):
        """Prueba la eliminación de un hotel inexistente."""
        self.sistema.eliminar_hotel("Hotel Inexistente")
        hotel = self.sistema.mostrar_hotel("Hotel Inexistente")
        self.assertIsNone(hotel)

    def test_modificar_hotel_inexistente(self):
        """Prueba la modificación de un hotel inexistente."""
        name = "Hotel Inexistente"
        ubicacion = "Nueva Ubicación"
        self.sistema.modificar_hotel(name, ubicacion, 15)
        hotel = self.sistema.mostrar_hotel(name)
        self.assertIsNone(hotel)


if __name__ == "__main__":
    unittest.main()
