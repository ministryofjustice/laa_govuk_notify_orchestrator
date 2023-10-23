from app.notify import NotifyClient


class TestSingleton:
    def test_same_object_returned(self):
        client_1 = NotifyClient()
        client_2 = NotifyClient()
        assert client_1 == client_2
        assert client_1 is client_2
