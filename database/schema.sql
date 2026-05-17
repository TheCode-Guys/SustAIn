-- PostgreSQL Database Schema for SustAIn

-- 1. Users Table (Managed by Member 5 for Auth)
CREATE TABLE IF NOT EXISTS users (
    matric_id VARCHAR(15) PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(50)
);

-- 2. Hardware Scraps Table (Managed by Members 3, 4, 6, and Kailo)
CREATE TABLE IF NOT EXISTS scraps (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    weight NUMERIC(6, 2) NOT NULL,
    damage_state VARCHAR(50) NOT NULL,
    value_tier VARCHAR(20) NOT NULL,
    impact_score NUMERIC(6, 2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'Available',
    donor_phone VARCHAR(20) NOT NULL,
    claimer_id VARCHAR(15) REFERENCES users(matric_id),
    claimer_intent TEXT
);

-- database/schema.sql
-- ==========================================
-- SECTION 1: TABLE ARCHITECTURE
-- ==========================================

-- 1. Users Table (Managed by Member 5 for Auth)
CREATE TABLE IF NOT EXISTS users (
    matric_id VARCHAR(15) PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(50)
);

-- 2. Hardware Scraps Table (Managed by Members 3, 4, 6, and Kailo)
CREATE TABLE IF NOT EXISTS scraps (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    weight NUMERIC(6, 2) NOT NULL,
    damage_state VARCHAR(50) NOT NULL,
    value_tier VARCHAR(20) NOT NULL,
    impact_score NUMERIC(6, 2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'Available',
    donor_phone VARCHAR(20) NOT NULL,
    claimer_id VARCHAR(15) REFERENCES users(matric_id),
    claimer_intent TEXT
);

-- ==========================================
-- SECTION 2: INITIAL MOCK DATA SEEDING
-- ==========================================

-- Insert Mock PAU Student Users (Runs only if they don't exist yet)
INSERT INTO users (matric_id, email, password_hash, nickname) VALUES
('220101', 'ruth.obama@pau.edu.ng', 'pbkdf2_sha256_mock_hash_1', 'Ruth'),
('220102', 'member3.oop@pau.edu.ng', 'pbkdf2_sha256_mock_hash_2', 'Archy'),
('220103', 'member6.integrator@pau.edu.ng', 'pbkdf2_sha256_mock_hash_3', 'SystemsGuy')
ON CONFLICT (matric_id) DO NOTHING;

-- Insert Mock E-Waste Scrap Items (Available for Claiming)
INSERT INTO scraps (item_name, category, weight, damage_state, value_tier, impact_score, donor_phone, status) VALUES
('Dell Monitor 24-inch', 'Display', 4.50, 'Minor Repair', 'Mid', 65.20, '+2348022223333', 'Available'),
('MacBook Air Battery A1466', 'Battery', 0.35, 'Functional', 'High', 92.00, '+2348133334444', 'Available'),
('HP Motherboard EliteBook', 'Motherboard', 0.60, 'Parts Only', 'Low', 45.10, '+2347044445555', 'Available'),
('Logitech G Pro Mouse', 'Peripherals', 0.08, 'Functional', 'Mid', 78.50, '+2349055556666', 'Available');

-- Insert an Item That Has Already Been Claimed (For History Tracking)
INSERT INTO scraps (item_name, category, weight, damage_state, value_tier, impact_score, donor_phone, status, claimer_id, claimer_intent) VALUES
('Broken iPhone X Screen', 'Display', 0.15, 'Parts Only', 'Low', 30.00, '+2348166667777', 'Claimed', '220101', 'Extracting copper coils for an engineering physics lab project.');