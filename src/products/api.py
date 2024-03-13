from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from product_parser.services import (get_all_products, get_product,
                                     get_product_for_detail)


class ProductAPIView(APIView):
    def get(self, request, product_name=None, product_field=None):
        if product_field:
            product_detail = get_product_for_detail(
                product_name=product_name, product_field=product_field
            )
            if product_detail is not None:
                if product_detail[product_field] is not None:
                    return Response({"result": product_detail})
                else:
                    return Response(
                        {
                            "error": f"Attribute '{product_field}' not found for product '{product_name}'"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"error": f"'{product_name}' not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        elif product_name:
            product = get_product(product_name=product_name)
            if product:
                return Response({"result": product})
            else:
                return Response(
                    {"error": f"'{product_name}' not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            all_products = get_all_products()
            return Response({"results": all_products})
