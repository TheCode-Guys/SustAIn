# SustAIn: The Intelligent Circular Economy Guardian

SustAIn is a sophisticated desktop application developed for the **Pan-Atlantic University COS 102 CA3 Group Project**. Framed strictly around the theme of **Artificial Intelligence and Society**, the platform serves as an intelligent intermediary for campus electronic waste (E-waste) management. It empowers students to reduce their environmental carbon footprint, prevent hazardous component dumping, and participate in a circular economy by exchanging vital hardware materials.

---

## 🏛️ Core Architectural Flow

SustAIn utilizes a **decoupled, modular package architecture** to ensure maintainability and scalability. The application logic is strictly separated into specialized layers:

*   **Master Traffic Router (`UI/navigation.py`)**: Acts as the centralized `NavigationController`. It manages global session states, shared assets, and dynamically routes between various view modules.
*   **Modular View Package (`UI/views/`)**: Each functional screen is encapsulated within its own module:
    *   `landing_view.py`: High-impact branded entry point.
    *   `login_view.py` & `signup_view.py`: Secure credential management.
    *   `dashboard_view.py`: Real-time user impact statistics and shortcuts.
    *   `donation_view.py`: Mandatory coordination input form for logging E-waste.
    *   `claim_view.py`: Marketplace interface featuring the **Handshake Exchange Protocol**.
    *   `leaderboard_view.py`: Dynamic campus-wide ecological contributor standings.
    *   `profile_view.py`: Personalized dashboard for tracking donations and claims.
*   **Utility & Styling**: 
    *   `UI/navigation_sidebar.py`: An independent utility to inject responsive, collapsible sidebars into any view.
    *   `config.py`: Centralized style guide and color tokens.

---

## 🧮 Detailed Component Breakdown: `src/scrap_item.py`

The heart of SustAIn's intelligence lies in its **Object-Oriented Polymorphic Design** and algorithmic scoring matrix.

### 1. Polymorphic Class Hierarchy
We utilize inheritance to handle specialized hardware types with distinct environmental impacts:
*   **`ScrapItem` (Base Class)**: Defines general E-waste attributes (Weight, Condition, Category).
*   **`BatteryScrapItem` (Subclass)**: Implements a **Toxicity Premium** in its scoring logic to reflect the higher environmental risk of chemical dumping.
*   **`PCBScrapItem` (Subclass)**: Scales impact based on a **Precious Metal Recovery Index**, incentivizing the salvage of gold and copper components.

### 2. Algorithmic Scoring Matrix
Impact scores are not static; they are computed dynamically based on physical metrics and degradation states:
| Condition | Multiplier | Rationale |
| :--- | :--- | :--- |
| **Fully Functional** | `1.5x` | Maximizes reuse value and landfill diversion. |
| **Minor Repair Required** | `1.0x` | Standard refurbishment baseline. |
| **Scrap / Raw Parts** | `0.5x` | Reflects raw material recycling value. |

### 3. Factory Design Pattern
The `scrap_item_factory` method abstracts the instantiation process. It takes a flat data row from the CSV and intelligently hydrates the correct polymorphic object type, ensuring the UI remains decoupled from the specific logic of different hardware categories.

---

## 👥 Individual Contributions & Commit History Mapping

| Full Name | Matric Number | Measurable Project Role | Key Contributions (Commit Mapping) |
| :--- | :--- | :--- | :--- |
| **Kailotachukwu Igwe** | 25120112108 | **Technical Product Lead** | Architectural refactoring, routing logic, Handshake Protocol, Local Image Storage. |
| **Michael** | 25120112111 | **Lead Logic Engineer** | Developed the `ScrapItem` polymorphic hierarchy and condition multiplier matrix. |
| **Seyi** | 25120112112 | **Database Architect** | Implemented the flat-file CSV CRUD operations and schema initialization. |
| **Romnic** | 25120112113 | **Security Engineer** | Designed the authorization portal, email validation, and password hashing logic. |
| **Isaac** | 25120112114 | **Data Integrity Specialist** | Engineered robust input sanitization, institutional email filters, and weight guardrails. |
| **Krampus** | 25120112115 | **UI/UX Designer** | Designed the `EcoTierManager` and integrated gamified rank badges into user panels. |

---

## 🛠️ Local Installation & Demo Walkthrough

Ensure you have **Python 3.10+** and the **Pillow** library installed.

### 1. Initialize Environment
```bash
# Clone the repository
git clone https://github.com/TheCode-Guys/SustAIn.git
cd SustAIn

# Install dependencies
pip install Pillow
```

### 2. Boot the Application
Launch the desktop window by executing the master gateway:
```bash
python main.py
```

### 3. System Navigation
*   **Enter**: Proceed from the Landing Page to the Login/Signup portal.
*   **Donate**: Log a hardware item, selecting category and condition to compute your Eco-Points.
*   **Claim**: Select an item in the Marketplace to trigger the **Handshake Coordination Pop-up**, revealing donor contact info and campus pickup venues.
*   **Compete**: Check the Leaderboard to see where you stand among campus Sustainability Titans.

---
*Developed for the Pan-Atlantic University COS 102 CA3 Assessment.*
