from rest_framework.response import Response
from rest_framework.views import APIView


class ProductAPIView(APIView):
    def get(self, request, product_name=None, product_field=None):
        if product_field:

            return Response(
                {"product_field": product_field, "product_name": product_name}
            )
        elif product_name:

            return Response({"product_name": product_name})

        else:

            return Response({"product": "all_product"})
