# 🚐 DriveLedger

**A premium, mobile-first fleet and route tracking system.**  
Built with FastAPI, SQLite, and Vanilla JavaScript. Designed and developed by **does4u**.

## 📖 Overview

DriveLedger simplifies the daily reporting process for delivery drivers and fleet managers. Drivers use a lightweight, mobile-optimized web app to log their daily metrics (route ID, hours, km, pickups, deliveries). The data is securely synced to a central server, where the Director Dashboard provides real-time analytics and monitoring.

## ✨ Key Features

- **📱 Mobile-First Driver App:** No app store required. Drivers just open the link, fill the form, and hit "Sync".
- **🔒 Secure Data Sync:** Automatically saves and updates daily records in the SQLite database.
- **📊 Director Dashboard:** Real-time overview of the entire fleet. Filter by date, view total parcels, total kilometers, and individual driver performance.
- **🌙 Premium Dark UI:** High-contrast, eye-friendly design customized for the logistics environment.

## 🛠️ Tech Stack

- **Backend:** Python 3, FastAPI, SQLAlchemy, SQLite.
- **Frontend:** HTML5, Vanilla CSS, JavaScript (LocalStorage for offline fallback).
- **Hosting:** Ready for Render (via `gunicorn` / `uvicorn`).

## 🚀 Quick Start (Local Development)

1. **Clone the repository:**
   ```bash
      git clone https://github.com/ntagiantas-dev/DriveLedger.git
         cd DriveLedger
