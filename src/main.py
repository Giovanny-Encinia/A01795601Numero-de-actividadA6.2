"""Sistema de reservacion de hoteles"""

import json
import os
from typing import List, Dict, Optional


class Hotel:
    """Clase que representa un Hotel."""

    def __init__(self, nombre: str, ubicacion: str, habitaciones: int):
        """
        Inicializa un objeto Hotel.

        :param nombre: Nombre del hotel.
        :param ubicacion: Ubicación del hotel.
        :param habitaciones: Número de habitaciones disponibles.
        """
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.habitaciones = habitaciones
        self.reservas = []

    def reservar_habitacion(self, reserva: "Reserva") -> bool:
        """
        Reserva una habitación en el hotel.

        :param reserva: Objeto Reserva.
        :return: True si la reserva fue exitosa, False si no hay
        habitaciones disponibles.
        """
        if len(self.reservas) < self.habitaciones:
            self.reservas.append(reserva)
            return True
        return False

    def cancelar_reserva(self, reserva: "Reserva") -> bool:
        """
        Cancela una reserva en el hotel.

        :param reserva: Objeto Reserva.
        :return: True si la reserva fue cancelada,
          False si no se encontró la reserva.
        """
        if reserva in self.reservas:
            self.reservas.remove(reserva)
            return True
        return False

    def to_dict(self) -> Dict:
        """
        Convierte el objeto Hotel a un diccionario.

        :return: Diccionario con la información del hotel.
        """
        return {
            "nombre": self.nombre,
            "ubicacion": self.ubicacion,
            "habitaciones": self.habitaciones,
            "reservas": [reserva.to_dict() for reserva in self.reservas],
        }

    @staticmethod
    def from_dict(data: Dict) -> "Hotel":
        """
        Crea un objeto Hotel a partir de un diccionario.

        :param data: Diccionario con la información del hotel.
        :return: Objeto Hotel.
        """
        hotel = Hotel(data["nombre"], data["ubicacion"], data["habitaciones"])
        r = "reservas"
        hotel.reservas = [Reserva.from_dict(reserva) for reserva in data[r]]
        return hotel


class Reserva:
    """Clase que representa una Reserva."""

    def __init__(self, cliente: "Cliente", hotel: Hotel, fecha: str):
        """
        Inicializa un objeto Reserva.

        :param cliente: Objeto Cliente.
        :param hotel: Objeto Hotel.
        :param fecha: Fecha de la reserva.
        """
        self.cliente = cliente
        self.hotel = hotel
        self.fecha = fecha

    def to_dict(self) -> Dict:
        """
        Convierte el objeto Reserva a un diccionario.

        :return: Diccionario con la información de la reserva.
        """
        return {
            "cliente": self.cliente.to_dict(),
            "hotel": self.hotel.nombre,
            "fecha": self.fecha,
        }

    @staticmethod
    def from_dict(data: Dict) -> "Reserva":
        """
        Crea un objeto Reserva a partir de un diccionario.

        :param data: Diccionario con la información de la reserva.
        :return: Objeto Reserva.
        """
        cliente = Cliente.from_dict(data["cliente"])
        hotel = Hotel(
            data["hotel"], "", 0
        )  # Se necesita un hotel temporal para la reserva
        return Reserva(cliente, hotel, data["fecha"])


class Cliente:
    """Clase que representa un Cliente."""

    def __init__(self, nombre: str, email: str):
        """
        Inicializa un objeto Cliente.

        :param nombre: Nombre del cliente.
        :param email: Correo electrónico del cliente.
        """
        self.nombre = nombre
        self.email = email

    def to_dict(self) -> Dict:
        """
        Convierte el objeto Cliente a un diccionario.

        :return: Diccionario con la información del cliente.
        """
        return {"nombre": self.nombre, "email": self.email}

    @staticmethod
    def from_dict(data: Dict) -> "Cliente":
        """
        Crea un objeto Cliente a partir de un diccionario.

        :param data: Diccionario con la información del cliente.
        :return: Objeto Cliente.
        """
        return Cliente(data["nombre"], data["email"])


