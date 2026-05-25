import pytest
from unittest.mock import MagicMock, patch

@pytest.mark.unit
def test_get_embedding_mock():
    # Import first to ensure the module is in sys.modules and accessible
    import services.shared.vector
    with patch('services.shared.vector.client') as mock_client:
        mock_res = MagicMock()
        mock_res.data = [MagicMock(embedding=[0.1] * 1536)]
        mock_client.embeddings.create.return_value = mock_res
        
        from services.shared.vector import get_embedding
        emb = get_embedding("test text")
        assert len(emb) == 1536
        assert emb[0] == 0.1

@pytest.mark.unit
def test_ensure_collection_mock():
    import services.shared.vector
    with patch('services.shared.vector.qdrant') as mock_qdrant:
        from services.shared.vector import ensure_collection
        mock_qdrant.get_collection.side_effect = Exception("Not found")
        ensure_collection()
        assert mock_qdrant.create_collection.called
