# metadata for all 46 lab experiments
EXPERIMENTS = [
    {
        "num": 1,
        "folder": "Exp-01-Library-Management",
        "title": "Local Library Management System",
        "category": "Portals & Management",
        "desc": "A streamlined library system with catalog search, user accounts for borrowing and managing books, librarian admin dashboard for inventory, issuing/returning books, fine calculation (Rs. 5/day), and semester-wise study material downloads.",
        "roles": ["Librarian Admin", "Student User"],
        "features": [
            "Librarian Admin login & dashboard",
            "Add, update, and delete books from catalog",
            "Issue book to student with issue & return dates",
            "Return book status & automatic overdue fine calculation",
            "Semester & year-wise study material upload & management",
            "Student registration & login",
            "Book catalog search & real-time availability check",
            "My Borrow History (issue date, expiry date, return status)",
            "Check & pay overdue fines",
            "Search & download academic study materials by year/semester",
            "Student profile management"
        ]
    },
    {
        "num": 2,
        "folder": "Exp-02-Hotel-Room-Booking",
        "title": "Online Hotel Room Booking System",
        "category": "Booking & Reservations",
        "desc": "Responsive hotel booking portal allowing users to search by destination, dates, and guests across 4 room types. Features strict 3-day cancellation/change policy enforcement, availability tracking, and admin dashboard for pricing and static page management.",
        "roles": ["Customer User", "Hotel Administrator"],
        "features": [
            "User registration, login, and profile modification",
            "Search by destination, check-in/out dates, and guest count",
            "4 Room Types: Standard ($80/night), Deluxe ($120/night), Executive Suite ($200/night), Presidential Suite ($350/night)",
            "Real-time room availability checker",
            "Booking history dashboard with booking status",
            "Change booking or cancel booking with 3-day arrival policy check (strict date difference validation)",
            "Admin panel to manage room quantity and price for all 4 room types",
            "Admin booking management (modify or cancel any specific booking)",
            "Admin CMS to edit static pages: About Us, Room Info, Contact Us, Q&A, Travel Guide, Privacy Policy"
        ]
    },
    {
        "num": 3,
        "folder": "Exp-03-Bus-Ticket-Booking",
        "title": "Online Bus Ticket Booking System",
        "category": "Booking & Reservations",
        "desc": "Online bus ticketing platform with route search, seat selection grid, passenger info, payment gateway, bus categories (Volvo, Sleeper, Coach), passenger review/comments, and admin bus & report management.",
        "roles": ["Passenger User", "Bus Administrator"],
        "features": [
            "User authentication (Login, Register, Forgot Password)",
            "Search buses by source, destination, date, and departure time",
            "Bus categories: Volvo Multi-Axle, AC Sleeper, Semi-Sleeper, Luxury Coach",
            "Interactive 32-seat layout with booked/available/selected states",
            "Passenger details form & fare calculation with tax",
            "Simulated secure payment gateway with instant booking confirmation",
            "Cancel booking ticket module with refund calculation",
            "User review and comments section for individual bus routes",
            "Admin bus schedule & category management (add/update bus, photo, route, seats)",
            "Admin analytics and booking revenue report generation"
        ]
    },
    {
        "num": 4,
        "folder": "Exp-04-Train-Reservation",
        "title": "Online Train Reservation System",
        "category": "Booking & Reservations",
        "desc": "Comprehensive railway reservation portal with route/class search, real-time seat availability, PNR generation, PNR status tracker (CNF/RAC/WL), ticket printing, cancellation with refund rules, and admin train master management.",
        "roles": ["Passenger", "Railway Administrator"],
        "features": [
            "Passenger login and registration with journey details",
            "Train search by origin, destination, date, and travel class (1A, 2A, 3A, SL, CC)",
            "Available train list with route via-details and live seat quotas",
            "Online / offline payment mode simulation",
            "Unique 10-digit PNR generation upon booking confirmation",
            "PNR Status inquiry (Confirmed, RAC, Waiting List)",
            "Cancellation module with refund rules (date of reservation, ticket fare, refundable %)",
            "Printable e-Ticket with passenger list and QR code",
            "Admin dashboard: add/update train details, zone/class/date fare management, view payment records"
        ]
    },
    {
        "num": 5,
        "folder": "Exp-05-Flight-Reservation",
        "title": "Online Flight Reservation System",
        "category": "Booking & Reservations",
        "desc": "Web-based airline reservation system consolidating flight data, real-time seat inventory, fare classes, payment simulation, e-ticket generation, cancellation with refund, customer feedback, and admin flight analytics.",
        "roles": ["Passenger", "Airlines Admin"],
        "features": [
            "Flight search by origin, destination, date, and travel class (Economy, Business, First)",
            "Real-time seat inventory and dynamic flight fare display",
            "Seat selection and passenger details entry",
            "Secure payment gateway simulation with instant PNR generation",
            "My Tickets dashboard with printable e-Tickets & travel itinerary",
            "Cancel ticket workflow with cancellation fee and refund computation",
            "Customer feedback & rating submission",
            "Admin login & flight schedule management",
            "Admin booking status viewer and flight revenue reports"
        ]
    },
    {
        "num": 6,
        "folder": "Exp-06-Cake-Ordering",
        "title": "Online Cake Ordering System",
        "category": "E-Commerce & Marketplaces",
        "desc": "E-commerce platform for ordering cakes with category/flavor/occasion filters, custom cake sizes & messages, eggless options, shopping cart, shipping address management, delivery tracking, and bakery admin product manager.",
        "roles": ["Customer", "Bakery Admin"],
        "features": [
            "Customer registration and login",
            "Browse cakes by Category (Birthday, Wedding, Anniversary, Festive)",
            "Filter by Flavor (Chocolate Truffle, Red Velvet, Black Forest, Pineapple, Vanilla) and Price Range",
            "Customization options: Size (0.5kg, 1kg, 2kg, 3kg), Custom Inscription Message, Eggless toggle",
            "Add to Cart, cart drawer with quantity edit, and order placement",
            "Shipping address manager (add/update delivery location)",
            "My Orders dashboard with real-time shipping/delivery status tracking",
            "Admin portal to post cake details, upload images, manage prices, and update order statuses"
        ]
    },
    {
        "num": 7,
        "folder": "Exp-07-Beauty-Parlour-Booking",
        "title": "Beauty Parlour Appointment Booking System",
        "category": "Booking & Reservations",
        "desc": "Online appointment system for beauty salons featuring service catalog, stylist profiles, interactive reservation calendar with lockout hours, partial deposit or full payment (Stripe/PayPal), and salon manager dashboard.",
        "roles": ["Customer", "Salon Manager / Stylist"],
        "features": [
            "Browse salon services (Hair Styling, Facial & Cleanup, Bridal Makeup, Spa & Wellness)",
            "Stylist profiles with experience, specialty, and ratings",
            "Interactive reservation calendar: select date, available time slots, and lockout of booked hours",
            "Payment options: Full payment or partial deposit via simulated Stripe / PayPal",
            "Automatic booking confirmation and appointment reminders",
            "Customer personal account: view upcoming reservations, booking history, reschedule/cancel",
            "Salon manager dashboard: reservations calendar, add/edit bookings, stylist shift management",
            "Customer feedback and service review module"
        ]
    },
    {
        "num": 8,
        "folder": "Exp-08-Hospital-Appointment-Booking",
        "title": "MedCare Hospital Online Appointment Booking",
        "category": "Booking & Reservations",
        "desc": "Hospital appointment booking platform allowing patients to search doctors by specialty and location, schedule convenient slots, submit online check-in details, view past medical visits, and rate doctors.",
        "roles": ["Patient User", "Hospital Admin / Doctor"],
        "features": [
            "Patient registration, login, and medical profile management",
            "Search doctors by medical specialty (Cardiology, Orthopedics, Pediatrics, Dermatology, Neurology)",
            "Doctor profiles with qualifications, consultation fees, and patient ratings",
            "Slot picker for flexible date and time appointment booking",
            "Online pre-appointment check-in form (symptoms, allergies, medical history)",
            "Appointment management (upcoming visits, cancellation, reschedule)",
            "Past appointment history and digital prescription notes",
            "Doctor review and rating system",
            "Hospital admin dashboard: doctor directory, appointment statistics, department analytics"
        ]
    },
    {
        "num": 9,
        "folder": "Exp-09-Electronic-Gadgets-Shopping",
        "title": "TechSavvy - Electronics Shopping Platform",
        "category": "E-Commerce & Marketplaces",
        "desc": "Feature-rich electronics e-commerce store with categorized gadget catalog (Smartphones, Laptops, Tablets, Audio), search/filter, dynamic cart, order checkout, order tracking, and admin product/pricing controls.",
        "roles": ["Shopper", "Store Admin"],
        "features": [
            "User registration, login, and persistent session",
            "Categorized catalog: Smartphones, Laptops, Tablets, Smartwatches, Audio & Accessories",
            "Instant keyword search and price filter",
            "Detailed product view with specifications, availability stock, and customer reviews",
            "Interactive shopping cart: add, update quantity, remove, and live subtotal/tax calculation",
            "Multi-step checkout with shipping address and simulated payment",
            "Order tracking with status workflow (Processing, Dispatched, In Transit, Delivered)",
            "Order history with past receipts",
            "Admin inventory management: add new gadget, edit price, update description, delete item, view customer checkout list"
        ]
    },
    {
        "num": 10,
        "folder": "Exp-10-Fashion-Store-StyleHub",
        "title": "StyleHub - Online Fashion Retailer",
        "category": "E-Commerce & Marketplaces",
        "desc": "Premier fashion e-commerce platform offering clothing, footwear, and accessories for Men, Women, and Kids with size guides, customer reviews, wishlist, cart, returns policy, and admin inventory management.",
        "roles": ["Fashion Shopper", "Store Admin"],
        "features": [
            "Clean navigation with categories: Men, Women, Kids (Casual, Formal, Seasonal collections)",
            "Interactive size guide modal (S, M, L, XL, XXL) with chest/waist measurements",
            "High-resolution image galleries, product reviews, and star ratings",
            "Wishlist system to save favorite apparel items",
            "Shopping cart with quantity editor and coupon discount code support",
            "Secure checkout and simulated payment processing",
            "Order tracking and hassle-free return/exchange request module",
            "Admin dashboard: add fashion items, update pricing and descriptions, track customer orders"
        ]
    },
    {
        "num": 11,
        "folder": "Exp-11-Real-Estate-HomeFinder",
        "title": "Home Finder - Real Estate Platform",
        "category": "Portals & Management",
        "desc": "Real estate discovery platform for residential and commercial properties with advanced search filters, saved criteria, interactive map visualization, mortgage EMI calculator, and viewing scheduler.",
        "roles": ["Property Buyer / Renter", "Real Estate Agent / Admin"],
        "features": [
            "User login/registration with saved search criteria feature",
            "Comprehensive property search: filter by location, price budget, property type (Apartment, Villa, Commercial, Plot), and BHK",
            "Interactive map location visualization for property listings",
            "Detailed property listings: high-resolution photos, amenities, floor plans, neighborhood info",
            "Built-in Mortgage & Loan EMI Calculator",
            "Schedule a property viewing form with agent notification",
            "Agent & real estate company search directory",
            "Admin property management: add/edit property, manage seller listings, view visitor statistics"
        ]
    },
    {
        "num": 12,
        "folder": "Exp-12-Insurance-Management-InsureEasy",
        "title": "InsureEasy - Online Insurance Platform",
        "category": "Portals & Management",
        "desc": "Cutting-edge insurance management platform enabling customers to compare and buy Health, Auto, and Home policies, calculate premiums, file claims, and receive automated SMS renewal alerts via agents.",
        "roles": ["Customer", "Insurance Agent", "System Admin"],
        "features": [
            "Policy comparison tool across Health, Motor/Auto, Life, and Home insurance",
            "Instant insurance premium calculation based on coverage amount and age",
            "Secure online policy application and purchase",
            "Customer policy dashboard: view active policies, download policy bond, file insurance claim",
            "Agent registration & administrator approval workflow",
            "Agent dashboard: create customer record, manage policies, track commission dues",
            "Simulated SMS alert dispatcher to remind policyholders before due dates",
            "Admin portal: approve agents, view all agent performance, oversee policy portfolio"
        ]
    },
    {
        "num": 13,
        "folder": "Exp-13-Flowers-Gifts-BlossomGifts",
        "title": "BlossomGifts - Flowers & Gifts Ordering",
        "category": "E-Commerce & Marketplaces",
        "desc": "User-friendly gift and flower shop categorized by occasion, recipient, and price range, with custom delivery date scheduler, personalized card messages, cart, order summary, and admin inventory control.",
        "roles": ["Customer", "Store Admin"],
        "features": [
            "Browse floral arrangements, gift baskets, and personalized gifts by occasion (Birthday, Anniversary, Romance, Congratulation)",
            "Filter by recipient (For Him, For Her, For Parents) and price range",
            "Customization options: select delivery date & time slot, add custom greeting card text",
            "Shopping cart with item adjustments and clear order summary",
            "Simulated checkout with email/SMS order confirmation",
            "Real-time order tracking and past order history",
            "Customer inquiry form via email simulator",
            "Admin inventory management: add new bouquet/gift, modify price, update description, delete out-of-stock items"
        ]
    },
    {
        "num": 14,
        "folder": "Exp-14-Second-Hand-Market-ReNewMarket",
        "title": "ReNewMarket - Second-Hand Goods Marketplace",
        "category": "E-Commerce & Marketplaces",
        "desc": "Sustainable peer-to-peer marketplace connecting buyers and sellers for pre-loved electronics, furniture, clothing, and books with listing creation, price negotiation simulator, and logistics tracking.",
        "roles": ["Buyer", "Seller", "Market Administrator"],
        "features": [
            "User authentication & profile management",
            "Seller module: create commodity listing with title, category, condition (Like New, Good, Fair), photos, and price",
            "Buyer search and filtering across second-hand categories (Electronics, Furniture, Fashion, Books)",
            "Interactive 'Make an Offer' / Price Negotiation simulator between buyer and seller",
            "Order management: track delivery status (Pending, Shipped, In Transit, Received)",
            "Feedback and seller rating system promoting trust & sustainability",
            "Administrator dashboard: manage user accounts, manage categories (add/delete), moderate commodity listings, manage logistics status"
        ]
    },
    {
        "num": 15,
        "folder": "Exp-15-Toll-Payment-EasyToll",
        "title": "EasyToll - Online Toll Payment System",
        "category": "Utilities & Calculations",
        "desc": "Advanced toll management system allowing drivers to recharge e-Wallets, buy advance toll e-Tickets, apply for monthly toll passes with QR Codes, and enable toll booth operators to scan & verify passes instantly.",
        "roles": ["Driver User", "Toll Booth Officer", "Toll Admin"],
        "features": [
            "Driver registration, login, and vehicle plate registration",
            "e-Wallet balance management with instant add-money simulation",
            "Buy advance single/return toll e-Tickets to skip toll booth queues",
            "Apply for new monthly toll pass & renew existing toll passes",
            "Dynamic QR Code generation for vehicle toll passes",
            "Toll Gate Operator interface: QR Code scanner / Pass ID verifier, check ticket validity, update toll gate location",
            "Admin portal: approve toll passes, manage toll booth logins, create toll gates & rate slabs, inspect transaction ledger"
        ]
    },
    {
        "num": 16,
        "folder": "Exp-16-Grievance-Redressal-ComplainEase",
        "title": "ComplainEase - Grievance Redressal System",
        "category": "Portals & Management",
        "desc": "Online public grievance filing platform with category classification, interactive map pin location marking, proof-of-work status updates by municipal officers, and full administrative governance.",
        "roles": ["Citizen User", "Municipal Officer", "System Admin"],
        "features": [
            "Citizen registration & login",
            "Submit complaint form with category (Roads, Water, Sanitation, Electricity, Garbage), detailed description, and interactive map coordinate pin",
            "Real-time grievance tracking with status timeline (Submitted, Under Review, In Progress, Resolved)",
            "Citizen feedback submission on resolved complaints",
            "Officer portal: view assigned ward complaints, update resolution status, upload photo proof-of-work",
            "Admin control panel: generate credentials for officers, manage department accounts, view system reports, configure feature visibility"
        ]
    },
    {
        "num": 17,
        "folder": "Exp-17-E-Voting-VoteOnline",
        "title": "VoteOnline - Secure E-Voting Platform",
        "category": "Utilities & Calculations",
        "desc": "Secure and transparent e-voting platform featuring Voter ID authentication, 2-factor OTP verification, candidate manifestos, one-person-one-vote cryptographic ballot casting, and real-time election results.",
        "roles": ["Registered Voter", "Election Administrator"],
        "features": [
            "Voter login using official Voter ID number",
            "Simulated Multi-Factor OTP verification sent to registered phone/email",
            "Interactive ballot interface: view candidate profiles, political party, and election manifestos",
            "Secure one-click vote casting with anti-double-voting prevention checks",
            "Instant digital voter confirmation receipt with encrypted vote token",
            "Admin dashboard: create election candidates, assign candidates to wards, import/manage voter roll",
            "Live election analytics: real-time vote count tallies, percentage turnout charts, and winning candidate declarations"
        ]
    },
    {
        "num": 18,
        "folder": "Exp-18-AgriMart-Farmer-Market",
        "title": "AgriMart - Farmer Supplies Marketplace",
        "category": "E-Commerce & Marketplaces",
        "desc": "Agricultural commerce portal empowering farmers to sell produce and buy seeds, fertilizers, and equipment. Features farmer sales dashboard, buyer shopping cart, wallet balance, and shipping tracker.",
        "roles": ["Farmer / Producer", "Public Buyer"],
        "features": [
            "Farmer & buyer registration with OTP mobile verification",
            "Farmer Dashboard: add agricultural products (seeds, organic fertilizers, pesticides, farm equipment, tools), upload photos, set stock and prices",
            "Farmer Sales tracker: view orders, manage shipping status, view revenue earnings",
            "Public Buyer Portal: search and filter agricultural supplies by category and price",
            "Buyer e-Wallet balance management with top-up feature",
            "Shopping cart, shipping address manager, order placement, and live shipment tracking",
            "Direct product inquiries and farmer support"
        ]
    },
    {
        "num": 19,
        "folder": "Exp-19-Animal-Healthcare-VetCare",
        "title": "VetCare - Animal Healthcare Consultation",
        "category": "Utilities & Calculations",
        "desc": "Tele-veterinary platform where farmers upload animal illness symptoms (text, images, audio/video links) for diagnosis. Features free Govt CVH vs paid private clinic consultations with payment integration and disease analytics.",
        "roles": ["Farmer / Pet Owner", "Veterinary Doctor"],
        "features": [
            "Farmer registration and profile management",
            "Post animal medical case: select livestock type (Cattle, Sheep, Poultry, Pets), describe symptoms, and attach images or media links",
            "Choose consultation tier: Free Govt. CVH clinic or Private specialist with payment gateway (Bank Transfer / EasyPaisa simulation)",
            "Doctor portal: review patient complaints, inspect symptom photos, and issue clinical prescriptions and diet instructions",
            "Farmer prescription viewer & treatment history",
            "Epidemiological analytics dashboard: regional heat-map of prevalent animal diseases based on submitted cases",
            "Doctor directory, veterinary news & disease prevention guides"
        ]
    },
    {
        "num": 20,
        "folder": "Exp-20-Vehicle-Rental-RentRide",
        "title": "RentRide - Modern Vehicle Rental Platform",
        "category": "Booking & Reservations",
        "desc": "Vehicle rental platform offering a fleet of sedans, SUVs, and trucks with date-range rental booking, check-in forms with driver's license verification, booking history, and admin fleet management.",
        "roles": ["Customer", "Rental Admin"],
        "features": [
            "Customer registration, login, and user dashboard",
            "Search and filter vehicle fleet by vehicle type (Sedan, Compact SUV, Luxury, Pickup Truck), seating capacity, and transmission",
            "Vehicle details with daily rates, mileage allowance, and high-res photos",
            "Booking engine: select pickup and return dates, calculate total rental cost with insurance options",
            "Online check-in form submitting driver's license number and identification details",
            "Customer booking history with real-time reservation status",
            "Admin vehicle manager: add vehicle, update price, manage maintenance status",
            "Admin booking manager: approve or decline customer bookings, monitor vehicle utilization"
        ]
    },
    {
        "num": 21,
        "folder": "Exp-21-Job-Portal-Vacancy",
        "title": "JobPortal - Vacancy & Recruitment Platform",
        "category": "Portals & Management",
        "desc": "Online employment platform enabling company directors to post job vacancies and review candidate resumes, while job seekers search vacancies, filter by category/location, and submit online applications.",
        "roles": ["Job Seeker", "Company Director / HR", "Portal Admin"],
        "features": [
            "Job seeker registration, profile creation, and resume details upload",
            "Company Director registration with admin approval workflow",
            "Director portal: post new job vacancies (title, department, experience, salary range, description, contact)",
            "Job seeker vacancy search with filters for job category, location, and employment type",
            "One-click job application with cover letter and qualification summary",
            "Director applicant tracking: review applied candidates, download resumes, shortlist or reject candidates",
            "Job seeker applied jobs dashboard with status updates (Applied, Shortlisted, Interview Scheduled)",
            "Admin management: approve directors, monitor active vacancies, view recruitment statistics"
        ]
    },
    {
        "num": 22,
        "folder": "Exp-22-Solid-Waste-Management",
        "title": "Smart Solid Waste Management System",
        "category": "Portals & Management",
        "desc": "Smart municipal waste management platform tracking sensor-monitored garbage bins, calculating optimal truck collection routes to dumping sites, logging driver loads, and processing public overflow complaints.",
        "roles": ["Municipal Administrator", "Sanitation Truck Driver", "General Public"],
        "features": [
            "Admin dashboard: interactive smart bin map with live fill-level percentages (0-100%) and segregation categories (Organic, Recyclable, Hazardous)",
            "Automated optimal collection route algorithm simulating best route through overflowing bins to the final dumping site",
            "Driver management and route assignment module",
            "Driver portal: view daily assigned collection route, update bin collection status, log collected garbage load (kg)",
            "General public portal: submit overflowing bin complaints with street address and photo proof",
            "Admin analytics: daily waste collection reports, driver efficiency stats, and resolved citizen complaints"
        ]
    },
    {
        "num": 23,
        "folder": "Exp-23-Blood-Bank-Management",
        "title": "Blood Management Information System",
        "category": "Portals & Management",
        "desc": "National blood donor registry and hospital inventory system facilitating rapid donor discovery, real-time blood bank stock tracking (A, B, AB, O +/-), and emergency hospital blood requisition management.",
        "roles": ["Blood Donor / User", "Hospital & Blood Bank Admin"],
        "features": [
            "Donor registration with blood group (A+, A-, B+, B-, AB+, AB-, O+, O-), contact, city, and last donation date",
            "Donor dashboard: update donor availability status, view personal donation history, eligibility check",
            "Public donor search: filter verified donors by required blood group and city",
            "Hospital portal: register blood bank, manage available blood units inventory matrix",
            "Emergency blood request broadcast module with urgent SMS/call indicator",
            "Hospital blood stock reports: safe reserves monitoring, expired blood unit tracking",
            "Confidential medical records management and donor health screening checklist"
        ]
    },
    {
        "num": 24,
        "folder": "Exp-24-Travel-Agency-Wanderlust",
        "title": "Wanderlust Travels - Online Travel Agency",
        "category": "Booking & Reservations",
        "desc": "All-in-one travel agency platform for booking vacation packages, hotels, flights, and food itineraries with interactive destination guides, booking vouchers, and tourism administration controls.",
        "roles": ["Traveler User", "Tourism Admin"],
        "features": [
            "Traveler registration, login, and travel preferences profile",
            "Browse holiday destinations with curated photo galleries, highlights, and climate guides",
            "Explore vacation packages: combined flights, luxury hotel stays, guided routes, and meal plans",
            "View hotel & hostel accommodation details with room options and pricing",
            "Booking engine: book complete travel package or customized accommodation with instant confirmation voucher",
            "My Bookings dashboard: view upcoming trips, download travel vouchers, cancel bookings",
            "Admin portal: post new tourism destinations, manage hotel tie-ups, configure dining packages, inspect customer booking logs"
        ]
    },
    {
        "num": 25,
        "folder": "Exp-25-Breakdown-Assistance",
        "title": "On-Road Breakdown Assistance System",
        "category": "Utilities & Calculations",
        "desc": "Emergency road assistance platform connecting stranded drivers with nearby certified mechanics via GPS location simulation, breakdown service requests (tire, battery, towing), and mechanic rating reviews.",
        "roles": ["Stranded Driver", "Licensed Mechanic", "System Admin"],
        "features": [
            "Driver registration and vehicle details management",
            "Emergency SOS breakdown request: select vehicle issue (Flat Tire, Battery Jumpstart, Engine Overheating, Towing Service)",
            "Simulated GPS radar locating nearest licensed mechanics with distance and estimated time of arrival (ETA)",
            "Mechanic registration with trade license verification and admin approval workflow",
            "Mechanic portal: toggle online/offline availability, receive SOS dispatch requests, accept jobs, view customer location",
            "Real-time assistance status tracking for driver (Dispatched, En Route, Arrived, Completed)",
            "Post-service feedback, rating, and transparent billing summary"
        ]
    },
    {
        "num": 26,
        "folder": "Exp-26-Traffic-Challan-Management",
        "title": "Traffic Squad - E-Challan & Penalty Management",
        "category": "Portals & Management",
        "desc": "Traffic police e-challan enforcement portal enabling officers to issue violation cases with photographic evidence, allowing citizens to search and pay fines online, with live traffic advisory updates.",
        "roles": ["Citizen Vehicle Owner", "Traffic Police Officer", "Admin"],
        "features": [
            "Citizen portal: lookup e-Challans by vehicle registration number or challan ID",
            "View violation details: date, time, location, rule broken, fine penalty amount, and officer photo proof",
            "Secure online fine payment gateway with digital payment receipt generation",
            "Police Officer portal: authenticate badge ID, access traffic rules handbook with predefined fines",
            "Create violation case: enter vehicle plate, select violation rule, upload photographic proof, generate instant e-Challan",
            "Live traffic advisory module: post road closures, accident alerts, and traffic congestion map links",
            "Admin portal: police officer credentials management, daily fine collection audit reports"
        ]
    },
    {
        "num": 27,
        "folder": "Exp-27-Bus-Pass-Management",
        "title": "Bus Pass Management System with QR Code",
        "category": "Portals & Management",
        "desc": "Digital bus pass issuing system with student concession passes (free for govt schools) and route employee passes, monthly renewal with e-wallet deduction, dynamic QR Code pass generation, and conductor verification scanner.",
        "roles": ["Passenger / Student", "Transport Admin", "Bus Conductor"],
        "features": [
            "User registration, login, and commuter profile",
            "Apply for Student Pass: input educational institution, upload photo ID, select validity (government school student free pass option)",
            "Apply for Route Bus Pass: input employer details, source and destination bus stops, route number",
            "e-Wallet system: add funds and buy single trip bus e-Tickets",
            "Monthly pass renewal workflow with automatic e-wallet balance deduction",
            "Dynamic QR Code pass generation containing encrypted pass ID, holder photo, route, and expiration date",
            "Bus Conductor portal: interactive QR scanner / Pass ID validator to verify pass authenticity, check route stops, and log bus location"
        ]
    },
    {
        "num": 28,
        "folder": "Exp-28-Artist-Portfolio-ArtistryHub",
        "title": "ArtistryHub - Emily Harris Artist Portfolio",
        "category": "Portfolios, Blogs & Content",
        "desc": "Bespoke digital portfolio celebrating artist Emily Harris featuring high-res artwork gallery, career biography timeline, discography/bibliography archives, media interview gallery, exhibition updates, and print store.",
        "roles": ["Art Enthusiast / Collector", "Artist / Curator"],
        "features": [
            "Engaging homepage with artistic hero banner, featured artworks, and artist vision statement",
            "About the Artist: comprehensive biography, creative influences, studio story, and high-quality artist portraits",
            "Categorized Art Portfolio: Oil Paintings, Watercolor, Sculptures, and Digital Works with lightbox preview and descriptions",
            "Discography & Bibliography: comprehensive catalog of published art monographs, books, exhibition catalogs with ISBNs",
            "Media Gallery: video interview player, press articles, podcasts, and exhibition vernissage recordings",
            "Exhibitions & Events: upcoming gallery exhibitions with dates and venue locations",
            "Interactive features: art print shop preview, newsletter subscription, and booking/inquiry form"
        ]
    },
    {
        "num": 29,
        "folder": "Exp-29-Event-Registration-Page",
        "title": "TechCon - Event Landing & Registration Page",
        "category": "Portfolios, Blogs & Content",
        "desc": "Modern conference landing page with featured keynote speakers, conference agenda schedule chunks (morning/afternoon), venue information with map, audience breakdown, and ticket registration form.",
        "roles": ["Event Attendee", "Event Organizer"],
        "features": [
            "Engaging header with conference countdown timer, dates, venue, and primary CTA",
            "Keynote Speakers showcase: speaker cards with headshots, topics, corporate affiliations, and social links",
            "Chunked Conference Schedule: interactive tabbed timeline for Day 1 and Day 2 (Keynote, Breakout sessions, Lunch, Panel, Networking)",
            "Event Purpose & Target Audience section: clearly defining who should attend (Engineers, Founders, Researchers, Students)",
            "Interactive Venue guide with map representation, directions, and nearby accommodation",
            "Attendee Registration Form: ticket tier selection (Student, Standard, VIP), participant details, dietary requirements, and instant ticket pass generation"
        ]
    },
    {
        "num": 30,
        "folder": "Exp-30-Academic-Journal-IJSSE",
        "title": "IJSSE - Academic Journal Publishing Portal",
        "category": "Portals & Management",
        "desc": "Official publisher portal for the International Journal of Scientific and Social Excellence (ISSN 2395-1443 / 2395-1451) with dedicated Author, Reviewer, and Editor workflows, manuscript tracking, and article archives.",
        "roles": ["Author", "Peer Reviewer", "Managing Editor", "Reader"],
        "features": [
            "Journal homepage with aims, scope, indexing credentials (Scopus indexed), print ISSN 2395-1443 and online ISSN 2395-1451",
            "Author Portal: manuscript submission form, download manuscript template & copyright form, fee guidelines, and real-time paper status tracking",
            "Reviewer Portal: reviewer registration, assigned papers queue, structured manuscript evaluation rubric (originality, methodology, clarity)",
            "Editor Portal: editorial board directory, assign manuscripts to peer reviewers, review recommendation verdicts (Accept, Revisions, Reject)",
            "Article Repository: Current Issue, Archive volumes, Most Viewed and Most Cited papers with DOI citations",
            "Call for Papers announcements, newsletter subscription, and editorial contact desk"
        ]
    },
    {
        "num": 31,
        "folder": "Exp-31-Dairy-Farm-KoMatha",
        "title": "Ko-Matha Smart Dairy Farm Management",
        "category": "E-Commerce & Marketplaces",
        "desc": "Smart dairy farm portal showcasing Indian A1 cow milk products (milk, curd, cova-sweet, butter, ghee), customer online ordering, daily/monthly stock inventory reports, and milk vendor collection records.",
        "roles": ["Customer", "Farm Administrator", "Milk Vendor"],
        "features": [
            "Farm showcase: heritage of Indian A1 cows, organic milking practices, hygiene testing, and health benefits",
            "Online Dairy Store: fresh A1 milk, curd, traditional cova-sweet, churned butter, and pure cow ghee with package sizes and pricing",
            "Customer online order placement with recurring daily/weekly delivery schedule",
            "Admin stock maintenance: daily milk production entry form, wastage log, and sales tracking",
            "Automated inventory reports: Daily, Monthly, and Yearly milk yield and product sales analytics",
            "Milk Vendor Management: registered vendor information, daily milk procurement logs, fat content quality testing, and cow health records"
        ]
    },
    {
        "num": 32,
        "folder": "Exp-32-Laptop-Sales-Service-RamInfotech",
        "title": "Ram Infotech - Laptop Sales & Service Portal",
        "category": "E-Commerce & Marketplaces",
        "desc": "Dual laptop sales and service management system featuring detailed model specs, service repair booking & ticket tracking, laptop rental agreement generator, and shop stock inventory control.",
        "roles": ["Customer", "Service Technician", "Store Admin"],
        "features": [
            "Online Laptop Store: filter laptops by brand (Dell, HP, Lenovo, Apple), processor, RAM, graphics, and price",
            "Laptop specifications modal with high-res photos and purchase checkout",
            "Service Center module: schedule laptop repair, specify fault symptoms (Screen, Motherboard, Battery, OS), and receive Service Ticket ID",
            "Real-time Service Status Tracker: check repair progress (Diagnosing, Waiting for Parts, Repaired, Ready for Pickup)",
            "Laptop Rental Agreement generator: select rental period, configuration, security deposit, and generate printable lease contract",
            "Admin Stock & Service Dashboard: track hardware stock in shop, manage pending repairs, assign technician tasks"
        ]
    },
    {
        "num": 33,
        "folder": "Exp-33-Restaurant-Booking-KodaikanalEats",
        "title": "KodaikanalEats - Restaurant & Resort Booking",
        "category": "Booking & Reservations",
        "desc": "Kodaikanal hospitality platform for booking dining tables and resort suites (Single, Double, Deluxe) with seasonal/non-seasonal pricing, room boy availability tracking, and menu ordering.",
        "roles": ["Guest / Tourist", "Resort & Restaurant Admin"],
        "features": [
            "Restaurant table reservation: select dining time, party size, indoor/balcony valley-view seating, and dietary preferences",
            "Resort accommodation booking: browse Single Room ($45/night), Double Room ($75/night), and Luxury Deluxe Suite ($130/night)",
            "Seasonal vs Non-Seasonal rate toggle with automatic price adjustment",
            "Real-time room availability checker across calendar dates",
            "Room boy / housekeeping staff availability tracker and room service assignment",
            "Local culinary highlights menu and special hill-station offer packages",
            "Admin dashboard: manage room rates, monitor daily occupancy, assign room attendants, inspect customer booking ledger"
        ]
    },
    {
        "num": 34,
        "folder": "Exp-34-Tuition-Centre-LearnWell",
        "title": "LearnWell Tuition Centre Management System",
        "category": "Portals & Management",
        "desc": "Comprehensive tuition centre management website managing course offerings, online/offline student enrollments, fee payment tracking, teacher allocations, academic progress reports, and maintenance requests.",
        "roles": ["Student / Parent", "Teacher / Tutor", "Centre Admin"],
        "features": [
            "Centre announcements board for class schedules, exam revisions, and holiday notices",
            "Subject catalog: Mathematics, Physics, Chemistry, Biology, and Computer Science with course duration, fee structure, and Online/Offline mode toggle",
            "Student registration and course enrollment with digital fee payment simulation",
            "Teacher portal: manage assigned classes, mark attendance, and log student performance feedback",
            "Student dashboard: view enrolled subjects, fee receipts, class timetable, and submit maintenance/help requests",
            "Admin analytics: monthly and yearly fee collection reports, teacher-subject allocation matrix, student enrollment trends"
        ]
    },
    {
        "num": 35,
        "folder": "Exp-35-Online-Teaching-EduConnect",
        "title": "EduConnect - Interactive Teaching Platform",
        "category": "Portals & Management",
        "desc": "Interactive learning management system featuring course catalog, student/instructor registration, subject allocation, video lecture streaming, downloadable materials, quizzes, and timetable management.",
        "roles": ["Student", "Instructor / Teacher", "Academic Admin"],
        "features": [
            "Course catalog: browse certified courses across Web Development, Data Science, AI, and Cloud Computing",
            "Student registration, course enrollment, and progress tracking dashboard",
            "Teacher registration and subject allocation by department",
            "Interactive classroom: video lecture player, downloadable lecture PDFs, and discussion forum",
            "Interactive knowledge quiz with instant scoring and explanation feedback",
            "Class schedule & time management timetable with upcoming live sessions",
            "Teacher course builder: upload lectures, create assignments, track enrolled students",
            "Admin academic dashboard: monitor active courses, student completion rates, and instructor workload"
        ]
    },
    {
        "num": 36,
        "folder": "Exp-36-Bookstore-BookHaven",
        "title": "BookHaven - Online Bookstore",
        "category": "E-Commerce & Marketplaces",
        "desc": "Online bookstore featuring bestseller book carousel, genre catalog filters (Fiction, Non-fiction, Academic), book preview modal, shopping cart, FAQs accordion, customer reviews, and literary blog.",
        "roles": ["Reader / Customer", "Bookstore Admin"],
        "features": [
            "Homepage with bestseller carousel, new release highlights, and editor's picks",
            "Catalog page with multi-criteria filtering: genre (Fiction, Science Fiction, Business, Self-Help, Academic), author, and price slider",
            "Book details modal: book cover, synopsis, author bio, rating stars, and customer reviews",
            "Interactive shopping cart with item quantity adjustments and checkout summary",
            "Literary Blog section sharing book reviews, author interviews, and reading lists",
            "Customer Support FAQ accordion covering shipping, returns, and orders",
            "Privacy policy page and store contact information",
            "Admin portal: add new book titles, update inventory stock, manage featured collections"
        ]
    },
    {
        "num": 37,
        "folder": "Exp-37-Professional-Showcase-Portfolio",
        "title": "MyProfessionalShowcase - Portfolio & Resume",
        "category": "Portfolios, Blogs & Content",
        "desc": "Portfolio website presenting professional bio, categorized skill bars, featured projects gallery with live demos, interactive career timeline, downloadable resume, testimonials, and contact form.",
        "roles": ["Recruiter / Client", "Portfolio Owner"],
        "features": [
            "Hero section with professional introduction, key specialties, and call-to-action buttons",
            "About Me page: career journey, educational background, philosophy, and colleague testimonials",
            "Skills Matrix: technical skills categorized into Frontend, Backend, Database, and DevOps with proficiency indicators",
            "Interactive Portfolio: filterable project cards with descriptions, tech stacks, live demo links, and GitHub repository links",
            "Interactive Resume Page: chronological milestone timeline of work experience, education, certifications, and one-click printable/downloadable resume modal",
            "Tech Insights Blog: articles on modern web architecture and engineering practices",
            "Contact Form with instant message validation and professional social media links"
        ]
    },
    {
        "num": 38,
        "folder": "Exp-38-Fine-Dining-GourmetHaven",
        "title": "Gourmet Haven - Fine Dining Restaurant",
        "category": "Portfolios, Blogs & Content",
        "desc": "Restaurant website featuring rotating ambiance carousel, categorized fine dining menu with prices, online table reservation calendar, executive chef profile, culinary philosophy, and patron reviews.",
        "roles": ["Dining Guest", "Restaurant Manager"],
        "features": [
            "Atmospheric homepage with rotating image carousel of dining ambiance and signature culinary creations",
            "About Us: restaurant heritage, farm-to-table culinary philosophy, and Executive Chef bio",
            "Interactive Categorized Menu: Appetizers, Main Courses, Chef's Specials, Artisan Desserts, and Wine Pairings with allergen tags and pricing",
            "Online Table Reservation System: date picker, time slot selector, guest count, seating area (Main Dining Room, Private Wine Cellar, Garden Terrace)",
            "Special Offers & Events section: tasting menus, weekend jazz brunch, and seasonal celebrations",
            "Patron Testimonials and Michelin-standard culinary reviews",
            "Contact & Location page: interactive map widget, address, opening hours, and private dining inquiry form"
        ]
    },
    {
        "num": 39,
        "folder": "Exp-39-Product-Catalog-Cart",
        "title": "TechStore - Clean Product Catalog & Cart",
        "category": "E-Commerce & Marketplaces",
        "desc": "E-commerce product catalog with category navigation, real-time search, price filtering, dynamic cart drawer, tax/shipping calculations, streamlined checkout, and simulated email confirmation.",
        "roles": ["Customer", "Store Operator"],
        "features": [
            "Clean and intuitive homepage showcasing featured products and category tabs (Electronics, Wearables, Accessories)",
            "Instant product search bar and filter by price range and rating",
            "Product cards with high-res imagery, price, stock status, and single-click 'Add to Cart'",
            "Interactive Shopping Cart drawer: increment/decrement quantities, remove items, clear cart, dynamic subtotal and tax calculation",
            "User Account management: saved shipping addresses and simulated past order history",
            "Streamlined two-step checkout process with credit card/UPI mock payment",
            "Order confirmation modal with unique order ID, itemized receipt, and simulated email confirmation dispatch"
        ]
    },
    {
        "num": 40,
        "folder": "Exp-40-Travel-Blog-Interactive-Map",
        "title": "Travel Explorer - Interactive Travel Blog",
        "category": "Portfolios, Blogs & Content",
        "desc": "Travel blog with interactive world map highlighting visited destinations, filterable adventure narratives, rich photo galleries, reader comment threads, travel packing tools, and author biography.",
        "roles": ["Travel Reader", "Travel Blogger"],
        "features": [
            "Inviting homepage with recent travel stories, featured expeditions, and clean navigation",
            "Interactive Visited Destinations Map: interactive coordinates pins linking directly to corresponding location journals",
            "Destination filter: browse articles by continent (Europe, Asia, Americas, Africa) and travel style (Solo, Adventure, Foodie)",
            "Immersive Blog Articles: rich narrative text, location travel tips, and responsive photo slideshow galleries",
            "Interactive Reader Comments: post feedback, ask travel questions, and join community discussions",
            "About the Traveler: author biography, travel milestones, camera gear, and essential packing checklists",
            "Social media share shortcuts to expand article reach"
        ]
    },
    {
        "num": 41,
        "folder": "Exp-41-Digital-Recipe-Book",
        "title": "CulinaryDelight - Digital Recipe Book",
        "category": "Portfolios, Blogs & Content",
        "desc": "Digital culinary platform featuring categorized recipes, dynamic serving size ingredient scaler, step-by-step cooking mode, user reviews, recipe search/filter, and weekly meal planner with shopping list export.",
        "roles": ["Home Cook", "Recipe Creator"],
        "features": [
            "Curated recipe collection categorized by meal type (Breakfast, Mains, Desserts, Beverages) and dietary tags (Vegetarian, Vegan, Gluten-Free, Keto)",
            "Recipe search bar and multi-filter (cooking time, difficulty level, cuisine)",
            "Detailed Recipe Page: dish photography, prep & cook times, calories, and user star ratings",
            "Dynamic Serving Size Scaler: change serving count (e.g. 2 to 4 to 8) to automatically recalculate all ingredient quantities in real-time",
            "Step-by-step Interactive Cooking Mode with ingredient check-off",
            "Community comments and review ratings section",
            "Weekly Meal Planner & automatic shopping list generator with export/print capability"
        ]
    },
    {
        "num": 42,
        "folder": "Exp-42-Electricity-Bill-Payment",
        "title": "Online Electricity Bill Payment System",
        "category": "Utilities & Calculations",
        "desc": "Online electricity bill calculation and payment system implementing exact domestic and commercial tariff slabs, bi-monthly billing cycles, late payment fine calculation (Rs. 10/day), and receipt generator.",
        "roles": ["Electricity Consumer", "Board Billing Admin"],
        "features": [
            "Consumer registration, login, and connection profile (Consumer Number, Meter ID)",
            "Exact Tariff Calculation Engine implemented strictly per norms:",
            "  * Domestic Connection: First 100 units @ Rs. 1.00/unit | 101-200 units @ Rs. 2.50/unit | 201-500 units @ Rs. 4.00/unit | >500 units @ Rs. 6.00/unit",
            "  * Commercial Connection: First 100 units @ Rs. 2.00/unit | 101-200 units @ Rs. 4.50/unit | 201-500 units @ Rs. 6.00/unit | >500 units @ Rs. 7.00/unit",
            "Bi-monthly billing period cycle (start date, end date, last date of payment)",
            "Late Fine Calculator: automatically applies Rs. 10 per day fine for payments made after the last date",
            "Bill breakdown display: energy charges by slab, fixed charges, late fine, and net payable amount",
            "Multi-method payment gateway (Credit Card, Debit Card, Net Banking, UPI, Digital Wallet)",
            "Downloadable & printable official EB Payment Receipt with transaction reference",
            "Admin portal: update tariff slab rates, modify billing cycle dates, inspect consumer payment records"
        ]
    },
    {
        "num": 43,
        "folder": "Exp-43-Online-Placement-Exam",
        "title": "Online Placement Examination System",
        "category": "Utilities & Calculations",
        "desc": "Online placement examination platform featuring admin exam scheduling & question bank, candidate timed test interface with countdown timer, automatic evaluation, scorecard generation, and merit rank list.",
        "roles": ["Candidate Student", "Placement Exam Admin"],
        "features": [
            "Candidate login with allotted roll number and exam schedule verification",
            "Admin portal: exam scheduling (date, time, duration), question bank upload (MCQs covering Quantitative Aptitude, Logical Reasoning, and Technical Coding)",
            "Candidate Examination Interface: real-time countdown timer, question navigator palette (Answered, Marked for Review, Not Visited)",
            "Automatic instant answer evaluation and scoring upon test submission or timer expiry",
            "Comprehensive Candidate Scorecard: sectional breakdown, accuracy percentage, time taken, and pass/fail outcome",
            "Placement Merit List & Ranking: dynamic leaderboard showing passed candidates ranked by highest score",
            "Online Re-evaluation / Review request submission module"
        ]
    },
    {
        "num": 44,
        "folder": "Exp-44-Painting-Rating-Review",
        "title": "Painting Rating & Review Platform",
        "category": "Portfolios, Blogs & Content",
        "desc": "Art review platform where admin uploads paintings under scheduled packages, painting owners track audience critiques, and customers rate paintings 1 to 5 stars with positive and negative sentiment analysis.",
        "roles": ["Art Customer", "Painting Owner / Artist", "Art Admin"],
        "features": [
            "Customer authenticated login via simulated social media or email ID",
            "Painting display gallery showcasing active exhibited artwork with title, artist, medium, and description",
            "Interactive 5-Star Rating System and structured feedback submission (Positive highlights and constructive critique)",
            "Real-time dynamic calculation of average star rating and positive/negative sentiment summary percentages",
            "Painting Owner portal: register painting, select exhibition package duration (days), complete package fee payment, and inspect reviews analytics",
            "Admin dashboard: upload new scheduled paintings, review historical feedback before cycling artworks, manage package pricing"
        ]
    },
    {
        "num": 45,
        "folder": "Exp-45-Income-Tax-Calculation",
        "title": "Income Tax Calculation Web Application",
        "category": "Utilities & Calculations",
        "desc": "Income tax calculation system implementing exact government tax formulas and slabs: Gross Pay, HRA, Standard Deduction (Rs. 50,000), Pension (capped at Rs. 150,000), Health Insurance, with slab tax rates and report download.",
        "roles": ["Salaried Employee", "Tax Admin"],
        "features": [
            "Employee authenticated login (simulated Google / Corporate credentials)",
            "Financial Details Input Form: Monthly Gross Pay, Monthly House Rent Allowance (HRA), Annual Pension contribution, Annual Health Insurance premium (Sec 80D)",
            "Exact Net Taxable Income Calculation Formula strictly implemented:",
            "  Net Taxable Income = (Gross Pay * 12) - (HRA * 12) - 50,000 [Standard Deduction] - min(Pension * 12, 150,000) - (Health Insurance * 12)",
            "Exact Government Tax Slabs Computation strictly implemented:",
            "  * If Net Taxable Income <= Rs. 500,000: Tax = Rs. 0 (Nil)",
            "  * If Net Taxable Income > Rs. 500,000:",
            "      - Up to Rs. 250,000: Rs. 0",
            "      - Rs. 250,001 to Rs. 500,000: 5% of (Net - 250,000)",
            "      - Rs. 500,001 to Rs. 1,000,000: Rs. 12,500 + 20% of (Net - 500,000)",
            "      - Above Rs. 1,000,000: Rs. 112,500 + 30% of (Net - 1,000,000)",
            "Itemized tax breakdown display: Total Gross, Total Deductions, Net Taxable Income, Slab-wise Tax Liability, Net Take-Home Salary",
            "Personalized Tax-Saving Recommendations and Printable Tax Computation Statement",
            "Admin portal: configure statutory deduction limits and tax slab threshold parameters"
        ]
    },
    {
        "num": 46,
        "folder": "Exp-46-Phone-Bill-Payment",
        "title": "Online Phone Bill Payment System",
        "category": "Utilities & Calculations",
        "desc": "Online telecommunications billing and payment platform with monthly billing duration, last date overdue fine calculation (Rs. 10/day), flexible full/custom amount payments, and receipt generator.",
        "roles": ["Telecom Customer", "Telecom Billing Admin"],
        "features": [
            "Customer registration, login, and telecom account dashboard (Mobile Number, Plan Details)",
            "Monthly billing period tracking (Billing Start Date, End Date, Due Date)",
            "Outstanding bill breakdown: plan rental, data add-ons, roaming, and previous balance",
            "Late Fine Calculation: automatically computes Rs. 10 per day fine for payments after the due date",
            "Flexible payment modes: Pay Full Outstanding Bill or Enter Custom Partial Amount",
            "Multi-channel payment options (Credit/Debit Card, Net Banking, UPI, Mobile Wallets)",
            "Instant payment confirmation with digital transaction receipt and simulated email delivery",
            "Billing history ledger and recurring payment autopay configuration",
            "Admin portal: update monthly billing cycle dates, manage tariff plans, inspect subscriber payment logs"
        ]
    }
]
print("Loaded metadata for", len(EXPERIMENTS), "experiments.")
