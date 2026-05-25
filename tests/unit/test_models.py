import pytest
from services.shared.models import Job, Resume, Match
import uuid

@pytest.mark.unit
def test_user_creation():
    from services.shared.models import User
    user = User(email="test@test.com", password_hash="hash")
    assert user.email == "test@test.com"
    assert user.id is not None

@pytest.mark.unit
def test_job_creation():
    job = Job(title="Software Engineer", company="Test Co", url="http://test.com")
    assert job.title == "Software Engineer"
    assert job.source == "indeed"

@pytest.mark.unit
def test_match_score_logic():
    match = Match(match_score=85.5)
    assert match.match_score > 80
    assert match.status == "new"
