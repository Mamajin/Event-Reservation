from ninja import NinjaAPI, Schema

stub_api = NinjaAPI()



@stub_api.post("/event/create")
def create_mock_event(request):
    pass