import logging
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer

# Get the logger for the 'inventory' app
logger = logging.getLogger('inventory')



class ItemCreateView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def post(self, request, *args, **kwargs):
        try:
            logger.info(f'Creating item - Request Data: {request.data}')
            response = super().post(request, *args, **kwargs)
            logger.info(f'Item created successfully: {response.data}')
            return response
        except Exception as e:
            logger.error(f'Error occurred while creating item: {str(e)}')
            return Response({"error": "Failed to create item."}, status=status.HTTP_400_BAD_REQUEST)


class ItemListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        try:
            logger.info('Fetching the list of inventory items')
            # Call the original get() method of ListAPIView to fetch the items
            response = super().get(request, *args, **kwargs)
            logger.info(f'Successfully retrieved {len(response.data)} items')
            return response
        except Exception as e:
            # Log the error if something goes wrong
            logger.error(f'Error occurred while retrieving items: {str(e)}')
            return Response({"error": "Failed to retrieve items"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ItemRetrieveView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        try:
            item_id = kwargs.get('pk')
            logger.info(f'Retrieving item with ID: {item_id}')
            response = super().get(request, *args, **kwargs)
            logger.info(f'Item retrieved successfully: {response.data}')
            return response
        except Item.DoesNotExist:
            logger.warning(f'Item with ID {item_id} not found.')
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Error occurred while retrieving item: {str(e)}')
            return Response({"error": "Failed to retrieve item."}, status=status.HTTP_400_BAD_REQUEST)

class ItemUpdateView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def put(self, request, *args, **kwargs):
        try:
            logger.info(f'Updating item with ID: {kwargs.get("pk")}')
            response = super().put(request, *args, **kwargs)
            logger.info(f'Item updated successfully: {response.data}')
            return response
        except Exception as e:
            logger.error(f'Error occurred while updating item: {str(e)}')
            return Response({"error": "Failed to update item."}, status=status.HTTP_400_BAD_REQUEST)

class ItemDeleteView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def delete(self, request, *args, **kwargs):
        try:
            logger.info(f'Deleting item with ID: {kwargs.get("pk")}')
            response = super().delete(request, *args, **kwargs)
            logger.info(f'Item deleted successfully.')
            return response
        except Exception as e:
            logger.error(f'Error occurred while deleting item: {str(e)}')
            return Response({"error": "Failed to delete item."}, status=status.HTTP_400_BAD_REQUEST)
