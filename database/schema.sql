-- ===========================================
-- AI Resume Screening System Database Schema
-- ===========================================

CREATE DATABASE IF NOT EXISTS ai_resume_screening_system;

USE ai_resume_screening_system;

-- ===========================================
-- Users Table
-- ===========================================

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin') DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ===========================================
-- Jobs Table
-- ===========================================

CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(150) NOT NULL,
    department VARCHAR(100) NOT NULL,
    location VARCHAR(150) NOT NULL,
    experience_required VARCHAR(100) NOT NULL,
    salary VARCHAR(100),
    required_skills TEXT NOT NULL,
    description TEXT NOT NULL,
    status ENUM('active', 'closed') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ===========================================
-- Resumes Table
-- ===========================================

CREATE TABLE IF NOT EXISTS resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_name VARCHAR(150),
    email VARCHAR(150),
    phone VARCHAR(50),
    original_filename VARCHAR(255) NOT NULL,
    stored_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_size INT NOT NULL,
    status ENUM('pending', 'shortlisted', 'rejected') DEFAULT 'pending',
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ===========================================
-- Resume Details Table
-- ===========================================

CREATE TABLE IF NOT EXISTS resume_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT NOT NULL,
    extracted_text LONGTEXT,
    extracted_email VARCHAR(150),
    extracted_phone VARCHAR(50),
    extracted_skills TEXT,
    education TEXT,
    experience TEXT,
    projects TEXT,
    certificates TEXT,
    languages TEXT,
    parsed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_resume_details_resume
        FOREIGN KEY (resume_id)
        REFERENCES resumes(id)
        ON DELETE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;