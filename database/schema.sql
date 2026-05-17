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