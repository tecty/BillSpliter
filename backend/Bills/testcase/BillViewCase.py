from .util import * 
from Bills.views import BillViewSet

class BillCreateViewCase(UserCaseEnv, ViewCaseMixIn):
    """
    Test the variation I made in the Bill Create view 
    """

    def setUp(self):
        super().setUp()
        # I need request factory to get the test aspect of view 
        self.factory = APIRequestFactory()

    def get_view(self):
        # set the wiew I want to test 
        return BillViewSet.as_view({'post':'create'})

    def check_create_bill_state(self,state:str):
        """
        Simplly checking the created bill state.
        """
        # because the setup stage has create 3 bills
        b = Bill.objects.get(pk = 4)
        self.assertEqual(b.state, state)
        

    def test_create_bill_success(self):
        res = self.mk_request(
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
            },
            self.ul[0]
        )
        self.assertEqual(res.status_code, 201)
        self.check_create_bill_state(PREPARE)


    def test_create_self_only_bill_success(self):
        res = self.mk_request(
            '/v0/bills/',
            {
                "title": "ss",
                "description": "ss",
                "group":1,
                "transactions":[
                    {
                        "from_u":1, 
                        "amount":"1.0"
                    }
                ]
            },
            self.ul[0]
        )
        self.assertEqual(res.status_code, 201)
        print(res.data)

        # concencus by he self, so it would be success 
        self.check_create_bill_state(CONCENCUS)
