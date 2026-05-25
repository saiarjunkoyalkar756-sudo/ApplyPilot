import pytest
from services.shared.models import Job, Resume, Match, User
import uuid

@pytest.mark.unit
def test_user_creation():
    user = User(email="test@test.com", password_hash="hash")
    user.id = uuid.uuid4() # Manually set for unit test
    assert user.email == "test@test.com"
    assert user.id is not None

@pytest.mark.unit
def test_job_creation():
    job = Job(title="Software Engineer", company="Test Co", url="http://test.com", source="indeed")
    assert job.title == "Software Engineer"
    assert job.source == "indeed"

@pytest.mark.unit
def test_match_score_logic():
    match = Match(match_score=85.5, status="new")
    assert match.match_score > 80
    assert match.status == "new"
