# In your tests

from unittest.mock import Mock
from pulsar.stages.send_messages import SendMessagesStage

def test_send_messages_stage():
    mock_producer = Mock()
    mock_metrics = Mock()
    
    stage = SendMessagesStage(
        producer=mock_producer,
        metrics=mock_metrics
    )
    
    stage.run(params={"message": "test"})
    
    mock_producer.send_message.assert_called_once_with("test")
    mock_metrics.record_send.assert_called_once()