class SistemaReservas:
    """Clase que maneja el sistema de reservas."""

    def __init__(
        self,
        archivo_hoteles: str = "hoteles.json",
        archivo_clientes: str = "clientes.json",
    ):
        """
        Inicializa el sistema de reservas.

        :param archivo_hoteles: Ruta del archivo de hoteles.
        :param archivo_clientes: Ruta del archivo de clientes.
        """
        self.archivo_hoteles = archivo_hoteles
        self.archivo_clientes = archivo_clientes
        self.hoteles = self.cargar_hoteles()
        self.clientes = self.cargar_clientes()

    def cargar_hoteles(self) -> List[Hotel]:
        """
        Carga los hoteles desde un archivo.

        :return: Lista de objetos Hotel.
        """
        if not os.path.exists(self.archivo_hoteles):
            return []
        with open(self.archivo_hoteles, "r", encoding="utf-8") as file:
            data = json.load(file)
        return [Hotel.from_dict(hotel) for hotel in data]

    def guardar_hoteles(self):
        """Guarda los hoteles en un archivo."""
        with open(self.archivo_hoteles, "w", encoding="utf-8") as file:
            json.dump([hotel.to_dict() for hotel in self.hoteles], file)

    def cargar_clientes(self) -> List[Cliente]:
        """
        Carga los clientes desde un archivo.

        :return: Lista de objetos Cliente.
        """
        if not os.path.exists(self.archivo_clientes):
            return []
        with open(self.archivo_clientes, "r", encoding="utf-8") as file:
            data = json.load(file)
        return [Cliente.from_dict(cliente) for cliente in data]

    def guardar_clientes(self):
        """Guarda los clientes en un archivo."""
        with open(self.archivo_clientes, "w", encoding="utf-8") as file:
            json.dump([cliente.to_dict() for cliente in self.clientes], file)

    def crear_hotel(self, nombre: str, ubicacion: str, habitaciones: int):
        """
        Crea un nuevo hotel.

        :param nombre: Nombre del hotel.
        :param ubicacion: Ubicación del hotel.
        :param habitaciones: Número de habitaciones disponibles.
        """
        hotel = Hotel(nombre, ubicacion, habitaciones)
        self.hoteles.append(hotel)
        self.guardar_hoteles()

    def eliminar_hotel(self, nombre: str):
        """
        Elimina un hotel.

        :param nombre: Nombre del hotel a eliminar.
        """
        hotels = self.hoteles
        self.hoteles = [hotel for hotel in hotels if hotel.nombre != nombre]
        self.guardar_hoteles()

    def mostrar_hotel(self, nombre: str) -> Optional[Dict]:
        """
        Muestra la información de un hotel.

        :param nombre: Nombre del hotel.
        :return: Diccionario con la información
        del hotel o None si no se encuentra.
        """
        for hotel in self.hoteles:
            if hotel.nombre == nombre:
                return hotel.to_dict()
        return None

    def modificar_hotel(
        self, nombre: str, nueva_ubicacion: str, nuevas_habitaciones: int
    ):
        """
        Modifica la información de un hotel.

        :param nombre: Nombre del hotel.
        :param nueva_ubicacion: Nueva ubicación del hotel.
        :param nuevas_habitaciones: Nuevo número de habitaciones disponibles.
        """
        for hotel in self.hoteles:
            if hotel.nombre == nombre:
                hotel.ubicacion = nueva_ubicacion
                hotel.habitaciones = nuevas_habitaciones
                self.guardar_hoteles()
                break

    def crear_cliente(self, nombre: str, email: str):
        """
        Crea un nuevo cliente.

        :param nombre: Nombre del cliente.
        :param email: Correo electrónico del cliente.
        """
        cliente = Cliente(nombre, email)
        self.clientes.append(cliente)
        self.guardar_clientes()

    def eliminar_cliente(self, email: str):
        """
        Elimina un cliente.

        :param email: Correo electrónico del cliente a eliminar.
        """
        self.clientes = [
            cliente for cliente in self.clientes if cliente.email != email
            ]
        self.guardar_clientes()

    def mostrar_cliente(self, email: str) -> Optional[Dict]:
        """
        Muestra la información de un cliente.

        :param email: Correo electrónico del cliente.
        :return: Diccionario con la información del
        cliente o None si no se encuentra.
        """
        for cliente in self.clientes:
            if cliente.email == email:
                return cliente.to_dict()
        return None

    def modificar_cliente(self, email: str, nuevo_nombre: str):
        """
        Modifica la información de un cliente.

        :param email: Correo electrónico del cliente.
        :param nuevo_nombre: Nuevo nombre del cliente.
        """
        for cliente in self.clientes:
            if cliente.email == email:
                cliente.nombre = nuevo_nombre
                self.guardar_clientes()
                break

    def crear_reserva(self, cliente_email: str, hotel_nombre: str, fecha: str):
        """
        Crea una nueva reserva.

        :param cliente_email: Correo electrónico del cliente.
        :param hotel_nombre: Nombre del hotel.
        :param fecha: Fecha de la reserva.
        """
        clients = self.clientes
        hotels = self.hoteles
        cliente = next((c for c in clients if c.email == cliente_email), None)
        hotel = next((h for h in hotels if h.nombre == hotel_nombre), None)
        if cliente and hotel:
            reserva = Reserva(cliente, hotel, fecha)
            if hotel.reservar_habitacion(reserva):
                self.guardar_hoteles()
            else:
                print("No hay habitaciones disponibles.")
        else:
            print("Cliente o hotel no encontrado.")

    def cancelar_reserva(
            self,
            cliente_email: str,
            hotel_nombre: str,
            fecha: str
            ):
        """
        Cancela una reserva.

        :param cliente_email: Correo electrónico del cliente.
        :param hotel_nombre: Nombre del hotel.
        :param fecha: Fecha de la reserva.
        """
        clients = self.clientes
        hotels = self.hoteles
        cliente = next((c for c in clients if c.email == cliente_email), None)
        hotel = next((h for h in hotels if h.nombre == hotel_nombre), None)
        if cliente and hotel:
            reserva = next(
                (
                    r
                    for r in hotel.reservas
                    if r.cliente.email == cliente_email and r.fecha == fecha
                ),
                None,
            )
            if reserva and hotel.cancelar_reserva(reserva):
                self.guardar_hoteles()
            else:
                print("Reserva no encontrada.")
        else:
            print("Cliente o hotel no encontrado.")
