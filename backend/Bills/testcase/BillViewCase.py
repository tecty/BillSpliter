from .util import * 
from Bills.views import BillViewSet

class BillViewCase(UserCaseEnv):
    
    def setUp(self):
        super().setUp()

        # I need request factory to get the test aspect of view 
        self.factory = APIRequestFactory()
        self.create_view = BillViewSet.as_view({'post':'create'})

    def test_create_bill_success(self):
        req = self.factory.post(
            '/v0/bills/',
            {
                "title": "ss",
                "description": "ss",
                "group":1,
                "transactions":[
                    {
                        "from_u":1, 
                        "amount":"1.0"
                    },
                    {
                        "from_u":2, 
                        "amount":"1.0"
                    }
                ]
            }
        )
        force_authenticate(req,user = self.ul[0])

        # finally we can get our response 
        res = self.create_view(req)

        self.assertEqual(res.status_code, 200)

