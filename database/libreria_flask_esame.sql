-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versione server:              10.4.32-MariaDB - mariadb.org binary distribution
-- S.O. server:                  Win64
-- HeidiSQL Versione:            12.17.0.7270
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dump della struttura del database libreria_flask_esame
CREATE DATABASE IF NOT EXISTS `libreria_flask_esame` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `libreria_flask_esame`;

-- Dump della struttura di tabella libreria_flask_esame.categorie
CREATE TABLE IF NOT EXISTS `categorie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dump dei dati della tabella libreria_flask_esame.categorie: ~-1 rows (circa)
INSERT INTO `categorie` (`id`, `nome`) VALUES
	(1, 'Narrativa'),
	(2, 'Horror'),
	(3, 'Fantascienza'),
	(4, 'Storia'),
	(5, 'Informatica');

-- Dump della struttura di tabella libreria_flask_esame.libri
CREATE TABLE IF NOT EXISTS `libri` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titolo` varchar(200) NOT NULL,
  `autore` varchar(150) NOT NULL,
  `isbn` varchar(20) DEFAULT NULL,
  `editore` varchar(150) DEFAULT NULL,
  `prezzo` decimal(8,2) NOT NULL DEFAULT 0.00,
  `categoria_id` int(11) DEFAULT NULL,
  `data_inserimento` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `isbn` (`isbn`),
  KEY `categoria_id` (`categoria_id`),
  CONSTRAINT `libri_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categorie` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dump dei dati della tabella libreria_flask_esame.libri: ~-1 rows (circa)
INSERT INTO `libri` (`id`, `titolo`, `autore`, `isbn`, `editore`, `prezzo`, `categoria_id`, `data_inserimento`) VALUES
	(3, 'Il nome della rosa', 'Umberto Eco', '9788845292613', 'Bompiani', 12.90, 1, '2026-09-24 21:25:27'),
	(4, 'Clean Code', 'Robert C. Martin', '9780132350884', 'Prentice Hall', 34.90, 5, '2026-09-24 21:25:27');

-- Dump della struttura di tabella libreria_flask_esame.magazzino
CREATE TABLE IF NOT EXISTS `magazzino` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libro_id` int(11) NOT NULL,
  `quantita` int(11) NOT NULL DEFAULT 0,
  `ultimo_aggiornamento` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `libro_id` (`libro_id`),
  CONSTRAINT `magazzino_ibfk_1` FOREIGN KEY (`libro_id`) REFERENCES `libri` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dump dei dati della tabella libreria_flask_esame.magazzino: ~-1 rows (circa)
INSERT INTO `magazzino` (`id`, `libro_id`, `quantita`, `ultimo_aggiornamento`) VALUES
	(3, 3, 3, '2026-10-02 22:45:31'),
	(4, 4, 4, '2026-10-02 22:22:07');

-- Dump della struttura di tabella libreria_flask_esame.operatori
CREATE TABLE IF NOT EXISTS `operatori` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `data_creazione` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dump dei dati della tabella libreria_flask_esame.operatori: ~-1 rows (circa)
INSERT INTO `operatori` (`id`, `username`, `password_hash`, `nome`, `data_creazione`) VALUES
	(1, 'matteo', 'matteo123', 'Matteo', '2026-09-26 20:58:52');

-- Dump della struttura di tabella libreria_flask_esame.utenti
CREATE TABLE IF NOT EXISTS `utenti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `cognome` varchar(100) NOT NULL,
  `email` varchar(150) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `indirizzo` varchar(200) DEFAULT NULL,
  `citta` varchar(100) DEFAULT NULL,
  `cap` varchar(10) DEFAULT NULL,
  `data_registrazione` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dump dei dati della tabella libreria_flask_esame.utenti: ~-1 rows (circa)
INSERT INTO `utenti` (`id`, `nome`, `cognome`, `email`, `telefono`, `indirizzo`, `citta`, `cap`, `data_registrazione`) VALUES
	(1, 'mario', 'rudi', 'mariorudi@gmail.com', '1234567890', 'via grande valle', 'Lucca', '00000', '2026-10-01 21:29:41'),
	(2, 'mario', 'dunio', 'fjfjfjfj@gmail.com', '1231237890', 'Corso Traiano, 34', 'Torino', '10135', '2026-10-02 22:45:31');

-- Dump della struttura di tabella libreria_flask_esame.vendite
CREATE TABLE IF NOT EXISTS `vendite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `utente_id` int(11) NOT NULL,
  `data_vendita` datetime DEFAULT current_timestamp(),
  `totale` decimal(10,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`id`),
  KEY `utente_id` (`utente_id`),
  CONSTRAINT `vendite_ibfk_1` FOREIGN KEY (`utente_id`) REFERENCES `utenti` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dump dei dati della tabella libreria_flask_esame.vendite: ~-1 rows (circa)
INSERT INTO `vendite` (`id`, `utente_id`, `data_vendita`, `totale`) VALUES
	(1, 1, '2026-10-02 22:21:41', 12.90),
	(2, 1, '2026-10-02 22:21:56', 12.90),
	(3, 1, '2026-10-02 22:22:07', 34.90),
	(4, 1, '2026-10-02 22:22:15', 12.90),
	(5, 1, '2026-10-02 22:22:27', 12.90),
	(6, 2, '2026-10-02 22:45:31', 12.90);

-- Dump della struttura di tabella libreria_flask_esame.vendite_dettagli
CREATE TABLE IF NOT EXISTS `vendite_dettagli` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vendita_id` int(11) NOT NULL,
  `libro_id` int(11) NOT NULL,
  `quantita` int(11) NOT NULL,
  `prezzo_unitario` decimal(8,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendita_id` (`vendita_id`),
  KEY `libro_id` (`libro_id`),
  CONSTRAINT `vendite_dettagli_ibfk_1` FOREIGN KEY (`vendita_id`) REFERENCES `vendite` (`id`) ON DELETE CASCADE,
  CONSTRAINT `vendite_dettagli_ibfk_2` FOREIGN KEY (`libro_id`) REFERENCES `libri` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dump dei dati della tabella libreria_flask_esame.vendite_dettagli: ~-1 rows (circa)
INSERT INTO `vendite_dettagli` (`id`, `vendita_id`, `libro_id`, `quantita`, `prezzo_unitario`) VALUES
	(1, 1, 3, 1, 12.90),
	(2, 2, 3, 1, 12.90),
	(3, 3, 4, 1, 34.90),
	(4, 4, 3, 1, 12.90),
	(5, 5, 3, 1, 12.90),
	(6, 6, 3, 1, 12.90);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
