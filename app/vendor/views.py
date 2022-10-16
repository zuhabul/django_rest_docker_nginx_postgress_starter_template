from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import action
from rest_framework.response import Response

from vendor import serializers
from core.models import Vendor, Offer



class VendorViewSet(viewsets.ModelViewSet):
    """Manage Vendor in database"""
    serializer_class = serializers.VendorSerializer
    queryset = Vendor.objects.all()
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def _params_to_int(self, qs):
        """Convert a list of string IDs to a list of ingegers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Rectrive recipe from authenticated user"""
        category = self.request.query_params.get('category')

        queryset = self.queryset
        if category:
            category_ids = self._params_to_int(category)
            queryset = queryset.filter(category__id__in=category_ids)

        return queryset


# class VendorDetailedViewSet(generics.GenericAPIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     def get(self, request, *args, **kwargs):
#         vendor = Vendor.objects.all()
#         offer = Offer.objects.all()

#         context = {
#             "request": request,
#         }

#         files_serializer = serializers.VendorSerializer(vendor, many=True, context=context)
#         dirs_serializer = serializers.OfferSerializer(offer, many=True, context=context)

#         response = files_serializer.data + dirs_serializer.data

#         return Response(response)


    # def get_serializer_class(self):
    #     """Return appropriate serializer class"""
    #     if self.action == 'retrieve':
    #         return serializers.RecipeDetailSerializer
    #     elif self.action == 'upload_image':
    #         return serializers.RecipeImageSerializer
    #     return self.serializer_class


    # @action(methods=['POST'], detail=True, url_path='upload-image')
    # def upload_image(self, request, pk=None):
    #     """Upload an image to recipe"""
    #     recipe = self.get_object()
    #     serializer = self.get_serializer(
    #         recipe,
    #         data=request.data
    #     )

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             serializer.data,
    #             status=status.HTTP_200_OK
    #         )
    #     return Response(
    #         serializer.errors,
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

