from pathlib import Path
from event_system.shared.utils.logging import setup_logging

TEST_DIR = Path(__file__).parent
TEST_LOG_DIR = TEST_DIR / "logs"
TEST_LOG_DIR.mkdir(exist_ok=True)

TEST_DATABASE_URL = "postgresql+asyncpg://admin:secret@localhost:5433/test_db"

logger = setup_logging("test")