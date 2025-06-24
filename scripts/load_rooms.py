import json
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from app.models.room import Room
from app.services.embedding import embed_text
from app.db.session import get_db
from app.core.logger import setup_logging, get_logger
from datetime import date

# Initialize logging for the script
setup_logging(log_level="INFO", enable_console=True, enable_file=False)
logger = get_logger(__name__)

# Example data
ROOM_DATA = [
    {
        "description": "A cozy sea-view apartment near the beach with free WiFi and balcony.",
        "price": 120.0,
        "location": "Odesa",
        "amenities": ["wifi", "balcony", "sea view"],
        "beds": 2,
        "max_guests": 4,
        "room_type": "apartment",
        "has_kitchen": True,
        "available_from": "2025-06-21",
        "available_to": "2025-07-31",
    },
    {
        "description": "Luxury hotel suite in downtown Kyiv with city skyline views, spa access, and premium amenities.",
        "price": 280.0,
        "location": "Kyiv",
        "amenities": ["wifi", "spa", "city view", "room service", "minibar"],
        "beds": 1,
        "max_guests": 2,
        "room_type": "suite",
        "has_kitchen": False,
        "available_from": "2025-06-25",
        "available_to": "2025-08-15",
    },
    {
        "description": "Budget-friendly hostel room in Lviv old town with shared bathroom and kitchen access.",
        "price": 35.0,
        "location": "Lviv",
        "amenities": ["wifi", "shared kitchen", "lockers"],
        "beds": 1,
        "max_guests": 1,
        "room_type": "hostel",
        "has_kitchen": False,
        "available_from": "2025-06-20",
        "available_to": "2025-09-30",
    },
    {
        "description": "Modern studio apartment in Kharkiv with full kitchen, workspace, and high-speed internet.",
        "price": 85.0,
        "location": "Kharkiv",
        "amenities": ["wifi", "workspace", "kitchen", "parking"],
        "beds": 1,
        "max_guests": 2,
        "room_type": "studio",
        "has_kitchen": True,
        "available_from": "2025-07-01",
        "available_to": "2025-08-31",
    },
    {
        "description": "Charming guesthouse room in Zakarpattia mountains with garden view and traditional breakfast.",
        "price": 60.0,
        "location": "Zakarpattia",
        "amenities": ["wifi", "garden view", "breakfast included", "hiking trails"],
        "beds": 2,
        "max_guests": 3,
        "room_type": "guesthouse",
        "has_kitchen": False,
        "available_from": "2025-06-24",
        "available_to": "2025-10-15",
    },
    {
        "description": "Spacious family apartment in Dnipro with 3 bedrooms, playground access, and pet-friendly policy.",
        "price": 150.0,
        "location": "Dnipro",
        "amenities": [
            "wifi",
            "playground",
            "pet-friendly",
            "washing machine",
            "parking",
        ],
        "beds": 3,
        "max_guests": 6,
        "room_type": "apartment",
        "has_kitchen": True,
        "available_from": "2025-07-05",
        "available_to": "2025-08-20",
    },
    {
        "description": "Beachfront villa in Berdyansk with private pool, BBQ area, and direct beach access.",
        "price": 350.0,
        "location": "Berdyansk",
        "amenities": ["wifi", "private pool", "bbq", "beach access", "parking"],
        "beds": 4,
        "max_guests": 8,
        "room_type": "villa",
        "has_kitchen": True,
        "available_from": "2025-06-28",
        "available_to": "2025-09-01",
    },
    {
        "description": "Historic boutique hotel room in Chernivtsi with antique furnishings and city center location.",
        "price": 95.0,
        "location": "Chernivtsi",
        "amenities": ["wifi", "historic building", "city center", "room service"],
        "beds": 1,
        "max_guests": 2,
        "room_type": "hotel room",
        "has_kitchen": False,
        "available_from": "2025-06-22",
        "available_to": "2025-07-30",
    },
    {
        "description": "Eco-friendly cabin in Carpathian National Park with solar power and nature trails.",
        "price": 75.0,
        "location": "Carpathian Mountains",
        "amenities": ["eco-friendly", "nature trails", "solar power", "fireplace"],
        "beds": 2,
        "max_guests": 4,
        "room_type": "cabin",
        "has_kitchen": True,
        "available_from": "2025-07-10",
        "available_to": "2025-09-15",
    },
    {
        "description": "Business hotel room in Poltava with conference facilities, executive lounge, and airport shuttle.",
        "price": 110.0,
        "location": "Poltava",
        "amenities": [
            "wifi",
            "conference facilities",
            "executive lounge",
            "airport shuttle",
        ],
        "beds": 1,
        "max_guests": 2,
        "room_type": "hotel room",
        "has_kitchen": False,
        "available_from": "2025-06-26",
        "available_to": "2025-08-10",
    },
]


def main():
    """Load room data into the database with embeddings."""
    logger.info("Starting room data loading process")
    logger.info(f"Loading {len(ROOM_DATA)} rooms into database")

    try:
        with get_db() as session:
            for i, room_data in enumerate(ROOM_DATA):
                logger.debug(
                    f"Processing room {i+1}/{len(ROOM_DATA)}: {room_data['location']}"
                )

                try:
                    # Generate embedding for room description
                    emb = embed_text(room_data["description"])
                    logger.debug(
                        f"Generated embedding for room in {room_data['location']}"
                    )

                    # Convert date strings to date objects
                    room_data_copy = room_data.copy()
                    room_data_copy["available_from"] = date.fromisoformat(
                        room_data["available_from"]
                    )
                    room_data_copy["available_to"] = date.fromisoformat(
                        room_data["available_to"]
                    )

                    # Create room object
                    room = Room(
                        embedding=emb,
                        **room_data_copy,
                    )

                    session.add(room)
                    logger.debug(
                        f"Added room to session: {room_data['location']} - ${room_data['price']}"
                    )

                except Exception as e:
                    logger.error(f"Error processing room {i+1}: {e}")
                    raise

            # Session is committed automatically when exiting the context manager
            logger.info("All rooms inserted successfully with embeddings")

    except Exception as e:
        logger.error(f"Failed to load room data: {e}")
        raise


if __name__ == "__main__":
    main()
