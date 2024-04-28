-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 28, 2024 at 05:04 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dynamicpowerpoint`
--

-- --------------------------------------------------------

--
-- Table structure for table `api_key`
--

CREATE TABLE `api_key` (
  `api_key_id` int(11) NOT NULL COMMENT 'API Key Primary Key',
  `api_key_llm` int(11) NOT NULL COMMENT 'API Key Large Language Model Foreign Key',
  `api_key_user` int(11) NOT NULL COMMENT 'API Key User ID number',
  `api_key_user_key` varchar(256) NOT NULL COMMENT 'API Key Encrypted API Key'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `api_key`
--

INSERT INTO `api_key` (`api_key_id`, `api_key_llm`, `api_key_user`, `api_key_user_key`) VALUES
(1, 1, 1, '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'),
(28, 2, 1, 'fake gemini key');

-- --------------------------------------------------------

--
-- Table structure for table `historical`
--

CREATE TABLE `historical` (
  `historical_id` int(11) NOT NULL COMMENT 'Primary Key',
  `historical_user_id` int(11) NOT NULL COMMENT 'User Name',
  `historical_presentation_name` varchar(255) NOT NULL COMMENT 'Name of Presentation',
  `historical_time_stamp` datetime NOT NULL DEFAULT current_timestamp() COMMENT 'Time Presentation created',
  `historical_presentation_location` varchar(255) NOT NULL COMMENT 'Stored Presentation'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `llm`
--

CREATE TABLE `llm` (
  `llm_id` int(11) NOT NULL COMMENT 'Large Language Model ID',
  `llm_name` varchar(30) NOT NULL COMMENT 'Large Language Model Name',
  `llm_api_link` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `llm`
--

INSERT INTO `llm` (`llm_id`, `llm_name`, `llm_api_link`) VALUES
(1, 'ChatGPT', 'https://openai.com/'),
(2, 'Gemini', 'https://gemini.google.com/app');

-- --------------------------------------------------------

--
-- Table structure for table `llm_model`
--

CREATE TABLE `llm_model` (
  `llm_model_id` int(11) NOT NULL COMMENT 'Large Language Model Cost ID',
  `llm_id` int(11) NOT NULL COMMENT 'Large Language Model Foreign Key',
  `llm_model_name` varchar(30) NOT NULL COMMENT 'Large Language Model Model Name',
  `llm_model_description` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `llm_model`
--

INSERT INTO `llm_model` (`llm_model_id`, `llm_id`, `llm_model_name`, `llm_model_description`) VALUES
(1, 1, 'gpt-4-0125-preview', 'ChatGPT4 - the latest model with data up to April 2023.'),
(5, 1, 'gpt-3.5-turbo-0125', 'ChatGPT 3.5 Turbo - High Accuracy Model, with data active up to September 2021. It is also a cheaper model to use.'),
(7, 2, 'Gemini-test', 'Gemini Test Model - Not usable');

-- --------------------------------------------------------

--
-- Table structure for table `user_information`
--

CREATE TABLE `user_information` (
  `user_id` int(11) NOT NULL COMMENT 'User ID',
  `username` varchar(255) NOT NULL COMMENT 'Unique Username',
  `user_first_name` varchar(32) NOT NULL COMMENT 'User First Name',
  `user_last_name` varchar(64) NOT NULL COMMENT 'User Last Name',
  `user_hashed_password` varbinary(255) NOT NULL COMMENT 'User Encrypted Password',
  `user_salt` varbinary(255) NOT NULL COMMENT 'Salt for User Login',
  `user_is_admin` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'Is User an Admin',
  `account_confirmed` tinyint(1) DEFAULT 0 COMMENT 'User Account is Confirmed'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_information`
--

INSERT INTO `user_information` (`user_id`, `username`, `user_first_name`, `user_last_name`, `user_hashed_password`, `user_salt`, `user_is_admin`, `account_confirmed`) VALUES
(1, 'Ad@min', 'Darren', 'McMenamin', 0x3d3d01b7454e1dd760c706b2fe60609aa320ef429a467a3a5ebcd1c9795dcd0c9bb79ebf10ce76e616e931e05c19e331930ed9bea05d821f5c162ccc5f8783e4, 0xb82c62831ab7dad523583e93ba2e6085021cad9c89ad99b2d9230f7a37214f07, 1, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `api_key`
--
ALTER TABLE `api_key`
  ADD PRIMARY KEY (`api_key_id`),
  ADD KEY `FK_API_KEY_LLM` (`api_key_llm`),
  ADD KEY `FK_API_KEY_USER` (`api_key_user`);

--
-- Indexes for table `historical`
--
ALTER TABLE `historical`
  ADD PRIMARY KEY (`historical_id`),
  ADD KEY `user_id_historical_id` (`historical_user_id`);

--
-- Indexes for table `llm`
--
ALTER TABLE `llm`
  ADD PRIMARY KEY (`llm_id`);

--
-- Indexes for table `llm_model`
--
ALTER TABLE `llm_model`
  ADD PRIMARY KEY (`llm_model_id`),
  ADD KEY `LLM_Name_ID` (`llm_id`);

--
-- Indexes for table `user_information`
--
ALTER TABLE `user_information`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `Unique_UserName` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `api_key`
--
ALTER TABLE `api_key`
  MODIFY `api_key_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'API Key Primary Key', AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `historical`
--
ALTER TABLE `historical`
  MODIFY `historical_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary Key', AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT for table `llm`
--
ALTER TABLE `llm`
  MODIFY `llm_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Large Language Model ID', AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `llm_model`
--
ALTER TABLE `llm_model`
  MODIFY `llm_model_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Large Language Model Cost ID', AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user_information`
--
ALTER TABLE `user_information`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'User ID', AUTO_INCREMENT=52;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `api_key`
--
ALTER TABLE `api_key`
  ADD CONSTRAINT `FK_API_KEY_LLM` FOREIGN KEY (`api_key_llm`) REFERENCES `llm` (`llm_id`),
  ADD CONSTRAINT `FK_API_KEY_USER` FOREIGN KEY (`api_key_user`) REFERENCES `user_information` (`user_id`);

--
-- Constraints for table `historical`
--
ALTER TABLE `historical`
  ADD CONSTRAINT `user_id_historical_id` FOREIGN KEY (`historical_user_id`) REFERENCES `user_information` (`user_id`);

--
-- Constraints for table `llm_model`
--
ALTER TABLE `llm_model`
  ADD CONSTRAINT `llm_model_ibfk_1` FOREIGN KEY (`llm_id`) REFERENCES `llm` (`llm_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
