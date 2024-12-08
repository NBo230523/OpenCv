-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 18, 2024 at 04:35 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ds_sinhvien`
--

-- --------------------------------------------------------

--
-- Table structure for table `sinhvien`
--

CREATE TABLE `sinhvien` (
  `MASV` int(10) NOT NULL,
  `HOTEN` varchar(50) NOT NULL,
  `DIACHI` varchar(50) NOT NULL,
  `SDT` int(10) NOT NULL,
  `ANHSINHVIEN` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sinhvien`
--

INSERT INTO `sinhvien` (`MASV`, `HOTEN`, `DIACHI`, `SDT`, `ANHSINHVIEN`) VALUES
(20212819, 'Đinh Văn Thi', 'Nam Định', 1234567899, 'D:/TTNT/OpenCv/dataset/Thi.2.7.jpg'),
(20212830, 'Nguyễn Văn Bộ', 'Vinh Phuc', 984172055, 'D:/TTNT/OpenCv/dataset/Bo.1.7.jpg'),
(20212896, 'Vương Minh Quân', 'Hà Nội', 123456789, 'D:/TTNT/OpenCv/dataset/Student.3.3.jpg'),
(20213005, 'Trương Văn Lượng', 'Đà Lạt', 845045267, 'D:/TTNT/OpenCv/dataset/Student.2.3.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `sinhvien`
--
ALTER TABLE `sinhvien`
  ADD PRIMARY KEY (`MASV`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
