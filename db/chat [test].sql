-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 27, 2024 at 02:30 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `chat`
--

-- --------------------------------------------------------

--
-- Table structure for table `mensaje`
--

CREATE TABLE `mensaje` (
  `mensaje` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mensaje`
--

INSERT INTO `mensaje` (`mensaje`, `created_at`) VALUES
('Torres', '2024-04-26 22:49:21'),
('adasda', '2024-04-26 22:51:45'),
('Torres', '2024-04-26 22:53:22'),
('asdadas', '2024-04-26 22:53:27'),
('Soy el cliente', '2024-04-26 22:53:35'),
('Soy el servidor', '2024-04-26 22:53:43'),
('adsad', '2024-04-26 23:56:05'),
('sadasdas', '2024-04-26 23:56:26'),
('dsadsa', '2024-04-26 23:56:26'),
('asd', '2024-04-27 00:00:51'),
('as', '2024-04-27 00:06:11'),
('asda', '2024-04-27 00:06:20');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
